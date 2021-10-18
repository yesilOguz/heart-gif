from PIL import Image
import os
import glob
from natsort import natsorted, ns

class epsToImage:
    def __init__(self, inputDir, outputDir=None):
        self.inputDir = inputDir + '/'

        if outputDir is None:
            outputDir = inputDir + '/'
        
        self.outputDir = outputDir 

    def convert(self):
        with os.scandir(self.inputDir) as it:
            for entry in it:
                if entry.name.endswith('.eps'):
                    TARGET_BOUNDS = (1024, 1024)

                    pic = Image.open(self.inputDir+entry.name)
                    pic.load(scale=10)

                    if pic.mode in ('P', '1'):
                        pic = pic.convert("RGB")

                    ratio = min(TARGET_BOUNDS[0] / pic.size[0],
                                TARGET_BOUNDS[1] / pic.size[1])
                    new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))

                    pic = pic.resize(new_size, Image.ANTIALIAS)

                    pic.save(self.outputDir+entry.name.replace('.eps','.png'))

                    os.remove(self.inputDir+entry.name)

class ImageToGif:
    def __init__(self, inputDir, outputDir=""):
        self.input = inputDir + '/'
        
        if outputDir.strip() != "":
            outputDir + '/'

        self.output = outputDir

    def convert(self):
        img, *imgs = [Image.open(f) for f in natsorted(glob.glob(self.input+'heart*.png'), alg=ns.IGNORECASE)]        
        img.save(fp='heart.gif', format='GIF', append_images=imgs,
                 save_all=True)

epsToImage('pngs').convert()
ImageToGif('pngs').convert()
