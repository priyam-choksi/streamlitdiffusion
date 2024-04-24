import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import random

# List of sample prompts for generating random prompts
sample_prompts = [
    "A futuristic cityscape at night, illuminated by neon lights",
    "A serene landscape with a mountain in the background and a lake in the foreground during sunrise",
    "An astronaut riding a horse on Mars",
    "A surreal painting of a cat with wings flying through a starry sky",
    "A portrait of a Victorian steampunk inventor in her workshop",
    "An ancient tree with a door leading into it, set in an enchanted forest",
    "A digital artwork of a cybernetic owl",
    "A scene from a busy medieval market",
    "A still life of futuristic gadgets on a table",
    "A dystopian city during a rainstorm"
]

def image_generation(prompt):
    """Generate an image from a prompt using the Hugging Face Stable Diffusion API."""
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    headers = {'Authorization': 'Bearer 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'}
    try:
        response = requests.post(url, headers=headers, json={"inputs": prompt})
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return Image.open(BytesIO(response.content))
    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        st.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        st.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        st.error(f"Error: {err}")
    return None

def main():
    st.set_page_config(page_title="G-AI-IG")
    st.title("AI Image Generator")
    st.write("Enter a description of the image you want to generate, or generate a random prompt!")

    if 'prompt' not in st.session_state or st.button("Generate Random Prompt"):
        st.session_state['prompt'] = random.choice(sample_prompts)

    prompt = st.text_input("Enter the prompt to generate an image:", value=st.session_state['prompt'])
    st.session_state['prompt'] = prompt

    if st.button("Generate Image"):
        with st.spinner('Generating image... Please wait.'):
            output_image = image_generation(prompt)
            if output_image:
                st.image(output_image, caption="Generated Image", use_column_width=True)
                st.success("Image generated successfully!")
                buf = BytesIO()
                output_image.save(buf, format="PNG")
                st.download_button("Download Image", buf.getvalue(), file_name="generated_image.png", mime="image/png")
            else:
                st.error("Failed to generate image. Please check the prompt or try again later.")

if __name__ == "__main__":
    main()
