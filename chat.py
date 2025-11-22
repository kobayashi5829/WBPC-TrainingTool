import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
from tkinter import filedialog

def main(args):
    # .envファイルの読み込み
    load_dotenv()

    # API設定
    client = OpenAI(api_key=os.getenv('API_KEY'))

    # 添削ファイルを読み込む
    file_path = filedialog.askopenfilename(
        title="添削ファイルを選択してください。",
        filetypes=[("Latexファイル", "*.tex")]    
    )

    if file_path == '': return
    print("document : " + os.path.basename(file_path))
    with open(file_path, "r", encoding="utf-8") as f:
        document_text = f.read()

    # クエリ
    messages = [
        {
            "role": "system",
            "content": "あなたは論文を添削する先生です。入力したLatex文章を添削してください。"
        },
        {
            "role": "user",
            "content": document_text
        }
    ]

    # 添削してもらう
    if args[1] is None: return
    response = client.chat.completions.create(
        model=args[1],
        messages=messages
    )

    print("answer : ")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main(sys.argv)
    