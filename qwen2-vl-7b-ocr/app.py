#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from PIL import Image
import os

# Page config
st.set_page_config(page_title="Qwen 2.5 OCR", layout="wide")

# Sidebar for image upload
st.sidebar.title("Qwen 2.5 OCR")
uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="Uploaded Image", use_container_width=True)  # Updated parameter
    
    # Save temporarily
    temp_image_path = "temp_uploaded_image.jpg"
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    image.save(temp_image_path)

# Inference function
def inference(image_path, prompt, sys_prompt="You are a helpful assistant.", max_new_tokens=4096):
    image = Image.open(image_path)
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"file://{image_path}"}},
        ]},
    ]
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = processor(text=[text], images=[image], padding=True, return_tensors="pt")
    inputs = inputs.to(device)  # Use GPU if available

    output_ids = model.generate(**inputs, max_new_tokens=max_new_tokens)
    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, output_ids)]
    output_text = processor.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return output_text[0]

# Load model
@st.cache_resource
def load_model():
    checkpoint = "Qwen/Qwen2-VL-7B-Instruct"  # Switch to "Qwen/Qwen2-VL-2B-Instruct" if VRAM < 16GB
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
    
    # Define device map for offloading if needed
    if torch.cuda.is_available() and torch.cuda.get_device_properties(0).total_memory < 16 * 1024**3:  # Less than 16GB
        device_map = {"": "cuda:0"}  # Primary on GPU, offload excess to CPU
    else:
        device_map = "auto"  # Full GPU usage
    
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        checkpoint,
        torch_dtype=dtype,
        device_map=device_map,
    )
    processor = AutoProcessor.from_pretrained(checkpoint)
    return model, processor, device

# Initialize model
with st.spinner("Loading model..."):
    model, processor, device = load_model()
    st.write(f"Running on: {device}")
    if torch.cuda.is_available():
        st.write(f"GPU: {torch.cuda.get_device_name(0)}, VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")

# Main content
st.title("Qwen 2.5 OCR")
mode = st.radio("Select Mode", ["Full Page OCR"])

if uploaded_file is not None:
    if mode == "Full Page OCR":
        st.header("Full Page OCR")
        if st.button("Extract Text"):
            with st.spinner("Extracting text..."):
                prompt = "Extract all readable text from the image and output it as plain text."
                try:
                    response = inference(temp_image_path, prompt)
                    st.markdown("### Extracted Text:")
                    st.markdown(response)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
else:
    st.info("Please upload an image to begin.")

# Clean up
if os.path.exists("temp_uploaded_image.jpg"):
    try:
        if not uploaded_file:
            os.remove("temp_uploaded_image.jpg")
    except:
        pass