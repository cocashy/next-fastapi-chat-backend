## Backend

サーバーを立ち上げる：

```bash
venv/Scripts/activate
python -m api.main
```

uvicornを使用する場合は：

```bash
venv/Scripts/activate
python -m uvicorn api.main:app --reload --host=localhost
```

http://localhost:8000 でサーバーが立ち上がる

## ディレクトリ構成

```
root/
├─api/
│  ├─db/
│  ├─entity/
│  ├─model/
│  ├─repository/
│  ├─schema/
│  └─usecase/
├─main.py
├─.env
├─db.sqlite3
└─requirements.txt
```

## Deploy

https://render.com にデプロイする

```bash
venv/Scripts/activate
pip freeze > requirements.txt
```

環境変数を追加する

15分間アクセスが無いとシャットダウンするので
GASで10分おきに`/health`にアクセスする
