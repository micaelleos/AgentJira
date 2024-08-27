import boto3
import uuid
# Inicializa o cliente do DynamoDB
dynamodb = boto3.resource('dynamodb')

# Especifica a tabela
table = dynamodb.Table('JiraUserTable')

def val_user_session(userId,session):
    user_data = get_user_data(userId)
    if session in user_data["Sessions"]:
        return True
    else:
        return False

def val_user_exist(userId):

    keys=[]
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
        
    for item in data:
        keys.append(item["UserId"]) 
    
    
    if userId in keys:
        return True
    else:
        return False

def put_user_session(userId):
    # Item que será inserido
    session = str(uuid.uuid4())
    user_data = get_user_data(userId)
    session_list = user_data["Sessions"]
    session_list.append(str(session))

    item = {
        'UserId': user_data["UserId"],    # Chave primária da tabela
        'Nome': user_data["Nome"],     # Outro atributo do item
        'Email': user_data["Email"],
        'Url':user_data["Url"],
        'password':user_data["password"],
        'Sessions':session_list
    }

    # Insere o item na tabela
    try:
        response = table.put_item(
            Item=item
        )
        return session
    except Exception as e:
        print("Erro ao inserir item:", e)

def get_user_data(userId):
    response = table.get_item(
        Key={'UserId':userId}
    )
    return response['Item']

def user_config(user_name:str,url:str=None,email:str=None,password:str=None):
    item = {
        'UserId': str(uuid.uuid4()),    # Chave primária da tabela
        'Nome': user_name,     # Outro atributo do item
        'Email': email,
        'Url':url,
        'Password':password,
        'Sessions':[]
    }

    # Insere o item na tabela
    try:
        response = table.put_item(
            Item=item
        )
        return item
    except Exception as e:
        print("Erro ao inserir item:", e)

def get_all_users():
    keys=[]
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
        
    for item in data:
        keys.append({"Userid": item["UserId"], 
                     "user_data":
                            {
                            'Nome': item["Nome"],     # Outro atributo do item
                            'Email':item["Email"],
                            'Sessions':item["Sessions"] 
                            }
                    }
        )

    return keys

if __name__=="__main__":
    #print(user_config('micaelle'))
    
    #print(put_user_session('99903cb0-616d-4278-af7b-f8d58ebcf9a1','4b4'))
    #print("-----------------")
    #print(get_user_data('99903cb0-616d-4278-af7b-f8d58ebcf9a1'))
    #print(val_user_session('99903cb0-616d-4278-af7b-f8d58ebcf9a1','b54'))
    #print(get_all_users())
    print(val_user_exist('9'))