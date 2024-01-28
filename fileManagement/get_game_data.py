import os
import json
import shutil
from subprocess import PIPE, run
import sys

GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go","build"]
def find_all_game_paths(source):
    game_paths = []
    for root, dirs, files in os.walk(source):
        # print(dirs)
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                # print(f"Game Paths : {path}")
                game_paths.append(path)
        break
    return game_paths

def get_name_from_paths(paths, to_strip):
    new_names =[]
    for path in paths:
        _, dir_name= os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)
    return new_names

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)

def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }
    
    with open(path, "w") as f:
        json.dump(data, f)

def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break
        break
    if code_file_name is None:
        return
    command = GAME_COMPILE_COMMAND + [code_file_name]
    run_command(command, path)

def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)

    result = run(command, stdout=PIPE, stdin=PIPE, universal_newLines=True)
    print("compiled result : ",result)

    os.chdir(cwd)

def main(source, target):
    # Hardcoding the pwd value is not recomended
    cwd = os.getcwd()           #currentWorkDirectory
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)
    # print(f"Full Paths : {source_path} {target_path}")
    game_paths = find_all_game_paths(source_path)
    new_game_dirs = get_name_from_paths(game_paths, "_game")
    # print(game_paths)    
    print(new_game_dirs)
    create_dir(target_path)
    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path)

    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs) 
    



# Command line Argumnets
if __name__=="__main__":   # Will only get executed when directly executing the file 
    args = sys.argv
    # print(f"Available Arguments {args}")
    if len(args) != 3: 
        raise Exception("YOu must pass a source and target directory - only !!")
    # Destructure the array to store the values in saparate variables 
    source, target = args[1:] # Here we dont want to consider the name of the script

    main(source, target)