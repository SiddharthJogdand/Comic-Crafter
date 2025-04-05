import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from huggingface_hub import login
import time

# Hugging Face Authentication
HF_TOKEN = os.getenv("HF_TOKEN")

class StoryGenerator:
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.1"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        # Load model
        if torch.cuda.is_available():
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map="auto",
                torch_dtype=torch.float16,
                load_in_4bit=True
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map="auto",
                torch_dtype=torch.float32
            )
        
        print("Model loaded from cache:", os.path.exists(os.path.expanduser('~/.cache/huggingface/hub'))) 

    def generate_story(self, theme: str) -> dict:
        prompt = f"""Create a comic story with:
        1. Introduction: {theme}
        2. Storyline: Develop the narrative
        3. Climax: Exciting conclusion
        4. Moral: Lesson learned
        
        Keep each section 2-3 sentences."""
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.7,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
            top_p=0.9
        )
        
        # FINAL FIX: Properly closed all parentheses
        story_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self._parse_story(story_text)
    
    def _parse_story(self, text: str) -> dict:
        sections = {
            "introduction": "",
            "storyline": "",
            "climax": "",
            "moral": ""
        }
        current_section = None
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if "1. Introduction" in line:
                current_section = "introduction"
                sections[current_section] = line.split(":", 1)[1].strip()
            elif "2. Storyline" in line:
                current_section = "storyline"
                sections[current_section] = line.split(":", 1)[1].strip()
            elif "3. Climax" in line:
                current_section = "climax"
                sections[current_section] = line.split(":", 1)[1].strip()
            elif "4. Moral" in line:
                current_section = "moral"
                sections[current_section] = line.split(":", 1)[1].strip()
            elif current_section:
                sections[current_section] += " " + line
        
        return sections

if __name__ == "__main__":
    try:
        print("Initializing story generator...")
        generator = StoryGenerator()
        
        theme = input("Enter your story theme: ")
        start_time = time.time()
        story = generator.generate_story(theme)
        end_time = time.time()
        
        print(f"\nGenerated in {end_time - start_time:.2f} seconds")
        print("\n=== Your Comic Story ===")
        print(f"Introduction: {story['introduction']}")
        print(f"Storyline: {story['storyline']}")
        print(f"Climax: {story['climax']}")
        print(f"Moral: {story['moral']}")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print("Possible solutions:")
        print("- Verify your Hugging Face token is correct")
        print("- Check you have enough GPU memory")
        print("- Try a smaller model like 'HuggingFaceH4/zephyr-7b-beta'")
