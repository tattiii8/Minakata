import re

def tokenize(text):
    # 1. 基本的な正規化（不要な空白を削除）
    text = text.strip()
    
    # 2. アポストロフィの扱い（l'homme や d'accord を分ける）
    text = re.sub(r"(\w+)([’'])(\w+)", r"\1\2 \3", text)
    
    # 3. 特殊なハイフンの扱い（aujourd'hui のような例）
    text = re.sub(r"(\w)-(\w)", r"\1 - \2", text)
    
    # 4. 句読点を分離
    text = re.sub(r"([.,!?;:()])", r" \1 ", text)
    
    # 5. スペースでトークンに分割
    tokens = text.split()
    
    return tokens

def lambda_handler(event, context):
    # イベントからテキストを取得
    text = event.get("text", "")
    if not text:
        return {
            "statusCode": 400,
            "body": "No text provided"
        }
    
    # トークン化処理
    tokens = tokenize(text)
    
    # 結果を返却
    return {
        "statusCode": 200,
        "body": {
            "original_text": text,
            "tokens": tokens
        }
    }
