import streamlit as st
from bs4 import BeautifulSoup
import requests
import io

def get_text_from_webpage(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text from HTML
        text = soup.get_text()

        return text
    except requests.exceptions.RequestException as e:
        return None
    except Exception as e:
        return None

def remove_empty_lines(text):
    lines = text.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def main():
    st.title("Webpage Text Extractor")
    st.image("images/txt file like.png")
    st.write("Sem nahraje txt subor ako na obrazku , treba trocha pockat , ked mate vela url.")
    uploaded_file = st.file_uploader("Upload a text file", type=['txt'])
    if uploaded_file is not None:
        file_contents = uploaded_file.getvalue().decode("utf-8")
        urls = file_contents.split('\n')
        
        # Process each URL
        result_text = ""
        for url in urls:
            text = get_text_from_webpage(url)
            if text:
                result_text += "URL: {}\n".format(url)
                result_text += "Text:\n{}\n\n".format(text)
        
        # Remove empty lines
        result_text = remove_empty_lines(result_text)

        # Provide download link for the result file
        if result_text:
            result_text_bytes = result_text.encode("utf-8")
            st.download_button(label="Download Result File", data=io.BytesIO(result_text_bytes), file_name="plain_text.txt", mime="text/plain")

if __name__ == "__main__":
    main()
