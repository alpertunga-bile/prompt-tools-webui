import gradio as gr
from WebUI.ParseUI import Parse

with gr.Blocks() as application:
    with gr.Tab("Parse"):
        with gr.Row():
            fileSelect = gr.Files(
                            label="Prompt Files or Directory", 
                            type="file",
                            interactive=True
                        )
            with gr.Column():
                translateCheckbox = gr.Checkbox(value=False, label="Translate", info="Translate the prompts to English")
                parseButton = gr.Button(value="Parse")

    parseButton.click(Parse, inputs=[fileSelect, translateCheckbox], show_progress=True)

if __name__ == '__main__':
    application.launch()