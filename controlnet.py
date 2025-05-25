import cv2
import base64
import requests

"""
    To use this example make sure you've done the following steps before executing:
    1. Ensure automatic1111 is running in api mode with the controlnet extension. 
       Use the following command in your terminal to activate:
            ./webui.sh --no-half --api
    2. Validate python environment meet package dependencies.
       If running in a local repo you'll likely need to pip install cv2, requests and PIL 
"""

class ControlnetRequest:
    def __init__(self, prompt, path):
        self.url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
        self.prompt = prompt
        self.img_path = path
        self.body = None

    def build_body(self):
        self.body = {
            "prompt": self.prompt,
            "negative_prompt": "",
            "batch_size": 1,
            "cfg_scale": 7,
            "width": 512,
            "height": 512,
            "sampler_name": "DPM++ 2M Karras",
            "steps": 15, # Sampling steps
            "cfg_scale": 7,
            "enable_hr": False, # Hires.fix
            "hr_scale": 2,
            "hr_upscaler": "Latent",
            "hr_second_pass_steps": 10, # Hires steps (0 for same steps as Sampler)
            "denoising_strength": 1,
            "batch_size": 1,
            "sd_model_name": "icbinpICantBelieveIts_seco", # Replace with SD checkpoint
            "sd_model_hash": "fa1224c923", # Replace with SD checkpoint
            "seed": -1,
            "seed_resize_from_w": -1,
            "seed_resize_from_h": -1,
            "restore_faces": False,
            "alwayson_scripts": {
                "controlnet": {
                    "args": [
                        {
                            "enabled": True,
                            "module": "invert (from white bg & black line)",
                            "model": "control_v1p_sd15_qrcode_monster_v2 [5e5778cb]", # ControlNet QR Model
                            "weight": 1.25, # Control Weight
                            "image": self.read_image(),
                            "resize_mode": "Crop and Resize",
                            "lowvram": False,
                            "processor_res": 512,
                            "guidance_start": 0.0, # Starting Control Step
                            "guidance_end": 0.75, # Ending Control Step
                            "control_mode": "Balanced",
                            "pixel_perfect": False
                        }
                    ]
                }
            }
        }
    
    def update_sd(self, update_dict):
        self.body.update(update_dict)
    
    def update_cn(self, update_dict):
        self.body["alwayson_scripts"]["controlnet"]["args"][0].update(update_dict)

    def send_request(self):
        print(self.body)
        response = requests.post(url=self.url, json=self.body)
        return response.json()

    def read_image(self):
        img = cv2.imread(self.img_path)
        retval, bytes = cv2.imencode('.png', img)
        encoded_image = base64.b64encode(bytes).decode('utf-8')
        return encoded_image