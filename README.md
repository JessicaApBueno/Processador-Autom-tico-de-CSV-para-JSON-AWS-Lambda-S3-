# Projeto DevOps: Processador Automático de CSV para JSON (AWS Lambda + S3)

Este projeto implementa um pipeline de dados serverless (ETL) simples na AWS. Ele utiliza uma Função Lambda para monitorar um bucket S3. Quando um arquivo `.csv` é enviado para o bucket de entrada, a Lambda é acionada automaticamente, converte o conteúdo para o formato JSON e o salva em um segundo bucket S3.

O projeto é totalmente gerenciado com práticas de DevOps usando o **AWS SAM (Serverless Application Model)** para definir e implantar a Infraestrutura como Código (IaC).
<img width="1088" height="617" alt="Captura de tela 2025-10-24 145449" src="https://github.com/user-attachments/assets/325e4e7f-8e21-45f3-a832-5a003ba82176" />
<img width="1225" height="482" alt="Captura de tela 2025-10-24 231437" src="https://github.com/user-attachments/assets/3534c1ec-ec10-42bb-9c72-f6ed2a8e14f7" />
<img width="1095" height="637" alt="Captura de tela 2025-10-24 151526" src="https://github.com/user-attachments/assets/731fe64c-f596-4357-ac4b-e3eb7e7f42c7" />
<img width="1904" height="991" alt="Captura de tela 2025-10-24 231556" src="https://github.com/user-attachments/assets/baa7227a-be76-4fc6-92fe-6e693466f19a" />
<img width="1897" height="423" alt="Captura de tela 2025-10-24 231625" src="https://github.com/user-attachments/assets/7df1757b-cdf2-4693-b9dc-64ff688e6527" />
<img width="1866" height="1029" alt="Captura de tela 2025-10-25 000218" src="https://github.com/user-attachments/assets/569399f9-cb4b-4b70-873b-e638e91d97d6" />
<img width="1918" height="1007" alt="Captura de tela 2025-10-25 000330" src="https://github.com/user-attachments/assets/c4876e11-cac3-42e2-adcd-bb67fcdeb821" />


## Arquitetura do Projeto

O fluxo de dados é simples e 100% serverless:

1.  Um usuário (ou sistema) faz o upload de um arquivo (ex: `vendas.csv`) no **Bucket S3 de Entrada**.
2.  O S3 detecta o evento de criação de objeto (`s3:ObjectCreated:*`) e aciona a **Função AWS Lambda**.
3.  A **Função Lambda** (escrita em Python) é executada. Ela:
    a. Recebe as informações do evento (nome do bucket e do arquivo).
    b. Lê e baixa o arquivo `.csv` do Bucket de Entrada.
    c. Processa o conteúdo, convertendo as linhas do CSV para uma estrutura JSON.
    d. Salva um novo arquivo (ex: `vendas.json`) no **Bucket S3 de Saída**.

## Tecnologias Utilizadas

* **AWS Lambda:** Para a computação serverless (execução do código Python).
* **Amazon S3:** Para armazenamento de objetos (buckets de entrada e saída).
* **AWS SAM CLI:** Para o build e deploy da infraestrutura como código.
* **AWS CloudFormation:** Orquestrador usado pelo SAM para criar os recursos na AWS.
* **AWS IAM:** Para gerenciar as permissões de execução da Lambda.
* **Python 3.12:** Linguagem de programação da Função Lambda.

## Estrutura do Projeto

A estrutura de pastas é otimizada para o AWS SAM:

```bash
.
├── processar_csv/      <-- Pasta com o código-fonte da Função Lambda
│   └── app.py          <-- O script Python que faz a conversão
├── samconfig.toml      <-- Arquivo de configuração gerado pelo SAM
└── template.yaml       <-- Template IaC (SAM/CloudFormation) que define TODOS os recursos


