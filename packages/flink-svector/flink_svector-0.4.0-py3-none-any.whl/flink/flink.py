import argparse
import fnmatch
import getpass
import hashlib
import json
import os
import zlib
from datetime import datetime, timedelta

import requests

# Firebase configuration for spark-vector
PROJECT_ID = "spark-vector"
API_KEY = "AIzaSyDHq5JLR9_KamZlSBgqzTQ-VUAAce9XDjE"
DATABASE_URL = "https://spark-vector-default-rtdb.firebaseio.com"
BUCKET_NAME = "spark-vector.appspot.com"

# Global variables
user_id = None
id_token = None
refresh_token = None
token_expiry = None

def refresh_id_token():
    global id_token, refresh_token, token_expiry
    if not refresh_token:
        print("No refresh token available. Please login again.")
        return False
    url = f"https://securetoken.googleapis.com/v1/token?key={API_KEY}"
    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        id_token = data['id_token']
        refresh_token = data['refresh_token']
        token_expiry = datetime.now() + timedelta(seconds=int(data['expires_in']))
        save_user_credentials(user_id, id_token, refresh_token, token_expiry.isoformat())
        print("Refreshed authentication token")
        return True
    else:
        print(f"Token refresh failed: {response.json()['error']['message']}")
        return False

def load_user_credentials():
    global user_id, id_token, refresh_token, token_expiry
    creds_path = os.path.expanduser('~/.flink/credentials.json')
    if os.path.exists(creds_path):
        with open(creds_path, 'r') as f:
            creds = json.load(f)
            user_id = creds.get('user_id')
            id_token = creds.get('id_token')
            refresh_token = creds.get('refresh_token')
            expiry_str = creds.get('token_expiry')
            token_expiry = datetime.fromisoformat(expiry_str) if expiry_str else None
        if token_expiry and datetime.now() > token_expiry:
            refresh_id_token()
        print(f"Loaded user ID: {user_id}")
    else:
        print("No user credentials found. Please login or register.")

def save_user_credentials(user_id, id_token, refresh_token, token_expiry):
    creds_path = os.path.expanduser('~/.flink')
    os.makedirs(creds_path, exist_ok=True)
    with open(os.path.join(creds_path, 'credentials.json'), 'w') as f:
        json.dump({
            'user_id': user_id,
            'id_token': id_token,
            'refresh_token': refresh_token,
            'token_expiry': token_expiry
        }, f)
    print("Saved user credentials")

def register(email, password):
    global user_id, id_token, refresh_token, token_expiry
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        user_id = data['localId']
        id_token = data['idToken']
        refresh_token = data['refreshToken']
        token_expiry = datetime.now() + timedelta(seconds=int(data['expiresIn']))
        user_data = {
            "email": email,
            "repos": []
        }
        requests.put(f"{DATABASE_URL}/users/{user_id}.json?auth={id_token}", json=user_data)
        save_user_credentials(user_id, id_token, refresh_token, token_expiry.isoformat())
        print(f"Registered user {email}")
    else:
        print(f"Registration failed: {response.json()['error']['message']}")

def login(email, password):
    global user_id, id_token, refresh_token, token_expiry
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        user_id = data['localId']
        id_token = data['idToken']
        refresh_token = data['refreshToken']
        token_expiry = datetime.now() + timedelta(seconds=int(data['expiresIn']))
        save_user_credentials(user_id, id_token, refresh_token, token_expiry.isoformat())
        print(f"Logged in as {email}")
    else:
        print(f"Login failed: {response.json()['error']['message']}")

def db_set(path, data, id_token):
    if token_expiry and datetime.now() > token_expiry:
        if not refresh_id_token():
            return None
    url = f"{DATABASE_URL}/{path}.json?auth={id_token}"
    response = requests.put(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error setting data: {response.text}")
        return None

def db_get(path, id_token=None):
    if id_token and token_expiry and datetime.now() > token_expiry:
        if not refresh_id_token():
            return None
    url = f"{DATABASE_URL}/{path}.json" + (f"?auth={id_token}" if id_token else "")
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting data: {response.text}")
        return None

def storage_upload(file_path, destination, id_token):
    if token_expiry and datetime.now() > token_expiry:
        if not refresh_id_token():
            return None
    url = f"https://storage.googleapis.com/upload/storage/v1/b/{BUCKET_NAME}/o?uploadType=media&name={destination}"
    headers = {"Authorization": f"Bearer {id_token}", "Content-Type": "application/octet-stream"}
    with open(file_path, 'rb') as f:
        response = requests.post(url, headers=headers, data=f)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error uploading file: {response.text}")
        return None

def storage_download(source, file_path, id_token):
    if id_token and token_expiry and datetime.now() > token_expiry:
        if not refresh_id_token():
            return False
    url = f"https://storage.googleapis.com/{BUCKET_NAME}/{source}"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"Error downloading file: {response.text}")
        return False

