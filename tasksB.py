# Phase B: LLM-based Automation Agent for DataWorks Solutions

# B1 & B2: Security Checks
import os

def B12(filepath):
    if filepath.startswith('/data'):
        # raise PermissionError("Access outside /data is not allowed.")
        # print("Access outside /data is not allowed.")
        return True
    else:
        return False

# B3: Fetch Data from an API
def B3(url, save_path):
    if not B12(save_path):
        return None
    import requests
    response = requests.get(url)
    with open(save_path, 'w') as file:
        file.write(response.text)

import subprocess

def B4(repo_url, commit_message="Auto commit by agent"):
    repo_path = "/data/repo"
    
    # Ensure the /data directory is used
    if not repo_url.startswith("https://github.com"):
        raise ValueError("Invalid repository URL")

    # Clone the repository
    subprocess.run(["git", "clone", repo_url, repo_path], check=True)

    # Create a dummy commit
    subprocess.run(["git", "-C", repo_path, "config", "user.name", "Agent"], check=True)
    subprocess.run(["git", "-C", repo_path, "config", "user.email", "agent@example.com"], check=True)
    subprocess.run(["git", "-C", repo_path, "add", "."], check=True)
    subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "-C", repo_path, "push"], check=True)

    return {"message": "Repository cloned and committed successfully."}
.run(["git", "-C", "/data/repo", "commit", "-m", commit_message])

# B5: Run SQL Query
def B5(db_path, query, output_filename):
    if not B12(db_path):
        return None
    import sqlite3, duckdb
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    with open(output_filename, 'w') as file:
        file.write(str(result))
    return result

# B6: Web Scraping
def B6(url, output_filename):
    import requests
    result = requests.get(url).text
    with open(output_filename, 'w') as file:
        file.write(str(result))

# B7: Image Processing
def B7(image_path, output_path, resize=None):
    from PIL import Image
    if not B12(image_path):
        return None
    if not B12(output_path):
        return None
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)

import openai

def B8(audio_path):
    # Ensure the path is within /data
    if not B12(audio_path):
        return None

    with open(audio_path, "rb") as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file)

    # Save the transcription
    output_path = audio_path.replace(".mp3", ".txt")
    with open(output_path, "w") as f:
        f.write(response["text"])

    return {"message": "Audio transcription completed.", "output_file": output_path}

# B9: Markdown to HTML Conversion
def B9(md_path, output_path):
    import markdown
    if not B12(md_path):
        return None
    if not B12(output_path):
        return None
    with open(md_path, 'r') as file:
        html = markdown.markdown(file.read())
    with open(output_path, 'w') as file:
        file.write(html)

import pandas as pd

def B10(csv_path, filter_column, filter_value, output_path):
    # Ensure the file is within /data
    if not B12(csv_path):
        return None

    df = pd.read_csv(csv_path)

    if filter_column not in df.columns:
        raise ValueError(f"Column '{filter_column}' not found in CSV file.")

    filtered_df = df[df[filter_column] == filter_value]
    filtered_df.to_csv(output_path, index=False)

    return {"message": f"Filtered CSV saved to {output_path}"}
