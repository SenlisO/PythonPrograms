import os

# get file directory from user
file_path = input("Enter working directory: ")

# move to working directory.  print error message if directory doesn't exist
try:
    os.chdir(file_path)
except FileNotFoundError as e:
    print("That directory was not found")

# iterate though all files in directory
for file_name in os.listdir():
    name, ext = os.path.splitext(file_name)
    if ext == ".zip":
    
        game_name = file_name
        game_name = game_name[7:]  # remove the first 7 characters

        os.rename(file_name, game_name)
