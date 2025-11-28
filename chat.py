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
    document_text = ""
    print("document : " + os.path.basename(file_path))
    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            document_text += f"{i+1}: {line}"

    print(document_text)

    # クエリ
    messages = [
        {
            "role": "system",
            "content": f"""
                あなたは論文を添削する先生です。
                入力したLatex文章を添削してください。
                その際に行番号と添削アドバイスを提示してください。
            """
        },
        {
            "role": "user",
            "content": document_text
        }
    ]

    # フォーマット
    format = {
        "type": "json_schema",
        "json_schema": {
            "name": "document_advice_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "advices": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "row": {
                                    "type": "integer"
                                },
                                "content": {
                                    "type": "string" 
                                },
                            },
                            "required": [
                                "row",
                                "content",
                            ],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["advices"],
                "additionalProperties": False,
            },
        },
    }

    # 添削してもらう
    if args[1] is None: return
    response = client.chat.completions.create(
        model=args[1],
        response_format=format,
        messages=messages
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main(sys.argv)
    