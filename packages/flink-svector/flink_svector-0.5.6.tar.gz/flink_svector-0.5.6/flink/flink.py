import argparse
import fnmatch
import getpass
import hashlib
import json
import logging
import os
import re
import zlib
from datetime import datetime, timedelta
from urllib.parse import urlparse

import requests
from tabulate import tabulate

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PROJECT_ID = "sparrkmail"
API_KEY = "AIzaSyAUjF_we6oZ9Ohqibn4hfJZEbK80OQPp5Y"
DATABASE_URL = "https://sparrkmail-default-rtdb.asia-southeast1.firebasedatabase.app"
BUCKET_NAME = "sparrkmail.appspot.com"

# Global variables
user_id = None
id_token = None
refresh_token = None
token_expiry = None

def refresh_id_token():
    global id_token, refresh_token, token_expiry
    if not refresh_token:
        logging.error("No refresh token available. Please login again.")
        return False
    url = f"https://securetoken.googleapis.com/v1/token?key={API_KEY}"
    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'id_token' not in data or 'refresh_token' not in data or 'expires_in' not in data:
                logging.error(f"Invalid token refresh response: {data}")
                return False
            id_token = data['id_token']
            refresh_token = data['refresh_token']
            token_expiry = datetime.now() + timedelta(seconds=int(data['expires_in']))
            save_user_credentials(user_id, id_token, refresh_token, token_expiry.isoformat())
            logging.info("Refreshed authentication token")
            return True
        else:
            logging.error(f"Token refresh failed: {response.status_code} {response.text}")
            return False
    except requests.RequestException as e:
        logging.error(f"Network error during token refresh: {e}")
        return False

def load_user_credentials():
    global user_id, id_token, refresh_token, token_expiry
    creds_path = os.path.expanduser('~/.flink/credentials.json')
    if os.path.exists(creds_path):
        try:
            with open(creds_path, 'r') as f:
                creds = json.load(f)
                user_id = creds.get('user_id')
                id_token = creds.get('id_token')
                refresh_token = creds.get('refresh_token')
                expiry_str = creds.get('token_expiry')
                token_expiry = datetime.fromisoformat(expiry_str) if expiry_str else None
            if id_token and token_expiry and datetime.now() > token_expiry:
                if not refresh_id_token():
                    logging.warning("Failed to refresh token. Clearing credentials.")
                    user_id = id_token = refresh_token = token_expiry = None
                    os.remove(creds_path)
            logging.info(f"Loaded user ID: {user_id}")
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error reading credentials file: {e}")
            user_id = id_token = refresh_token = token_expiry = None
    else:
        logging.warning("No user credentials found. Please login or register.")

def save_user_credentials(user_id, id_token, refresh_token, token_expiry):
    creds_path = os.path.expanduser('~/.flink')
    try:
        os.makedirs(creds_path, exist_ok=True)
        creds_file = os.path.join(creds_path, 'credentials.json')
        with open(creds_file, 'w') as f:
            json.dump({
                'user_id': user_id,
                'id_token': id_token,
                'refresh_token': refresh_token,
                'token_expiry': token_expiry
            }, f)
        os.chmod(creds_file, 0o600)
        logging.info("Saved user credentials")
    except (IOError, OSError) as e:
        logging.error(f"Error saving credentials: {e}")