def find_repo_path():
    current_dir = os.getcwd()
    while current_dir != '/':
        flink_dir = os.path.join(current_dir, '.flink')
        if os.path.isdir(flink_dir) and os.path.exists(os.path.join(flink_dir, 'config')):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    return None

def hash_object(data, type_):
    header = f"{type_} {len(data)}\0".encode()
    full_data = header + data
    hash_ = hashlib.sha256(full_data).hexdigest()
    return hash_, full_data

def write_object(hash_, data, repo_path):
    object_dir = os.path.join(repo_path, '.flink', 'objects', hash_[:2])
    os.makedirs(object_dir, exist_ok=True)
    object_path = os.path.join(object_dir, hash_[2:])
    with open(object_path, 'wb') as f:
        f.write(zlib.compress(data))

def read_object(hash_, repo_path):
    object_path = os.path.join(repo_path, '.flink', 'objects', hash_[:2], hash_[2:])
    with open(object_path, 'rb') as f:
        data = zlib.decompress(f.read())
    header, content = data.split(b'\0', 1)
    type_, _ = header.decode().split(' ', 1)
    return type_, content

def create_blob(file_path, repo_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    hash_, full_data = hash_object(content, 'blob')
    write_object(hash_, full_data, repo_path)
    return hash_

def parse_tree(data):
    entries = []
    pos = 0
    while pos < len(data):
        null_pos = data.index(b'\0', pos)
        entry_header = data[pos:null_pos].decode()
        mode, name = entry_header.split(' ', 1)
        hash_ = data[null_pos+1:null_pos+33].hex()
        entries.append((mode, name, hash_))
        pos = null_pos + 33
    return entries

def create_tree(entries, repo_path):
    tree_content = b''
    for mode, name, hash_ in entries:
        tree_content += f"{mode} {name}\0".encode() + bytes.fromhex(hash_)
    hash_, full_data = hash_object(tree_content, 'tree')
    write_object(hash_, full_data, repo_path)
    return hash_

def build_tree_from_index(index, repo_path):
    tree_entries = {}
    for path, blob_hash in index.items():
        parts = path.split('/')
        current = tree_entries
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                current[part] = ('100644', blob_hash)
            else:
                if part not in current:
                    current[part] = ({}, None)
                current = current[part][0]

    def create_subtree(structure):
        entries = []
        for name, value in structure.items():
            if value[1]:  # Blob
                entries.append((value[0], name, value[1]))
            else:  # Tree
                subtree_hash = create_subtree(value[0])
                entries.append(('040000', name, subtree_hash))
        return create_tree(entries, repo_path)

    return create_subtree(tree_entries)

def create_commit(tree_hash, parent_hash, author, message, repo_path):
    commit_content = f"tree {tree_hash}\n"
    if parent_hash:
        commit_content += f"parent {parent_hash}\n"
    commit_content += f"author {author}\ncommitter {author}\n\n{message}\n"
    hash_, full_data = hash_object(commit_content.encode(), 'commit')
    write_object(hash_, full_data, repo_path)
    return hash_

def get_reachable_objects(commit_hash, repo_path, objects=None):
    if objects is None:
        objects = set()
    if commit_hash in objects:
        return objects
    objects.add(commit_hash)
    type_, content = read_object(commit_hash, repo_path)
    if type_ != 'commit':
        return objects
    lines = content.decode().split('\n')
    tree_hash = lines[0].split(' ')[1]
    objects.add(tree_hash)
    parent_hash = None
    if len(lines) > 1 and lines[1].startswith('parent'):
        parent_hash = lines[1].split(' ')[1]
    type_, tree_data = read_object(tree_hash, repo_path)
    for mode, _, hash_ in parse_tree(tree_data):
        objects.add(hash_)
        if mode == '040000':
            get_reachable_objects(hash_, repo_path, objects)
    if parent_hash:
        get_reachable_objects(parent_hash, repo_path, objects)
    return objects

def checkout(tree_hash, repo_path, base_path):
    type_, data = read_object(tree_hash, repo_path)
    for mode, name, hash_ in parse_tree(data):
        path = os.path.join(base_path, name)
        if mode == '100644':
            _, content = read_object(hash_, repo_path)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as f:
                f.write(content)
        elif mode == '040000':
            os.makedirs(path, exist_ok=True)
            checkout(hash_, repo_path, path)

def init(repo_name=None):
    global user_id, id_token
    if not user_id or not id_token:
        print("Please login or register first.")
        return
    repo_path = os.getcwd()
    if not repo_name:
        repo_name = os.path.basename(repo_path)
    visibility = input("Make repository public or private? (public/private): ").strip().lower()
    if visibility not in ['public', 'private']:
        print("Invalid choice. Choose 'public' or 'private'.")
        return
    flink_dir = os.path.join(repo_path, '.flink')
    os.makedirs(os.path.join(flink_dir, 'objects'), exist_ok=True)
    os.makedirs(os.path.join(flink_dir, 'refs', 'heads'), exist_ok=True)
    os.makedirs(os.path.join(flink_dir, 'refs', 'remotes', 'origin'), exist_ok=True)
    with open(os.path.join(flink_dir, 'config'), 'w') as f:
        f.write(f"repo_id = {repo_name}")
    repo_data = {
        "refs": {},
        "visibility": visibility,
        "owner": user_id
    }
    db_set(f"repositories/{repo_name}", repo_data, id_token)
    user_data = db_get(f"users/{user_id}", id_token)
    user_data['repos'] = user_data.get('repos', []) + [repo_name]
    db_set(f"users/{user_id}", user_data, id_token)
    print(f"Initialized {visibility} Flink repository '{repo_name}' at {repo_path}")

def add(files):
    global user_id, id_token
    if not user_id or not id_token:
        print("Please login or register first.")
        return
    repo_path = find_repo_path()
    if not repo_path:
        init()
        repo_path = os.getcwd()
    elif os.getcwd() != repo_path:
        print(f"Error: Run 'flink add .' from the repository root ({repo_path})")
        return

    index_path = os.path.join(repo_path, '.flink', 'index.json')
    index = {}
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            try:
                index = json.load(f)
            except json.JSONDecodeError:
                index = {}

    gitignore_path = os.path.join(repo_path, '.gitignore')
    ignore_patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    def is_ignored(file_path):
        rel_path = os.path.relpath(file_path, repo_path).replace(os.sep, '/')
        if rel_path.startswith('.flink') or rel_path == '.flink':
            return True
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(file_path), pattern):
                return True
        return False

    def add_file(file_path):
        if not os.path.isfile(file_path) or is_ignored(file_path):
            return
        rel_path = os.path.relpath(file_path, repo_path).replace(os.sep, '/')
        blob_hash = create_blob(file_path, repo_path)
        index[rel_path] = blob_hash
        print(f"Staged {rel_path}")

    def add_directory():
        repo_abs = os.path.abspath(repo_path)
        for root, _, filenames in os.walk(repo_abs, followlinks=False):
            root_abs = os.path.abspath(root)
            if root_abs == os.path.abspath(os.path.join(repo_abs, '.flink')) or not root_abs.startswith(repo_abs):
                continue
            for filename in filenames:
                file_path = os.path.join(root, filename)
                file_abs = os.path.abspath(file_path)
                if not file_abs.startswith(repo_abs):
                    continue
                add_file(file_path)

    if not files:
        print("No files specified")
        return
    for item in files:
        item_path = os.path.join(os.getcwd(), item)
        item_abs = os.path.abspath(item_path)
        repo_abs = os.path.abspath(repo_path)
        if item == '.':
            add_directory()
        elif os.path.isfile(item_abs):
            if not item_abs.startswith(repo_abs):
                print(f"Error: File {item} is outside repository ({repo_path})")
                continue
            add_file(item_abs)
        elif os.path.isdir(item_abs):
            print(f"Error: Cannot add subdirectory {item} alone; use 'flink add .' to include all files")
        else:
            print(f"Path {item} does not exist")

    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)
    print(f"Added {len(index)} file(s) to staging area")

