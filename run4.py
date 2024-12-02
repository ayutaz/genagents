# simulation.py

import os
import sys
import random
import logging

# 現在のディレクトリをモジュール検索パスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from genagents.genagents import GenerativeAgent

# ----- ログの設定 -----

# ログを保存するディレクトリとファイル名
log_dir = "simulation_logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, "simulation.log")

# ログの設定
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(message)s",  # メッセージのみをログに記録
)

# ----- 1. エージェントの初期化 -----

agent_profiles = [
    {
        "first_name": "たかし",
        "last_name": "すずき",
        "age": 25,
        "occupation": "農民",
        "interests": ["農業", "漁業", "物語"]
    },
    {
        "first_name": "あいこ",
        "last_name": "たなか",
        "age": 23,
        "occupation": "織物師",
        "interests": ["織物", "薬草", "音楽"]
    },
    # 他の8人のプロフィールを追加
]

# プログラムで追加のプロフィールを生成
names = [
    ("ひろし", "やまだ"),
    ("ゆみ", "さとう"),
    ("けんた", "こばやし"),
    ("さくら", "わたなべ"),
    ("だいち", "いとう"),
    ("ゆうこ", "なかむら"),
    ("さとし", "かとう"),
    ("めぐみ", "よしだ")
]

occupations = ["狩人", "陶芸家", "漁師", "大工", "薬草師", "語り部", "交易商", "庭師"]
interests = [
    ["狩猟", "追跡", "登山"],
    ["陶芸", "芸術", "デザイン"],
    ["漁業", "船作り", "水泳"],
    ["木工", "建築", "絵画"],
    ["薬草学", "園芸", "料理"],
    ["物語", "音楽", "踊り"],
    ["交易", "探索", "交渉"],
    ["農業", "植栽", "自然"]
]

for i in range(8):
    profile = {
        "first_name": names[i][0],
        "last_name": names[i][1],
        "age": random.randint(20, 40),
        "occupation": occupations[i],
        "interests": interests[i]
    }
    agent_profiles.append(profile)

# エージェントの初期化
agents = []

for profile in agent_profiles:
    agent = GenerativeAgent()
    agent.update_scratch(profile)
    agents.append(agent)

# エージェントを保存するディレクトリを作成
agent_save_dir = "simulation_agents"
if not os.path.exists(agent_save_dir):
    os.makedirs(agent_save_dir)

# ----- 2. 年次シミュレーション -----

total_years = 100
current_year = 3000  # 西暦3000年からスタート
time_step = 0  # タイムステップ

for year in range(total_years):
    current_year += 1
    time_step += 1
    logging.info(f"\n===== 年 {current_year} =====")

    # --- 集落イベントの動的生成 ---
    # 天候の要素を含めたイベント生成
    weather = random.choice(["晴天", "雨天", "嵐", "乾燥", "雪", "霧"])
    event_type = random.choices(
        ["収穫", "災害", "交流", "祭り", "技術発展"],
        weights=[0.4, 0.2, 0.1, 0.2, 0.1],
        k=1
    )[0]

    if event_type == "収穫":
        event = f"{weather}の影響で作物の生育が良好だった。"
    elif event_type == "災害":
        disaster = random.choice(["洪水", "地震", "火災", "疫病"])
        event = f"{weather}の中、{disaster}が発生し、被害が出た。"
    elif event_type == "交流":
        event = "他の集落との交流が行われ、新しい情報がもたらされた。"
    elif event_type == "祭り":
        event = f"{weather}の中、伝統的な祭りが盛大に開催された。"
    elif event_type == "技術発展":
        discovery = random.choice(["新しい農具", "保存技術", "建築技術"])
        event = f"{discovery}が開発され、生活が改善された。"
    else:
        event = "特筆すべきことは起こらなかった。"

    logging.info(f"集落イベント: {event}")

    # エージェントがイベントを記憶
    for agent in agents:
        agent.remember(f"{current_year}年に、{event}", time_step)

    # --- エージェントのライフイベント ---
    for agent in agents[:]:  # リストをコピーしてイテレート
        # 年齢を増やす
        agent_age = agent.scratch.get('age', 25) + 1
        agent.scratch['age'] = agent_age

        # 死亡チェック（簡易的な確率モデル）
        death_chance = max(0, (agent_age - 50) * 0.02)
        if random.random() < death_chance:
            logging.info(f"{agent.scratch['first_name']} {agent.scratch['last_name']} が {agent_age} 歳で亡くなりました。")
            agents.remove(agent)
            continue

        # 出生イベント
        if 18 <= agent_age <= 45 and random.random() < 0.2:
            # 子供を持つ可能性
            child_first_name = random.choice(["はると", "ゆい", "かいと", "はな", "そら", "まお", "れん", "みこ"])
            child_last_name = agent.scratch['last_name']
            child_profile = {
                "first_name": child_first_name,
                "last_name": child_last_name,
                "age": 0,
                "occupation": "子供",
                "interests": ["遊び", "学び"]
            }
            child_agent = GenerativeAgent()
            child_agent.update_scratch(child_profile)
            agents.append(child_agent)
            agent.remember(f"{child_first_name}という子供が生まれた。", time_step)
            logging.info(f"{agent.scratch['first_name']} に {child_first_name} という子供が生まれました。")

        # 内省の実行
        agent.reflect(anchor="年次イベント", time_step=time_step)

    # --- エージェント間の相互作用 ---
    for i in range(len(agents)):
        for j in range(i + 1, len(agents)):
            agent_a = agents[i]
            agent_b = agents[j]

            # シンプルな対話
            if random.random() < 0.1:
                dialogue = [
                    (agent_a.scratch['first_name'], "最近どうですか？"),
                    (agent_b.scratch['first_name'], "元気です。最近の出来事は興味深いですね。"),
                ]
                agent_a.utterance(dialogue)
                # 相互に記憶
                agent_a.remember(f"{agent_b.scratch['first_name']} と会話した。", time_step)
                agent_b.remember(f"{agent_a.scratch['first_name']} と会話した。", time_step)

    # --- エージェントの状態を毎年保存 ---
    for agent in agents:
        agent_folder = os.path.join(agent_save_dir, f"{agent.scratch['first_name']}_{agent.scratch['last_name']}")
        if not os.path.exists(agent_folder):
            os.makedirs(agent_folder)
        agent.save(agent_folder)

logging.info("\n===== シミュレーション完了 =====")
logging.info(f"シミュレーション終了時のエージェント数: {len(agents)}")
for agent in agents:
    logging.info(f"{agent.scratch['first_name']} {agent.scratch['last_name']}, 年齢: {agent.scratch['age']}, 職業: {agent.scratch['occupation']}")
    # 最近の記憶を表示
    recent_memories = agent.memory_stream[-3:]  # 最新の3つの記憶
    logging.info("最近の記憶:")
    for memory in recent_memories:
        logging.info(f"- {memory}")
    logging.info("")