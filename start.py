from VenvManager import VenvManager
from os.path import exists
from os import mkdir
from argparse import ArgumentParser
from subprocess import call
from shutil import rmtree

def CheckAndCreateDirectory(foldername : str):
    if exists(foldername) is False:
        mkdir(foldername)

def CreateDirectories():
    CheckAndCreateDirectory("dataset")
    CheckAndCreateDirectory("prompts")
    CheckAndCreateDirectory("upscaleInput")
    CheckAndCreateDirectory("upscaleOutput")

def CreateEnvironmentForRealESRGAN(osName : str):
    if exists("Real-ESRGAN"):
        return

    print("Cloning repository ...")
    process = call("git clone https://github.com/xinntao/Real-ESRGAN.git", shell=True)
    print("Installing required packages ...")
    command = ""
    if osName == 'Windows':
        command += "venv\Scripts\\activate.bat && "
        command += "venv\Scripts\pip.exe install basicsr facexlib gfpgan && "
        command += "venv\Scripts\pip.exe install -r Real-ESRGAN\\requirements.txt && "
        command += "cd Real-ESRGAN && call ..\\venv\Scripts\python.exe setup.py develop && "
        command += "..\\venv\Scripts\pip.exe uninstall torch torchvision --yes && "
        command += "..\\venv\Scripts\pip.exe install torch torchvision --index-url https://download.pytorch.org/whl/cu117 && "
        command += "cd .. && venv\Scripts\\deactivate.bat"
    elif osName == 'Linux':
        command += "source venv/Scripts/activate && "
        command += "pip3 install basicsr facexlib gfpgan && "
        command += "pip3 install -r Real-ESRGAN/requirements.txt && "
        command += "cd Real-ESRGAN && python setup.py develop && "
        command += "pip3 uninstall torch torchvision --yes && "
        command += "pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu117 && "
        command += "cd .. && deactivate"
    process = call(command, shell=True)
    print("Installation is completed!!! You can continue")

def CreateEnvrionment(venvManager : VenvManager, isRecreate : bool):
    if venvManager.IsEnvironmentCreated() is True and isRecreate is False:
        print(f"{venvManager.venvName} virtual environment is already exists")
        return
    
    if exists("Real-ESRGAN"):
        rmtree("Real-ESRGAN")
        
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

    CreateEnvironmentForRealESRGAN()
    CreateDirectories()

    venvManager.RunFile("main.py")