def Train(modelName, epochs, batchSize, modelFolderName, dataset):
    upperModelName = modelName.upper()

    if modelName.find("/") != -1:
        upperModelName = modelName.split("/")[1].upper()

    from happytransformer import HappyGeneration, GENTrainArgs

    generator = HappyGeneration(upperModelName, modelName)
    args = GENTrainArgs(num_train_epochs=epochs, batch_size=batchSize)
    generator.train(dataset.name, args=args)
    generator.save(f"dataset/{modelFolderName}")
    print("DONE !!!")