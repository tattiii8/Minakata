import re
import requests

# トークン化の関数
def tokenize(text):
    """
    テキストをトークンに分割する。
    """
    text = text.strip()  # 不要な空白を削除
    text = re.sub(r"(\w+)([’'])(\w+)", r"\1\2 \3", text)  # アポストロフィを分ける
    text = re.sub(r"(\w)-(\w)", r"\1 - \2", text)  # ハイフンの扱い
    text = re.sub(r"([.,!?;:()])", r" \1 ", text)  # 句読点を分離
    tokens = text.split()  # スペースで分割
    return tokens

# Wiktionary APIを利用して意味だけを抽出
def search_wiktionary_meaning(word, language="fr"):
    """
    フランス語Wiktionary APIを使用して単語の「Nom commun」セクションから意味を取得。

    :param word: 単語
    :param language: 言語コード（デフォルトはフランス語 'fr'）
    :return: 単語の意味（リスト形式）またはエラーメッセージ
    """
    url = f"https://{language}.wiktionary.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": word,
        "prop": "extracts",
        "explaintext": True
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"Error: Failed to fetch data for '{word}'. HTTP Status Code: {response.status_code}"

    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    for page_id, page_content in pages.items():
        if page_id == "-1":  # 単語が見つからない場合
            return f"Aucune définition trouvée pour '{word}'"

        # 抽出結果から「Nom commun」セクションを探す
        extract = page_content.get("extract", "")
        nom_commun_match = re.search(r"=== Nom commun ===(.*?)(===|$)", extract, re.DOTALL)
        if not nom_commun_match:
            return f"Aucune définition trouvée pour '{word}' dans 'Nom commun'"

        # 意味を箇条書きから抽出
        nom_commun_content = nom_commun_match.group(1)
        meanings = re.findall(r"- (.*?)\n", nom_commun_content)
        return meanings if meanings else f"Aucune définition claire pour '{word}'"
    
    return "Erreur: Réponse inattendue du serveur."

# Lambdaハンドラー関数
def lambda_handler(event, context):
    """
    AWS Lambda用のメインハンドラー関数。
    テキストをトークン化し、各トークンの意味を取得して返す。
    """
    text = event.get("text", "")
    if not text:
        return {
            "statusCode": 400,
            "body": "Aucun texte fourni"
        }

    # トークン化
    tokens = tokenize(text)

    # 各トークンの意味を取得
    token_definitions = {}
    for token in tokens:
        definitions = search_wiktionary_meaning(token, language="fr")  # フランス語Wiktionaryを使用
        token_definitions[token] = definitions

    # 結果を返却
    return {
        "statusCode": 200,
        "body": {
            "original_text": text,
            "tokens": tokens,
            "definitions": token_definitions
        }
    }
