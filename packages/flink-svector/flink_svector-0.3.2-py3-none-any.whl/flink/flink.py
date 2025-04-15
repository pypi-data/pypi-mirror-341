import argparse
import getpass
import hashlib
import json
import os
import zlib
from mimetypes import init

import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1 import DocumentReference
from tabulate import tabulate

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
        print("Service account file found")
        cred = credentials.Certificate(service_account_path)
        print("Credentials loaded")
        if firebase_admin._apps:
            print("Firebase app already initialized")
        else:
            firebase_admin.initialize_app(cred, {'storageBucket': 'sparrkmail.appspot.com'})
            print("Firebase app initialized")
        db = firestore.client()
        print("Firestore client created")
        bucket = storage.bucket()
        print("Storage bucket accessed")
    except Exception as e:
        print(f"Firebase initialization failed: {type(e).__name__}: {str(e)}")
        raise

def load_user_credentials():
    global user_id
    creds_path = os.path.expanduser('~/.flink/credentials.json')
    if os.path.exists(creds_path):
        with open(creds_path, 'r') as f:
            creds = json.load(f)
            user_id = creds.get('user_id')
        print(f"Loaded user ID: {user_id}")
    else:
        print("No user credentials found. Please login or register.")

def save_user_credentials(user_id):
    creds_path = os.path.expanduser('~/.flink')
    os.makedirs(creds_path, exist_ok=True)
    with open(os.path.join(creds_path, 'credentials.json'), 'w') as f:
        json.dump({'user_id': user_id}, f)
    print(f"Saved user credentials for {user_id}")

def register(email, password):
    global user_id
    initialize_firebase()
    user_id = hashlib.sha256(email.encode()).hexdigest()
    user_ref = db.collection('users').document(user_id)
    if user_ref.get().exists:
        print("User already exists. Please login.")
        return
    user_ref.set({
        'email': email,
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'repos': []
    })
    save_user_credentials(user_id)
    print(f"Registered user {email} with ID {user_id}")

def login(email, password):
    global user_id
    initialize_firebase()
    user_id = hashlib.sha256(email.encode()).hexdigest()
    user_ref = db.collection('users').document(user_id)
    doc = user_ref.get()
    if not doc.exists:
        print("User does not exist. Please register.")
        return
    data = doc.to_dict()
    if data['password'] != hashlib.sha256(password.encode()).hexdigest():
        print("Invalid password.")
        return
    save_user_credentials(user_id)
    print(f"Logged in as {email} (ID: {user_id})")

def find_repo_path():
    current_dir = os.getcwd()
    while current_dir != '/':
        if os.path.exists(os.path.join(current_dir, '.flink')):
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

def find_repo_path():
    """
    Find the root path of the Flink repository.
    Returns the repository root path if found, None otherwise.
    The function verifies not only that .flink directory exists but also that it contains a valid config file.
    """
    current_dir = os.getcwd()
    original_dir = current_dir
    
    # Traverse up the directory tree until we find a valid .flink directory or reach the filesystem root
    while current_dir != '/':
        flink_dir = os.path.join(current_dir, '.flink')
        config_file = os.path.join(flink_dir, 'config')
        
        # Check if both .flink directory exists and it contains a config file
        if os.path.isdir(flink_dir) and os.path.isfile(config_file):
            # Verify the config file has valid content
            try:
                with open(config_file, 'r') as f:
                    config_content = f.read().strip()
                    if config_content and 'repo_id' in config_content:
                        return current_dir
            except:
                pass  # If config file can't be read or is invalid, continue searching
        
        # Move up one directory
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # Safety check for Windows
            break
        current_dir = parent_dir
    
    return None

