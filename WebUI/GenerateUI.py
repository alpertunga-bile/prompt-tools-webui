def RemoveDuplicates(line):
    uniqueList = []
    [uniqueList.append(x) for x in line if x.replace(" ", "") not in uniqueList]
    return uniqueList

def Preprocess(line):
    tempLine = line.replace(u'\xa0', u' ')
    tempLine = tempLine.replace("\n", ", ")
    tempLine = tempLine.replace("  ", " ")
    tempLine = tempLine.replace("\t", " ")
    tempLine = tempLine.replace(",,", ",")
    tempLine = tempLine.replace(",, ", ", ")

    tempLine = ', '.join(RemoveDuplicates(tempLine.split(",")))

    return tempLine

def Generate(modelName, modelFoldername, seed, minLength, maxLength, doSample, earlyStop, recursiveLevel, selfRecursive):
    recursiveLevel = int(recursiveLevel)
    
    from happytransformer import HappyGeneration, GENSettings

    generatorArgs = GENSettings(
        min_length=minLength,
        max_length=maxLength,
        do_sample=doSample,
        early_stopping=earlyStop
    )

    upperModelName = modelName.upper()

    if modelName.find("/") != -1:
        upperModelName = modelName.split("/")[1].upper()

    modelPath = f"dataset/{modelFoldername}"

    generator = HappyGeneration(upperModelName, modelName, load_path=modelPath)
    result = generator.generate_text(seed, generatorArgs)

    generatedText = Preprocess(result.text)

    if selfRecursive:
        for _ in range(0, recursiveLevel):
            result = generator.generate_text(generatedText, generatorArgs)
            generatedText = Preprocess(result.text)
        generatedText = Preprocess(seed + generatedText)
    else:
        for _ in range(0, recursiveLevel):
            result = generator.generate_text(generatedText, generatorArgs)
            generatedText += result.text
            generatedText = Preprocess(generatedText)

    return generatedText