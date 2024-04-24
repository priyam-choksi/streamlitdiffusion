import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import random

# Sample prompts for the random generation feature
prompts_list = [
    "Futuristic city at night with neon lights",
    "Serene sunrise landscape with mountains and a lake",
    "Astronaut riding a horse on Mars",
    "Surreal art of a winged cat flying in a starry sky",
    "Victorian steampunk inventor in her workshop",
    "Ancient tree with a door in an enchanted forest",
    "Cybernetic owl digital artwork",
    "Medieval market scene",
    "Futuristic gadgets on a table still life",
    "Dystopian cityscape during a rainstorm"
]

def generate_image(prompt):
    """Call the Hugging Face API to generate an image based on the input prompt."""
    api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    headers = {'Authorization': 'Bearer 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'}
    
    response = requests.post(api_url, headers=headers, json={"inputs": prompt})
    try:
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except requests.RequestException as e:
        st.error(f"Failed to fetch image: {str(e)}")
        return None

def app_main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="AI-Powered Image Generator")
    st.header("AI-Powered Image Generator")
    st.subheader("Generate images from textual descriptions or use a random prompt!")

    # Handling the session state for user prompt
    if 'prompt' not in st.session_state or st.button("Generate a Random Prompt"):
        st.session_state['prompt'] = random.choice(prompts_list)

    user_prompt = st.text_input("Type your prompt below:", value=st.session_state['prompt'])
    st.session_state['prompt'] = user_prompt

    if st.button("Generate Image"):
        with st.spinner('Please wait while your image is being generated...'):
            generated_image = generate_image(user_prompt)
            if generated_image:
                st.image(generated_image, caption="Your AI-generated Image", use_column_width=True)
                st.success("Image generated successfully! 🎉")
                buffer = BytesIO()
                generated_image.save(buffer, format="PNG")
                st.download_button("Download this Image", buffer.getvalue(), file_name="ai_generated_image.png", mime="image/png")
            else:
                st.error("Unable to generate image. Please try again with a different prompt.")

if __name__ == "__main__":
    app_main()
