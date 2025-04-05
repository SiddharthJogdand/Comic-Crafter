from story_generator import StoryGenerator
from image_generator import ComicImageGenerator
from PIL import Image, ImageDraw, ImageFont
import os
from typing import List, Dict
import time

class ComicCrafter:
    def __init__(self):
        self.story_gen = StoryGenerator()
        self.image_gen = ComicImageGenerator()
        self.font = ImageFont.truetype("arial.ttf", 20)  # Custom font (fallback to Arial)

    def create_comic(self, theme: str, output_dir: str = "comic_output") -> str:
        """Generates a comic from a theme and returns the final image path."""
        try:
            print(f"\n🚀 Generating comic: '{theme}'")
            start_time = time.time()

            # Step 1: Generate structured story
            story = self.story_gen.generate_story(theme)
            print("✅ Story generated!")

            # Step 2: Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Step 3: Generate and annotate panels
            panels = self._generate_panels(story, output_dir)

            # Step 4: Combine panels into a final comic strip
            final_path = self._combine_panels(panels, output_dir)
            
            print(f"\n🎉 Comic generated in {time.time() - start_time:.2f}s! Saved to: {final_path}")
            return final_path

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            raise

    def _generate_panels(self, story: Dict[str, str], output_dir: str) -> List[Image.Image]:
        """Generates and annotates images for each story section."""
        panels = []
        for section, text in story.items():
            panel_path = os.path.join(output_dir, f"panel_{section}.png")
            
            # Generate image from text
            image = self.image_gen.generate_image(
                f"Comic panel, clear outlines, vibrant colors: {text}",
                output_path=panel_path
            )
            
            # Add text overlay with a semi-transparent background for readability
            self._annotate_panel(image, text)
            panels.append(image)
            print(f"✅ Panel '{section}' saved to {panel_path}")
        
        return panels

    def _annotate_panel(self, image: Image.Image, text: str):
        """Adds styled text overlay to a panel."""
        draw = ImageDraw.Draw(image)
        
        # Add semi-transparent background for text
        text_bg = Image.new("RGBA", image.size, (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_bg)
        text_draw.rectangle([(10, 10), (image.width - 10, 100)], fill=(0, 0, 0, 128))
        
        # Composite the background and original image
        image.paste(Image.alpha_composite(image.convert("RGBA"), text_bg), (0, 0))
        
        # Draw the text
        draw.text((20, 20), text, font=self.font, fill="white")

    def _combine_panels(self, panels: List[Image.Image], output_dir: str) -> str:
        """Combines panels vertically into a single image."""
        if not panels:
            raise ValueError("No panels to combine!")
            
        # Calculate total height and max width
        total_height = sum(panel.height for panel in panels)
        max_width = max(panel.width for panel in panels)
        
        # Create a blank canvas
        combined = Image.new("RGB", (max_width, total_height), color=(255, 255, 255))
        y_offset = 0
        
        # Paste each panel onto the canvas
        for panel in panels:
            combined.paste(panel, (0, y_offset))
            y_offset += panel.height
        
        # Save the final comic
        final_path = os.path.join(output_dir, "final_comic.png")
        combined.save(final_path)
        return final_path

if __name__ == "__main__":
    try:
        crafter = ComicCrafter()
        theme = input("Enter your comic theme (e.g., 'Robot detective in Paris'): ").strip()
        if not theme:
            theme = "Superhero squirrel saves the day"  # Default theme
        
        final_comic_path = crafter.create_comic(theme)
        print(f"\n🔥 Open your comic here: file://{os.path.abspath(final_comic_path)}")
    
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")