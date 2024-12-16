import requests
import os

# URL of the webpage to monitor
url = "https://www.r-wellness.com/fuji5/"

# Path to the file where the old content is stored
file_path = "old_content.txt"

# Fetch the webpage content
def fetch_webpage(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Load the old content from the file
def load_old_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    return ""

# Save the new content to the file
def save_new_content(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# Main function to monitor webpage changes
def monitor_webpage(url, file_path):
    try:
        new_content = fetch_webpage(url)
        old_content = load_old_content(file_path)

        if old_content != new_content:
            print("Webpage content changed!")
            with open("change_log.txt", 'a') as log_file:
                log_file.write("Webpage content changed!\n")
            save_new_content(file_path, new_content)
        else:
            print("No changes detected.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")

# Run the monitor function
monitor_webpage(url, file_path)
