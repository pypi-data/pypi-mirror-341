import argparse
import getpass
import hashlib
import json
import logging
import os
import zlib
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1 import DocumentReference
from tabulate import tabulate

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global Firebase variables
db = None
bucket = None
user_id = None

def initialize_firebase():
    global db, bucket
    if db is not None and bucket is not None:
        return  # Already initialized
    try:
        service_account_path = os.getenv('FLINK_SERVICE_ACCOUNT')
        if not service_account_path:
            raise ValueError("FLINK_SERVICE_ACCOUNT environment variable not set")
        if not os.path.exists(service_account_path):
            raise FileNotFoundError(f"Service account file does not exist: {service_account_path}")
        logging.info("Service account file found")
        cred = credentials.Certificate(service_account_path)
        logging.info("Credentials loaded")
        if firebase_admin._apps:
            logging.info("Firebase app already initialized")
        else:
            firebase_admin.initialize_app(cred, {'storageBucket': 'sparrkmail.appspot.com'})
            logging.info("Firebase app initialized")
        db = firestore.client()
        logging.info("Firestore client created")
        bucket = storage.bucket()
        logging.info("Storage bucket accessed")
    except Exception as e:
        logging.error(f"Firebase initialization failed: {type(e).__name__}: {str(e)}")
        raise

def load_user_credentials():
    global user_id
    creds_path = os.path.expanduser('~/.flink/credentials.json')
    if os.path.exists(creds_path):
        with open(creds_path, 'r') as f:
            creds = json.load(f)
            user_id = creds.get('user_id')
        logging.info(f"Loaded user ID: {user_id}")
    else:
        logging.warning("No user credentials found. Please login or register.")

def save_user_credentials(user_id):
    creds_path = os.path.expanduser('~/.flink')
    os.makedirs(creds_path, exist_ok=True)
    with open(os.path.join(creds_path, 'credentials.json'), 'w') as f:
        json.dump({'user_id': user_id}, f)
    logging.info(f"Saved user credentials for {user_id}")

def register(email, password):
    global user_id
    initialize_firebase()
    user_id = hashlib.sha256(email.encode()).hexdigest()
    user_ref = db.collection('users').document(user_id)
    if user_ref.get().exists:
        logging.error("User already exists. Please login.")
        return
    user_ref.set({
        'email': email,
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'repos': []
    })
    save_user_credentials(user_id)
    logging.info(f"Registered user {email} with ID {user_id}")

def login(email, password):
    global user_id
    initialize_firebase()
    user_id = hashlib.sha256(email.encode()).hexdigest()
    user_ref = db.collection('users').document(user_id)
    doc = user_ref.get()
    if not doc.exists:
        logging.error("User does not exist. Please register.")
        return
    data = doc.to_dict()
    if data['password'] != hashlib.sha256(password.encode()).hexdigest():
        logging.error("Invalid password.")
        return
    save_user_credentials(user_id)
    logging.info(f"Logged in as {email} (ID: {user_id})")

def find_repo_path():
    current_dir = os.getcwd()
    while current_dir != '/':
        if os.path.exists(os.path.join(current_dir, '.flink')):
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
    os.makedirs(object_dir, exist_ok=True)
    object_path = os.path.join(object_dir, hash_[2:])
    with open(object_path, 'wb') as f:
        f.write(zlib.compress(data))
    logging.info(f"Wrote object {hash_} to {object_path}")

