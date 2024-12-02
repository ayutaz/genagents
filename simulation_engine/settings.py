from pathlib import Path
from dotenv import load_dotenv
import os

# プロジェクトのルートディレクトリを取得
BASE_DIR = Path(__file__).resolve().parent.parent

# .envファイルのパスを指定して読み込む
load_dotenv(dotenv_path=BASE_DIR / '.env')

# .envファイルから環境変数を取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
KEY_OWNER = os.getenv("KEY_OWNER")

# APIキーが存在するかチェック
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEYが設定されていません。'.env' ファイルを確認してください。")

DEBUG = False

MAX_CHUNK_SIZE = 4

LLM_VERS = "gpt-4o-mini"

POPULATIONS_DIR = f"{BASE_DIR}/agent_bank/populations"
LLM_PROMPT_DIR = f"{BASE_DIR}/simulation_engine/prompt_template"