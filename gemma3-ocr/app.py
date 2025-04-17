import streamlit as st
import ollama
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Gemma-3 OCR",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area without external assets
st.markdown("""
    # 🔎 Gemma-3 OCR
""", unsafe_allow_html=True)

st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Gemma-3 Vision!</p>', unsafe_allow_html=True)
st.markdown("---")

# Move upload and model selection controls to sidebar
with st.sidebar:
    st.header("Configuration")

    # Add model selection
    selected_model = st.radio(
        "Select Gemma-3 Model",
        options=["gemma3:4b", "gemma3:12b"],
        index=1  # Default to 4b
    )
    
    st.markdown("### Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        
        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    response = ollama.chat(
                        model=selected_model,
                        messages=[{
                            'role': 'user',
                            'content': (
                                "Analyze the text in the provided image. Extract all readable content and "
                                "present it in a structured Markdown format that is clear, concise, and well-organized. "
                                "Ensure proper formatting (e.g., headings, lists, or code blocks) as necessary to represent "
                                "the content effectively."
                            ),
                            'images': [uploaded_file.getvalue()]
                        }]
                    )
                    st.session_state['ocr_result'] = response.message.content
                except Exception as e:
                    st.error(f"Error processing image: {e}")

# Main content area for results
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Gemma-3 Vision Model")
