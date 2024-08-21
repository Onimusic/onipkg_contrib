# Onipkg Contrib

Pra criar novas versões, coloque o número da versão atualizada no setup.cfg, no campo `version`. Em seguida, execute o
comando `python3 -m build` no diretório raiz do projeto. Verifique que os arquivos com extensão `.tar.gz` e `.whl` foram
criados com a versão correta contida no filename sob o diretório `dist`.

## Instalação

Para instalar o pacote basta adicionar `onipkg_contrib @ git+https://github.com/Onimusic/onipkg_contrib.git@v1.2b` no
seu `requirements.txt`.

## Implementação Logger

Para implementar o pacote de logger, basta adicionar o logger do onipkg_contrib no seu arquivo de "local.py" dentro do ansible do sistema desejado,
sendo DEBUG a flag que indica se você está em ambiente de desenvolvimento ou não.

Exemplo:

```python
'handlers': {
        'file': {
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'class': 'contrib.googlelogging.google_logging_helper.OniCloudHandler',
            'formatter': 'verbose',
            'oni_services_token':ONI_SERVICES_TOKEN,
            'telegram_onitificator_bot_token': TELEGRAM_ONITIFICATOR_BOT_TOKEN,
            'chat_ids': {'dev':DEV_TELEGRAM_CHAT_ID},
            'project_name': {PROJECT_NAME},
            'client':client,
            }
       }
```

