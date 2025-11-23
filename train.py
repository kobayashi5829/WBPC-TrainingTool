import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

def main():
    # .envファイルを読み込む
    load_dotenv()

    # API設定
    client = OpenAI(api_key=os.getenv('API_KEY'))

    # データセットをアップロードする
    training_file = client.files.create(
        file=open("dataset.jsonl", "rb"),
        purpose="fine-tune",
        expires_after=2592000 # 1か月後に削除
    )

    # ファインチューニングジョブを作成
    job = client.fine_tuning.jobs.create(
        training_file=training_file.id,
        model="gpt-4.1-mini-2025-04-14",
        hyperparameters={
            "n_epochs": 3, # 学習回数（3が推奨）
        }
    )

    # ジョブの待機
    while True:
        job = client.fine_tuning.jobs.retrieve(job.id)
        print(f"{datetime.now()} {job.status}")
        if job.status == "succeeded":
            print(f"{datetime.now()} {job.status}")
            break
        elif job.status == "failed":
            print(f"{datetime.now()} {job.status}")
            break
        time.sleep(60)

    print(f"model name : {job.fine_tuned_model}")

if __name__ == "__main__":
    main()