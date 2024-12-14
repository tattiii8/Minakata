from typing import Union
from fastapi import FastAPI
import pymysql
import httpx  # HTTPクライアントライブラリ

app = FastAPI()

EXTERNAL_API_URL = "https://8tofhjnexd.execute-api.ap-northeast-1.amazonaws.com/dev/users"  # 外部APIのURLの例


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/external/")
async def get_external_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(EXTERNAL_API_URL)  # 外部APIを非同期でGET
    if response.status_code == 200:
        return {"status": "success", "data": response.json()}  # JSONデータを返す
    return {"status": "error", "message": "Failed to fetch data"}

@app.get("/flaubert/api/users")
def get_users():
    """
    MySQLデータベースからユーザー情報を取得するエンドポイント
    """
    try:
        # データベース接続
        connection = pymysql.connect(
            host="192.168.8.23",
            user="api",
            password="040629602t",
            database="redmine",
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,  # 辞書形式で結果を取得
        )

        with connection.cursor() as cursor:
            # SQLクエリの実行
            sql_query = "SELECT * FROM users"  # テーブル名を適宜変更
            cursor.execute(sql_query)
            result = cursor.fetchall()  # 全ての結果を取得

        # 接続を閉じる
        connection.close()

        # データをJSON形式で返す
        return {"status": "success", "data": result}

    except Exception as e:
        # エラーハンドリング
        return {"status": "error", "message": str(e)}