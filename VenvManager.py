from shutil import rmtree
from os import remove
from subprocess import call, STDOUT
from os.path import exists
from platform import system
from time import sleep

class VenvManager:
    osName = ""
    venvName = "venv"
    isSilent = False

    def __init__(self, envName, isSilent=False):
        self.osName = system()
        self.venvName = envName
        self.isSilent = isSilent

    def RunCommand(self, command):
        if self.isSilent:
            logFile = open("logs.txt", mode="w")
            result = call(command, shell=True, stdout=logFile, stderr=STDOUT)
            logFile.close()
        else:
            result = call(command, shell=True)
            _ = print("Command executed successfully") if result == 0 else print(f"Error occured when running {command}")

    def IsEnvironmentCreated(self):
        return exists(self.venvName)

    """
    Get Command Functions
    """

    def GetCreateEnvironmentCommand(self):
        venvCommand = ""
        if self.osName == 'Linux':
            venvCommand += f"pip install virtualenv && virtual {self.venvName}"
        elif self.osName == 'Windows':
            venvCommand += f"python -m venv {self.venvName}"
        
        return venvCommand
    
    def GetInstallWRequirementsCommand(self):
        venvCommand = ""
        if self.osName == 'Linux':
            venvCommand += f"source {self.venvName}/bin/activate && "
            venvCommand += "pip3 install -r requirements.txt && "
            venvCommand += "deactivate"
        elif self.osName == 'Windows':
            venvCommand += f".\\{self.venvName}\\Scripts\\activate.bat && "
            venvCommand += f".\\{self.venvName}\\Scripts\\pip.exe install -r requirements.txt && "
            venvCommand += f".\\{self.venvName}\\Scripts\\deactivate.bat"
        
        return venvCommand
    
    def GetInstallWPackagesCommand(self, path):
        packageFile = open(path, "r")
        packages = packageFile.readlines()
        packageFile.close()

        pipPackageCommand = "".join(packages).replace("\n", " ")

        venvCommand = ""
        if self.osName == 'Linux':
            venvCommand += f"source {self.venvName}/bin/activate && "
            venvCommand += f"pip3 install {pipPackageCommand} && "
            venvCommand += "deactivate"
        elif self.osName == 'Windows':
            venvCommand += f".\\{self.venvName}\\Scripts\\activate.bat && "
            venvCommand += f".\\{self.venvName}\\Scripts\\pip.exe install {pipPackageCommand} && "
            venvCommand += f".\\{self.venvName}\\Scripts\\deactivate.bat"
        
        return venvCommand
    
    def GetCreateRequirementsFileCommand(self):
        venvCommand = ""
        if self.osName == 'Linux':
            venvCommand += f"source {self.venvName}/bin/activate && "
            venvCommand += f"pip3 freeze > requirements.txt && "
            venvCommand += "deactivate"
        elif self.osName == 'Windows':
            venvCommand += f".\\{self.venvName}\\Scripts\\activate.bat && "
            venvCommand += f".\\{self.venvName}\\Scripts\\pip.exe freeze > requirements.txt && "
            venvCommand += f".\\{self.venvName}\\Scripts\\deactivate.bat"

        return venvCommand
    
    def GetCreateNewRequirementsFileCommand(self):
        venvCommand = ""
        if self.osName == 'Linux':
            venvCommand += f"source {self.venvName}/bin/activate && pip3 freeze > new_requirements.txt"
        elif self.osName == 'Windows':
            venvCommand += f".\\{self.venvName}\\Scripts\\activate.bat && .\\{self.venvName}\\Scripts\\pip.exe freeze > new_requirements.txt"

        return venvCommand
    
    def GetInstallWNewRequirementsFileCommand(self):
        venvCommand = ""
        if self.osName == 'Linux':
            venvCommand += "pip3 install -r new_requirements.txt --upgrade && "
            venvCommand += "deactivate"
        elif self.osName == 'Windows':
            venvCommand += f".\\{self.venvName}\\Scripts\\pip.exe install -r new_requirements.txt --upgrade && "
            venvCommand += f".\\{self.venvName}\\Scripts\\deactivate.bat"
        
        return venvCommand
    
    def GetRunFileCommand(self, filepath):
        venvCommand = ""
        if self.osName == 'Linux':
            venvCommand += f"source {self.venvName}/bin/activate && "
            venvCommand += f"python3 {filepath} && "
            venvCommand += "deactivate"
        elif self.osName == 'Windows':
            venvCommand += f".\\{self.venvName}\\Scripts\\activate.bat && "
            venvCommand += f".\\{self.venvName}\\Scripts\\python.exe {filepath} && "
            venvCommand += f".\\{self.venvName}\\Scripts\\deactivate.bat"

        return venvCommand
    
    def GetRunCommandInEnvironmentCommand(self, command):
        venvCommand = ""
        if self.osName == 'Linux':
            venvCommand += f"source {self.venvName}/bin/activate && "
            venvCommand += f"{command} && "
            venvCommand += "deactivate"
        elif self.osName == 'Windows':
            venvCommand += f".\\{self.venvName}\\Scripts\\activate.bat && "
            venvCommand += f"{command} && "
            venvCommand += f".\\{self.venvName}\\Scripts\\deactivate.bat"

        return venvCommand
    
    def GetReInstallTorchCommand(self):
        venvCommand = ""
        venvCommand = ""
        if self.osName == "Linux":
            venvCommand = "pip3 uninstall torch --yes && pip3 "
        elif self.osName == "Windows":
            venvCommand = "venv\\Scripts\\pip.exe uninstall torch --yes && venv\\Scripts\\pip.exe "
        
        venvCommand += "install torch --index-url https://download.pytorch.org/whl/cu118"

        return venvCommand 
    
    """
    Run Functions
    """

    def RunFile(self, filepath):
        if exists(self.venvName) is False:
            print(f"{self.venvName} is not exists")
            return
        
        if exists(filepath) is False:
            print(f"{filepath} is not exists")
            return

        self.RunCommand(self.GetRunFileCommand(filepath))

    def RunCommandInEnvironment(self, command):
        if exists(self.venvName) is False:
            print(f"{self.venvName} is not exists")
            return
        
        self.RunCommand(self.GetRunCommandInEnvironmentCommand(command))

    """
    Create Functions
    """

    def CreateEnvironment(self, removeExistsEnvironment=False):
        if removeExistsEnvironment is False and exists(self.venvName):
            print(f"{self.venvName} virtual environment is already exists")
            return
        
        if exists(self.venvName):
            rmtree(self.venvName)

        self.RunCommand(self.GetCreateEnvironmentCommand())

    def CreateEnvironmentWRequirementsFile(self, removeExistsEnvironment=False):
        self.CreateEnvironment(removeExistsEnvironment)
        self.InstallWRequirementsFile()

    def CreateEnvironmentWPackageNames(self, packagesPath, removeExistsEnvironment=False):
        self.CreateEnvironment(removeExistsEnvironment)
        self.InstallWPackageNames(packagesPath)

    """
    Install Functions
    """

    def InstallWRequirementsFile(self):
        if exists(self.venvName) is False:
            print(f"{self.venvName} is not exists")
            return

        if exists("requirements.txt") is False:
            print("requirements.txt is not found")
            return

        self.RunCommand(self.GetInstallWRequirementsCommand())

    def InstallWPackageName(self, packageName):
        if exists(self.venvName) is False:
            print(f"{self.venvName} is not exists")
            return
        
        filepath = "single_package.txt"

        file = open(filepath, "w")
        file.write(packageName)
        file.close()

        self.InstallWPackageNames(filepath)

        remove(filepath)

    def InstallWPackageNames(self, path):
        if exists(self.venvName) is False:
            print(f"{self.venvName} is not exists")
            return

        if exists(path) is False:
            print(f"{path} is not exists")
            return

        self.RunCommand(self.GetInstallWPackagesCommand(path))
        self.RunCommand(self.GetCreateRequirementsFileCommand())

    def ReInstallTorch(self):
        if exists(self.venvName) is False:
            print(f"{self.venvName} is not exists")
            return
        
        command = self.GetReInstallTorchCommand()
        self.RunCommandInEnvironment(command)

    """
    Update Functions
    """
    def UpdateEnvironment(self):
        if exists(self.venvName) is False:
            print(f"{self.venvName} is not exists")
            return

        print("Updating ...")
        self.RunCommand(self.GetCreateNewRequirementsFileCommand())

        sleep(0.5)

        file = open("new_requirements.txt", "r")
        lines = file.readlines()
        file.close()

        file = open("new_requirements.txt", "w")
        for line in lines:
            file.writelines(line.replace("==", ">="))

        file.close()
        
        sleep(0.5)

        self.RunCommand(self.GetInstallWNewRequirementsFileCommand())
        remove("new_requirements.txt")