import requests
from bs4 import BeautifulSoup
import re
import sys

URL = "https://www.narita-airport.jp/ja/access/parking/"
BARK_KEY = "Rfaj33ucMe8nZksDJKPEib"


def get_p5_status():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    divs = soup.find_all("div", class_=lambda x: x and x.startswith("styles_p"))

    for div in divs:
        class_name = " ".join(div.get("class", []))
        match = re.search(r'styles_(p\d+)-module', class_name)
        if match and match.group(1).lower() == "p5":
            bubble = div.find("div", class_=lambda x: x and "bubble" in x)
            if bubble:
                return bubble.get_text(strip=True)

    return None


def notify():
    url = f"https://api.day.app/{BARK_KEY}/成田停车/P5空车了"
    requests.get(url, timeout=5)


def main():
    status = get_p5_status()
    print("Current P5:", status)

    if status == "空車":
        notify()
        print("Notification sent.")
    else:
        print("No notification.")


if __name__ == "__main__":
    main()
