import streamlit as st
import pandas as pd
import json
import paramiko
import os
import re
from io import StringIO

from dotenv import load_dotenv, dotenv_values
load_dotenv()

# Load remote connection details from environment variables
REMOTE_HOST = os.getenv('REMOTE_HOST')
REMOTE_PORT = int(os.getenv('REMOTE_PORT', 22))
USERNAME = os.getenv('REMOTE_USER')
PRIVATE_KEY = os.getenv('PRIVATE_KEY') 
remote_path = os.getenv('REMOTE_PATH')

# Function to clean up private key and ensure it has proper formatting
def clean_private_key(private_key_str):
    # Ensure the private key is formatted with newline characters correctly
    clean_key = private_key_str.strip().replace("\\n", "\n")
    return clean_key

# Function to connect to the remote server using public key authentication
def connect_to_server():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Try using an SSH agent first, if no agent then use the key from environment variable
    try:
        # Connect using an SSH agent if available
        client.connect(REMOTE_HOST, port=REMOTE_PORT, username=USERNAME)
    except paramiko.SSHException:
        # If agent fails, load private key from environment variable
        if PRIVATE_KEY:
            clean_key_str = clean_private_key(PRIVATE_KEY)  # Clean the private key string
            key_stream = StringIO(clean_key_str)  # Treat cleaned private key string as a file-like object

            # Try to load the key explicitly as RSA or Ed25519 with an empty password
            try:
                # Try RSA key first
                private_key = paramiko.RSAKey.from_private_key(key_stream, password="")
            except paramiko.PasswordRequiredException:
                raise ValueError("The provided private key appears to be encrypted but no passphrase was given.")
            except paramiko.SSHException:
                key_stream.seek(0)  # Reset the stream to the start in case of failure
                try:
                    # Try Ed25519 key as a fallback
                    private_key = paramiko.Ed25519Key.from_private_key(key_stream, password="")
                except paramiko.SSHException as e:
                    raise ValueError(f"Failed to parse private key: {e}")

            client.connect(REMOTE_HOST, port=REMOTE_PORT, username=USERNAME, pkey=private_key)
        else:
            raise ValueError("No private key found in the environment variable.")
    
    sftp = client.open_sftp()
    return client, sftp

