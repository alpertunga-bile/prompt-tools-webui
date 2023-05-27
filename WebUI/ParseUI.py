from deep_translator import GoogleTranslator
from os.path import exists, join
from pathlib import Path
from os import getcwd
from glob import glob
from gradio import Progress

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

def Parse(files, isTranslate, progress=Progress(), isParsingAll = False):
    filenames = []

    if isParsingAll:
        filenames = files
    else:
        filenames = GetFiles(files)

    if len(filenames) == 0:
        print("There are no files to parse")
        return "::ERROR:: There are no files to parse"

    for promptFile in progress.tqdm(filenames, desc="Parsing"):
        if exists(promptFile) is False:
            continue
        ParseAndSave(promptFile, isTranslate)

    print("DONE !!!")
    return "DONE !!!"

def ParseAll(isTranslate):
    fastPath = join(getcwd(), "prompts")
    promptFiles = glob(f"{fastPath}\*.md")
    Parse(promptFiles, isTranslate, True)

def ParseAndSave(promptFile, isTranslate):
        file = open(promptFile, "r")
        lines = file.readlines()
        file.close()

        """
        Get folder path where is the Markdown file located
        """
        filename = Path(promptFile).stem
        
        positiveFilename = join("prompts", f"{filename}_positive.txt")
        negativeFilename = join("prompts", f"{filename}_negative.txt")

        positiveStr = ""
        negativeStr = ""

        isPositive = True
        for line in lines:
            """
            Determine if positive or negative prompt
            """
            if line.find("Positive Prompts") != -1:
                isPositive = True
            elif line.find("Negative Prompts") != -1:
                isPositive = False
            
            """
            Continue if it is heading, new line, long line
            """
            if line.startswith("#") or line == "\n" or line.startswith("---") or line == '  \n':
                continue

            line = Preprocess(line, isTranslate)

            if isPositive:
                positiveStr = positiveStr + line
            else:
                negativeStr = negativeStr + line

        """
        Delete comma and white space ', ' which is added in preprocess stage from the last of the line
        """
        positiveStr = positiveStr[:-2]
        negativeStr = negativeStr[:-2]

        positiveFile = open(positiveFilename, "w")
        positiveFile.write(positiveStr)
        positiveFile.close()

        negativeFile = open(negativeFilename, "w")
        negativeFile.write(negativeStr)
        negativeFile.close()

"""
Preprocess the line that get from markdown file
"""
def Preprocess(line, isTranslate):
    """
    Check mostly used starting syntax
    """
    if line.startswith("- [ ] ") or line.startswith("- [x] "):
        line = line[6:]
    elif line.startswith("-[ ] ") or line.startswith("-[x] "):
        line = line[5:]
    elif line.startswith("-[] "):
        line = line[4:]
    elif line.startswith("- ") or line.startswith("> "):
        line = line[2:]
    
    """
    Check for newline operator
    """
    if line.endswith("\n"):
        line = line[:-1]

    """
    Check for whitespaces
    """
    line = line.strip()

    """
    translation progress is done line by line because summed string's length will exceed the character limit of the translator
    and in experiments it's seen that translator can not translate the non English word from the whole string
    """
    translator = GoogleTranslator(source='auto', target='en')
    if isTranslate:
        line = translator.translate(line)

    """
    Add comma to seperate prompts and provide continuousness 
    """
    line = line + ", "

    return line