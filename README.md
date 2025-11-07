# Biblioteca de Upload para SharePoint (sp_uploader)

Um pacote simples para automatizar uploads de arquivos no SharePoint.

## Instalação

```bash
pip install git+https://github.com/PlanejamentoNecxt/sharepoint_uploader
```

## Exemplo de Uso

O código agora não produz logs. A autenticação levantará uma `Exception` se falhar, e o método `upload_arquivo` retornará `True` (sucesso) ou `False` (falha).

```python
import os
from dotenv import load_dotenv
from sp_uploader import SharePointUploader

# Carregue suas variáveis de ambiente
load_dotenv()

URL_SITE_SHAREPOINT = os.getenv("URL_SITE_SHAREPOINT")
USUARIO_SHAREPOINT = os.getenv("USUARIO_SHAREPOINT")
SENHA_SHAREPOINT = os.getenv("SENHA_SHAREPOINT")
PASTA_DESTINO = os.getenv("PASTA_DESTINO")

try:
    # 1. Instanciar a classe
    # A autenticação ocorre aqui. Se falhar, levantará uma exceção.
    uploader = SharePointUploader(url_site_sp=URL_SITE,
                                  usuario_sp=USUARIO,
                                  senha_sp=SENHA)

    # 2. Tentar o upload
    sucesso = uploader.upload_arquivo(caminho_arquivo_local="relatorio_suri.csv",
                                      pasta_alvo_sharepoint=PASTA_DESTINO)
    
    if sucesso:
        print("Upload realizado com sucesso!")
    else:
        # Isso pode acontecer se a pasta não existir ou por falta de permissão
        print("Falha no upload do arquivo.")

except Exception as e:
    # Captura falhas de autenticação ou outros erros inesperados
    print(f"Ocorreu um erro (provavelmente na autenticação): {e}")

```
