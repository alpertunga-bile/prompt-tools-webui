from json import loads
from requests import get
from re import sub
from os.path import exists
import gc
from gradio import Progress
from os import startfile

def Show():
    startfile("dataset")

def GetMaxPage():
    url = f"https://civitai.com/api/v1/images?limit=1"
    header = {"content-type":"application.json"}
    jsonFile = loads(get(url, headers=header).text)
    maxPage = int(jsonFile['metadata']['totalPages'])

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
    url = GetUrl(imageLimit, sort, period, nsfw)

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
        url = url + str(pageNumber)
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

        positivePrompts = list(set(positivePrompts))
        negativePrompts = list(set(negativePrompts))
        gc.collect()

    positiveFile = open(positiveFilename, "w")
    positiveFile.writelines(positivePrompts)
    positiveFile.close()

    positivePrompts.clear()

    negativeFile = open(negativeFilename, "w")
    negativeFile.writelines(negativePrompts)
    negativeFile.close()

    negativePrompts.clear()

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

def CanAdd(positivePrompt, wantedPrompts, unwantedPrompts):
    canAdd = True

    for unwanted in unwantedPrompts:
        if unwanted in positivePrompt:
            canAdd = False

    if canAdd is False:
        return canAdd

    canAdd = False

    for wanted in wantedPrompts:
        if wanted in positivePrompt:
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
