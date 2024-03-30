import pandas as pd
from openpyxl import Workbook, load_workbook
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

st.title("Sledovaná veličina")
st.write("##### Sem nahrajte Excel súbor , ktorý má 2 stĺpc ako na obrázku")
st.write("Excel file , ktory sem vlozite ma byt v nasledujucom tvare: ")
st.image("images/excel_like.png", caption="Excel-like Data Upload", width=300)

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(uploaded_file)
    
    # Convert 'Date' column to datetime if it exists
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    
    # Computing statistics
    statistics = {
        "Maximum": round(df['Value'].max(), 2),
        "Minimum": round(df['Value'].min(), 2),
        "Average": round(df['Value'].mean(), 2),
        "Standard Deviation": round(df['Value'].std(), 2),
        "Median": round(df['Value'].median(), 2),
        "Range": round(df['Value'].max() - df['Value'].min(), 2),
        "Variance": round(df['Value'].var(), 2),
        "Interquartile Range": round(df['Value'].quantile(0.75) - df['Value'].quantile(0.25), 2)
    }

    y_label_name = st.text_input("Zadajte názov cryptomeny", "Value")

    # Plot line graph with dates on x-axis
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Value'], marker='o')
    plt.xlabel('Date')
    plt.ylabel(y_label_name)
    plt.title('Line Graph of ' + y_label_name + ' over Time')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Display the plot
    st.pyplot(plt)

    # Provide download button for the Excel file
    excel_data = BytesIO()
    with pd.ExcelWriter(excel_data, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)  # Write DataFrame to Excel
        
        # Create a new worksheet and set it as active
        writer.book.create_sheet(title="Statistics")
        ws = writer.book["Statistics"]
        writer.book.active = ws
        
        # Write statistics to Excel
        ws.append(["Statistics:"])
        for key, value in statistics.items():
            ws.append([key, value])

    excel_data.seek(0)
    st.download_button(label="Download Crypto stats",
                       data=excel_data.getvalue(),
                       file_name="crypto_stats.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       key=None)

    st.write("Click the button above to download the Crypto stats as an Excel file.")
else:
    pass
