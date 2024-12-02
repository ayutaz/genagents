import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from genagents.genagents import GenerativeAgent

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

# カテゴリカルな質問をする
questions = {
    "あなたはアウトドア活動が好きですか？": ["はい", "いいえ", "時々"]
}

response = agent.categorical_resp(questions)
print(response["responses"])

# 数値的な質問をする
questions = {
    "プログラミングはどのくらい好きですか？（1から10のスケール）": [1, 10]
}

response = agent.numerical_resp(questions, float_resp=False)
print(response["responses"])

# オープンエンドの質問をする
dialogue = [
    ("インタビュアー", "あなたの好きな趣味について教えてください。"),
]

response = agent.utterance(dialogue)
print(response)