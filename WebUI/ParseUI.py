def GetFiles(input):
    filesToParse = []

    if input is None:
        return filesToParse
    
    if isinstance(input, list) is False:
        filesToParse.append(input.name)
    else:
        for component in input:
            filesToParse.append(component.name)
    
    return filesToParse

def Parse(files, isTranslate):
    filenames = GetFiles(files)
    if len(filenames) == 0:
        return

    print("Parsed")
