# Comic Crafter 🎨

AI-powered comic generator using:
- Transformers (for story generation)
- Stable Diffusion (for images)
- Streamlit (for GUI)

## Features
- Generate 4-panel comics from any theme
- Customizable art styles
- Local CPU/GPU support

## Installation
```bash
git clone https://github.com/your-username/Comic-Crafter.git
cd Comic-Crafter
pip install -r requirements.txt
```

## Usage

Run the comic generator via:

```bash
# Command Line Interface
python src/comic_assembler.py --prompt "Your comic theme here" --style "watercolor"

# Web Interface (requires Streamlit)
streamlit run src/app.py
```