def read_object(hash_, repo_path):
    object_path = os.path.join(repo_path, '.flink', 'objects', hash_[:2], hash_[2:])
    if not os.path.exists(object_path):
        raise FileNotFoundError(f"Object {hash_} not found at {object_path}")
    with open(object_path, 'rb') as f:
        data = zlib.decompress(f.read())
    header, content = data.split(b'\0', 1)
    type_, _ = header.decode('utf-8').split(' ', 1)
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
        try:
            null_pos = data.index(b'\0', pos)
            entry_header = data[pos:null_pos].decode('utf-8', errors='replace')
            mode, name = entry_header.split(' ', 1)
            if not mode.isdigit() or len(mode) != 6:
                logging.warning(f"Invalid mode in tree entry at pos {pos}: {mode}")
                pos = null_pos + 21
                continue
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
    for mode, name, hash_ in entries:
        try:
            tree_content += f"{mode} {name}\0".encode('utf-8') + bytes.fromhex(hash_)
        except UnicodeEncodeError:
            logging.warning(f"Skipping invalid filename: {name}")
            continue
    hash_, full_data = hash_object(tree_content, 'tree')
    write_object(hash_, full_data, repo_path)
    return hash_

def build_tree_from_index(index, repo_path):
    tree_entries = {}
    for path, blob_hash in index.items():
        parts = path.split('/')
        current = tree_entries
        for i, part in enumerate(parts):
            try:
                part.encode('utf-8')
                if i == len(parts) - 1:
                    current[part] = ('100644', blob_hash)
                else:
                    if part not in current:
                        current[part] = ({}, None)
                    current = current[part][0]
            except UnicodeEncodeError:
                logging.warning(f"Invalid path component: {part}")
    def create_subtree(structure):
        entries = []
        for name, value in structure.items():
            try:
                if value[1]:  # Blob
                    entries.append((value[0], name, value[1]))
                else:  # Tree
                    subtree_hash = create_subtree(value[0])
                    entries.append(('040000', name, subtree_hash))
            except Exception as e:
                logging.warning(f"Error creating subtree for {name}: {e}")
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
            for mode, _, hash_ in parse_tree(tree_data):
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
            if mode == '100644':
                try:
                    _, content = read_object(hash_, repo_path)
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, 'wb') as f:
                        f.write(content)
                except FileNotFoundError:
                    logging.warning(f"Blob {hash_} not found, skipping")
            elif mode == '040000':
                os.makedirs(path, exist_ok=True)
                checkout(hash_, repo_path, path)
    except FileNotFoundError:
        logging.warning(f"Tree {tree_hash} not found, skipping")

def init(repo_name):
    global db, user_id
    if not user_id:
        logging.error("Please login or register first.")
        return
    initialize_firebase()
    visibility = input("Make repository public or private? (public/private): ").strip().lower()
    if visibility not in ['public', 'private']:
        logging.error("Invalid choice. Choose 'public' or 'private'.")
        return
    if repo_name:
        os.makedirs(repo_name, exist_ok=True)
        os.chdir(repo_name)
    repo_path = os.getcwd()
    flink_dir = os.path.join(repo_path, '.flink')
    os.makedirs(os.path.join(flink_dir, 'objects'), exist_ok=True)
    os.makedirs(os.path.join(flink_dir, 'refs', 'heads'), exist_ok=True)
    os.makedirs(os.path.join(flink_dir, 'refs', 'remotes', 'origin'), exist_ok=True)
    with open(os.path.join(flink_dir, 'config'), 'w') as f:
        f.write(f"repo_id = {repo_name}")
    doc_ref = db.collection('repositories').document(repo_name)
    doc_ref.set({
        'refs': {},
        'visibility': visibility,
        'owner': user_id
    })
    user_ref = db.collection('users').document(user_id)
    user_ref.update({
        'repos': firestore.ArrayUnion([repo_name])
    })
    logging.info(f"Initialized {visibility} Flink repository '{repo_name}' at {repo_path}")

def add(files):
    repo_path = find_repo_path()
    if not repo_path:
        logging.error("Not in a Flink repository")
        return
    index_path = os.path.join(repo_path, '.flink', 'index.json')
    index = {}
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            index = json.load(f)
    for file in files:
        rel_path = os.path.relpath(file, repo_path)
        blob_hash = create_blob(file, repo_path)
        index[rel_path] = blob_hash
    with open(index_path, 'w') as f:
        json.dump(index, f)
    logging.info(f"Added {len(files)} file(s) to staging area")

