import gradio as gr
from WebUI.ParseUI import Parse, ParseAll

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

    parseButton.click(Parse, inputs=[fileSelect, translateCheckbox], show_progress=True)
    parseAllButton.click(ParseAll, inputs=[translateCheckbox], show_progress=True)

if __name__ == '__main__':
    application.launch()
