#!/usr/bin/env python3
import argparse
import fnmatch
import getpass
import hashlib
import json
import os
import zlib
from datetime import datetime, timedelta
from urllib.parse import urlparse

import requests
from tabulate import tabulate

# -- Configuration Constants --
PROJECT_ID = "spark-vector"
API_KEY = "AIzaSyDHq5JLR9_KamZlSBgqzTQ-VUAAce9XDjE"
DATABASE_URL = "https://spark-vector-default-rtdb.firebaseio.com"
BUCKET_NAME = "spark-vector.appspot.com"

# -- Global Authentication State --
user_id = None
id_token = None
refresh_token = None
token_expiry = None

# -- Authentication Helpers --
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
        error = response.json().get('error', {}).get('message', 'Unknown error')
        print(f"Token refresh failed: {error}")
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
    creds_dir = os.path.expanduser('~/.flink')
    os.makedirs(creds_dir, exist_ok=True)
    with open(os.path.join(creds_dir, 'credentials.json'), 'w') as f:
        json.dump({
            'user_id': user_id,
            'id_token': id_token,
            'refresh_token': refresh_token,
            'token_expiry': token_expiry
        }, f)
    print("Saved user credentials")

# -- Firebase Realtime Database Helpers --
def db_set(path, data, id_token):
    if token_expiry and datetime.now() > token_expiry:
        if not refresh_id_token():
            return None
    url = f"{DATABASE_URL}/{path}.json?auth={id_token}"
    response = requests.put(url, json=data)
    if response.status_code == 200:
        return response.json()
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
    print(f"Error getting data: {response.text}")
    return None

# -- Cloud Storage Helpers --
def storage_upload(file_path, destination, id_token):
    if token_expiry and datetime.now() > token_expiry:
        if not refresh_id_token():
            return None
    url = (
        f"https://storage.googleapis.com/upload/storage/v1/b/{BUCKET_NAME}/o"
        f"?uploadType=media&name={destination}"
    )
    headers = {"Authorization": f"Bearer {id_token}", "Content-Type": "application/octet-stream"}
    with open(file_path, 'rb') as f:
        response = requests.post(url, headers=headers, data=f)
    if response.status_code == 200:
        return response.json()
    print(f"Error uploading file: {response.text}")
    return None


