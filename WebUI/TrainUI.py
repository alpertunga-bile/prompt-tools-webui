def Train(modelName, epochs, batchSize, modelFolderName, dataset):
    upperModelName = modelName.upper()

    if modelName.find("/") != -1:
        upperModelName = modelName.split("/")[1].upper()

    from happytransformer import HappyGeneration, GENTrainArgs
    from os.path import exists, join

    modelPath = join("dataset", modelFolderName)

    if exists(modelPath):
        generator = HappyGeneration(upperModelName, modelName, load_path=modelPath)
    else:
        generator = HappyGeneration(upperModelName, modelName)

    args = GENTrainArgs(num_train_epochs=epochs, batch_size=batchSize)
    generator.train(dataset.name, args=args)
    generator.save(modelPath)
    result = generator.eval(dataset.name)
    print("Train> DONE !!!")
    return ["Done !!!", f"Evaluation Score : {result.loss}"]