# Function to convert the data into a DataFrame
def data_to_dataframe(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df['price'] = df['price'] / 100  # Divide price by 100
    df = df.sort_values('date')
    return df

# Function to find the 5 cheapest combinations
def find_cheapest_combinations(df1, df2):
    combinations = []
    for index1, row1 in df1.iterrows():
        for index2, row2 in df2.iterrows():
            if row1['date'] < row2['date']:
                total_price = row1['price'] + row2['price']
                combinations.append((row1['date'], row1['price'], row2['date'], row2['price'], total_price))
    combinations.sort(key=lambda x: x[4])
    return combinations[:5]

# Function to load the latest JSON file from the selected folder on the remote server
def load_latest_data(sftp, folder, suffix):
    files = sftp.listdir(folder)
    files = [f for f in files if f.endswith(f'_{suffix}.json')]
    files.sort(reverse=True)
    latest_file = files[0] if files else None
    if latest_file:
        with sftp.open(f"{folder}/{latest_file}", 'r') as f:
            data = json.load(f)
        return data, latest_file
    else:
        return None, None

# Function to find the 5 cheapest items
def find_cheapest_items(df):
    return df.nsmallest(5, 'price')

# Function to find folder names matching the pattern "XXX_XXX" on the remote server
def find_folder_names(sftp, remote_path):
    folders = [f for f in sftp.listdir(remote_path) if sftp.stat(f"{remote_path}/{f}").st_mode & 0o040000 and re.match(r'^\w{3}_\w{3}$', f)]
    return folders

# Main function to run the Streamlit app
def main():
    st.title('Price Data Bar Charts')

    # Connect to the remote server
    client, sftp = connect_to_server()
    
    # Automatically load folder options from the remote server
    folder_options = find_folder_names(sftp, remote_path)
    folder = st.sidebar.selectbox('Select folder name:', [''] + folder_options)

    if folder:
        full_folder_path = f"{remote_path}/{folder}"
        
        # Load the latest roundtrip data from the selected folder
        data, filename = load_latest_data(sftp, full_folder_path, 'roundtrip')
        if data:
            st.header(f'Section 1 - {filename}')
            df1 = data_to_dataframe(data['data'][0])
            st.bar_chart(df1.set_index('date')['price'])

            st.header(f'Section 2 - {filename}')
            df2 = data_to_dataframe(data['data'][1])
            st.bar_chart(df2.set_index('date')['price'])

            st.header('5 Cheapest Combinations')
            cheapest_combinations = find_cheapest_combinations(df1, df2)
            for combo in cheapest_combinations:
                st.write(f"First Date: {combo[0].strftime('%Y-%m-%d')}, First Price: ${combo[1]:.2f}, Second Date: {combo[2].strftime('%Y-%m-%d')}, Second Price: ${combo[3]:.2f}, Total Price: ${combo[4]:.2f}")

        else:
            st.error('No roundtrip data found in the selected folder.')

        # Load the latest oneway data from the selected folder
        data, filename = load_latest_data(sftp, full_folder_path, 'oneway')
        if data:
            st.header(f'Oneway Data - {filename}')
            df_oneway = data_to_dataframe(data['data'][0])
            st.bar_chart(df_oneway.set_index('date')['price'])

            st.header('5 Cheapest Items (Oneway)')
            cheapest_items = find_cheapest_items(df_oneway)
            for _, row in cheapest_items.iterrows():
                st.write(f"Date: {row['date'].strftime('%Y-%m-%d')}, Price: ${row['price']:.2f}")

        else:
            st.error('No oneway data found in the selected folder.')

        # Load the latest reversed oneway data from the selected folder
        reversed_suffix = folder.split('_')[1] + '_' + folder.split('_')[0] + '_oneway'
        data, filename = load_latest_data(sftp, full_folder_path, reversed_suffix)
        if data:
            st.header(f'Oneway Data (Reversed) - {filename}')
            df_reversed_oneway = data_to_dataframe(data['data'][0])
            st.bar_chart(df_reversed_oneway.set_index('date')['price'])

            st.header('5 Cheapest Items (Oneway Reversed)')
            cheapest_items_reversed = find_cheapest_items(df_reversed_oneway)
            for _, row in cheapest_items_reversed.iterrows():
                st.write(f"Date: {row['date'].strftime('%Y-%m-%d')}, Price: ${row['price']:.2f}")

        else:
            st.error('No reversed oneway data found in the selected folder.')

    else:
        all_cheapest_combinations = []
        all_cheapest_oneway = []
        all_cheapest_reversed = []

        # Loop through each folder to get the summary
        for folder_name in folder_options:
            full_folder_path = f"{remote_path}/{folder_name}"
            # Load the latest roundtrip data
            data, _ = load_latest_data(sftp, full_folder_path, 'roundtrip')
            if data:
                df1 = data_to_dataframe(data['data'][0])
                df2 = data_to_dataframe(data['data'][1])
                cheapest_combinations = find_cheapest_combinations(df1, df2)
                if cheapest_combinations:
                    all_cheapest_combinations.append((folder_name, cheapest_combinations[0]))

            # Load the latest oneway data
            data, _ = load_latest_data(sftp, full_folder_path, 'oneway')
            if data:
                df_oneway = data_to_dataframe(data['data'][0])
                cheapest_items = find_cheapest_items(df_oneway)
                if not cheapest_items.empty:
                    all_cheapest_oneway.append((folder_name, cheapest_items.iloc[0]))

            # Load the latest reversed oneway data
            reversed_suffix = folder_name.split('_')[1] + '_' + folder_name.split('_')[0] + '_oneway'
            data, _ = load_latest_data(sftp, full_folder_path, reversed_suffix)
            if data:
                df_reversed_oneway = data_to_dataframe(data['data'][0])
                cheapest_items_reversed = find_cheapest_items(df_reversed_oneway)
                if not cheapest_items_reversed.empty:
                    all_cheapest_reversed.append((folder_name, cheapest_items_reversed.iloc[0]))

        # Sort and display the summaries
        all_cheapest_combinations.sort(key=lambda x: x[1][4])
        all_cheapest_oneway.sort(key=lambda x: x[1].price)
        all_cheapest_reversed.sort(key=lambda x: x[1].price)

        st.header('Cheapest Combination from Each Folder')
        for folder_name, combo in all_cheapest_combinations:
            st.write(f"Folder: {folder_name}, First Date: {combo[0].strftime('%Y-%m-%d')}, First Price: ${combo[1]:.2f}, Second Date: {combo[2].strftime('%Y-%m-%d')}, Second Price: ${combo[3]:.2f}, Total Price: ${combo[4]:.2f}")

        st.header('Cheapest Oneway Item from Each Folder')
        for folder_name, item in all_cheapest_oneway:
            st.write(f"Folder: {folder_name}, Date: {item.date.strftime('%Y-%m-%d')}, Price: ${item.price:.2f}")

        st.header('Cheapest Oneway Reversed Item from Each Folder')
        for folder_name, item in all_cheapest_reversed:
            st.write(f"Folder: {folder_name}, Date: {item.date.strftime('%Y-%m-%d')}, Price: ${item.price:.2f}")

    # Close the connection to the server
    sftp.close()
    client.close()

if __name__ == '__main__':
    main()
