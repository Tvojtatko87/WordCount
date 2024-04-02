import streamlit as st
import random
from openpyxl import Workbook
import io

# Function to generate random weather data for February
def generate_weather_data_february(date):
    max_temp = random.randint(5, 12)
    min_temp = random.randint(0, max_temp)  # Ensure min_temp is less than or equal to max_temp
    weather_conditions = ["Jasno", "Oblačno", "Polooblacno", "Dážď", "Zamračené", "Malá oblačnosť"]
    weather = random.choice(weather_conditions)
    rain_chance = random.randint(0, 70)
    rain_mm = random.randint(0, 15)
    wind_speed = random.randint(5, 30)
    return date, max_temp, min_temp, weather, rain_chance, rain_mm, wind_speed

# Function to generate random weather data for March
def generate_weather_data_march(date):
    max_temp = random.randint(14, 20)
    min_temp = random.randint(8, max_temp - 3)
    weather_conditions = ["Jasno", "Oblačno", "Polooblacno", "Dážď", "Zamračené", "Malá oblačnosť"]
    weather = random.choice(weather_conditions)
    rain_chance = random.randint(0, 70)
    rain_mm = random.randint(0, 15)
    wind_speed = random.randint(5, 30)
    return date, max_temp, min_temp, weather, rain_chance, rain_mm, wind_speed

def generate_and_download_weather_forecast():
    # Generate weather forecast data
    weather_data = []
    date = "1.2.2024"
    for i in range(29):
        
        date, max_temp, min_temp, weather, rain_chance, rain_mm, wind_speed = generate_weather_data_february(date)
        weather_data.append([date, max_temp, min_temp, weather, rain_chance, rain_mm, wind_speed])
        date_list = date.split('.')
        day = int(date_list[0])
        month = int(date_list[1])
        year = int(date_list[2])

        if day == 28 and month == 2:  # Handle leap year
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                day = 29
            else:
                day = 1
                month = 3
        elif day == 29 and month == 2:  # Reset to March 1 after February 29
            day = 1
            month = 3
        elif day == 31 and month in [1, 3]:
            day = 1
            month += 1
        elif day == 30 and month in [4, 6, 9, 11]:
            day = 1
            month += 1
        elif day == 31 and month == 12:
            day = 1
            month = 1
            year += 1
        else:
            day += 1
        date = f"{day:02d}.{month:02d}.{year}"
        
    for i in range(21):
        
        date, max_temp, min_temp, weather, rain_chance, rain_mm, wind_speed = generate_weather_data_march(date)
        weather_data.append([date, max_temp, min_temp, weather, rain_chance, rain_mm, wind_speed])
        date_list = date.split('.')
        day = int(date_list[0])
        month = int(date_list[1])
        year = int(date_list[2])

        if day == 28 and month == 2:  # Handle leap year
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                day = 29
            else:
                day = 1
                month = 3
        elif day == 29 and month == 2:  # Reset to March 1 after February 29
            day = 1
            month = 3
        elif day == 31 and month in [1, 3]:
            day = 1
            month += 1
        elif day == 30 and month in [4, 6, 9, 11]:
            day = 1
            month += 1
        elif day == 31 and month == 12:
            day = 1
            month = 1
            year += 1
        else:
            day += 1
        date = f"{day:02d}.{month:02d}.{year}"

    # Write to Excel file in memory
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.append(["Date", "Max. Temp (°C)", "Min. Temp (°C)", "Weather", "Rain (%)", "Rain (mm)", "Wind Speed (km/h)"])
    for row in weather_data:
        ws.append(row)
    wb.save(output)
    output.seek(0)

    # Provide download link for the result file
    st.download_button(label="Download Weather Forecast", data=output, file_name="weather_forecast.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def main():
    st.title("Weather Forecast Generator")
    st.write("Click the button below to generate and download the weather forecast Excel file.")
    if st.button("Generate Weather Forecast"):
        generate_and_download_weather_forecast()

if __name__ == "__main__":
    main()