def db_set(path, data, id_token):
    if not id_token:
        logging.error("No authentication token available. Please login.")
        return None
    if token_expiry and datetime.now() > token_expiry:
        if not refresh_id_token():
            return None
    url = f"{DATABASE_URL}/{path}.json?auth={id_token}"
    try:
        response = requests.put(url, json=data, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Error setting data: {response.status_code} {response.text}")
            return None
    except requests.RequestException as e:
        logging.error(f"Network error during database write: {e}")
        return None

def db_get(path, id_token=None):
    if id_token and token_expiry and datetime.now() > token_expiry:
        if not refresh_id_token():
            return None
    url = f"{DATABASE_URL}/{path}.json" + (f"?auth={id_token}" if id_token else "")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Error getting data: {response.status_code} {response.text}")
            return None
    except requests.RequestException as e:
        logging.error(f"Network error during database read: {e}")
        return None

def storage_upload(file_path, destination, id_token):
    if not id_token:
        logging.error("No authentication token available. Please login.")
        return None
    if token_expiry and datetime.now() > token_expiry:
        if not refresh_id_token():
            logging.error("Failed to refresh token for upload.")
            return None
    url = f"https://storage.googleapis.com/upload/storage/v1/b/{BUCKET_NAME}/o?uploadType=media&name={destination}"
    headers = {"Authorization": f"Bearer {id_token}", "Content-Type": "application/octet-stream"}
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(url, headers=headers, data=f, timeout=30)
        if response.status_code == 200:
            logging.info(f"Uploaded {file_path} to {destination}")
            return response.json()
        else:
            logging.error(f"Error uploading file: {response.status_code} {response.text}")
            return None
    except (IOError, requests.RequestException) as e:
        logging.error(f"Error during file upload: {e}")
        return None

def storage_download(source, file_path, id_token=None):
    if id_token and token_expiry and datetime.now() > token_expiry:
        if not refresh_id_token():
            logging.error("Failed to refresh token for download.")
            return False
    url = f"https://storage.googleapis.com/storage/v1/b/{BUCKET_NAME}/o/{source.replace('/', '%2F')}?alt=media"
    headers = {"Authorization": f"Bearer {id_token}"} if id_token else {}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            logging.info(f"Downloaded {source} to {file_path}")
            return True
        else:
            logging.error(f"Error downloading file: {response.status_code} {response.text}")
            return False
    except (IOError, requests.RequestException) as e:
        logging.error(f"Error during file download: {e}")
        return False

def sanitize_path(base_path, path):
    abs_base = os.path.abspath(base_path)
    abs_path = os.path.abspath(os.path.join(base_path, path))
    if not abs_path.startswith(abs_base):
        raise ValueError(f"Invalid path: {path} escapes repository directory")
    return abs_path

def find_repo_path():
    current_dir = os.getcwd()
    while current_dir != '/':
        flink_dir = os.path.join(current_dir, '.flink')
        if os.path.isdir(flink_dir) and os.path.exists(os.path.join(flink_dir, 'config')):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    return None

def hash_object(data, type_):
    header = f"{type_} {len(data)}\0".encode('utf-8')
    full_data = header + data
    hash_ = hashlib.sha256(full_data).hexdigest()
    return hash_, full_data

def write_object(hash_, data, repo_path):
    object_dir = os.path.join(repo_path, '.flink', 'objects', hash_[:2])
    object_path = os.path.join(object_dir, hash_[2:])
    try:
        sanitize_path(repo_path, object_path)
        os.makedirs(object_dir, exist_ok=True)
        with open(object_path, 'wb') as f:
            f.write(zlib.compress(data))
        logging.info(f"Wrote object {hash_}")
    except (ValueError, IOError) as e:
        logging.error(f"Error writing object {hash_}: {e}")

def read_object(hash_, repo_path):
    object_path = os.path.join(repo_path, '.flink', 'objects', hash_[:2], hash_[2:])
    try:
        sanitize_path(repo_path, object_path)
        if not os.path.exists(object_path):
            raise FileNotFoundError(f"Object {hash_} not found")
        with open(object_path, 'rb') as f:
            data = zlib.decompress(f.read())
        header, content = data.split(b'\0', 1)
        type_, _ = header.decode('utf-8').split(' ', 1)
        return type_, content
    except (ValueError, IOError, UnicodeDecodeError) as e:
        logging.error(f"Invalid object {hash_}: {e}")
        raise FileNotFoundError(f"Invalid object {hash_}")

def create_blob(file_path, repo_path):
    try:
        sanitize_path(repo_path, file_path)
        with open(file_path, 'rb') as f:
            content = f.read()
        hash_, full_data = hash_object(content, 'blob')
        write_object(hash_, full_data, repo_path)
        return hash_
    except (ValueError, IOError) as e:
        logging.error(f"Error creating blob for {file_path}: {e}")
        return None

def parse_tree(data):
    entries = []
    pos = 0
    while pos < len(data):
        try:
            null_pos = data.index(b'\0', pos)
            entry_header = data[pos:null_pos].decode('utf-8', errors='replace')
            parts = entry_header.split(' ', 1)
            if len(parts) != 2:
                logging.warning(f"Invalid tree entry at pos {pos}: {entry_header}")
                pos = null_pos + 21
                continue
            mode, name = parts
            if mode not in ('100644', '040000') or not name:
                logging.warning(f"Invalid tree entry at pos {pos}: mode={mode}, name={name}")
                pos = null_pos + 21
                continue
            if null_pos + 21 > len(data):
                logging.warning(f"Incomplete tree entry at pos {pos}")
                break
            hash_ = data[null_pos+1:null_pos+21].hex()
            entries.append((mode, name, hash_))
            pos = null_pos + 21
        except ValueError:
            logging.warning(f"No null separator found after pos {pos}")
            break
        except UnicodeDecodeError:
            logging.warning(f"Invalid UTF-8 in tree entry at pos {pos}")
            pos += 1
    return entries

def create_tree(entries, repo_path):
    tree_content = b''
    for mode, name, hash_ in sorted(entries, key=lambda x: x[1]):  # Sort for consistency
        try:
            name.encode('utf-8')
            if mode not in ('100644', '040000'):
                logging.warning(f"Invalid mode for {name}: {mode}")
                continue
            tree_content += f"{mode} {name}\0".encode('utf-8') + bytes.fromhex(hash_)
        except (UnicodeEncodeError, ValueError) as e:
            logging.warning(f"Invalid filename or hash in tree: {name}, {e}")
            continue
    if not tree_content:
        logging.warning("No valid entries for tree object")
        return None
    hash_, full_data = hash_object(tree_content, 'tree')
    write_object(hash_, full_data, repo_path)
    return hash_

def build_tree_from_index(index, repo_path):
    tree_entries = {}
    for path, blob_hash in index.items():
        try:
            path.encode('utf-8')
            parts = path.split('/')
            current = tree_entries
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    current[part] = ('100644', blob_hash)
                else:
                    if part not in current:
                        current[part] = ({}, None)
                    current = current[part][0]
        except (UnicodeEncodeError, ValueError) as e:
            logging.warning(f"Invalid path in index: {path}, {e}")
            continue
    def create_subtree(structure):
        entries = []
        for name, value in structure.items():
            try:
                name.encode('utf-8')
                if value[1]:
                    entries.append((value[0], name, value[1]))
                else:
                    subtree_hash = create_subtree(value[0])
                    if subtree_hash:
                        entries.append(('040000', name, subtree_hash))
            except UnicodeEncodeError as e:
                logging.warning(f"Invalid subtree name: {name}, {e}")
                continue
        return create_tree(entries, repo_path)
    return create_subtree(tree_entries)

def create_commit(tree_hash, parent_hash, author, message, repo_path):
    commit_content = f"tree {tree_hash}\n"
    if parent_hash:
        commit_content += f"parent {parent_hash}\n"
    commit_content += f"author {author}\ncommitter {author}\n\n{message}\n"
    hash_, full_data = hash_object(commit_content.encode('utf-8'), 'commit')
    write_object(hash_, full_data, repo_path)
    return hash_

def get_reachable_objects(commit_hash, repo_path, objects=None):
    if objects is None:
        objects = set()
    if not commit_hash or commit_hash in objects:
        return objects
    objects.add(commit_hash)
    try:
        type_, content = read_object(commit_hash, repo_path)
        if type_ != 'commit':
            return objects
        lines = content.decode('utf-8').split('\n')
        tree_hash = lines[0].split(' ')[1]
        objects.add(tree_hash)
        parent_hash = None
        for line in lines[1:]:
            if line.startswith('parent'):
                parent_hash = line.split(' ')[1]
                break
        try:
            type_, tree_data = read_object(tree_hash, repo_path)
            for mode, name, hash_ in parse_tree(tree_data):
                objects.add(hash_)
                if mode == '040000':
                    get_reachable_objects(hash_, repo_path, objects)
        except FileNotFoundError:
            logging.warning(f"Tree {tree_hash} not found")
        if parent_hash:
            get_reachable_objects(parent_hash, repo_path, objects)
    except (FileNotFoundError, UnicodeDecodeError) as e:
        logging.warning(f"Commit {commit_hash} invalid, skipping: {e}")
    return objects

def checkout(tree_hash, repo_path, base_path):
    try:
        type_, data = read_object(tree_hash, repo_path)
        for mode, name, hash_ in parse_tree(data):
            path = os.path.join(base_path, name)
            try:
                sanitize_path(repo_path, path)
                if mode == '100644':
                    try:
                        type_blob, content = read_object(hash_, repo_path)
                        os.makedirs(os.path.dirname(path), exist_ok=True)
                        with open(path, 'wb') as f:
                            f.write(content)
                    except FileNotFoundError:
                        logging.warning(f"Blob {hash_} not found, skipping")
                elif mode == '040000':
                    os.makedirs(path, exist_ok=True)
                    checkout(hash_, repo_path, path)
            except ValueError as e:
                logging.warning(f"Invalid path {path}, skipping: {e}")
    except FileNotFoundError:
        logging.warning(f"Tree {tree_hash} not found, skipping")

def validate_filename(filename):
    try:
        filename.encode('utf-8')
        if '/' in filename or '\\' in filename or filename in ('.', '..'):
            raise ValueError("Invalid filename")
        return filename
    except UnicodeEncodeError:
        raise ValueError("Filename contains invalid characters")

def register(email, password, username):
    global user_id, id_token, refresh_token, token_expiry
    try:
        users_data = db_get("users", id_token if id_token else None)
        if users_data:
            for user in users_data.values():
                if user.get('username') == username:
                    logging.error(f"Username '{username}' is already taken.")
                    return
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            user_id = data['localId']
            id_token = data['idToken']
            refresh_token = data['refreshToken']
            token_expiry = datetime.now() + timedelta(seconds=int(data['expiresIn']))
            user_data = {"email": email, "username": username, "repos": []}
            db_set(f"users/{user_id}", user_data, id_token)
            save_user_credentials(user_id, id_token, refresh_token, token_expiry.isoformat())
            logging.info(f"Registered user {username} ({email})")
        else:
            logging.error(f"Registration failed: {response.text}")
    except requests.RequestException as e:
        logging.error(f"Network error during registration: {e}")

def login(email, password):
    global user_id, id_token, refresh_token, token_expiry
    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            user_id = data['localId']
            id_token = data['idToken']
            refresh_token = data['refreshToken']
            token_expiry = datetime.now() + timedelta(seconds=int(data['expiresIn']))
            save_user_credentials(user_id, id_token, refresh_token, token_expiry.isoformat())
            user_data = db_get(f"users/{user_id}", id_token)
            username = user_data.get('username', 'Not set')
            logging.info(f"Logged in as {username} ({email})")
        else:
            logging.error(f"Login failed: {response.text}")
    except requests.RequestException as e:
        logging.error(f"Network error during login: {e}")

def set_username(username):
    global user_id, id_token
    if not user_id or not id_token:
        logging.error("Please login or register first.")
        return
    try:
        users_data = db_get("users", id_token)
        if users_data:
            for uid, user in users_data.items():
                if user.get('username') == username and uid != user_id:
                    logging.error(f"Username '{username}' is already taken.")
                    return
        user_data = db_get(f"users/{user_id}", id_token)
        user_data['username'] = username
        db_set(f"users/{user_id}", user_data, id_token)
        logging.info(f"Set username to '{username}'")
    except Exception as e:
        logging.error(f"Error setting username: {e}")

def profile():
    global user_id, id_token
    if not user_id or not id_token:
        logging.error("Please login or register first.")
        return
    user_data = db_get(f"users/{user_id}", id_token)
    if not user_data:
        logging.error("User not found.")
        return
    username = user_data.get('username', 'Not set')
    email = user_data.get('email', 'N/A')
    repos = user_data.get('repos', [])
    print("User Profile")
    print("-" * 40)
    print(f"Username: {username}")
    print(f"Email: {email}")
    print("-" * 40)
    if repos:
        repo_list = []
        for repo_name in repos:
            repo_data = db_get(f"repositories/{repo_name}", id_token)
            if repo_data:
                visibility = repo_data.get('visibility', 'unknown')
                master_hash = repo_data.get('refs', {}).get('master', 'none')[:8]
                repo_list.append([repo_name, visibility, master_hash, f"https://api.flink.svector.co.in/{username}/{repo_name}"])
        if repo_list:
            print("Repositories:")
            print(tabulate(repo_list, headers=["Name", "Visibility", "Latest Commit", "URL"], tablefmt="grid"))
    else:
        print("No repositories found.")

def init(repo_name=None):
    global user_id, id_token
    if not user_id or not id_token:
        logging.error("Please login or register first.")
        return
    repo_path = os.getcwd()
    if not repo_name:
        repo_name = os.path.basename(repo_path)
    try:
        repo_name = re.sub(r'[^a-zA-Z0-9_-]', '', repo_name)
        if not repo_name:
            logging.error("Invalid repository name")
            return
        repo_path = os.path.join(repo_path, repo_name)
        sanitize_path(os.getcwd(), repo_path)
        os.makedirs(repo_path, exist_ok=True)
        flink_dir = os.path.join(repo_path, '.flink')
        os.makedirs(os.path.join(flink_dir, 'objects'), exist_ok=True)
        os.makedirs(os.path.join(flink_dir, 'refs', 'heads'), exist_ok=True)
        os.makedirs(os.path.join(flink_dir, 'refs', 'remotes', 'origin'), exist_ok=True)
        with open(os.path.join(flink_dir, 'config'), 'w') as f:
            f.write(f"repo_id = {repo_name}")
        visibility = input("Make repository public or private? (public/private): ").strip().lower()
        if visibility not in ['public', 'private']:
            logging.error("Invalid choice. Choose 'public' or 'private'.")
            return
        repo_data = {"refs": {}, "visibility": visibility, "owner": user_id}
        db_set(f"repositories/{repo_name}", repo_data, id_token)
        user_data = db_get(f"users/{user_id}", id_token)
        user_data['repos'] = user_data.get('repos', []) + [repo_name]
        db_set(f"users/{user_id}", user_data, id_token)
        logging.info(f"Initialized {visibility} Flink repository '{repo_name}' at {repo_path}")
    except ValueError as e:
        logging.error(f"Invalid repository path: {e}")

def add(files):
    global user_id, id_token
    if not user_id or not id_token:
        logging.error("Please login or register first.")
        return
    repo_path = find_repo_path()
    if not repo_path:
        logging.error("Not in a Flink repository")
        return
    index_path = os.path.join(repo_path, '.flink', 'index.json')
    index = {}
    if os.path.exists(index_path):
        try:
            with open(index_path, 'r') as f:
                index = json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Error reading index file: {e}")
            return
    # Load .gitignore patterns
    gitignore_path = os.path.join(repo_path, '.gitignore')
    ignore_patterns = []
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, 'r') as f:
                ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except IOError as e:
            logging.error(f"Error reading .gitignore: {e}")
    # Function to check if a path should be ignored
    def is_ignored(file_path):
        rel_path = os.path.relpath(file_path, repo_path)
        if rel_path.startswith('.flink'):
            return True
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(rel_path, pattern):
                return True
        return False
    # Function to add a single file to the index
    def add_file(file_path):
        if not os.path.isfile(file_path) or is_ignored(file_path):
            return
        rel_path = os.path.relpath(file_path, repo_path)
        blob_hash = create_blob(file_path, repo_path)
        if blob_hash:
            index[rel_path] = blob_hash
            logging.info(f"Staged {rel_path}")
    # Function to add all files in a directory
    def add_directory(dir_path):
        for root, dirs, filenames in os.walk(dir_path):
            if '.flink' in dirs:
                dirs.remove('.flink')
            for filename in filenames:
                file_path = os.path.join(root, filename)
                add_file(file_path)
    # Process each item in the files argument
    for item in files:
        item_path = os.path.join(repo_path, item)
        if item == '.':
            add_directory(repo_path)
        elif os.path.isdir(item_path):
            add_directory(item_path)
        elif os.path.isfile(item_path):
            add_file(item_path)
        else:
            logging.error(f"Path {item} does not exist")
    # Save the updated index
    try:
        with open(index_path, 'w') as f:
            json.dump(index, f)
        logging.info(f"Added {len(index)} file(s) to staging area")
    except IOError as e:
        logging.error(f"Error writing index file: {e}")

