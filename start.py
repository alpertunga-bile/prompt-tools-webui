from VenvManager import VenvManager
from os.path import exists
from os import mkdir

if __name__ == '__main__':
    venvManager = VenvManager("venv")

    if venvManager.IsEnvironmentCreated() is False:
        venvManager.CreateEnvironmentWPackageNames("packages.txt")

    if exists("dataset") is False:
        mkdir("dataset")

    if exists("prompts") is False:
        mkdir("prompts")
    
    venvManager.RunFile("main.py")