from VenvManager import VenvManager

if __name__ == '__main__':
    venvManager = VenvManager("venv")

    if venvManager.IsEnvironmentCreated is False:
        venvManager.CreateEnvironmentWPackageNames("packages.txt")
    
    venvManager.RunFile("main.py")