import streamlit as st
import ollama
from PIL import Image
import io
import re

# Page configuration
st.set_page_config(
    page_title="LaTeX OCR with Llama 3.2 Vision",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
st.title("🦙 LaTeX OCR with Llama 3.2 Vision")

# Add clear button to top right
col1, col2 = st.columns([6,1])
with col2:
    if st.button("Clear 🗑️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract LaTeX code from images using Llama 3.2 Vision!</p>', unsafe_allow_html=True)

st.markdown("---")
# Move upload controls to sidebar
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        
        if st.button("Extract LaTeX 🔍", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    response = ollama.chat(
                        model='llama3.2-vision',
                        messages=[{
                            'role': 'user',
                            'content': """Extract the mathematical equation from the provided image and output the corresponding LaTeX code. Follow these strict rules, or the output will be rejected:
                            - Output ONLY the LaTeX code for the equation itself (e.g., D_{KL}(P \Vert Q) = \sum P(x) \log \frac{P(x)}{Q(x)}).
                            - DO NOT include \documentclass, \begin{document}, \end{document}, or any preamble.
                            - DO NOT wrap the code in dollar signs ($$...$$), \[...\], or any other delimiters.
                            - DO NOT include any explanations, comments, or additional text.
                            - DO NOT simplify the equation; preserve its exact form.
                            - DO NOT explain the symbols or their meanings.
                            If you fail to follow these rules, the output will be invalid.""",
                            'images': [uploaded_file.getvalue()]
                        }]
                    )
                    st.session_state['ocr_result'] = response['message']['content']
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")

# Main content area for results
if 'ocr_result' in st.session_state:
    st.markdown("### LaTeX Code")
    st.code(st.session_state['ocr_result'], language='latex')

    st.markdown("### LaTeX Rendered")
    # Clean the LaTeX code by removing document-level commands and delimiters
    cleaned_latex = st.session_state['ocr_result']
    # Remove \documentclass, \begin{document}, \end{document}
    cleaned_latex = re.sub(r'\\documentclass\{.*?\}|\s*\\begin\{document\}|\s*\\end\{document\}', '', cleaned_latex)
    # Remove $$...$$, \[...\], and any leading/trailing whitespace
    cleaned_latex = re.sub(r'\$\$|\[|\]', '', cleaned_latex).strip()
    
    try:
        st.latex(cleaned_latex)
    except Exception as e:
        st.error(f"Failed to render LaTeX: {str(e)}. The extracted code might not be a valid math expression. See the raw code above.")

else:
    st.info("Upload an image and click 'Extract LaTeX' to see the results here.")

# Footer with updated GitHub link
st.markdown("---")
st.markdown("Made with ❤️ using Llama Vision Model | [Report an Issue](https://github.com/tahsinsoyak/llm-ocr-apps/issues) | [Source Code](https://github.com/tahsinsoyak/llm-ocr-apps)")