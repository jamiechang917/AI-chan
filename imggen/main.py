# Generate image from messages by using stable-diffusion
# https://github.com/mix1009/sdwebuiapi

import os, sys
import webuiapi

#.\webui.bat --api

class ImageGenerator:
    def __init__(self):
        # create API client
        self.api = webuiapi.WebUIApi()

    def txt2img(self, prompt, negative_prompt, output_path):
        result = self.api.txt2img(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    # seed=1003,
                    sampler_name="Euler a",
                    steps=20,
                    cfg_scale=7.0,
                    width=548,
                    height=412,
                    styles=["anime"],
                    batch_size=1,
                    n_iter=1,
                    )
        return result.image # PIL.PngImagePlugin.PngImageFile
    
if __name__ == '__main__':
    img_generator = ImageGenerator()
    img = img_generator.txt2img(
        prompt="studies, friends, Astronomy Club, stargazing, astronomy, golden hair, ponytail, blue eye, cute, JK, high school, 4k, high-resolution",
        negative_prompt="painting, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs",
        output_path=""
    )
    img.show()