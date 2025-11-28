import os
import uuid
import zipfile
import json
import shutil

def main():
    # データセットフォルダの初期化
    if os.path.exists("dataset_zip"):
        shutil.rmtree("dataset_zip")
    os.makedirs("dataset_zip")

    if os.path.exists("dataset"):
        shutil.rmtree("dataset")
    os.makedirs("dataset")

    # データZipファイルにUUIDを付与する
    for zipname in os.listdir("dataset_input"):
        new_zipname = str(uuid.uuid4())
        src_path = os.path.join("dataset_input", zipname)
        dst_path = os.path.join("dataset_zip", new_zipname + ".zip")
        shutil.copy2(src_path, dst_path)

    # データZipファイルを解凍する
    for zipname in os.listdir("dataset_zip"):
        with zipfile.ZipFile(os.path.join("dataset_zip", zipname)) as z:
            z.extractall("dataset")

    # データファイルをjson形式データに整理する
    jsonl_text = ""
    for foldername in os.listdir("dataset"):
        pre_text, rst_text = "", ""

        # テキストを取得
        try:
            with open(os.path.join("dataset", foldername, "pre.txt"), "r", encoding="utf-8") as f:
                pre_text = f.read()

            with open(os.path.join("dataset", foldername, "rst.txt"), "r", encoding="utf-8") as f:
                rst_text = f.read()

        except FileNotFoundError as e:
            print(e)

        # データを保存する
        data = {"messages": [
            {"role": "user", "content": pre_text},
            {"role": "assistant", "content": rst_text}
        ]}
        jsonl_row = json.dumps(data, ensure_ascii=False) + "\n"
        jsonl_text += jsonl_row

    # jsonlファイルを作成する
    with open("dataset.jsonl", "w", encoding="utf-8") as f:
        f.write(jsonl_text)

if __name__ == "__main__":
    main()