def commit(message):
    global user_id, id_token
    if not user_id or not id_token:
        logging.error("Please login or register first.")
        return
    repo_path = find_repo_path()
    if not repo_path:
        logging.error("Not in a Flink repository")
        return
    index_path = os.path.join(repo_path, '.flink', 'index.json')
    if not os.path.exists(index_path):
        logging.error("Nothing to commit")
        return
    try:
        with open(index_path, 'r') as f:
            index = json.load(f)
        if not index:
            logging.error("Nothing to commit")
            return
        tree_hash = build_tree_from_index(index, repo_path)
        if not tree_hash:
            logging.error("Failed to create tree object")
            return
        master_ref = os.path.join(repo_path, '.flink', 'refs', 'heads', 'master')
        parent_hash = None
        if os.path.exists(master_ref):
            with open(master_ref, 'r') as f:
                parent_hash = f.read().strip()
        user_data = db_get(f"users/{user_id}", id_token)
        username = user_data.get('username', 'unknown')
        commit_hash = create_commit(tree_hash, parent_hash, username, message, repo_path)
        with open(master_ref, 'w') as f:
            f.write(commit_hash)
        os.remove(index_path)
        logging.info(f"Committed {commit_hash}")
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Error during commit: {e}")

def push():
    global user_id, id_token
    if not user_id or not id_token:
        logging.error("Please login or register first.")
        return
    repo_path = find_repo_path()
    if not repo_path:
        logging.error("Not in a Flink repository")
        return
    try:
        with open(os.path.join(repo_path, '.flink', 'config'), 'r') as f:
            repo_id = f.read().split('=')[1].strip()
        logging.info(f"Repository ID: {repo_id}")
        repo_data = db_get(f"repositories/{repo_id}", id_token)
        if not repo_data:
            logging.error(f"Repository {repo_id} does not exist in database")
            return
        if repo_data.get('owner') != user_id:
            logging.error("You do not own this repository.")
            return
        master_ref = os.path.join(repo_path, '.flink', 'refs', 'heads', 'master')
        if not os.path.exists(master_ref):
            logging.error("Nothing to push")
            return
        with open(master_ref, 'r') as f:
            local_master = f.read().strip()
        logging.info(f"Local master hash: {local_master}")
        if 'refs' not in repo_data:
            logging.warning(f"Refs missing in repo_data for {repo_id}. Initializing empty refs.")
            repo_data['refs'] = {}
        remote_refs = repo_data['refs']
        remote_master = remote_refs.get('master')
        objects = get_reachable_objects(local_master, repo_path)
        if remote_master:
            remote_objects = get_reachable_objects(remote_master, repo_path)
            objects -= remote_objects
        logging.info(f"Uploading {len(objects)} new objects")
        failed_uploads = []
        for obj_hash in objects:
            obj_path = os.path.join(repo_path, '.flink', 'objects', obj_hash[:2], obj_hash[2:])
            if not storage_upload(obj_path, f"repositories/{repo_id}/objects/{obj_hash}", id_token):
                failed_uploads.append(obj_hash)
        if failed_uploads:
            logging.error(f"Failed to upload {len(failed_uploads)} objects: {failed_uploads}")
            return
        repo_data['refs']['master'] = local_master
        if not db_set(f"repositories/{repo_id}", repo_data, id_token):
            logging.error("Failed to update database refs")
            return
        with open(os.path.join(repo_path, '.flink', 'refs', 'remotes', 'origin', 'master'), 'w') as f:
            f.write(local_master)
        user_data = db_get(f"users/{user_id}", id_token)
        username = user_data.get('username', 'unknown')
        logging.info(f"Pushed changes to https://api.flink.svector.co.in/{username}/{repo_id}")
    except (IOError, ValueError) as e:
        logging.error(f"Error during push: {e}")

