from PIL import Image
from glob import glob
from VenvManager import VenvManager

def Upscale(modelName, scale, faceEnhance, fp32):
    venvManager = VenvManager("venv")

    start = f'Real-ESRGAN\\inference_realesrgan.py -n {modelName} -i '
    end = f"--ext png -s {scale}"
    
    if faceEnhance:
        end += " --face_enhance"

    if fp32:
        end += " --fp32"
    
    command = f"{start} upscaleInput -o upscaleOutput {end}"

    venvManager.RunFile(command)

    images = []

    imagePaths = glob('upscaleOutput/*.png')

    for path in imagePaths:
        images.append(Image.open(path))

    print("DONE !!!")

    return images