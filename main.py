import gradio as gr
from WebUI.ParseUI import Parse, ParseAll
from WebUI.CivitaiUI import GetMaxPage, Enhance

with gr.Blocks() as application:
    with gr.Tab("Parse"):
        with gr.Row():
            fileSelect = gr.Files(
                            label="Choose Prompt Files", 
                            type="file",
                            file_types=[".md"],
                            interactive=True
                        )
            with gr.Column():
                translateCheckbox = gr.Checkbox(value=False, label="Translate", info="Translate the prompts to English")
                parseAllButton = gr.Button(value="Parse All Files In Prompts Folder")
                parseButton = gr.Button(value="Parse")

    with gr.Tab("Civitai"):
        with gr.Row():
            positiveFilenameTextbox = gr.Textbox(label="Positive Filename", value="positive", interactive=True, lines=1)
            negativeFilenameTextbox = gr.Textbox(label="Negative Filename", value="negative", interactive=True, lines=1)
            
        imageLimitSlider = gr.Slider(1, 200, value=1, label="Image Limit Per Page", interactive=True)
        pageNumberToStart = gr.Slider(1, GetMaxPage() - 1, value=1, label="Page Number To Start", interactive=True)
        pageNumberToEnd = gr.Slider(2, GetMaxPage(), value=2, label="Page Number To End", interactive=True)
        with gr.Row():
            wantedPromptsTextBox = gr.Textbox(label="Wanted Prompts",
                                              value="beautiful, female, breasts, woman, girl, masterpiece",
                                              interactive=True,
                                              lines=2)
            unwantedPromptsTextbox = gr.Textbox(label="Unwanted Prompts",
                                                value="obese, fat, ugly, weird, creepy, loli, old woman, old, child, creature, kid",
                                                interactive=True,
                                                lines=2)
        with gr.Row():
            sortDropdown = gr.Dropdown(choices=["Most Reactions", "Most Comments", "Newest"],
                                    value="Most Reactions",
                                    label="Sort",
                                    interactive=True)
            periodDropdown = gr.Dropdown(choices=["All Time", "Year", "Month", "Week", "Day"],
                                        value="All Time",
                                        label="Period",
                                        interactive=True)
            nsfwDropdown = gr.Dropdown(choices=["None", "Soft", "Mature", "X", "All"],
                                    value="All",
                                    label="NSFW",
                                    interactive=True)
        enhanceButton = gr.Button(value="Enhance")

    # Parse Tab Listeners
    parseButton.click(Parse, inputs=[fileSelect, translateCheckbox])
    parseAllButton.click(ParseAll, inputs=[translateCheckbox])

    # Civitai Tab Listeners
    enhanceButton.click(Enhance,
                        inputs=[positiveFilenameTextbox, negativeFilenameTextbox, imageLimitSlider, pageNumberToStart, pageNumberToEnd,
                                sortDropdown, periodDropdown, nsfwDropdown, wantedPromptsTextBox, unwantedPromptsTextbox])

if __name__ == '__main__':
    application.launch()
