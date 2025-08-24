# ベースとなるPythonの環境を指定
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なライブラリをインストール
COPY requirements.txt .
# ▼▼▼ この行を修正しました ▼▼▼
RUN pip install --no-cache-dir --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# コンテナ起動時に実行するコマンド
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "app:app"]

