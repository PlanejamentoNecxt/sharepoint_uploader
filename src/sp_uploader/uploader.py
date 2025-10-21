# src/sp_uploader/uploader.py
import os
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext


class SharePointUploader:
    """
    Classe para lidar com autenticação e upload de arquivos para o SharePoint.
    As credenciais são fornecidas durante a instanciação.
    Levanta uma exceção se a autenticação falhar.
    """

    def __init__(self, url_site_sp, usuario_sp, senha_sp):
        self.url_site_sp = url_site_sp
        self.usuario_sp = usuario_sp
        self.senha_sp = senha_sp
        self.ctx = None
        # A autenticação é chamada aqui e pode levantar uma exceção
        self._authenticate()

    def _authenticate(self):
        """Autentica no SharePoint e armazena o contexto (self.ctx)."""
        try:
            ctx_auth = AuthenticationContext(self.url_site_sp)
            if not ctx_auth.acquire_token_for_user(self.usuario_sp, self.senha_sp):
                error_msg = ctx_auth.get_last_error()
                # Em vez de logar, lança a exceção para o app principal
                raise Exception(f"Falha na autenticação do SharePoint: {error_msg}")

            self.ctx = ClientContext(self.url_site_sp, ctx_auth)
        except Exception as e:
            self.ctx = None
            # Relança a exceção para o app principal saber que falhou
            raise Exception(f"Erro detalhado na autenticação: {e}")

    def upload_arquivo(self, caminho_arquivo_local, pasta_alvo_sharepoint):
        """
        Faz o upload de um arquivo para uma pasta específica no SharePoint,
        substituindo se já existir.

        :param caminho_arquivo_local: Caminho completo do arquivo local.
        :param pasta_alvo_sharepoint: URL relativa da pasta (ex: "Documentos Compartilhados")
        :return: True em sucesso, False em falha.
        """
        if not self.ctx:
            # Se a autenticação falhou (ctx é None), não faz nada e retorna falha
            return False

        try:
            nome_arquivo = os.path.basename(caminho_arquivo_local)
            target_folder = self.ctx.web.get_folder_by_server_relative_url(pasta_alvo_sharepoint)

            with open(caminho_arquivo_local, 'rb') as content_file:
                file_content = content_file.read()

            target_folder.files.add(nome_arquivo, file_content, overwrite=True).execute_query()

            return True  # Sucesso
        except Exception as e:
            # Qualquer erro durante o upload (ex: pasta não existe, permissão)
            # apenas retorna False. O app principal decide o que fazer.
            # print(f"Erro no upload: {e}") # Evitamos 'print' em bibliotecas
            return False  # Falha