def clone(repo_arg):
    global user_id, id_token
    repo_name = None
    username = None
    try:
        # Check if input is a URL
        if repo_arg.startswith("https://"):
            parsed = urlparse(repo_arg)
            if parsed.netloc != 'api.flink.svector.co.in':
                logging.error("Invalid URL. Use https://api.flink.svector.co.in/username/repo-name")
                return
            path_parts = parsed.path.strip('/').split('/')
            if len(path_parts) != 2:
                logging.error("Invalid URL format. Use https://api.flink.svector.co.in/username/repo-name")
                return
            username, repo_name = path_parts
        else:
            # Handle repo-name or username/repo-name
            if '/' in repo_arg:
                parts = repo_arg.split('/')
                if len(parts) != 2:
                    logging.error("Invalid format. Use repo-name or username/repo-name")
                    return
                username, repo_name = parts
            else:
                if not user_id or not id_token:
                    logging.error("Please login to clone using just repo-name")
                    return
                repo_name = re.sub(r'[^a-zA-Z0-9_-]', '', repo_arg)
                user_data = db_get(f"users/{user_id}", id_token)
                username = user_data.get('username', None)
                if not username:
                    logging.error("User has no username set")
                    return

        # Validate repo_name
        repo_name = re.sub(r'[^a-zA-Z0-9_-]', '', repo_name)
        if not repo_name:
            logging.error("Invalid repository name")
            return

        # Find owner_id if username is provided
        if username:
            users_data = db_get("users", id_token if id_token else None)
            owner_id = None
            for uid, user in (users_data or {}).items():
                if user.get('username') == username:
                    owner_id = uid
                    break
            if not owner_id:
                logging.error(f"User '{username}' not found")
                return
        else:
            owner_id = user_id

        # Fetch repository data
        repo_data = db_get(f"repositories/{repo_name}", id_token if id_token else None)
        if not repo_data or repo_data.get('owner') != owner_id:
            logging.error(f"Repository '{repo_name}' not found for user '{username}'")
            return

        visibility = repo_data.get('visibility', 'public')
        owner = repo_data.get('owner')
        if visibility == 'private' and (not user_id or owner != user_id):
            logging.error("Cannot clone private repository. Please login as the owner.")
            return

        refs = repo_data.get('refs', {})
        master_hash = refs.get('master')
        repo_path = os.path.join(os.getcwd(), repo_name)
        sanitize_path(os.getcwd(), repo_path)
        os.makedirs(repo_path, exist_ok=True)
        flink_dir = os.path.join(repo_path, '.flink')
        os.makedirs(os.path.join(flink_dir, 'objects'), exist_ok=True)
        os.makedirs(os.path.join(flink_dir, 'refs', 'heads'), exist_ok=True)
        os.makedirs(os.path.join(flink_dir, 'refs', 'remotes', 'origin'), exist_ok=True)
        with open(os.path.join(flink_dir, 'config'), 'w') as f:
            f.write(f"repo_id = {repo_name}")
        logging.info(f"Initialized Flink repository '{repo_name}' at {repo_path}")

        if master_hash:
            downloaded = set()
            def download_object(hash_):
                obj_path = os.path.join(repo_path, '.flink', 'objects', hash_[:2], hash_[2:])
                return storage_download(f"repositories/{repo_name}/objects/{hash_}", obj_path, id_token if user_id else None)
            def download_recursive(hash_):
                if hash_ in downloaded:
                    return
                if download_object(hash_):
                    downloaded.add(hash_)
                    try:
                        type_, content = read_object(hash_, repo_path)
                        if type_ == 'commit':
                            tree_hash = content.decode('utf-8').split('\n')[0].split(' ')[1]
                            download_recursive(tree_hash)
                            parent_line = [l for l in content.decode('utf-8').split('\n') if l.startswith('parent')]
                            if parent_line:
                                download_recursive(parent_line[0].split(' ')[1])
                        elif type_ == 'tree':
                            for _, _, hash_ in parse_tree(content):
                                download_recursive(hash_)
                    except (FileNotFoundError, UnicodeDecodeError) as e:
                        logging.warning(f"Object {hash_} invalid, skipping: {e}")
            download_recursive(master_hash)
            with open(os.path.join(repo_path, '.flink', 'refs', 'heads', 'master'), 'w') as f:
                f.write(master_hash)
            with open(os.path.join(repo_path, '.flink', 'refs', 'remotes', 'origin', 'master'), 'w') as f:
                f.write(master_hash)
            try:
                type_, content = read_object(master_hash, repo_path)
                tree_hash = content.decode('utf-8').split('\n')[0].split(' ')[1]
                checkout(tree_hash, repo_path, repo_path)
                logging.info(f"Cloned repository {repo_name}")
            except (FileNotFoundError, UnicodeDecodeError) as e:
                logging.warning(f"Commit {master_hash} invalid, cloned empty repository: {e}")
        else:
            logging.info(f"Cloned empty repository {repo_name}")
    except (ValueError, IOError) as e:
        logging.error(f"Error cloning repository: {e}")

