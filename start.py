from VenvManager import VenvManager
from os.path import exists
from os import mkdir
from argparse import ArgumentParser

def CreateEnvrionment(venvManager : VenvManager, isRecreate : bool):
    if venvManager.IsEnvironmentCreated() is True and isRecreate is False:
        print(f"{venvManager.venvName} virtual environment is already exists")
        return
    
    venvManager.CreateEnvironmentWPackageNames("packages.txt", isRecreate)
    venvManager.ReInstallTorch()

def ReInstall(venvManager : VenvManager):
    venvManager.InstallWPackageNames("packages.txt")
    venvManager.ReInstallTorch()

if __name__ == '__main__':
    parser = ArgumentParser(description="Prompt Tools WebUI")
    parser.add_argument("--reinstall", action="store_true", help="Reinstall the envrionment")
    parser.add_argument("--recreate", action="store_true", help="Recreate virtual environment")
    args = parser.parse_args()

    venvManager = VenvManager("venv")
    CreateEnvrionment(venvManager, args.recreate)

    if args.reinstall:
        ReInstall(venvManager)

    if exists("dataset") is False:
        mkdir("dataset")

    if exists("prompts") is False:
        mkdir("prompts")

    venvManager.RunFile("main.py")