def commit(message):
    global user_id, id_token
    if not user_id or not id_token:
        print("Please login or register first.")
        return
    repo_path = find_repo_path()
    if not repo_path:
        print("Not in a Flink repository")
        return
    index_path = os.path.join(repo_path, '.flink', 'index.json')
    if not os.path.exists(index_path):
        print("Nothing to commit")
        return
    with open(index_path, 'r') as f:
        index = json.load(f)
    if not index:
        print("Nothing to commit")
        return
    tree_hash = build_tree_from_index(index, repo_path)
    master_ref = os.path.join(repo_path, '.flink', 'refs', 'heads', 'master')
    parent_hash = None
    if os.path.exists(master_ref):
        with open(master_ref, 'r') as f:
            parent_hash = f.read().strip()
    user_data = db_get(f"users/{user_id}", id_token)
    email = user_data.get('email', 'unknown')
    commit_hash = create_commit(tree_hash, parent_hash, email, message, repo_path)
    with open(master_ref, 'w') as f:
        f.write(commit_hash)
    os.remove(index_path)
    print(f"Committed {commit_hash}")

def push():
    global user_id, id_token
    if not user_id or not id_token:
        print("Please login or register first.")
        return
    repo_path = find_repo_path()
    if not repo_path:
        print("Not in a Flink repository")
        return
    with open(os.path.join(repo_path, '.flink', 'config'), 'r') as f:
        repo_id = f.read().split('=')[1].strip()
    repo_data = db_get(f"repositories/{repo_id}", id_token)
    if not repo_data:
        print(f"Repository {repo_id} does not exist in database")
        return
    if repo_data['owner'] != user_id:
        print("You do not own this repository.")
        return
    master_ref = os.path.join(repo_path, '.flink', 'refs', 'heads', 'master')
    if not os.path.exists(master_ref):
        print("Nothing to push")
        return
    with open(master_ref, 'r') as f:
        local_master = f.read().strip()
    print(f"Local master hash: {local_master}")
    remote_refs = repo_data.get('refs', {})
    remote_master = remote_refs.get('master')
    objects = get_reachable_objects(local_master, repo_path)
    if remote_master:
        remote_objects = get_reachable_objects(remote_master, repo_path)
        objects -= remote_objects
    for obj_hash in objects:
        obj_path = os.path.join(repo_path, '.flink', 'objects', obj_hash[:2], obj_hash[2:])
        storage_upload(obj_path, f"repositories/{repo_id}/objects/{obj_hash}", id_token)
        print(f"Uploaded object {obj_hash}")
    repo_data['refs']['master'] = local_master
    db_set(f"repositories/{repo_id}", repo_data, id_token)
    print(f"Updated database refs to: {{'master': '{local_master}'}}")
    with open(os.path.join(repo_path, '.flink', 'refs', 'remotes', 'origin', 'master'), 'w') as f:
        f.write(local_master)
    print("Pushed changes to remote")

