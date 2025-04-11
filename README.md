# LLM OCR APPS

LLM OCR APPS is a collection of web applications designed to perform Optical Character Recognition (OCR) using various large language models (LLMs). Each application is tailored to extract specific types of content from images, such as structured text or LaTeX code, leveraging advanced vision models.

## Project Structure

- **gemma3-ocr**: Extracts structured text from images using the Gemma-3 Vision model.
- **llama3.2-latex-ocr**: Extracts LaTeX code from images containing mathematical equations using the Llama 3.2 Vision model.
- **llama3.2-ocr**: General OCR application using the Llama 3.2 Vision model.
- **qwen2-vl-7b-ocr**: OCR application using the Qwen2 VL 7B model.
- **venv**: Virtual environment for managing project dependencies.

## Prerequisites

- Python 3.10 or higher
- Streamlit
- Pillow
- Ollama for Llama3.2 and Gemma3
- transformers For Qwen2

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tahsinsoyak/llm-ocr-apps.git
   cd llm-ocr-apps
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  
   # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running Applications

Each application can be run independently using Streamlit. Navigate to the respective directory and execute the following command:

```bash
streamlit run app.py
```

Replace `app.py` with the appropriate script name if different.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Acknowledgments

- Built with ❤️ using the Llama Vision Model
- Powered by Streamlit and Ollama

For any questions or support, please contact [tahsinsoyakk@gmail.com].
