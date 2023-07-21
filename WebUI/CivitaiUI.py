from json import loads
from requests import get
from re import sub, compile, IGNORECASE
from os.path import exists
import gc
from gradio import Progress
from os import startfile

def Show():
    startfile("dataset")

def GetMaxPage():
    maxPage = 200000
    try:
        url = f"https://civitai.com/api/v1/images?limit=1"
        header = {"content-type":"application.json"}
        jsonFile = loads(get(url, headers=header).text)
        maxPage = int(jsonFile['metadata']['totalPages'])
    except:
        maxPage = 200000

    return maxPage

def GetUrl(imageLimit, sort, period, nsfw):
    sort = sort.replace(" ", "+")
    period = period.replace(" ", "")

    url = ""
    if nsfw == "All":
        url = f"https://civitai.com/api/v1/images?limit={imageLimit}&sort={sort}&period={period}&page="
    else:
        url = f"https://civitai.com/api/v1/images?limit={imageLimit}&sort={sort}&period={period}&nsfw={nsfw}&page="

    return url

def Enhance(positiveFilename, negativeFilename, imageLimit, pageStart, pageEnd, sort, period, nsfw, wantedPrompts, unwantedPrompts, progress=Progress()):
    baseUrl = GetUrl(imageLimit, sort, period, nsfw)

    wantedPromptsList = wantedPrompts.split(",")
    unwantedPromptsList = unwantedPrompts.split(",")

    positiveFilename = f"dataset/{positiveFilename}.txt"
    negativeFilename = f"dataset/{negativeFilename}.txt"

    positivePrompts = []
    negativePrompts = []

    if exists(positiveFilename) is False:
        file = open(positiveFilename, "w")
        file.close()
    else:
        file = open(positiveFilename, "r")
        positivePrompts = file.readlines()
        file.close()
    
    if exists(negativeFilename) is False:
        file = open(negativeFilename, "w")
        file.close()
    else:
        file = open(negativeFilename, "r")
        negativePrompts = file.readlines()
        file.close()

    header = {"content-type":"application.json"}

    for pageNumber in progress.tqdm(range(pageStart, pageEnd + 1), desc="Getting Data From Pages"):
        url = baseUrl + str(pageNumber)
        try:
            jsonFile = loads(get(url, headers=header).text)
        except:
            continue

        for imageIndex in range(0, imageLimit + 1):
            positive, negative = GetPrompts(jsonFile, imageIndex)
            if positive is None: 
                continue

            positive = Preprocess(positive).lower()

            if CanAdd(positive, wantedPromptsList, unwantedPromptsList) is False:
                continue
            
            positive += "\n"
            positivePrompts.append(positive)

            if negative is None:
                continue

            negative = Preprocess(negative).lower()

            negative += "\n"
            negativePrompts.append(negative)

        positivePrompts = [*set(positivePrompts)]
        negativePrompts = [*set(negativePrompts)]
        gc.collect()

    positiveFile = open(positiveFilename, "w")
    positiveFile.writelines(positivePrompts)
    positiveFile.close()

    del positivePrompts

    negativeFile = open(negativeFilename, "w")
    negativeFile.writelines(negativePrompts)
    negativeFile.close()

    del negativePrompts

    gc.collect()

    print("Civitai> DONE !!!")
    return "Done !!!"

def GetPrompts(jsonFile, imageIndex):
    positivePrompt = None
    negativePrompt = None

    try:
        positivePrompt = jsonFile['items'][imageIndex]['meta']['prompt']
    except:
        positivePrompt = None

    try:
        negativePrompt = jsonFile['items'][imageIndex]['meta']['negativePrompt']
    except:
        negativePrompt = None

    return positivePrompt, negativePrompt

def CheckWholeWord(word : str, whole_string : str) -> bool:
    return True if compile(r'\b({0})\b'.format(word), flags=IGNORECASE).search(whole_string) is not None else False

def CanAdd(positivePrompt, wantedPrompts, unwantedPrompts):
    canAdd = False

    for unwanted in unwantedPrompts:
        if CheckWholeWord(unwanted, positivePrompt):
            return False

    if any(wanted in positivePrompt for wanted in wantedPrompts):
        canAdd = True

    return canAdd

def Preprocess(line):
    tempLine = line.encode("ascii", "ignore")
    tempLine = tempLine.decode()
    tempLine = tempLine.replace("\n", ", ")
    tempLine = sub(r'<.+?>', '', tempLine)
    tempLine = tempLine.strip()
    tempLine = tempLine.replace("  ", " ")
    tempLine = tempLine.replace("\t", " ")
    tempLine = tempLine.replace(", ,", ", ")
    tempLine = tempLine.replace(",,", ",")
    tempLine = tempLine.replace(",  , ", ", ")
    if tempLine.startswith(" "):
        tempLine = tempLine[1:]
    return tempLine