def clone(repo_name):
    global user_id, id_token
    repo_data = db_get(f"repositories/{repo_name}", id_token if user_id else None)
    if not repo_data:
        print(f"Repository {repo_name} does not exist in database")
        return
    visibility = repo_data.get('visibility', 'public')
    owner = repo_data.get('owner')
    if visibility == 'private' and (not user_id or owner != user_id):
        print("Cannot clone private repository. Please login as the owner.")
        return
    refs = repo_data.get('refs', {})
    master_hash = refs.get('master')
    if not master_hash:
        print("Remote repository is empty")
        return
    repo_path = os.path.join(os.getcwd(), repo_name)
    os.makedirs(repo_path, exist_ok=True)
    flink_dir = os.path.join(repo_path, '.flink')
    os.makedirs(os.path.join(flink_dir, 'objects'), exist_ok=True)
    os.makedirs(os.path.join(flink_dir, 'refs', 'heads'), exist_ok=True)
    os.makedirs(os.path.join(flink_dir, 'refs', 'remotes', 'origin'), exist_ok=True)
    with open(os.path.join(flink_dir, 'config'), 'w') as f:
        f.write(f"repo_id = {repo_name}")
    print(f"Initialized empty Flink repository at {repo_path}")
    downloaded = set()
    def download_object(hash_):
        obj_path = os.path.join(repo_path, '.flink', 'objects', hash_[:2], hash_[2:])
        if storage_download(f"repositories/{repo_name}/objects/{hash_}", obj_path, id_token if user_id else None):
            print(f"Downloaded object {hash_}")
            return True
        return False
    def download_recursive(hash_):
        if hash_ in downloaded:
            return
        if download_object(hash_):
            downloaded.add(hash_)
            type_, content = read_object(hash_, repo_path)
            if type_ == 'commit':
                tree_hash = content.decode().split('\n')[0].split(' ')[1]
                download_recursive(tree_hash)
                parent_line = [l for l in content.decode().split('\n') if l.startswith('parent')]
                if parent_line:
                    download_recursive(parent_line[0].split(' ')[1])
            elif type_ == 'tree':
                for _, _, hash_ in parse_tree(content):
                    download_recursive(hash_)
    download_recursive(master_hash)
    with open(os.path.join(repo_path, '.flink', 'refs', 'heads', 'master'), 'w') as f:
        f.write(master_hash)
    with open(os.path.join(repo_path, '.flink', 'refs', 'remotes', 'origin', 'master'), 'w') as f:
        f.write(master_hash)
    type_, content = read_object(master_hash, repo_path)
    tree_hash = content.decode().split('\n')[0].split(' ')[1]
    checkout(tree_hash, repo_path, repo_path)
    print(f"Cloned repository {repo_name}")

