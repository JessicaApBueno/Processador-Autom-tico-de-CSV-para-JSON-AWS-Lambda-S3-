import json
import csv
import boto3
import os  # <-- 1. Importamos a biblioteca 'os'

# Crie clientes S3 fora do handler para reutilizar conexões
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    
    # 2. Pegamos o nome do bucket de saída da variável de ambiente
    # O SAM vai injetar essa variável baseado no 'template.yaml'
    try:
        output_bucket = os.environ['OUTPUT_BUCKET_NAME']
    except KeyError:
        print("ERRO: Variável de ambiente OUTPUT_BUCKET_NAME não definida.")
        return {'statusCode': 500, 'body': 'Erro de configuração.'}

    # 1. Obter informações do evento S3
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    print(f"Novo arquivo detectado: {file_key} no bucket {bucket_name}")
    
    # Só processa se for .csv (uma boa prática)
    if not file_key.endswith('.csv'):
        print("Não é um arquivo .csv, ignorando.")
        return
        
    # 2. Baixar o arquivo .csv do S3 de "Entrada"
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        # Lê o conteúdo do arquivo como texto, tratando quebras de linha
        data = response['Body'].read().decode('utf-8').splitlines()
        
        # Converte as linhas do CSV para uma lista de dicionários
        csv_reader = csv.DictReader(data)
        # Força a conversão para lista (melhor que deixar como gerador)
        json_data = list(csv_reader) 
        
        print(f"Arquivo CSV lido e convertido para JSON com {len(json_data)} linhas.")

    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        raise e

    # 3. Salvar o arquivo .json no S3 de "Saída"
    
    # Muda a extensão do arquivo de .csv para .json
    output_key = file_key.replace('.csv', '.json')
    
    try:
        s3_client.put_object(
            Bucket=output_bucket, # <-- 3. Usamos a variável
            Key=output_key,
            Body=json.dumps(json_data, indent=2), # Converte o Python dict para string JSON
            ContentType='application/json'
        )
        print(f"Arquivo JSON salvo com sucesso em: {output_bucket}/{output_key}")
        
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")
        raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Processamento concluído com sucesso!')
    }
