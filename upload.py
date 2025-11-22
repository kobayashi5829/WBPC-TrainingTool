import os
from dotenv import load_dotenv
import json
from openai import OpenAI
from tkinter import filedialog

def main():
    # .envを読み込む
    load_dotenv()

    # API設定
    client = OpenAI(api_key=os.getenv('API_KEY'))

    # 添削前ファイルの読み込み
    file_path = filedialog.askopenfilename(
        title="添削前ファイルを選択してください。",
        filetypes=[("Latexファイル", "*.tex")]    
    )

    if file_path == '': return
    print("pre document : " + os.path.basename(file_path))
    with open(file_path, "r", encoding="utf-8") as f:
        pre_text = f.read()

    # 添削後ファイルの読み込み
    file_path = filedialog.askopenfilename(
        title="添削後ファイルを選択してください。",
        filetypes=[("Latexファイル", "*.tex")]    
    )

    if file_path == '': return
    print("post document : " + os.path.basename(file_path))
    with open(file_path, "r", encoding="utf-8") as f:
        post_text = f.read()

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

    with open("dataset.jsonl", "a", encoding="utf-8") as f:
        line = json.dumps(data, ensure_ascii=False)
        f.write(line + "\n")

if __name__ == "__main__":
    main()