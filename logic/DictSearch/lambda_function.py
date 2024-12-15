# DictSearch
import boto3
import json

# DynamoDBリソースの初期化
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Dict')

def get_mot_sens(mot):
    # DynamoDBからアイテムを取得
    response = table.get_item(Key={'Mot': mot})
    if 'Item' in response:
        return response['Item']  # アイテムが見つかった場合
    else:
        return None  # 見つからない場合は None を返す

def lambda_handler(event, context):
    # リクエストから 'mot' を取得
    mot = event.get('mot')
    
    if not mot:
        # 入力エラー
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Mot non spécifié'})  # 入力が不足している場合
        }
    
    # get_mot_sens関数を呼び出して結果を取得
    result = get_mot_sens(mot)
    
    if result:
        # データが見つかった場合
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    else:
        # データが見つからない場合
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Mot introuvable'})
        }
