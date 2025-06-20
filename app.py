from flask import Flask, render_template, request, jsonify
from pypinyin import lazy_pinyin
import json
import random
import os

app = Flask(__name__)

# Load all poem files from the data directory
poems = []
data_dir = "chinese_poetry_json"
for file in os.listdir(data_dir):
    if file.endswith(".json"):
        path = os.path.join(data_dir, file)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                for entry in data:
                    entry["content"] = entry.get("paragraphs", [])
                    poems.append(entry)
        except json.JSONDecodeError:
            print(f"Skipped invalid JSON file: {file}")
        except Exception as e:
            print(f"Error loading {file}: {e}")

def get_pinyin(char):
    return lazy_pinyin(char)[0] if char else ""

def find_relay_line(last_char, used_lines):
    target_py = get_pinyin(last_char)
    candidates = [
        line for poem in poems for line in poem["content"]
        if line and get_pinyin(line[0]) == target_py and line not in used_lines
    ]
    return random.choice(candidates) if candidates else None

def find_feihua_line(keyword, used_lines):
    candidates = [
        line for poem in poems for line in poem["content"]
        if keyword in line and line not in used_lines
    ]
    return random.choice(candidates) if candidates else None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_line", methods=["POST"])
def get_line():
    data = request.json
    mode = data["mode"]
    prev = data["prev"]
    keyword = data["keyword"]
    used = data.get("used", [])

    if mode == "relay":
        if prev:
            response = find_relay_line(prev[-1], used)
            if not response:
                response = "我输了，找不到更多的接龙诗句了。"
        else:
            response = random.choice([line for poem in poems for line in poem["content"]])
    elif mode == "feihua":
        response = find_feihua_line(keyword, used)
        if not response:
            response = "我输了，找不到更多的诗句了。"
    else:
        response = "未知模式"

    return jsonify({"line": response})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
