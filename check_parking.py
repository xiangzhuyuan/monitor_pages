import json
import requests
from pathlib import Path

STATE_FILE = "state.json"

def load_last_state():
    if Path(STATE_FILE).exists():
        return json.loads(Path(STATE_FILE).read_text())
    return {}

def save_state(state):
    Path(STATE_FILE).write_text(json.dumps(state, ensure_ascii=False))

def notify():
    requests.get("https://api.day.app/Rfaj33ucMe8nZksDJKPEib/成田停车/p5空了")

def main():
    # 这里替换成你真实抓 P5 的逻辑
    p5_status = get_p5_status()  # "空車" or "満車"

    last_state = load_last_state()
    last_p5 = last_state.get("p5")

    if last_p5 == p5_status:
        print("No change")
        return

    print(f"Changed: {last_p5} -> {p5_status}")

    if p5_status == "空車":
        notify()

    save_state({"p5": p5_status})

if __name__ == "__main__":
    main()
