from flask import Flask, render_template, request, jsonify
from pypinyin import lazy_pinyin
import json
import random

app = Flask(__name__)

with open("poems.json", encoding="utf-8") as f:
    poems = json.load(f)

def get_pinyin(char):
    return lazy_pinyin(char)[0]

def find_relay_line(last_char):
    target_py = get_pinyin(last_char)
    for poem in poems:
        for line in poem["content"]:
            if get_pinyin(line[0]) == target_py:
                return line
    return None

def find_feihua_line(keyword, used_lines):
    candidates = [line for poem in poems for line in poem["content"]
                  if keyword in line and line not in used_lines]
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
        response = find_relay_line(prev[-1]) if prev else "白日依山尽"
    elif mode == "feihua":
        response = find_feihua_line(keyword, used)
        if not response:
            response = "我输了，找不到更多的诗句了。"
    else:
        response = "未知模式"

    return jsonify({"line": response})

if __name__ == "__main__":
    app.run(debug=True)
