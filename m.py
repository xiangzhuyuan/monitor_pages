import requests
import os
from datetime import datetime

# URL of the webpage to monitor
url = ['https://www.r-wellness.com/fuji5/',
       'https://www.r-wellness.com/nobeyama/', 
       'https://www.r-wellness.com/takayama/', 
       'https://www.r-wellness.com/tango/', 
       'https://www.r-wellness.com/nara/']

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

def log_change(log_file, url, old_content, new_content):
    with open(log_file, 'a', encoding='utf-8') as log:  # ✅ 改成 append
        log.write(f'\n--- {datetime.now()} ---\n')
        log.write(f'Change detected at {url}\n')
        log.write('Old (first 300 chars):\n')
        log.write(old_content[:300] + '\n')
        log.write('New (first 300 chars):\n')
        log.write(new_content[:300] + '\n')

def send_notification(url, site_name):
    try:
        # 在通知标题里带上 site_name
        r = requests.get(f"{url}/{site_name}")
        if r.status_code == 200:
            print(f"Notification sent for {site_name}.")
        else:
            print(f"Failed to send notification for {site_name}.")
    except Exception as e:
        print(f"Notification error: {e}")

def main(u):
    # ✅ 文件名根据网址区分
    safe_name = u.replace("https://", "").replace("http://", "").replace("/", "_")
    old_content_file = f'old_{safe_name}.txt'
    change_log_file = f'change_{safe_name}.log'

    try:
        new_content = fetch_webpage_content(u)
    except Exception as e:
        print(f"Error fetching webpage content: {e}")
        return

    old_content = load_old_content(old_content_file)

    if old_content is None:
        print(f"First time fetching {u}, creating old content file.")
        save_content(old_content_file, new_content)
        return

    if new_content != old_content:
        print(f"🔔 Content changed at {u}")
        log_change(change_log_file, u, old_content, new_content)
        save_content(old_content_file, new_content)
        send_notification(notification_url, safe_name)
    else:
        print(f"No change detected for {u}")

if __name__ == '__main__':
    for u in urls:
        main(u)