def commit(message):
    global user_id
    if not user_id:
        logging.error("Please login or register first.")
        return
    initialize_firebase()
    repo_path = find_repo_path()
    if not repo_path:
        logging.error("Not in a Flink repository")
        return
    index_path = os.path.join(repo_path, '.flink', 'index.json')
    if not os.path.exists(index_path):
        logging.error("Nothing to commit")
        return
    with open(index_path, 'r') as f:
        index = json.load(f)
    if not index:
        logging.error("Nothing to commit")
        return
    tree_hash = build_tree_from_index(index, repo_path)
    master_ref = os.path.join(repo_path, '.flink', 'refs', 'heads', 'master')
    parent_hash = None
    if os.path.exists(master_ref):
        with open(master_ref, 'r') as f:
            parent_hash = f.read().strip()
    email = db.collection('users').document(user_id).get().to_dict()['email']
    commit_hash = create_commit(tree_hash, parent_hash, email, message, repo_path)
    with open(master_ref, 'w') as f:
        f.write(commit_hash)
    os.remove(index_path)
    logging.info(f"Committed {commit_hash}")

def push():
    global db, bucket, user_id
    if not user_id:
        logging.error("Please login or register first.")
        return
    initialize_firebase()
    repo_path = find_repo_path()
    if not repo_path:
        logging.error("Not in a Flink repository")
        return
    with open(os.path.join(repo_path, '.flink', 'config'), 'r') as f:
        repo_id = f.read().split('=')[1].strip()
    doc_ref = db.collection('repositories').document(repo_id)
    doc = doc_ref.get()
    if not doc.exists:
        logging.error(f"Repository {repo_id} does not exist in Firestore")
        return
    repo_data = doc.to_dict()
    if repo_data['owner'] != user_id:
        logging.error("You do not own this repository.")
        return
    master_ref = os.path.join(repo_path, '.flink', 'refs', 'heads', 'master')
    if not os.path.exists(master_ref):
        logging.error("Nothing to push")
        return
    with open(master_ref, 'r') as f:
        local_master = f.read().strip()
    logging.info(f"Local master hash: {local_master}")
    remote_refs = repo_data.get('refs', {})
    remote_master = remote_refs.get('master')
    objects = get_reachable_objects(local_master, repo_path)
    if remote_master:
        remote_objects = get_reachable_objects(remote_master, repo_path)
        objects -= remote_objects
    logging.info(f"Uploading {len(objects)} new objects")
    for obj_hash in objects:
        obj_path = os.path.join(repo_path, '.flink', 'objects', obj_hash[:2], obj_hash[2:])
        if not os.path.exists(obj_path):
            logging.error(f"Object {obj_hash} not found locally")
            continue
        try:
            with open(obj_path, 'rb') as f:
                blob = bucket.blob(f"repositories/{repo_id}/objects/{obj_hash}")
                if not blob.exists():
                    blob.upload_from_file(f)
                    logging.info(f"Uploaded object {obj_hash}")
        except Exception as e:
            logging.error(f"Failed to upload object {obj_hash}: {e}")
    repo_data['refs']['master'] = local_master
    doc_ref.set(repo_data)
    logging.info(f"Updated Firestore refs to: {repo_data['refs']}")
    with open(os.path.join(repo_path, '.flink', 'refs', 'remotes', 'origin', 'master'), 'w') as f:
        f.write(local_master)
    logging.info("Pushed changes to remote")

