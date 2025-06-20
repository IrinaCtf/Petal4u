import os
import requests

# base_url = "https://github.com/chinese-poetry/chinese-poetry/blob/master/%E5%85%A8%E5%94%90%E8%AF%97/"
# ✅ Use the raw content link
base_url = "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/refs/heads/master/%E5%85%A8%E5%94%90%E8%AF%97/"
save_dir = "chinese_poetry_json"
os.makedirs(save_dir, exist_ok=True)

def download_series(prefix):
    for i in range(0, 60000, 1000):  # Try poet.xxx.0.json to poet.xxx.50000.json
        filename = f"{prefix}.{i}.json"
        local_path = os.path.join(save_dir, filename)
        
        if os.path.exists(local_path):
            print(f"Skipped (already exists): {filename}")
            continue
        
        url = base_url + filename
        print(f"Attempting to download: {filename}")
        # print(url)
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded successfully: {filename}")
        else:
            print(f"File not found: {filename}. Stopping this series.")
            break

# Download Tang and Song poetry files
download_series("poet.song")
download_series("poet.tang")