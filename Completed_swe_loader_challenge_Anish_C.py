import os
import csv
import re
directory_path = 'C:\\Users\\hichh\\swe_cardinal-challenge-fall-2024\\data'

def load_csv_files(directory_path):
    """
    Load all CSV files from the specified directory, extract and process the tick data.
    Exceptuon handling too
    """
    all_data = []
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    csv_files.sort()  # Sort files based on their naming convention

    for file in csv_files:
        file_path = os.path.join(directory_path, file)
        try:
            with open(file_path, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # Skip header row if it exists

                for row in csv_reader:
                    try:
                        timestamp = row[0]
                        price = float(row[1].strip())  # Convert price to float
                        size = int(row[2].strip())  # Convert size to integer
                        all_data.append((timestamp, price, size))

                    except (ValueError, IndexError):
                        # Skip the row if there's an error (either conversion issue or missing field)
                        continue

        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    return all_data

all_ticks_data = load_csv_files(directory_path)
def clean_data(data):
    """
    Clean the data by handling missing values, correcting malformed entries,
    removing outliers, and filtering duplicate rows.
    """
    cleaned_data = []
    seen_entries = set()  # To track duplicates
    
    for row in data:
        timestamp, price, size = row
        
        # 1. Handle Missing Values
        if not timestamp or price is None or size is None:
            continue  # Skip rows with missing data
        
        # 2. Handle Malformed Data
        try:
            price = float(price)
            size = int(size)
        except ValueError:
            continue  # Skip rows with malformed data
        
        # 3. Remove Outliers (Example: Price or size values out of reasonable range)
        if price < 0 or size < 0:  # Assuming negative values are erroneous
            continue
        
        # 4. Filter Duplicates
        if (timestamp, price, size) in seen_entries:
            continue
        seen_entries.add((timestamp, price, size))
        
        cleaned_data.append((timestamp, price, size))
    print ("dataloader ran")
    return cleaned_data

# Example of cleaning the loaded data
cleaned_ticks_data = clean_data(all_ticks_data)
from datetime import datetime, timedelta

def parse_time_interval(interval_str):
    """Convert string time intervals like '4s', '15m', '2h' to a timedelta object."""
    time_units = {
        'd': 1440,  
        'h': 60,       
        'm': 1,        
        's': 1 / 60    
    }
    
    # Regex to capture the number and the unit (e.g., 1h, 30m, etc.)
    time_regex = r'(\d+)([dhms])'
    
    total_minutes = 0
    
    # Find all matches in the input string
    matches = re.findall(time_regex, interval_str)
    
    for value, unit in matches:
        # Convert the captured value to integer and multiply by the corresponding time unit
        total_minutes += int(value) * time_units[unit]
    
    return timedelta (minutes=total_minutes)




def generate_ohlcv(data, interval_str, start_time, end_time):
    """
    Generate OHLCV data from tick data for a given time interval.
    Each interval will contain Open, High, Low, Close prices and total Volume.
    """
    interval = parse_time_interval(interval_str)
    current_time = start_time
    ohlcv_data = []
    
    while current_time < end_time:
        # Collect data for the current time interval
        interval_data = [row for row in data if current_time <= datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f') < current_time + interval]
        
        if interval_data:
            open_price = interval_data[0][1]
            high_price = max(row[1] for row in interval_data)
            low_price = min(row[1] for row in interval_data)
            close_price = interval_data[-1][1]
            volume = sum(row[2] for row in interval_data)
            
            ohlcv_data.append((current_time, open_price, high_price, low_price, close_price, volume))
        
        current_time += interval
        print("completed cycle")
    
    return ohlcv_data

# Example usage for generating OHLCV data
start_time = datetime(2024, 9, 16, 9, 30)
end_time = datetime(2024, 9, 16, 16, 0)

interval = input("Select interval")

ohlcv_data = generate_ohlcv(cleaned_ticks_data, interval, start_time, end_time)
print (ohlcv_data)


with open('OHLCV_output'+interval+".csv", mode='w', newline='') as file:
    writer=csv.writer(file)
    writer.writerows(ohlcv_data)
    print("complete")
