## backend

サーバーを立ち上げる：

```bash
cd backend
python -m api.main
```

uvicornを使用する場合は：

```bash
cd backend
python -m uvicorn api.main:app --reload --host=localhost
```
