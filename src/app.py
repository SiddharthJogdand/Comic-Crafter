import streamlit as st
from comic_assembler import ComicCrafter
import os
from PIL import Image

# --- Streamlit App Setup ---
st.set_page_config(
    page_title="Comic Crafter",
    page_icon="🎨",
    layout="wide"
)

# --- Sidebar Controls ---
with st.sidebar:
    st.title("⚙️ Settings")
    theme = st.text_input(
        "Comic Theme",
        value="Superhero squirrel saves the day",
        help="Example: 'Robot detective in Paris'"
    )
    generate_btn = st.button("Generate Comic", type="primary")

    st.markdown("---")
    st.markdown("### How It Works")
    st.markdown("""
    1. Enter your comic theme
    2. Click the generate button
    3. View/download your custom comic!
    """)

# --- Main App ---
st.title("🎨 Comic Crafter")
st.caption("Turn your ideas into custom comics with AI!")

if generate_btn:
    with st.spinner("Generating your comic... This may take 2-3 minutes"):
        # Initialize and generate comic
        crafter = ComicCrafter()
        output_path = crafter.create_comic(theme)
        
        # Display results
        st.success("Comic generated successfully!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Final Comic Strip")
            final_comic = Image.open(output_path)
            st.image(final_comic, use_column_width=True)
            
            # Download button
            with open(output_path, "rb") as file:
                st.download_button(
                    label="Download Comic",
                    data=file,
                    file_name="my_comic.png",
                    mime="image/png"
                )
        
        with col2:
            st.subheader("Individual Panels")
            panel_dir = os.path.dirname(output_path)
            panels = sorted([
                os.path.join(panel_dir, f) 
                for f in os.listdir(panel_dir) 
                if f.startswith("panel_") and f.endswith(".png")
            ])
            
            for panel_path in panels:
                panel_name = os.path.basename(panel_path).replace("panel_", "").replace(".png", "")
                st.caption(f"Panel: {panel_name.replace('_', ' ').title()}")
                st.image(Image.open(panel_path))
else:
    # Show placeholder before generation
    st.info("Enter a theme and click 'Generate Comic' to begin")
    st.image("https://via.placeholder.com/800x400?text=Your+Comic+Will+Appear+Here", 
             use_column_width=True)

# --- Footer ---
st.markdown("---")
st.caption("Powered by Mistral-7B and Stable Diffusion | Made with Streamlit")