def list_repos():
    global user_id, id_token
    if not user_id or not id_token:
        print("Please login or register first.")
        return
    user_data = db_get(f"users/{user_id}", id_token)
    if not user_data:
        print("User not found.")
        return
    repos = user_data.get('repos', [])
    if not repos:
        print("You have no repositories.")
        return
    print("Your repositories:")
    for repo_name in repos:
        repo_data = db_get(f"repositories/{repo_name}", id_token)
        if repo_data:
            visibility = repo_data.get('visibility', 'unknown')
            master_hash = repo_data.get('refs', {}).get('master', 'none')
            print(f"- {repo_name} ({visibility}, latest commit: {master_hash[:8]})")
        else:
            print(f"- {repo_name} (not found in database)")

def search(query):
    global id_token
    query_lower = query.lower()
    repo_results = []
    repos_data = db_get("repositories", id_token if id_token else None)
    if repos_data:
        for repo_name, repo in repos_data.items():
            if query_lower in repo_name.lower() and repo.get('visibility') == 'public':
                owner = repo.get('owner', 'unknown')
                master_hash = repo.get('refs', {}).get('master', 'none')
                repo_results.append([repo_name, owner, master_hash[:8]])
    from tabulate import tabulate
    if repo_results:
        print("Matching repositories:")
        print(tabulate(repo_results, headers=["Repo Name", "Owner", "Latest Commit"], tablefmt="grid"))
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
            owner = repo.get('owner', 'unknown')
            master_hash = repo.get('refs', {}).get('master', 'none')
            repo_list.append([repo_name, owner, master_hash[:8]])
    from tabulate import tabulate
    if repo_list:
        print("All public repositories:")
        print(tabulate(repo_list, headers=["Repo Name", "Owner", "Latest Commit"], tablefmt="grid"))
    else:
        print("No public repositories found.")

def main():
    load_user_credentials()
    parser = argparse.ArgumentParser(description="Flink: An open source version control system")
    parser.add_argument('--version', action='version', version='flink 0.3.8')
    subparsers = parser.add_subparsers(dest='command')
    register_parser = subparsers.add_parser('register', help='Register a new user')
    register_parser.add_argument('email', help='User email')
    register_parser.add_argument('password', help='User password', nargs='?', default=None)
    login_parser = subparsers.add_parser('login', help='Login as a user')
    login_parser.add_argument('email', help='User email')
    login_parser.add_argument('password', help='User password', nargs='?', default=None)
    init_parser = subparsers.add_parser('init', help='Initialize a new repository')
    init_parser.add_argument('repo_name', nargs='?', default=None, help='Repository name')
    add_parser = subparsers.add_parser('add', help='Add files to staging area')
    add_parser.add_argument('files', nargs='+', help='Files to add')
    commit_parser = subparsers.add_parser('commit', help='Commit staged changes')
    commit_parser.add_argument('-m', '--message', required=True, help='Commit message')
    push_parser = subparsers.add_parser('push', help='Push changes to remote')
    clone_parser = subparsers.add_parser('clone', help='Clone a repository')
    clone_parser.add_argument('repo_name', help='Repository name to clone')
    list_parser = subparsers.add_parser('list-repos', help='List your repositories')
    search_parser = subparsers.add_parser('search', help='Search for repositories')
    search_parser.add_argument('query', help='Search query')
    all_repos_parser = subparsers.add_parser('all-repos', help='List all public repositories')
    args = parser.parse_args()
    if args.command == 'register':
        password = args.password or getpass.getpass("Enter password: ")
        register(args.email, password)
    elif args.command == 'login':
        password = args.password or getpass.getpass("Enter password: ")
        login(args.email, password)
    elif args.command == 'init':
        init(args.repo_name)
    elif args.command == 'add':
        add(args.files)
    elif args.command == 'commit':
        commit(args.message)
    elif args.command == 'push':
        push()
    elif args.command == 'clone':
        clone(args.repo_name)
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