def clone(repo_name):
    global db, bucket, user_id
    initialize_firebase()
    doc_ref = db.collection('repositories').document(repo_name)
    doc = doc_ref.get()
    if not doc.exists:
        logging.error(f"Repository {repo_name} does not exist in Firestore")
        return
    repo_data = doc.to_dict()
    visibility = repo_data.get('visibility', 'public')
    if visibility == 'private' and (not user_id or repo_data.get('owner') != user_id):
        logging.error("Cannot clone private repository. Please login as the owner.")
        return
    refs = repo_data.get('refs', {})
    master_hash = refs.get('master')
    if not master_hash:
        logging.info("Remote repository is empty")
        return
    repo_path = os.path.join(os.getcwd(), repo_name)
    os.makedirs(repo_path, exist_ok=True)
    flink_dir = os.path.join(repo_path, '.flink')
    os.makedirs(os.path.join(flink_dir, 'objects'), exist_ok=True)
    os.makedirs(os.path.join(flink_dir, 'refs', 'heads'), exist_ok=True)
    os.makedirs(os.path.join(flink_dir, 'refs', 'remotes', 'origin'), exist_ok=True)
    with open(os.path.join(flink_dir, 'config'), 'w') as f:
        f.write(f"repo_id = {repo_name}")
    logging.info(f"Initialized empty Flink repository at {repo_path}")
    downloaded = set()
    def download_object(hash_):
        blob = bucket.blob(f"repositories/{repo_name}/objects/{hash_}")
        if blob.exists():
            object_dir = os.path.join(repo_path, '.flink', 'objects', hash_[:2])
            os.makedirs(object_dir, exist_ok=True)
            blob.download_to_filename(os.path.join(object_dir, hash_[2:]))
            logging.info(f"Downloaded object {hash_}")
            return True
        logging.error(f"Object {hash_} not found in Firebase")
        return False
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
            except Exception as e:
                logging.error(f"Error reading object {hash_}: {e}")
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
    except Exception as e:
        logging.error(f"Failed to checkout repository: {e}")

def list_repos():
    global db, user_id
    if not user_id:
        logging.error("Please login or register first.")
        return
    initialize_firebase()
    user_ref = db.collection('users').document(user_id)
    doc = user_ref.get()
    if not doc.exists:
        logging.error("User not found.")
        return
    repos = doc.to_dict().get('repos', [])
    if not repos:
        logging.info("You have no repositories.")
        return
    repo_list = []
    for repo_name in repos:
        repo_ref = db.collection('repositories').document(repo_name)
        repo_doc = repo_ref.get()
        if repo_doc.exists:
            data = repo_doc.to_dict()
            visibility = data.get('visibility', 'unknown')
            master_hash = data.get('refs', {}).get('master', 'none')[:8]
            repo_list.append([repo_name, visibility, master_hash])
    if repo_list:
        print("Your repositories:")
        print(tabulate(repo_list, headers=["Name", "Visibility", "Latest Commit"], tablefmt="grid"))
    else:
        print("No repositories found.")

def search(query):
    initialize_firebase()
    query_lower = query.lower()
    repo_results = []
    repos_ref = db.collection('repositories').where('visibility', '==', 'public').stream()
    for repo in repos_ref:
        repo_name = repo.id
        if query_lower in repo_name.lower():
            repo_data = repo.to_dict()
            owner_id = repo_data.get('owner', 'unknown')
            owner_email = db.collection('users').document(owner_id).get().to_dict().get('email', 'unknown')
            master_hash = repo_data.get('refs', {}).get('master', 'none')[:8]
            repo_results.append([repo_name, owner_email, master_hash])
    if repo_results:
        print("Matching repositories:")
        print(tabulate(repo_results, headers=["Repo Name", "Owner Email", "Latest Commit"], tablefmt="grid"))
    else:
        print("No matching repositories found.")

def all_repos():
    initialize_firebase()
    repos_ref = db.collection('repositories').where('visibility', '==', 'public').stream()
    repo_list = []
    for repo in repos_ref:
        repo_name = repo.id
        repo_data = repo.to_dict()
        owner_id = repo_data.get('owner', 'unknown')
        owner_email = db.collection('users').document(owner_id).get().to_dict().get('email', 'unknown')
        master_hash = repo_data.get('refs', {}).get('master', 'none')[:8]
        repo_list.append([repo_name, owner_email, master_hash])
    if repo_list:
        print("All public repositories:")
        print(tabulate(repo_list, headers=["Repo Name", "Owner Email", "Latest Commit"], tablefmt="grid"))
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
    clone_parser.add_argument('repo_arg', help='Repository name or URL')
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