import requests
import os
from datetime import datetime
import difflib
import re

from bs4 import BeautifulSoup

# URL of the webpage to monitor
urls = ['https://www.r-wellness.com/fuji5/',
       'https://www.r-wellness.com/nobeyama/', 
       'https://www.r-wellness.com/takayama/', 
       'https://www.r-wellness.com/tango/', 
       'https://www.r-wellness.com/nara/']

notification_url = 'https://api.day.app/Rfaj33ucMe8nZksDJKPEib/fuji'

def write_to_file_with_timestamp(file_path, content, mode='a', encoding='utf-8'):
    """
    将内容写入文件，并在内容前加上时间戳。
    
    参数：
    - file_path: 文件路径
    - content: 要写入的内容（字符串）
    - mode: 文件模式，默认 'a' 追加，'w' 覆盖
    - encoding: 文件编码
    """
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    content_with_timestamp = f"{timestamp} {content}\n"
    
    try:
        with open(file_path, mode, encoding=encoding) as f:
            f.write(content_with_timestamp)
        print(f"✅ 内容已写入 {file_path}")
    except Exception as e:
        print(f"❌ 写入文件失败: {e}")

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

def extract_visible_text(html):
    """
    Extract visible text from HTML using BeautifulSoup, remove scripts/styles,
    normalize whitespace and collapse multiple blank lines.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # remove script/style elements
    for s in soup(['script', 'style', 'noscript', 'iframe']):
        s.decompose()

    text = soup.get_text(separator='\n', strip=True)

    # Normalize whitespace: trim leading/trailing spaces on lines, collapse multiple blank lines
    lines = [line.strip() for line in text.splitlines()]
    normalized = '\n'.join(lines)
    normalized = re.sub(r'\n\s*\n+', '\n\n', normalized).strip()
    return normalized

def log_change(log_file, url, old_content, new_content):
    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_")
    fromfile = f'old_{safe_name}'
    tofile = f'new_{safe_name}'

    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)

    diff_lines = list(difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=fromfile,
        tofile=tofile,
        n=5,
        lineterm=''
    ))

    with open(log_file, 'a', encoding='utf-8') as log:
        log.write(f'\n--- {datetime.now()} ---\n')
        log.write(f'Change detected at {url}\n')
        if diff_lines:
            log.write('Unified diff (context lines = %d):\n' % 5)
            for line in diff_lines:
                log.write(line + '\n')

def send_notification(url, site_name):
    try:
        # notification URL expects /site_name appended
        r = requests.get(f"{url}/{site_name}")
        if r.status_code == 200:
            print(f"Notification sent for {site_name}.")
        else:
            print(f"Failed to send notification for {site_name}. Status: {r.status_code}")
    except Exception as e:
        print(f"Notification error: {e}")

def main(u):
    safe_name = u.replace("https://", "").replace("http://", "").replace("/", "_")
    old_content_file = f'old_{safe_name}.txt'
    change_log_file = f'change_{safe_name}.log'

    try:
        new_content_raw = fetch_webpage_content(u)
    except Exception as e:
        print(f"Error fetching webpage content: {e}")
        return
    
    new_compare = extract_visible_text(new_content_raw)
    
    old_content_raw = load_old_content(old_content_file)

    if old_content_raw is None:
        print(f"First time fetching {u}, creating old content file (text only).")
        save_content(old_content_file, new_compare)
        return

    old_compare = extract_visible_text(old_content_raw)
       
    if new_compare != old_compare:
        print(f"🔔 Content changed at {u} (mode=text-only)")
        log_change(change_log_file, u, old_compare, new_compare)
        save_content(old_content_file, new_compare)
        send_notification(notification_url, safe_name)
    else:
        print(f"No change detected for {u} (mode=text-only)")
if __name__ == '__main__':
    for u in urls:
        main(u)
