from os import getcwd
from gradio import Blocks, Button, Checkbox, Column, Dropdown, File, Files, Gallery, Label, Row, Tab, Textbox, Slider
from gradio.themes import Monochrome
from WebUI.ParseUI import Parse, ParseAll
from WebUI.CivitaiUI import GetMaxPage, Enhance, Show
from WebUI.TrainUI import Train
from WebUI.GenerateUI import Generate
from WebUI.UpscaleUI import Upscale

with Blocks(title="Prompt Tools WebUI", theme=Monochrome()) as application:
    with Tab("Parse"):
        with Row():
            fileSelect = Files(
                            label="Choose Prompt Files", 
                            type="file",
                            file_types=[".md"],
                            interactive=True
                        )
            with Column():
                translateCheckbox = Checkbox(value=False, label="Translate", info="Translate the prompts to English")
                parserProgress = Label(label="Info")
                parseAllButton = Button(value="Parse All Files In Prompts Folder")
                parseButton = Button(value="Parse")
    with Tab("Civitai"):
        with Row():
            positiveFilenameTextbox = Textbox(label="Positive Filename", value="positive", interactive=True, lines=1)
            negativeFilenameTextbox = Textbox(label="Negative Filename", value="negative", interactive=True, lines=1)
            
        imageLimitSlider = Slider(1, 200, value=1, step=1, label="Image Limit Per Page", interactive=True)
        with Row():
            pageNumberToStart = Slider(1, GetMaxPage() - 1, value=1, step=1, label="Page Number To Start", interactive=True)
            pageNumberToEnd = Slider(2, GetMaxPage(), value=2, step=1, label="Page Number To End", interactive=True)
        with Row():
            wantedPromptsTextBox = Textbox(label="Wanted Prompts",
                                              value="beautiful, female, breasts, woman, girl, masterpiece",
                                              interactive=True,
                                              lines=2)
            unwantedPromptsTextbox = Textbox(label="Unwanted Prompts",
                                                value="obese, fat, ugly, weird, creepy, loli, old woman, old, child, creature, kid",
                                                interactive=True,
                                                lines=2)
        with Row():
            sortDropdown = Dropdown(choices=["Most Reactions", "Most Comments", "Newest"],
                                    value="Most Reactions",
                                    label="Sort",
                                    interactive=True)
            periodDropdown = Dropdown(choices=["All Time", "Year", "Month", "Week", "Day"],
                                        value="All Time",
                                        label="Period",
                                        interactive=True)
            nsfwDropdown = Dropdown(choices=["None", "Soft", "Mature", "X", "All"],
                                    value="All",
                                    label="NSFW",
                                    interactive=True)
        civitaiProgress = Label(label="Info")
        with Row():
            enhanceButton = Button(value="Enhance")
            civitaiShowButton = Button(value="Show Dataset Folder")
    with Tab("Train"):
        with Row():
            modelNameTextbox = Textbox(value="gpt2", label="Model name for text generator model", interactive=True, lines=1)
            modelFolderNameTextbox = Textbox(value="myTextGenerator", label="Model folder name", interactive=True, lines=1)
        with Row():
            epochSlider = Slider(label="Epochs", minimum=1, maximum=1000, value=10, step=1, interactive=True)
            batchSlider = Slider(label="Batch Size", minimum=1, maximum=512, value=32, step=1, interactive=True)
        datasetFileSelect = File(label="Choose Dataset", file_types=["text"], interactive=True)
        with Row():
            trainInfoLabel = Label(label="Train Info")
            evaluateInfoLabel = Label(label="Evaluate Info")
        trainButton = Button(value="Train", interactive=True)
    with Tab("Generate"):
        with Row():
            generateModelFolderNameTextbox = Textbox(label="Model Folder Name", value="myTextGenerator", lines=1, interactive=True)
            generateModelNameTextbox = Textbox(label="Model Name", value="gpt2", lines=1, interactive=True)
            generateShowButton = Button(value="Show Dataset Folder")
        with Row():
            generateMinLengthSlider = Slider(10, 100, step=1, label="Min Length", info="Minimum number of generated tokens", value=10, interactive=True)
            generateMaxLengthSlider = Slider(50, 300, step=1, label="Max Length", info="Maximum number of generated tokens", value=100,interactive=True)
        with Row():
            generateDoSampleCheckbox = Checkbox(value=False, label="Do Sample", info='When checked, picks words based on their conditional probability', interactive=True)
            generateEarlyStopCheckbox = Checkbox(value=False, label="Early Stop", info='When checked, generation finishes if the EOS token is reached', interactive=True)
        with Row():
            generateRecursiveLevel = Slider(0, 20, value=0, step=1, label="Recursive Level", interactive=True)
            generateSelfRecursiveCheckbox = Checkbox(value=False, label="Self Recursive", interactive=True)
        generateSeedTextbox = Textbox(label="Seed", value="masterpiece", interactive=True)
        generateGenTextbox = Textbox(label="Generated Text", interactive=False, lines=10)
        generateGenerateButton = Button("Generate")
    with Tab("Upscale"):
        with Row():
            upscaleInputTextbox = Textbox(value=f"{getcwd()}/upscaleInput", label="Input Directory", interactive=False)
            upscaleOutputTextbox = Textbox(value=f"{getcwd()}/upscaleOutput", label="Output Directory", interactive=False)
        with Row():
            upscaleModelDropbox = Dropdown(choices=['RealESRGAN_x4plus',
                                            'RealESRNet_x4plus',
                                            'RealESRGAN_x4plus_anime_6B',
                                            'RealESRGAN_x2plus',
                                            'realesr-general-x4v3'],
                                            value='RealESRGAN_x4plus',
                                            interactive=True)
            upscaleScaleSlider = Slider(2, 4, value=2, step=1, label="Scale", interactive=True)
            upscaleFaceEnhanceCheckbox = Checkbox(value=False, label="Face Enhancement with GPFGAN", interactive=True)
            upscaleFP32Checkbox = Checkbox(value=False, label="FP32", interactive=True)
        upscaleOutputGallery = Gallery(label="Outputs")
        upscaleUpscaleButton = Button("Upscale")

    # Parse Tab Listeners
    parseButton.click(Parse, inputs=[fileSelect, translateCheckbox], outputs=[parserProgress])
    parseAllButton.click(ParseAll, inputs=[translateCheckbox], outputs=[parserProgress])

    # Civitai Tab Listeners
    enhanceButton.click(Enhance,
                        inputs=[positiveFilenameTextbox, negativeFilenameTextbox, imageLimitSlider, pageNumberToStart, pageNumberToEnd,
                                sortDropdown, periodDropdown, nsfwDropdown, wantedPromptsTextBox, unwantedPromptsTextbox], 
                        outputs=[civitaiProgress])
    civitaiShowButton.click(Show)
    
    # Train Tab Listeners
    trainButton.click(Train, 
                      [modelNameTextbox, epochSlider, batchSlider, modelFolderNameTextbox, datasetFileSelect],
                      outputs=[trainInfoLabel, evaluateInfoLabel])
    
    # Generate Tab Listeners
    generateShowButton.click(Show)
    generateGenerateButton.click(Generate, 
                                inputs=[generateModelNameTextbox, generateModelFolderNameTextbox, generateSeedTextbox, generateMinLengthSlider, generateMaxLengthSlider,
                                        generateDoSampleCheckbox, generateEarlyStopCheckbox, generateRecursiveLevel, generateSelfRecursiveCheckbox],
                                outputs=[generateGenTextbox])
    
    # Upscale Tab Listeners
    upscaleUpscaleButton.click(Upscale, 
                               inputs=[upscaleModelDropbox, upscaleScaleSlider, upscaleFaceEnhanceCheckbox, upscaleFP32Checkbox],
                               outputs=[upscaleOutputGallery])

if __name__ == '__main__':
    application.queue(concurrency_count=4).launch(server_port=8080)