def list_repos():
    global user_id, id_token
    if not user_id or not id_token:
        logging.error("Please login or register first.")
        return
    user_data = db_get(f"users/{user_id}", id_token)
    if not user_data:
        logging.error("User not found.")
        return
    repos = user_data.get('repos', [])
    username = user_data.get('username', 'unknown')
    if not repos:
        logging.info("You have no repositories.")
        return
    repo_list = []
    for repo_name in repos:
        repo_data = db_get(f"repositories/{repo_name}", id_token)
        if repo_data:
            visibility = repo_data.get('visibility', 'unknown')
            master_hash = repo_data.get('refs', {}).get('master', 'none')[:8]
            repo_list.append([repo_name, visibility, master_hash, f"https://api.flink.svector.co.in/{username}/{repo_name}"])
    print("Your repositories:")
    print(tabulate(repo_list, headers=["Name", "Visibility", "Latest Commit", "URL"], tablefmt="grid"))

def search(query):
    global id_token
    query_lower = query.lower()
    repo_results = []
    repos_data = db_get("repositories", id_token if id_token else None)
    if repos_data:
        for repo_name, repo in repos_data.items():
            if query_lower in repo_name.lower() and repo.get('visibility') == 'public':
                owner_id = repo.get('owner', 'unknown')
                owner_data = db_get(f"users/{owner_id}", id_token if id_token else None)
                owner_username = owner_data.get('username', 'unknown') if owner_data else 'unknown'
                master_hash = repo.get('refs', {}).get('master', 'none')[:8]
                repo_results.append([repo_name, owner_username, master_hash, f"https://api.flink.svector.co.in/{owner_username}/{repo_name}"])
    if repo_results:
        print("Matching repositories:")
        print(tabulate(repo_results, headers=["Repo Name", "Owner", "Latest Commit", "URL"], tablefmt="grid"))
    else:
        print("No matching repositories found.")

