# run_multiple_agents.py

import os
import sys

# 現在のディレクトリをモジュール検索パスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from genagents.genagents import GenerativeAgent

# ----- エージェントのプロフィール作成 -----

agent_profiles = [
    {
        "first_name": "太郎",
        "last_name": "山田",
        "age": 30,
        "occupation": "ソフトウェアエンジニア",
        "interests": ["読書", "ハイキング", "プログラミング"]
    },
    {
        "first_name": "花子",
        "last_name": "佐藤",
        "age": 28,
        "occupation": "デザイナー",
        "interests": ["イラスト", "カフェ巡り", "映画鑑賞"]
    },
    {
        "first_name": "健一",
        "last_name": "高橋",
        "age": 35,
        "occupation": "教師",
        "interests": ["歴史", "旅行", "料理"]
    },
    {
        "first_name": "美咲",
        "last_name": "鈴木",
        "age": 26,
        "occupation": "看護師",
        "interests": ["音楽", "ランニング", "写真"]
    },
    {
        "first_name": "一郎",
        "last_name": "田中",
        "age": 40,
        "occupation": "営業",
        "interests": ["ゴルフ", "ワイン", "ビジネス書"]
    },
    {
        "first_name": "由美",
        "last_name": "伊藤",
        "age": 32,
        "occupation": "エディター",
        "interests": ["読書", "ヨガ", "アート"]
    },
    {
        "first_name": "直樹",
        "last_name": "渡辺",
        "age": 29,
        "occupation": "エンジニア",
        "interests": ["ゲーム", "アニメ", "プログラミング"]
    },
    {
        "first_name": "理恵",
        "last_name": "中村",
        "age": 31,
        "occupation": "マーケティング",
        "interests": ["ファッション", "SNS", "料理"]
    },
    {
        "first_name": "健二",
        "last_name": "小林",
        "age": 27,
        "occupation": "カメラマン",
        "interests": ["写真", "登山", "ドキュメンタリー"]
    },
    {
        "first_name": "美香",
        "last_name": "加藤",
        "age": 33,
        "occupation": "弁護士",
        "interests": ["映画", "ジョギング", "旅行"]
    }
]

# ----- エージェントの作成と初期化 -----

agents = []

for profile in agent_profiles:
    agent = GenerativeAgent()
    agent.update_scratch(profile)
    agents.append(agent)

# ----- メモリの追加とリフレクション -----

for agent in agents:
    # メモリの追加
    memory_text = f"{agent.scratch['first_name']}は最近、{agent.scratch['interests'][0]}に関する新しい経験をした。"
    agent.remember(memory_text, time_step=1)
    
    # リフレクションの実行
    agent.reflect(anchor=agent.scratch['interests'][0], time_step=2)

# ----- 共通の質問 -----

# カテゴリカルな質問
categorical_questions = {
    "あなたはアウトドア活動が好きですか？": ["はい", "いいえ", "時々"]
}

# 数値的な質問
numerical_questions = {
    "あなたの仕事への満足度はどのくらいですか？（1から10のスケール）": [1, 10]
}

# オープンエンドの質問
dialogue = [
    ("インタビュアー", "最近の出来事について教えてください。"),
]

# ----- 各エージェントに質問を行う -----

for idx, agent in enumerate(agents):
    print(f"\n===== エージェント {idx + 1}: {agent.scratch['first_name']} {agent.scratch['last_name']} =====")
    
    # カテゴリカルな質問の回答
    categorical_response = agent.categorical_resp(categorical_questions)
    print("カテゴリカルな質問の回答:", categorical_response["responses"])
    
    # 数値的な質問の回答
    numerical_response = agent.numerical_resp(numerical_questions, float_resp=False)
    print("数値的な質問の回答:", numerical_response["responses"])
    
    # オープンエンドの質問の回答
    open_ended_response = agent.utterance(dialogue)
    print("オープンエンドの質問の回答:", open_ended_response)