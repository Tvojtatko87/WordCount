import streamlit as st
import re
from collections import Counter
import pandas as pd
import io

def count_unique_words(text):
    # Decode bytes to string with utf-8 encoding
    text = text.decode("utf-8")
    # Use regular expression to find words (ignoring non-alphabetic characters)
    words = re.findall(r'\b\w+\b', text, flags=re.UNICODE)
    # Convert words to lowercase
    words = [word.lower() for word in words]
    # Count occurrences of each word
    word_counts = Counter(words)
    return word_counts

def main():
    st.title("Word Counter")
    st.write("Upload a text file below:")

    uploaded_file = st.file_uploader("Choose a file", type="txt")

    if uploaded_file is not None:
        text = uploaded_file.getvalue()
        
        # Add Streamlit widgets for user input
        min_word_length = st.slider("Minimum Word Length", min_value=1, max_value=15, value=3)
        min_word_count = st.slider("Minimum Word Count", min_value=1, max_value=500, value=100)

        word_counts = count_unique_words(text)
        
        # Filter words based on user input
        filtered_words = [(word, count, len(word)) for word, count in word_counts.items() if count > min_word_count and len(word) > min_word_length]
        
        # Sort the filtered words based on their counts in descending order
        filtered_words.sort(key=lambda x: x[1], reverse=True)
        
        # Convert filtered words to a DataFrame
        df = pd.DataFrame(filtered_words, columns=["Word", "Count", "Length"])
        
        # Calculate additional statistics
        longest_word = df.loc[df['Length'].idxmax()]
        max_count = df['Count'].max()
        min_count = df['Count'].min()
        average_count = df['Count'].mean()
        std_dev = df['Count'].std()
        median_value = round(df['Count'].median(), 2)
        range_value = round(df['Count'].max() - df['Count'].min(), 2)
        variance_value = round(df['Count'].var(), 2)
        iqr_value = round(df['Count'].quantile(0.75) - df['Count'].quantile(0.25), 2)
        
        # Create a dictionary for statistics
        statistics_dict = {
            'LongestWord': longest_word['Word'],
            'LongestWordLength': longest_word['Length'],
            'MaxCount': max_count,
            'MinCount': min_count,
            'AverageCount': average_count,
            'StdDev': std_dev,
            'Median': median_value,
            'Range': range_value,
            'Variance': variance_value,
            'IQR': iqr_value
        }

        # Append statistics to the DataFrame
        statistics_df = pd.DataFrame(statistics_dict, index=[0])

        # Concatenate the statistics DataFrame with the filtered words DataFrame with a blank column between them
        blank_column = pd.DataFrame({'' : [None] * len(df)})
        final_df = pd.concat([df, blank_column, statistics_df], axis=1)
        
        # Save DataFrame to an Excel file in memory
        excel_file = io.BytesIO()
        final_df.to_excel(excel_file, index=False)
        excel_file.seek(0)
        
        # Provide a download button for the Excel file
        st.download_button(label="Download Filtered Words",
                           data=excel_file.getvalue(),
                           file_name="filtered_words_with_statistics.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           key=None)
        
        st.write("Click the button above to download the filtered words with statistics as an Excel file.")

if __name__ == "__main__":
    main()
