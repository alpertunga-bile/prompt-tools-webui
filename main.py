from gradio import Blocks, Column, Tab, Row, Label,  Files, File, Checkbox, Button, Textbox, Slider, Dropdown
from gradio.themes import Monochrome
from WebUI.ParseUI import Parse, ParseAll
from WebUI.CivitaiUI import GetMaxPage, Enhance
from WebUI.TrainUI import Train

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
                parseAllButton = Button(value="Parse All Files In Prompts Folder")
                parseButton = Button(value="Parse")
                parserProgress = Label(label="Info")
    with Tab("Civitai"):
        with Row():
            positiveFilenameTextbox = Textbox(label="Positive Filename", value="positive", interactive=True, lines=1)
            negativeFilenameTextbox = Textbox(label="Negative Filename", value="negative", interactive=True, lines=1)
            
        imageLimitSlider = Slider(1, 200, value=1, label="Image Limit Per Page", interactive=True)
        pageNumberToStart = Slider(1, GetMaxPage() - 1, value=1, label="Page Number To Start", interactive=True)
        pageNumberToEnd = Slider(2, GetMaxPage(), value=2, label="Page Number To End", interactive=True)
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
        enhanceButton = Button(value="Enhance")
        civitaiProgress = Label(label="Info")
    with Tab("Train"):
        modelNameTextbox = Textbox(value="gpt2", label="Model name for text generator model", interactive=True, lines=1)
        epochSlider = Slider(label="Epochs", minimum=1, maximum=1000, value=10, interactive=True)
        batchSlider = Slider(label="Batch Size", minimum=1, maximum=512, value=32, interactive=True)
        modelFolderNameTextbox = Textbox(value="myTextGenerator", label="Model folder name", interactive=True, lines=1)
        datasetFileSelect = File(label="Choose Dataset", file_types=["text"], interactive=True)
        trainButton = Button(value="Train", interactive=True)

    # Parse Tab Listeners
    parseButton.click(Parse, inputs=[fileSelect, translateCheckbox], outputs=[parserProgress])
    parseAllButton.click(ParseAll, inputs=[translateCheckbox], outputs=[parserProgress])

    # Civitai Tab Listeners
    enhanceButton.click(Enhance,
                        inputs=[positiveFilenameTextbox, negativeFilenameTextbox, imageLimitSlider, pageNumberToStart, pageNumberToEnd,
                                sortDropdown, periodDropdown, nsfwDropdown, wantedPromptsTextBox, unwantedPromptsTextbox], 
                        outputs=[civitaiProgress])
    
    # Train Tab Listeners
    trainButton.click(Train, 
                      [modelNameTextbox, epochSlider, batchSlider, modelFolderNameTextbox, datasetFileSelect])

if __name__ == '__main__':
    application.queue(concurrency_count=4).launch()
