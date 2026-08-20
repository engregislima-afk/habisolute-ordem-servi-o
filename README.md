
# Habisolute OS

Sistema inicial de Ordens de Serviço e fechamento mensal para controle tecnológico.

## Recursos incluídos

- Cadastro de clientes
- Busca automática de dados por CNPJ via BrasilAPI
- Cadastro de obras por cliente
- Catálogo de serviços
- Tabela de preços por cliente e por obra
- Vigência de preços
- Criação de OS com vários serviços
- Numeração automática de OS
- Impressão / download da OS em PDF
- Exportação da OS em Excel
- Envio da OS por e-mail com PDF anexado
- Histórico de envio por OS (data/hora, destinatário, assunto e status)
- Reenvio rápido do último e-mail
- Fechamento mensal por cliente, obra e período
- Exportação do fechamento mensal em Excel
- Dashboard básico
- Banco compatível com SQLite ou PostgreSQL

## Rodar localmente

1. Instale Python 3.11 ou 3.12.
2. Abra a pasta do projeto.
3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute:

```bash
streamlit run app.py
```

## Banco de dados

Por padrão o sistema usa SQLite, criando o arquivo:

`habisolute_os.db`

Para produção, configure a variável de ambiente `DATABASE_URL` com PostgreSQL.

Exemplo:

```text
postgresql://usuario:senha@host:5432/banco
```

No Streamlit Community Cloud, essa variável pode ser configurada nos Secrets / Environment Variables.

## Próximas melhorias recomendadas

- Login e níveis de acesso
- Cadastro/edição/exclusão completa
- Logo oficial no PDF
- Assinatura digital na OS
- QR Code
- Status de faturamento/recebimento
- Fechamento em PDF
- Nota fiscal / número da NF
- Importação de clientes
- Dashboard financeiro avançado
- Anexos/fotos por OS
- Integração com certificados/laudos

## Envio de OS por e-mail

Na tela **Consultar OS**, cada ordem possui o botão **Enviar OS por e-mail**. O endereço é preenchido com o e-mail da obra e, se não houver, com o e-mail do cliente. Antes de enviar é possível alterar destinatário, assunto e mensagem. O PDF da OS é anexado automaticamente.

Configure no Streamlit Secrets ou como variáveis de ambiente:

```toml
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = "587"
SMTP_USER = "seu-email@dominio.com.br"
SMTP_PASSWORD = "senha-de-app-ou-senha-smtp"
SMTP_FROM = "seu-email@dominio.com.br"
SMTP_FROM_NAME = "Habisolute Engenharia e Controle Tecnológico"
```

Para Gmail/Google Workspace, recomenda-se usar uma **senha de app** quando disponível, em vez da senha normal da conta.


## Configuração de e-mail SMTP

Defina estas variáveis no ambiente/Secrets:

```text
SMTP_HOST=smtp.seudominio.com
SMTP_PORT=587
SMTP_USER=seuemail@seudominio.com
SMTP_PASSWORD=sua_senha_ou_senha_de_app
SMTP_FROM=seuemail@seudominio.com
SMTP_USE_TLS=true
```

A senha não deve ser colocada diretamente no código-fonte.
