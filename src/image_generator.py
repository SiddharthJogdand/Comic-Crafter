import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import torch
from diffusers import StableDiffusionPipeline
from huggingface_hub import login
from PIL import Image
import time

# Hugging Face Authentication
HF_TOKEN = os.getenv("HF_TOKEN")  # Replace with your token

class ComicImageGenerator:
    def __init__(self):
        torch.set_num_threads(1)  # CPU optimization
        
        # Tiny CPU-compatible model
        self.model_id = "OFA-Sys/small-stable-diffusion-v0"  # 10x faster than SDXL
        
        # Memory-efficient configuration
        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float32,
            safety_checker=None,  # Disable for faster generation
            requires_safety_checker=False
        )
        
        # Warmup with tiny generation
        print("Warming up image generator...")
        self.pipe("warmup", num_inference_steps=1)
        print("Image generator ready")

    def generate_image(self, prompt: str, output_path: str = "comic_panel.png") -> Image.Image:
        """Ultra-fast CPU image generation with fail-safes"""
        try:
            # Simplify prompt for faster generation
            simplified_prompt = self._simplify_prompt(prompt)
            
            # Critical CPU optimizations
            image = self.pipe(
                simplified_prompt,
                num_inference_steps=15,          
                guidance_scale=7.5,
                width=512,                        
                height=512,
                num_images_per_prompt=1,
                max_time=30                      
            ).images[0]
            
            image.save(output_path)
            return image
            
        except Exception as e:
            print(f"Image generation failed: {str(e)}")
            return self._generate_fallback_image(output_path)
    
    def _simplify_prompt(self, prompt: str) -> str:
        """Reduces prompt complexity for CPU"""
        keywords = [
            "comic book style",
            "clear outlines",
            "vibrant colors",
            "white background"
        ]
        return f"{prompt[:100]}, {', '.join(keywords)}"  # Truncate long prompts

    def _generate_fallback_image(self, output_path: str) -> Image.Image:
        """Emergency image when generation fails"""
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (512, 512), color=(255, 253, 245))
        d = ImageDraw.Draw(img)
        d.text((50, 200), "COMIC IMAGE\nWILL APPEAR HERE", fill=(0, 0, 0))
        img.save(output_path)
        return img

if __name__ == "__main__":
    print("Initializing Comic Image Generator...")
    start_time = time.time()
    generator = ComicImageGenerator()
    print(f"Loaded in {time.time()-start_time:.1f}s")
    
    while True:
        prompt = input("\nEnter image prompt (or 'quit'): ").strip()
        if prompt.lower() == 'quit':
            break
            
        print("Generating (may take 20-40s on CPU)...")
        start_gen = time.time()
        image = generator.generate_image(prompt, "output.png")
        print(f"Generated in {time.time()-start_gen:.1f}s")
        image.show()  # Opens the image in default viewer