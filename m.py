import requests
import os

# URL of the webpage to monitor
url = 'https://www.r-wellness.com/fuji5/'

# Filenames for storing old content and change logs
old_content_file = 'old_content.txt'
change_log_file = 'change_log.txt'
notification_url = 'https://api.day.app/Rfaj33ucMe8nZksDJKPEib/fuji'

def fetch_webpage_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def load_old_content(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_content(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def log_change(change_log_file, old_content, new_content):
    with open(change_log_file, 'a', encoding='utf-8') as log:
        log.write('---\n')
        log.write('Old content:\n')
        log.write(old_content + '\n')
        log.write('New content:\n')
        log.write(new_content + '\n')
        log.write('---\n')

def send_notification(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")

def main():
    try:
        new_content = fetch_webpage_content(url)
    except Exception as e:
        print(f"Error fetching webpage content: {e}")
        return

    old_content = load_old_content(old_content_file)

    if old_content is None:
        print("Old content file not found. Creating a new one.")
        save_content(old_content_file, new_content)
        return

    if new_content != old_content:
        print("Content has changed!")
        log_change(change_log_file, old_content, new_content)
        save_content(old_content_file, new_content)
        send_notification(notification_url)
    else:
        print("No changes detected.")

if __name__ == '__main__':
    main()
