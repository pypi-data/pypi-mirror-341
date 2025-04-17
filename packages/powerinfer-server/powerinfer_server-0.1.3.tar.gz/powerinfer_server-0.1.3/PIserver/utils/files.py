import csv
from PIserver.constants import *
import tabulate
import shutil
from pathlib import Path
import sys
import json

# All the printings


def print_table(data: list, header: list):
    '''print data in table format using tabulate'''
    print(tabulate.tabulate(data, headers=header, tablefmt="plain"))
    
def log_error(msg):
    sys.stderr.write(f"Error: {msg}\n")

# All the file operations
def check_existence(path):
    return Path(path).exists()

def check_list_file():
    if not DEFAULT_MODEL_LIST_FILE.exists():
        with open(DEFAULT_MODEL_LIST_FILE, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(LOCAL_LIST_HEADER)  

def get_absolute_path(path):
    return Path(path).resolve()

def get_folder_size(path: Path):
    return sum(f.stat().st_size if f.is_file() else get_folder_size(f) for f in path.glob('**/*'))

def remove_dir(path):
    path = Path(path)
    if not path.exists():
        log_error(f"Directory {path} not found.")
        return REMOVE_RESULT.NOT_FOUND
    try:
        shutil.rmtree(path)
    except Exception as e:
        log_error(f"Unable to remove directory {path}: {e}")
        return REMOVE_RESULT.ERROR  
    return REMOVE_RESULT.SUCCESS
        
def remove_file(path):
    path = Path(path)
    if path.exists():
        try:
            path.unlink()
            print(f"File {path} successfully removed.")
            return REMOVE_RESULT.SUCCESS
        except Exception as e:
            log_error(f"Unable to remove file {path}: {e}")
            return REMOVE_RESULT.ERROR
    else:
        return REMOVE_RESULT.NOT_FOUND
            
# All the csv file operations
def add_row(model: list):
    '''add a row to the model list file'''
    check_list_file()
    with open(DEFAULT_MODEL_LIST_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(model)
    
def filter_rows(check):
    '''filter rows in the model list file'''
    check_list_file()
    with open(DEFAULT_MODEL_LIST_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows, rest = [], []
        for row in reader:
            if len(row) > 0 and check(row):
                rows.append(row)
            else:
                rest.append(row)
        return rows, rest
    
def write_rows(rows: list):
    '''write rows to the model list file'''
    check_list_file()
    with open(DEFAULT_MODEL_LIST_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(LOCAL_LIST_HEADER)
        writer.writerows(rows)

# All the string operations        
def parse_model(name):
    arr = name.split(':')
    return arr[0], arr[1] if len(arr) > 1 else None

def check_model_name_with_size(name):
    if ':' not in name:
        log_error("Please specify the model size. Format the model name like 'USR/NAME:SIZE'.")
        return name, ""
    return parse_model(name)

def get_uname_from_model(mname):
    if '/' not in mname:
        return mname, ""
    return mname.split('/')[1], mname.split('/')[0]

def parse_condition(model):
    name, size = parse_model(model)
    if size is None:
        return lambda x: x[0] == name
    else:
        return lambda x: x[0] == name and x[1] == size
    
# All the json file operations
def read_file(path: Path) -> dict:
    try:
        with open(path, 'r') as f:
            return dict(json.load(f))
    except json.JSONDecodeError:
        return {}
    except FileNotFoundError:
        path.touch(0o755, exist_ok=True)
        return {}
    
def write_file(path: Path | str, data: dict) -> bool:
    path = Path(path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
            return True
    except Exception as e:
        log_error(f"Unable to write to file {path}: {e}")
        return False
    
def add_engine(name, path):
        if not check_existence(path):
            log_error(f"File {path} does not exist. Please check the path and try again.")
            return False
        path = str(get_absolute_path(path))
        engines = read_file(DEFAULT_ENGINE_LIST_FILE)
        if name in engines:
            response = input(f"Engine {name} already exists. Do you want to overwrite it? (y/n)")
            if response != "y":
                print("Installation cancelled.")
                return False
            if engines[name] != path and check_existence(engines[name]):
                print(f"Removing old engine file {engines[name]}...")
                res = remove_file(engines[name])
                if res == REMOVE_RESULT.ERROR:
                    log_error(f"Unable to remove old engine file {engines[name]}. Remove it manually or try after fixing the error.")
                    return False
        engines[name] = path
        write_file(DEFAULT_ENGINE_LIST_FILE, engines)
        return True