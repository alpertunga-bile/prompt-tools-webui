from re import compile, sub

def RemoveDuplicates(lineList):
    return list(dict.fromkeys(lineList))

def Preprocess(line):
    pattern = compile(r'(,\s){2,}')

    tempLine = line.replace(u'\xa0', u' ')
    tempLine = tempLine.replace("\n", ", ")
    tempLine = tempLine.replace("  ", " ")
    tempLine = tempLine.replace("\t", " ")
    tempLine = sub(pattern, ', ', tempLine)

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

    generatedText = Preprocess(seed + result.text)

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