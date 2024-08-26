import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('JiraSessionTable')

# Defina a chave primária da sua tabela (Partition Key e, se aplicável, Sort Key)
partition_key_name = 'SessionId'  # Substitua pelo nome da sua chave de partição

def get_all_keys():
    keys=[]
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
        
        for item in data:
            keys.append({
            partition_key_name: item[partition_key_name]
            })

    return keys

if __name__=="__main__":
    print(get_all_keys())