def storage_download(source, file_path, id_token=None):
    if id_token and token_expiry and datetime.now() > token_expiry:
        if not refresh_id_token():
            return False
    url = (
        f"https://storage.googleapis.com/storage/v1/b/{BUCKET_NAME}/o/"
        f"{source.replace('/', '%2F')}?alt=media"
    )
    headers = {"Authorization": f"Bearer {id_token}"} if id_token else {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return True
    print(f"Error downloading file: {response.text}")
    return False

# -- Local Repository Discovery --
def find_repo_path():
    current_dir = os.getcwd()
    while current_dir and current_dir != '/':
        flink_dir = os.path.join(current_dir, '.flink')
        if os.path.isdir(flink_dir) and os.path.exists(os.path.join(flink_dir, 'config')):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    return None

# -- Object Storage (SHA-256 based) --
def hash_object(data, type_):
    header = f"{type_} {len(data)}\0".encode('utf-8')
    full_data = header + data
    digest = hashlib.sha256(full_data).hexdigest()
    return digest, full_data


def write_object(hash_, data, repo_path):
    object_dir = os.path.join(repo_path, '.flink', 'objects', hash_[:2])
    os.makedirs(object_dir, exist_ok=True)
    object_path = os.path.join(object_dir, hash_[2:])
    with open(object_path, 'wb') as f:
        f.write(zlib.compress(data))


def read_object(hash_, repo_path):
    object_path = os.path.join(repo_path, '.flink', 'objects', hash_[:2], hash_[2:])
    if not os.path.exists(object_path):
        raise FileNotFoundError(f"Object {hash_} not found")
    raw = zlib.decompress(open(object_path, 'rb').read())
    header, content = raw.split(b'\0', 1)
    type_, _ = header.decode('utf-8').split(' ', 1)
    return type_, content


def create_blob(file_path, repo_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    hash_, full_data = hash_object(content, 'blob')
    write_object(hash_, full_data, repo_path)
    return hash_

# -- Tree Parsing (32-byte SHA-256) --
def parse_tree(data):
    entries = []
    pos = 0
    hash_len = hashlib.sha256().digest_size  # 32 bytes
    while pos < len(data):
        null_pos = data.index(b'\0', pos)
        entry_header = data[pos:null_pos].decode('utf-8')
        mode, name = entry_header.split(' ', 1)

        start = null_pos + 1
        end = start + hash_len
        hash_ = data[start:end].hex()

        entries.append((mode, name, hash_))
        pos = end
    return entries


def create_tree(entries, repo_path):
    tree_content = b''
    for mode, name, hash_ in entries:
        tree_content += f"{mode} {name}\0".encode('utf-8') + bytes.fromhex(hash_)
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
            mode, blob = value
            if blob:
                entries.append((mode, name, blob))
            else:
                subtree_hash = create_subtree(mode)
                entries.append(('040000', name, subtree_hash))
        return create_tree(entries, repo_path)

    return create_subtree(tree_entries)

# -- Commit Objects --
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
    except FileNotFoundError:
        return objects
    if type_ != 'commit':
        return objects

    lines = content.decode('utf-8').split('\n')
    tree_hash = lines[0].split(' ')[1]
    objects.add(tree_hash)

    parent_hash = None
    for line in lines[1:]:
        if line.startswith('parent '):
            parent_hash = line.split(' ')[1]
            break

    try:
        _, tree_data = read_object(tree_hash, repo_path)
        for mode, _, obj in parse_tree(tree_data):
            objects.add(obj)
            if mode == '040000':
                get_reachable_objects(obj, repo_path, objects)
    except FileNotFoundError:
        pass

    if parent_hash:
        get_reachable_objects(parent_hash, repo_path, objects)
    return objects


def checkout(tree_hash, repo_path, base_path):
    try:
        _, data = read_object(tree_hash, repo_path)
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
    except FileNotFoundError:
        print(f"Warning: Tree {tree_hash} not found, skipping")

# -- User/Repo Commands --
def register(email, password, username):
    global user_id, id_token, refresh_token, token_expiry
    users_data = db_get("users")
    if users_data:
        for user in users_data.values():
            if user.get('username') == username:
                print(f"Username '{username}' is already taken. Choose another.")
                return
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        user_id = data['localId']
        id_token = data['idToken']
        refresh_token = data['refreshToken']
        token_expiry = datetime.now() + timedelta(seconds=int(data['expiresIn']))
        user_data = {"email": email, "username": username, "repos": []}
        db_set(f"users/{user_id}", user_data, id_token)
        save_user_credentials(user_id, id_token, refresh_token, token_expiry.isoformat())
        print(f"Registered user {username} ({email})")
    else:
        print(f"Registration failed: {response.json().get('error', {}).get('message')}")

def login(email, password):
    global user_id, id_token, refresh_token, token_expiry
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        user_id, id_token, refresh_token = data['localId'], data['idToken'], data['refreshToken']
        token_expiry = datetime.now() + timedelta(seconds=int(data['expiresIn']))
        save_user_credentials(user_id, id_token, refresh_token, token_expiry.isoformat())
        user_data = db_get(f"users/{user_id}", id_token)
        username = user_data.get('username', 'Not set')
        print(f"Logged in as {username} ({email})")
    else:
        print(f"Login failed: {response.json().get('error', {}).get('message')}")

def set_username(username):
    global user_id, id_token
    if not user_id or not id_token:
        print("Please login or register first.")
        return
    users_data = db_get("users", id_token)
    if users_data:
        for uid, user in users_data.items():
            if user.get('username') == username and uid != user_id:
                print(f"Username '{username}' is already taken.")
                return
    user_data = db_get(f"users/{user_id}", id_token)
    user_data['username'] = username
    db_set(f"users/{user_id}", user_data, id_token)
    print(f"Set username to '{username}'")

def profile():
    global user_id, id_token
    if not user_id or not id_token:
        print("Please login or register first.")
        return
    user_data = db_get(f"users/{user_id}", id_token)
    if not user_data:
        print("User not found.")
        return
    username = user_data.get('username', 'Not set')
    email = user_data.get('email', 'N/A')
    repos = user_data.get('repos', [])
    print("User Profile")
    print("-"*40)
    print(f"Username: {username}")
    print(f"Email: {email}")
    print("-"*40)
    if repos:
        table = []
        for repo_name in repos:
            repo_data = db_get(f"repositories/{repo_name}", id_token)
            visibility = repo_data.get('visibility', 'unknown')
            latest = repo_data.get('refs', {}).get('master', '')[:8]
            url = f"https://api.flink.svector.co.in/{username}/{repo_name}"
            table.append([repo_name, visibility, latest, url])
        print(tabulate(table, headers=["Name","Visibility","Latest","URL"], tablefmt="grid"))
    else:
        print("No repositories found.")

def init(repo_name=None):
    global user_id, id_token
    if not user_id or not id_token:
        print("Please login or register first.")
        return
    repo_path = os.getcwd()
    if not repo_name:
        repo_name = os.path.basename(repo_path)
    os.makedirs(repo_path, exist_ok=True)
    flink_dir = os.path.join(repo_path, '.flink')
    os.makedirs(os.path.join(flink_dir, 'objects'), exist_ok=True)
    os.makedirs(os.path.join(flink_dir, 'refs', 'heads'), exist_ok=True)
    os.makedirs(os.path.join(flink_dir, 'refs', 'remotes', 'origin'), exist_ok=True)
    with open(os.path.join(flink_dir, 'config'), 'w') as f:
        f.write(f"repo_id = {repo_name}")
    visibility = input("Make repository public or private? (public/private): ").strip().lower()
    if visibility not in ['public','private']:
        print("Invalid choice.")
        return
    repo_meta = {"refs":{},"visibility":visibility,"owner":user_id}
    db_set(f"repositories/{repo_name}", repo_meta, id_token)
    user_data = db_get(f"users/{user_id}", id_token)
    user_data['repos'] = user_data.get('repos',[])+[repo_name]
    db_set(f"users/{user_id}", user_data, id_token)
    print(f"Initialized {visibility} repository '{repo_name}' at {repo_path}")

def add(files):
    global user_id, id_token
    if not user_id or not id_token:
        print("Please login or register first.")
        return
    repo_path = find_repo_path()
    if not repo_path:
        print("Not in a Flink repository.")
        return
    if os.getcwd() != repo_path:
        print(f"Error: Run 'flink add .' from root ({repo_path})")
        return

    index_path = os.path.join(repo_path, '.flink', 'index.json')
    index = {}
    if os.path.exists(index_path):
        with open(index_path,'r') as f:
            index = json.load(f)

    ignore_patterns = []
    gitignore = os.path.join(repo_path, '.gitignore')
    if os.path.exists(gitignore):
        with open(gitignore) as f:
            for line in f:
                line=line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.append(line)

    def is_ignored(path):
        rel = os.path.relpath(path,repo_path).replace(os.sep,'/')
        if rel.startswith('.flink'):
            return True
        for pat in ignore_patterns:
            if fnmatch.fnmatch(rel,pat) or fnmatch.fnmatch(os.path.basename(path),pat):
                return True
        return False

    def stage_file(fp):
        if not os.path.isfile(fp) or is_ignored(fp):
            return
        rel = os.path.relpath(fp,repo_path).replace(os.sep,'/')
        h = create_blob(fp,repo_path)
        index[rel] = h
        print(f"Staged {rel}")

    for item in files:
        abspath = os.path.abspath(item)
        if item == '.':
            for root,_,files in os.walk(repo_path):
                for fn in files:
                    stage_file(os.path.join(root,fn))
        elif os.path.isfile(abspath):
            stage_file(abspath)
        else:
            print(f"Skipping {item}")

    with open(index_path,'w') as f:
        json.dump(index,f,indent=2)
    print(f"Added {len(index)} files to staging")

def commit(message):
    global user_id, id_token
    if not user_id or not id_token:
        print("Please login or register first.")
        return
    repo_path = find_repo_path()
    if not repo_path:
        print("Not in a Flink repository.")
        return
    index_path = os.path.join(repo_path, '.flink', 'index.json')
    if not os.path.exists(index_path):
        print("Nothing to commit.")
        return
    with open(index_path,'r') as f:
        index = json.load(f)
    if not index:
        print("Nothing to commit.")
        return
    tree = build_tree_from_index(index,repo_path)
    head = os.path.join(repo_path, '.flink', 'refs', 'heads', 'master')
    parent = None
    if os.path.exists(head):
        parent = open(head).read().strip()
    user = db_get(f"users/{user_id}",id_token).get('username','unknown')
    chash = create_commit(tree,parent,user,message,repo_path)
    with open(head,'w') as f:
        f.write(chash)
    os.remove(index_path)
    print(f"Committed {chash}")

def push():
    global user_id, id_token
    if not user_id or not id_token:
        print("Please login or register first.")
        return
    repo_path = find_repo_path()
    if not repo_path:
        print("Not in a Flink repository.")
        return
    cfg = open(os.path.join(repo_path,'.flink','config')).read()
    repo_id = cfg.split('=')[1].strip()
    meta = db_get(f"repositories/{repo_id}",id_token)
    if not meta:
        print("Remote repo not found.")
        return
    if meta['owner'] != user_id:
        print("You do not own this repository.")
        return
    head_local = open(os.path.join(repo_path,'.flink','refs','heads','master')).read().strip()
    print(f"Local master hash: {head_local}")
    remote = meta['refs'].get('master')
    to_upload = get_reachable_objects(head_local,repo_path)
    if remote:
        old = get_reachable_objects(remote,repo_path)
        to_upload -= old
    for obj in to_upload:
        path = os.path.join(repo_path,'.flink','objects',obj[:2],obj[2:])
        storage_upload(path,f"repositories/{repo_id}/objects/{obj}",id_token)
        print(f"Uploaded object {obj}")
    meta['refs']['master'] = head_local
    db_set(f"repositories/{repo_id}",meta,id_token)
    origin_ref = os.path.join(repo_path,'.flink','refs','remotes','origin','master')
    open(origin_ref,'w').write(head_local)
    usern = db_get(f"users/{user_id}",id_token).get('username','unknown')
    print(f"Pushed to https://api.flink.svector.co.in/{usern}/{repo_id}")

def clone(repo_arg):
    global user_id, id_token
    repo_name = None
    if repo_arg.startswith("https://"):
        parsed = urlparse(repo_arg)
        if parsed.netloc != 'api.flink.svector.co.in':
            print("Invalid URL. Use https://api.flink.svector.co.in/username/repo-name")
            return
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) != 2:
            print("Invalid URL format. Use https://api.flink.svector.co.in/username/repo-name")
            return
        username, repo_name = path_parts
        users_data = db_get("users", id_token if id_token else None)
        owner_id = None
        for uid, user in (users_data or {}).items():
            if user.get('username') == username:
                owner_id = uid
                break
        if not owner_id:
            print(f"User '{username}' not found")
            return
        repo_data = db_get(f"repositories/{repo_name}", id_token if id_token else None)
        if not repo_data or repo_data.get('owner') != owner_id:
            print(f"Repository '{repo_name}' not found for user '{username}'")
            return
    else:
        repo_name = repo_arg
        repo_data = db_get(f"repositories/{repo_name}", id_token if id_token else None)
        if not repo_data:
            print(f"Repository '{repo_name}' does not exist in database")
            return

    visibility = repo_data.get('visibility', 'public')
    owner = repo_data.get('owner')
    if visibility == 'private' and (not user_id or owner != user_id):
        print("Cannot clone private repository. Please login as the owner.")
        return

    refs = repo_data.get('refs', {})
    master_hash = refs.get('master')
    repo_path = os.path.join(os.getcwd(), repo_name)
    os.makedirs(repo_path, exist_ok=True)
    flink_dir = os.path.join(repo_path, '.flink')
    os.makedirs(os.path.join(flink_dir, 'objects'), exist_ok=True)
    os.makedirs(os.path.join(flink_dir, 'refs', 'heads'), exist_ok=True)
    os.makedirs(os.path.join(flink_dir, 'refs', 'remotes', 'origin'), exist_ok=True)
    with open(os.path.join(flink_dir, 'config'), 'w') as f:
        f.write(f"repo_id = {repo_name}")
    print(f"Initialized Flink repository '{repo_name}' at {repo_path}")

    if master_hash:
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
                try:
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
                except FileNotFoundError:
                    print(f"Warning: Object {hash_} not found, skipping")

        download_recursive(master_hash)
        with open(os.path.join(repo_path, '.flink', 'refs', 'heads', 'master'), 'w') as f:
            f.write(master_hash)
        with open(os.path.join(repo_path, '.flink', 'refs', 'remotes', 'origin', 'master'), 'w') as f:
            f.write(master_hash)
        try:
            type_, content = read_object(master_hash, repo_path)
            tree_hash = content.decode().split('\n')[0].split(' ')[1]
            checkout(tree_hash, repo_path, repo_path)
            print(f"Cloned repository {repo_name}")
        except FileNotFoundError:
            print(f"Warning: Commit {master_hash} not found, cloned empty repository")
    else:
        print(f"Cloned empty repository {repo_name}")

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
    username = user_data.get('username', 'unknown')
    if not repos:
        print("You have no repositories.")
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
    parser = argparse.ArgumentParser(description="Flink: open-source VCS")
    parser.add_argument('--version', action='version', version='flink ${VERSION}')
    sub = parser.add_subparsers(dest='command')
    # register
    p = sub.add_parser('register')
    p.add_argument('email'); p.add_argument('username'); p.add_argument('password', nargs='?')
    # login
    p = sub.add_parser('login')
    p.add_argument('email'); p.add_argument('password', nargs='?')
    # set username
    p = sub.add_parser('set'); p.add_argument('property', choices=['username']); p.add_argument('value')
    # profile, init, add, commit, push, clone, list-repos, search, all-repos
    for cmd in ['profile','init','add','commit','push','clone','list-repos','search','all-repos']:
        sub.add_parser(cmd)

    args = parser.parse_args()
    cmd = args.command
    if cmd == 'register':
        pwd = args.password or getpass.getpass('Enter password: ')
        register(args.email, pwd, args.username)
    elif cmd == 'login':
        pwd = args.password or getpass.getpass('Enter password: ')
        login(args.email, pwd)
    elif cmd == 'set' and args.property == 'username':
        set_username(args.value)
    elif cmd == 'profile': profile()
    elif cmd == 'init': init()
    elif cmd == 'add': add([args.command])
    elif cmd == 'commit': commit(getpass.getpass('Commit message: '))
    elif cmd == 'push': push()
    elif cmd == 'clone': clone()
    elif cmd == 'list-repos': list_repos()
    elif cmd == 'search': search(getpass.getpass('Query: '))
    elif cmd == 'all-repos': all_repos()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()