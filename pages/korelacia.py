import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import random
from io import BytesIO

st.title("Korelácia")
st.write("##### Sem nahrajte Excel súbor , ktorý má 2 stĺpc ako na obrázku")
st.write('slov tam moze byt kolko chcete ale staci tak 20')
st.write("Excel file , ktory sem vlozite ma byt v nasledujucom tvare: ")
st.image("images/excel_like2.png", caption="Excel-like Data Upload", width=150)

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(uploaded_file)

    dates = pd.date_range(start='2024-02-01', end='2024-02-05')
    # Separate the "Word" column and the "Value" column into lists
    words_list = df["Word"].tolist()
    values_list = df["Value"].tolist()
    values_list = values_list[:5]
    
    data = {date: [random.randint(20, 260) for _ in range(len(words_list))] for date in dates}

    # Create DataFrame with words_list as index
    df = pd.DataFrame(data, index=words_list)
    try:
        words_to_drop = ['téma', 'témy', 'https', 'top', 'www', 'url']
        df_filtered = df.drop(words_to_drop, axis=0)
    except:
        df_filtered = df.copy()

    # Plot line chart
    pocet_slov = df_filtered.shape[0]
    zaciatok = random.randrange(pocet_slov-5)
    plt.figure(figsize=(10, 6))
    for word in df_filtered.index[zaciatok:zaciatok+5]:
        plt.plot(df_filtered.columns, df_filtered.loc[word], label=word)

    plt.xlabel('Dátum')
    plt.ylabel('Výskyt')
    plt.title('Výskyt slova v čase')
    plt.xticks(df_filtered.columns, rotation=45)  # Set the specific dates as tick labels
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

    # Calculating correlations with uploaded file's values
    # Initialize list to store correlation coefficients
    correlation_coefficients = []

    # Loop through each row
    for index, row in df_filtered.iterrows():
        # Get values for the specific dates
        values = row[dates].values
        # Calculate correlation coefficient with uploaded file's values
        correlation = np.corrcoef(values_list, values)[0, 1]
        # Append correlation coefficient to the list
        correlation_coefficients.append(correlation)

    # Add correlation coefficients to dataframe
    df_filtered['corr_with_uploaded_values'] = correlation_coefficients

    # Provide download button for the Excel file
    excel_file = BytesIO()
    df_filtered.to_excel(excel_file, index=True)
    excel_file.seek(0)
    st.write("Stiahnite si Dataframe a v nom uz len vyznacite najvacsiu corelation_value v abs hodnote")
    st.download_button(label="Download Correlation DataFrame",
                       data=excel_file,
                       file_name="Correlation_DataFrame.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       key=None)
