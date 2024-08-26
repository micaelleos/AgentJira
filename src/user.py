import boto3

# Inicializa o cliente do DynamoDB
dynamodb = boto3.resource('dynamodb')

# Especifica a tabela
table = dynamodb.Table('MinhaTabela')

# Item que será inserido
item = {
    'PrimaryKey': '12345',    # Chave primária da tabela
    'Nome': 'João Silva',     # Outro atributo do item
    'Email': 'joao@example.com',
    'Idade': 30,
    'Ativo': True,
    'DataCriacao': '2024-08-25'
}

# Insere o item na tabela
try:
    response = table.put_item(
        Item=item
    )
    print("Item inserido com sucesso:", response)
except Exception as e:
    print("Erro ao inserir item:", e)