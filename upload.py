import sys
import os
from dotenv import load_dotenv
import json
from openai import OpenAI
from tkinter import filedialog
import uuid
import shutil

def main():
    # .envを読み込む
    load_dotenv()

    # API設定
    client = OpenAI(api_key=os.getenv('API_KEY'))

    # データセットの作成
    if not os.path.exists("dataset") or os.path.isdir("dataset"):
        dataset_path = os.path.abspath("dataset")
    else:
        dataset_path = os.makedirs("dataset")

    folder_id = str(uuid.uuid4())
    folder_path = os.makedirs(os.path.join(dataset_path, folder_id))

    print(dataset_path)
    # 添削前ファイルの読み込み
    file_path = filedialog.askopenfilename(
        title="添削前ファイルを選択してください。",
        filetypes=[("Latexファイル", "*.tex")]    
    )

    with open(file_path, "r", encoding="utf-8") as f:
        pre_text = f.read()

    source_path = file_path
    dst_path = os.path.join(folder_path, os.path.basename(source_path))
    print(type(dst_path))
    shutil.copy(source_path, dst_path)

    # 添削後ファイルの読み込み
    file_path = filedialog.askopenfilename(
        title="添削前ファイルを選択してください。",
        filetypes=[("Latexファイル", "*.tex")]    
    )

    with open(file_path, "r", encoding="utf-8") as f:
        post_text = f.read()

    source_path = file_path
    dst_path = os.path.join(folder_path, os.path.basename(source_path))
    shutil.copy(source_path, dst_path)

    # ファイル差分を出力する
    messages = [
        {
            "role": "system",
            "content": "二つの文章の差分を取り、先生のアドバイス文章をそのまま出力してください。"
        },
        {
            "role": "user",
            "content": pre_text
        },
        {
            "role": "user",
            "content": post_text
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    # データを保存する
    data = {"messages": [{"role": "user", "content": pre_text}, {"role": "assistant", "content": response.choices[0].message.content}]}
    
    with open(os.path.join(folder_path, "out.jsonl"), "a", encoding="utf-8") as f:
        line = json.dumps(data, ensure_ascii=False)
        f.write(line)

if __name__ == "__main__":
    main()