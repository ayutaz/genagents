# run_agent_example.py

import os
import sys

# 現在のディレクトリをモジュール検索パスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from genagents.genagents import GenerativeAgent

# ----- エージェントの作成と初期化 -----

# エージェントを初期化
agent = GenerativeAgent()

# 個人情報を更新
agent.update_scratch({
    "first_name": "太郎",
    "last_name": "山田",
    "age": 30,
    "occupation": "ソフトウェアエンジニア",
    "interests": ["読書", "ハイキング", "プログラミング"]
})

# ----- メモリの追加 -----

# エージェントにメモリを追加
agent.remember("昨日、友人と一緒に山でハイキングを楽しんだ。", time_step=1)
agent.remember("新しいプログラミング言語を学び始めた。", time_step=2)

# ----- リフレクションの実行 -----

# アウトドア活動に関するリフレクション
agent.reflect(anchor="アウトドア活動", time_step=3)

# プログラミングに関するリフレクション
agent.reflect(anchor="プログラミング", time_step=4)

# ----- エージェントとの対話 -----

# カテゴリカルな質問をする
categorical_questions = {
    "あなたはアウトドア活動が好きですか？": ["はい", "いいえ", "時々"]
}
categorical_response = agent.categorical_resp(categorical_questions)
print("カテゴリカルな質問の回答:", categorical_response["responses"])

# 数値的な質問をする
numerical_questions = {
    "プログラミングはどのくらい好きですか？（1から10のスケール）": [1, 10]
}
numerical_response = agent.numerical_resp(numerical_questions, float_resp=False)
print("数値的な質問の回答:", numerical_response["responses"])

# オープンエンドの質問をする
dialogue = [
    ("インタビュアー", "あなたの好きな趣味について教えてください。"),
]
open_ended_response = agent.utterance(dialogue)
print("オープンエンドの質問の回答:", open_ended_response)

# ----- エージェントの保存 -----

# エージェントを保存するディレクトリを指定
save_directory = "saved_agents/agent_taro"

# ディレクトリが存在しない場合は作成
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# エージェントを保存
agent.save(save_directory)
print(f"エージェントを '{save_directory}' に保存しました。")

# ----- エージェントの読み込み -----

# 保存したエージェントを読み込む
loaded_agent = GenerativeAgent(agent_folder=save_directory)
print("保存したエージェントを読み込みました。")

# 読み込んだエージェントとの対話
dialogue = [
    ("インタビュアー", "最近学んだことについて教えてください。"),
]
loaded_response = loaded_agent.utterance(dialogue)
print("読み込んだエージェントからの回答:", loaded_response)