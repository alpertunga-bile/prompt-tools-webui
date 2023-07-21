def Train(modelName, epochs, batchSize, modelFolderName, dataset):
    upperModelName = modelName.upper()

    if modelName.find("/") != -1:
        upperModelName = modelName.split("/")[1].upper()

    from happytransformer import HappyGeneration, GENTrainArgs
    from torch.cuda import is_available, empty_cache
    from os.path import exists, join

    modelPath = join("dataset", modelFolderName)

    if exists(modelPath):
        generator = HappyGeneration(upperModelName, modelName, load_path=modelPath)
    else:
        generator = HappyGeneration(upperModelName, modelName)

    args = GENTrainArgs(learning_rate=1e-3, num_train_epochs=epochs, batch_size=batchSize)
    generator.train(dataset.name, args=args)
    generator.save(modelPath)
    result = generator.eval(dataset.name)
    print("Train> DONE !!!")
    
    if is_available():
        empty_cache()

    return ["Done !!!", f"Evaluation Score : {result.loss}"]