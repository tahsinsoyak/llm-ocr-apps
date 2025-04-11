import streamlit as st
import ollama
from PIL import Image

# Sayfa yapılandırması
st.set_page_config(
    page_title="Llama OCR",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ana başlık ve açıklama
st.title("🦙 Llama OCR")
st.markdown(
    '<p style="margin-top: -20px;">Extract structured text from images using Llama 3.2 Vision!</p>',
    unsafe_allow_html=True
)
st.markdown("---")

# Sağ üst köşede "Clear" butonu
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("Clear 🗑️"):
        st.session_state.pop('ocr_result', None)
        st.experimental_rerun()

# Yan menüde resim yükleme
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Yüklenen resmi göster
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        
        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    messages = [{
                        'role': 'user',
                        'content': (
                            "Analyze the text in the provided image. Extract all readable content and present it in a "
                            "structured Markdown format that is clear, concise, and well-organized. Ensure proper formatting "
                            "(e.g., headings, lists, or code blocks) as necessary to represent the content effectively."
                        ),
                        'images': [uploaded_file.getvalue()]
                    }]
                    response = ollama.chat(model='llama3.2-vision', messages=messages)
                    st.session_state['ocr_result'] = response.message.content
                except Exception as e:
                    st.error(f"Error processing image: {e}")

# Ana içerik alanında sonuçları göster
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using Llama Vision Model2 | "
    "[Tahsin Soyak GitHub](https://github.com/tahsinsoyak)"
)