def is_ignored(file_path, repo_path, ignore_patterns=None):
    """
    Check if a file should be ignored based on .gitignore patterns.
    Returns True if the file should be ignored, False otherwise.
    """
    # Always ignore the .flink directory
    rel_path = os.path.relpath(file_path, repo_path)
    if rel_path.startswith('.flink' + os.sep) or rel_path == '.flink':
        return True
    
    # If no ignore patterns were provided, try to load them from .gitignore
    if ignore_patterns is None:
        ignore_patterns = []
        gitignore_path = os.path.join(repo_path, '.gitignore')
        if os.path.isfile(gitignore_path):
            try:
                with open(gitignore_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            ignore_patterns.append(line)
            except:
                pass  # If .gitignore can't be read, proceed without ignore patterns
    
    # Check if the file matches any ignore pattern
    for pattern in ignore_patterns:
        # Handle directory patterns (ending with /)
        if pattern.endswith('/'):
            if rel_path.startswith(pattern) or rel_path.startswith(pattern[:-1] + os.sep):
                return True
        # Handle file patterns
        elif pattern.endswith('/*'):
            dir_pattern = pattern[:-1]
            if os.path.dirname(rel_path) == dir_pattern[:-1] or os.path.dirname(rel_path).startswith(dir_pattern):
                return True
        # Handle wildcard patterns
        elif '*' in pattern:
            import fnmatch
            if fnmatch.fnmatch(rel_path, pattern):
                return True
        # Handle exact matches
        elif rel_path == pattern or rel_path.startswith(pattern + os.sep):
            return True
    
    return False

def expand_path(path, repo_path):
    """
    Expand a path, which may include wildcards, to a list of actual file paths.
    All paths are guaranteed to be within the repository boundaries.
    """
    expanded_paths = []
    
    # Handle the special case of '.' (current directory)
    if path == '.':
        for root, dirs, files in os.walk(repo_path):
            # Filter out .flink directory
            if '.flink' in dirs:
                dirs.remove('.flink')
            
            # Add all files to the list
            for file in files:
                full_path = os.path.join(root, file)
                expanded_paths.append(full_path)
    
    # Handle specific file or directory
    elif os.path.exists(path):
        # If it's a directory, add all files within it recursively
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                # Filter out .flink directory if we're at repo_path
                if root == repo_path and '.flink' in dirs:
                    dirs.remove('.flink')
                
                # Add all files to the list
                for file in files:
                    full_path = os.path.join(root, file)
                    expanded_paths.append(full_path)
        # If it's a file, just add it
        else:
            expanded_paths.append(path)
    
    return expanded_paths

def add(paths):
    """
    Add files to the staging area.
    
    This function:
    1. Validates that we're in a repository
    2. Requires the command to be run from the repository root
    3. Expands wildcard paths to actual files
    4. Filters out files that are outside the repository
    5. Respects .gitignore patterns
    6. Always skips the .flink directory
    7. Provides feedback for each staged file
    """
    # Find the repository root
    repo_path = find_repo_path()
    if not repo_path:
        print("Not in a Flink repository")
        return
    
    # Verify that we're running from the repository root
    current_dir = os.getcwd()
    if current_dir != repo_path:
        print(f"Error: Run 'flink add .' from the repository root ({repo_path})")
        return
    
    # Load ignore patterns from .gitignore
    ignore_patterns = []
    gitignore_path = os.path.join(repo_path, '.gitignore')
    if os.path.isfile(gitignore_path):
        try:
            with open(gitignore_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        ignore_patterns.append(line)
        except:
            pass  # If .gitignore can't be read, proceed without ignore patterns
    
    # Load the current index
    index_path = os.path.join(repo_path, '.flink', 'index.json')
    index = {}
    if os.path.exists(index_path):
        try:
            with open(index_path, 'r') as f:
                index = json.load(f)
        except:
            # If index can't be read, start with an empty index
            index = {}
    
    # Process each path argument
    staged_files = []
    for path_arg in paths:
        # Expand the path to actual file paths
        expanded_paths = expand_path(path_arg, repo_path)
        
        for file_path in expanded_paths:
            # Verify the file is within the repository boundaries
            if not os.path.abspath(file_path).startswith(repo_path):
                print(f"Error: File {file_path} is outside repository")
                continue
            
            # Skip files that should be ignored
            if is_ignored(file_path, repo_path, ignore_patterns):
                continue
            
            # Add the file to the index
            rel_path = os.path.relpath(file_path, repo_path)
            try:
                blob_hash = create_blob(file_path, repo_path)
                index[rel_path] = blob_hash
                staged_files.append(rel_path)
                print(f"Staged {rel_path}")
            except Exception as e:
                print(f"Error staging {rel_path}: {str(e)}")
    
    # Save the updated index
    if staged_files:
        try:
            with open(index_path, 'w') as f:
                json.dump(index, f)
            print(f"Added {len(staged_files)} file(s) to staging area")
        except Exception as e:
            print(f"Error saving index: {str(e)}")
    else:
        print("No files staged")

def commit(message):
    global user_id
    if not user_id:
        print("Please login or register first.")
        return
    initialize_firebase()
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
    email = db.collection('users').document(user_id).get().to_dict()['email']
    commit_hash = create_commit(tree_hash, parent_hash, email, message, repo_path)
    with open(master_ref, 'w') as f:
        f.write(commit_hash)
    os.remove(index_path)
    print(f"Committed {commit_hash}")

def push():
    global db, bucket, user_id
    if not user_id:
        print("Please login or register first.")
        return
    initialize_firebase()
    repo_path = find_repo_path()
    if not repo_path:
        print("Not in a Flink repository")
        return
    with open(os.path.join(repo_path, '.flink', 'config'), 'r') as f:
        repo_id = f.read().split('=')[1].strip()
    doc_ref = db.collection('repositories').document(repo_id)
    doc = doc_ref.get()
    if not doc.exists:
        print(f"Repository {repo_id} does not exist in Firestore")
        return
    repo_data = doc.to_dict()
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
    print(f"Remote refs before push: {remote_refs}")
    remote_master = remote_refs.get('master')
    objects = get_reachable_objects(local_master, repo_path)
    if remote_master:
        remote_objects = get_reachable_objects(remote_master, repo_path)
        objects -= remote_objects
    for obj_hash in objects:
        obj_path = os.path.join(repo_path, '.flink', 'objects', obj_hash[:2], obj_hash[2:])
        with open(obj_path, 'rb') as f:
            blob = bucket.blob(f"repositories/{repo_id}/objects/{obj_hash}")
            if not blob.exists():
                blob.upload_from_file(f)
                print(f"Uploaded object {obj_hash}")
    doc_ref.set({
        'refs': {'master': local_master},
        'visibility': repo_data['visibility'],
        'owner': user_id
    })
    print(f"Updated Firestore refs to: {{'master': '{local_master}'}}")
    with open(os.path.join(repo_path, '.flink', 'refs', 'remotes', 'origin', 'master'), 'w') as f:
        f.write(local_master)
    print("Pushed changes to remote")

def clone(repo_name):
    global db, bucket, user_id
    initialize_firebase()
    doc_ref = db.collection('repositories').document(repo_name)
    doc = doc_ref.get()
    print(f"Firestore doc exists: {doc.exists}")
    if not doc.exists:
        print(f"Repository {repo_name} does not exist in Firestore")
        return
    repo_data = doc.to_dict()
    visibility = repo_data.get('visibility', 'public')
    if visibility == 'private' and (not user_id or repo_data.get('owner') != user_id):
        print("Cannot clone private repository. Please login as the owner.")
        return
    refs = repo_data.get('refs', {})
    print(f"Refs: {refs}")
    master_hash = refs.get('master')
    print(f"Master hash: {master_hash}")
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
    doc_ref.set({
        'refs': refs,
        'visibility': visibility,
        'owner': repo_data.get('owner', 'unknown')
    })
    downloaded = set()
    def download_object(hash_):
        blob = bucket.blob(f"repositories/{repo_name}/objects/{hash_}")
        if blob.exists():
            object_dir = os.path.join(repo_path, '.flink', 'objects', hash_[:2])
            os.makedirs(object_dir, exist_ok=True)
            blob.download_to_filename(os.path.join(object_dir, hash_[2:]))
            print(f"Downloaded object {hash_}")
            return True
        print(f"Object {hash_} not found in Firebase")
        return False
    def download_recursive(hash_):
        if hash_ in downloaded:
            return
        if download_object(hash_):
            downloaded.add(hash_)
            try:
                type_, content = read_object(hash_, repo_path)
                print(f"Read object {hash_} as {type_}")
                if type_ == 'commit':
                    tree_hash = content.decode().split('\n')[0].split(' ')[1]
                    download_recursive(tree_hash)
                    parent_line = [l for l in content.decode().split('\n') if l.startswith('parent')]
                    if parent_line:
                        download_recursive(parent_line[0].split(' ')[1])
                elif type_ == 'tree':
                    for _, _, hash_ in parse_tree(content):
                        download_recursive(hash_)
            except Exception as e:
                print(f"Error reading object {hash_}: {e}")
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
    global db, user_id
    if not user_id:
        print("Please login or register first.")
        return
    initialize_firebase()
    user_ref = db.collection('users').document(user_id)
    doc = user_ref.get()
    if not doc.exists:
        print("User not found.")
        return
    repos = doc.to_dict().get('repos', [])
    if not repos:
        print("You have no repositories.")
        return
    print("Your repositories:")
    for repo_name in repos:
        repo_ref = db.collection('repositories').document(repo_name)
        repo_doc = repo_ref.get()
        if repo_doc.exists:
            data = repo_doc.to_dict()
            visibility = data.get('visibility', 'unknown')
            master_hash = data.get('refs', {}).get('master', 'none')
            print(f"- {repo_name} ({visibility}, latest commit: {master_hash[:8]})")
        else:
            print(f"- {repo_name} (not found in Firestore)")

def search(query):
    initialize_firebase()
    query_lower = query.lower()
    repo_results = []
    user_results = []

    # Search repositories
    repos_ref = db.collection('repositories')
    repo_query = repos_ref.where('visibility', '==', 'public').stream()
    for repo in repo_query:
        repo_name = repo.id
        if query_lower in repo_name.lower():
            repo_data = repo.to_dict()
            owner = repo_data.get('owner', 'unknown')
            master_hash = repo_data.get('refs', {}).get('master', 'none')
            repo_results.append([repo_name, owner, master_hash[:8]])

    # Search users
    users_ref = db.collection('users')
    user_query = users_ref.stream()
    for user in user_query:
        user_data = user.to_dict()
        email = user_data.get('email', 'unknown')
        if query_lower in email.lower():
            user_results.append([email, user.id])

    # Display results
    if repo_results:
        print("Matching repositories:")
        print(tabulate(repo_results, headers=["Repo Name", "Owner", "Latest Commit"], tablefmt="grid"))
    else:
        print("No matching repositories found.")

    if user_results:
        print("\nMatching users:")
        print(tabulate(user_results, headers=["Email", "User ID"], tablefmt="grid"))
    else:
        print("\nNo matching users found.")

def all_repos():
    initialize_firebase()
    repos_ref = db.collection('repositories')
    repo_query = repos_ref.where('visibility', '==', 'public').order_by('__name__').stream()
    repo_list = []
    for repo in repo_query:
        repo_name = repo.id
        repo_data = repo.to_dict()
        owner = repo_data.get('owner', 'unknown')
        master_hash = repo_data.get('refs', {}).get('master', 'none')
        repo_list.append([repo_name, owner, master_hash[:8]])

    if repo_list:
        print("All public repositories:")
        print(tabulate(repo_list, headers=["Repo Name", "Owner", "Latest Commit"], tablefmt="grid"))
    else:
        print("No public repositories found.")

def main():
    load_user_credentials()
    parser = argparse.ArgumentParser(description="Flink: A custom Git-like version control system")
    parser.add_argument('--version', action='version', version='flink 0.1.4')
    subparsers = parser.add_subparsers(dest='command')

    register_parser = subparsers.add_parser('register', help='Register a new user')
    register_parser.add_argument('email', help='User email')
    register_parser.add_argument('password', help='User password', nargs='?', default=None)

    login_parser = subparsers.add_parser('login', help='Login as a user')
    login_parser.add_argument('email', help='User email')
    login_parser.add_argument('password', help='User password', nargs='?', default=None)

    init_parser = subparsers.add_parser('init', help='Initialize a new repository')
    init_parser.add_argument('repo_name', nargs='?', default=os.getcwd().split(os.sep)[-1], help='Repository name')

    add_parser = subparsers.add_parser('add', help='Add files to staging area')
    add_parser.add_argument('files', nargs='+', help='Files to add')

    commit_parser = subparsers.add_parser('commit', help='Commit staged changes')
    commit_parser.add_argument('-m', '--message', required=True, help='Commit message')

    push_parser = subparsers.add_parser('push', help='Push changes to remote')

    clone_parser = subparsers.add_parser('clone', help='Clone a repository')
    clone_parser.add_argument('repo_name', help='Repository name to clone')

    list_parser = subparsers.add_parser('list-repos', help='List your repositories')

    search_parser = subparsers.add_parser('search', help='Search for repositories or users')
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