def all_repos():
    global id_token
    repo_list = []
    repos_data = db_get("repositories", id_token if id_token else None)
    if not repos_data:
        print("No repositories found or access denied.")
        return
    for repo_name, repo in repos_data.items():
        if repo.get('visibility') == 'public':
            owner_id = repo.get('owner', 'unknown')
            owner_data = db_get(f"users/{owner_id}", id_token if id_token else None)
            owner_username = owner_data.get('username', 'unknown') if owner_data else 'unknown'
            master_hash = repo.get('refs', {}).get('master', 'none')[:8]
            repo_list.append([repo_name, owner_username, master_hash, f"https://api.flink.svector.co.in/{owner_username}/{repo_name}"])
    if repo_list:
        print("All public repositories:")
        print(tabulate(repo_list, headers=["Repo Name", "Owner", "Latest Commit", "URL"], tablefmt="grid"))
    else:
        print("No public repositories found.")

def main():
    load_user_credentials()
    parser = argparse.ArgumentParser(description="Flink: An open source version control system")
    parser.add_argument('--version', action='version', version='flink 0.5.3')
    subparsers = parser.add_subparsers(dest='command')
    register_parser = subparsers.add_parser('register', help='Register a new user')
    register_parser.add_argument('email', help='User email')
    register_parser.add_argument('username', help='User username')
    register_parser.add_argument('password', help='User password', nargs='?', default=None)
    login_parser = subparsers.add_parser('login', help='Login as a user')
    login_parser.add_argument('email', help='User email')
    login_parser.add_argument('password', help='User password', nargs='?', default=None)
    set_parser = subparsers.add_parser('set', help='Set user properties')
    set_parser.add_argument('property', choices=['username'], help='Property to set')
    set_parser.add_argument('value', help='Value to set')
    profile_parser = subparsers.add_parser('profile', help='View user profile')
    init_parser = subparsers.add_parser('init', help='Initialize a new repository')
    init_parser.add_argument('repo_name', nargs='?', default=None, help='Repository name')
    add_parser = subparsers.add_parser('add', help='Add files to staging area')
    add_parser.add_argument('files', nargs='+', help='Files to add')
    commit_parser = subparsers.add_parser('commit', help='Commit staged changes')
    commit_parser.add_argument('-m', '--message', required=True, help='Commit message')
    push_parser = subparsers.add_parser('push', help='Push changes to remote')
    clone_parser = subparsers.add_parser('clone', help='Clone a repository')
    clone_parser.add_argument('repo_arg', help='Repository name, username/repo-name, or URL')
    list_parser = subparsers.add_parser('list-repos', help='List your repositories')
    search_parser = subparsers.add_parser('search', help='Search for repositories')
    search_parser.add_argument('query', help='Search query')
    all_repos_parser = subparsers.add_parser('all-repos', help='List all public repositories')
    args = parser.parse_args()
    if args.command == 'register':
        password = args.password or getpass.getpass("Enter password: ")
        register(args.email, args.username, password)
    elif args.command == 'login':
        password = args.password or getpass.getpass("Enter password: ")
        login(args.email, password)
    elif args.command == 'set':
        if args.property == 'username':
            set_username(args.value)
    elif args.command == 'profile':
        profile()
    elif args.command == 'init':
        init(args.repo_name)
    elif args.command == 'add':
        add(args.files)
    elif args.command == 'commit':
        commit(args.message)
    elif args.command == 'push':
        push()
    elif args.command == 'clone':
        clone(args.repo_arg)
    elif args.command == 'list-repos':
        list_repos()
    elif args.command == 'search':
        search(args.query)
    elif args.command == 'all-repos':
        all_repos()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()