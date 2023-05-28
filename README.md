# prompt-tools-webui

- Going to add [prompt-markdown-parser](https://github.com/alpertunga-bile/prompt-markdown-parser) and [AIUpscaleGUI](https://github.com/alpertunga-bile/AIUpscaleGUI) repository functions.

## Updates
- [x] Two repositories functionalities are added.

## TODO
- [ ] Add tab for generate images with [Automatic1111 API](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API#api-guide-by-kilvoctu).
- [x] Adding guides to README file
- [ ] Adding video guides for tabs

## Tabs
### Parser Tab
- Choose prompt files to parse.
- Choose if you want to translate your prompts to English.
- Click **Parse** button to parse.
- If your files are under the **prompts** folder, you can parse all of them by just clicking **Parse All Files In Prompts Folder** button.
- Wait for **Done !!!** text to appear in **Info** label. Files are going to save in **prompts** folder.
### Civitai Tab
- [x] Files can be already exists in **dataset** folder. In this condition, new datasets are added to files. Otherwise files are created under **dataset** folder.
- Choose filename for saved datasets. Datasets are going to be saved in **dataset** folder.
- Choose image per page.
- Choose page number to start and end.
- Write wanted and unwanted prompts seperated with comma(","). The example is given.
- Choose sort, period and NSFW options with dropdowns.
- Click **Enhance** button. Wait for the progress bar in **Info** label to finish.
- You can check the datasets with **Show Dataset Folder** button. It opens the **dataset** folder in the project.
### Train Tab
- Write model name of the text generator. You can choose the models from this [site](https://huggingface.co/models?pipeline_tag=text-generation). You have to right full name e.g. bigscience/bloom-560m.
- Write a model folder name to be saved in **dataset** folder.
- Choose epochs and batch size variables.
- Choose the dataset you want to use for training.
- Click **Train** button. Check the progress from the terminal. When finished in **Train Info** label will show **Done !!!** text and in **Evaluate Info** label will show loss value of the trained model.
### Generate Tab
- Give the full model name and model folder name. You can check the model folder name with **Show Dataset Folder** button. It will open the **dataset** folder so you can get the model folder name easily.
- Select minimum and maximum lengths for the generated tokens for the text.
- Choose do sample and early stop variables. Do sample picks words based on their conditional probability. If early stop is selected, generation finishes if the EOS token is reached.
- Choose recursive level and check if you want the self recursive feature.
- Enter your seed and click **Generate** button.
- Wait until the text shows up in the **Generated Text** textbox.
#### How Recursive Works?
- Let's say we give ```a, ``` as seed and recursive level is 1. I am going to use the same outputs for this example to understand the functionality more accurately.
- With self recursive, let's say generator's output is ```b```. So next seed is going to be ```b``` and generator's output is ```c```. Final output is ```a, c```. It can be used for generating random outputs.
- Without self recursive, let's say generator's output is ```b```. So next seed is going to be ```a, b``` and generator's output is ```a, b, c```. Final output is ```a, b, c```. It can be used for more accurate prompts.
### Upscale Tab
- Put your images under **upscaleInput** folder in the project. The output is going to be under **upscaleOutput** folder.
- Select Real-ESRGAN model to upscale.
- Choose scale factor and face enhancement feature.
- Choose FP32 feature if the outputs are black.
- Click **Upscale** button. Wait until the outputs are appeared in the **Outputs** label.
