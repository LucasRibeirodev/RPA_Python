import os
import json
import time
import logging
import paramiko
import pyautogui
from pathlib import Path
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    filename='rpa_process.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

class AutomatedSFTPProcess:
    def __init__(self, config_file):
        try:
            with open(config_file, 'r') as file:
                config = json.load(file)
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao carregar config.json: {str(e)}")
            raise
        except FileNotFoundError:
            logger.error(f"Arquivo {config_file} não encontrado")
            raise

        # Carregar configurações
        self.sftp_config = config['sftp']
        self.local_base_dir = config['local_base_dir']
        self.cslog_config = config['cslog']
        
        # Trabalhar apenas com o diretório CarteiraDeCobranca
        self.directory = "CarteiraDeCobranca"
        self.sftp = None
        self.transport = None

    def setup_sftp_connection(self):
        """Estabelece conexão SFTP"""
        try:
            self.transport = paramiko.Transport((self.sftp_config['host'], self.sftp_config['port']))
            self.transport.connect(username=self.sftp_config['username'], password=self.sftp_config['password'])
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            logger.info("Conexão SFTP estabelecida com sucesso")
        except Exception as e:
            logger.error(f"Erro ao conectar ao servidor SFTP: {str(e)}")
            raise

    def close_sftp_connection(self):
        """Fecha conexão SFTP"""
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()
        logger.info("Conexão SFTP fechada")

    def check_file_date(self):
        """Verifica se existe um arquivo com a data atual"""
        directory = f"{self.sftp_config['base_dir']}/{self.directory}"
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            logger.info(f"Verificando arquivos no diretório: {directory}")
            for file in self.sftp.listdir(directory):
                logger.info(f"Arquivo encontrado: {file}")
                file_attr = self.sftp.stat(f"{directory}/{file}")
                file_date = datetime.fromtimestamp(file_attr.st_mtime).strftime("%Y-%m-%d")
                if file_date == today:
                    logger.info(f"Arquivo com a data atual encontrado: {file}")
                    return f"{directory}/{file}"
            logger.info(f"Nenhum arquivo encontrado com a data de hoje em {self.directory}")
            return None
        except Exception as e:
            logger.error(f"Erro ao verificar arquivos no diretório {directory}: {str(e)}")
            return None

    def wait_for_stable_file(self, file_path):
        """Aguarda o arquivo estabilizar em tamanho"""
        prev_size = -1
        while True:
            try:
                file_attr = self.sftp.stat(file_path)
                current_size = file_attr.st_size
                if current_size == prev_size:
                    logger.info(f"Arquivo estabilizou: {file_path}")
                    return True
                prev_size = current_size
                logger.info(f"Tamanho atual: {current_size}. Reavaliando em 1 minuto...")
                time.sleep(60)
            except Exception as e:
                logger.error(f"Erro ao verificar estabilidade: {str(e)}")
                return False

    def clear_local_directory(self):
        """Limpa a pasta de destino"""
        try:
            if os.path.exists(self.local_base_dir):
                for root, dirs, files in os.walk(self.local_base_dir):
                    for file in files:
                        os.remove(os.path.join(root, file))
            logger.info("Diretório local limpo")
        except Exception as e:
            logger.error(f"Erro ao limpar diretório: {str(e)}")

    def download_file(self, remote_path, local_path):
        """Baixa o arquivo do servidor SFTP"""
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            self.sftp.get(remote_path, local_path)
            logger.info(f"Arquivo baixado: {local_path}")
        except Exception as e:
            logger.error(f"Erro ao baixar arquivo: {str(e)}")

    def automate_cslog(self, file_path):
        """Automatiza a importação do arquivo no CSLOG"""
        try:
            logger.info("Iniciando automação do CSLOG")
            pyautogui.hotkey('win', 'r')
            pyautogui.write(self.cslog_config['exe_path'])
            pyautogui.press('enter')
            time.sleep(5)  # Aguardar a abertura do CSLOG
            
            # Login no CSLOG
            pyautogui.write(self.cslog_config['username'])
            pyautogui.press('tab')
            pyautogui.write(self.cslog_config['password'])
            pyautogui.press('enter')
            time.sleep(3)  # Aguardar login
            
            # Navegar até o módulo de importação e selecionar o arquivo
            
            pyautogui.click(x=86, y=37)   
            pyautogui.click(x=134, y=53)  
            pyautogui.click(x=414, y=77) 
            time.sleep(5)
            pyautogui.click(x=441, y=54)
            pyautogui.click(x=235, y=84)
            pyautogui.click(x=443, y=81)
            pyautogui.click(x=223, y=110)
            pyautogui.click(x=438, y=111)
            pyautogui.click(x=237, y=169)
            time.sleep(2)
            pyautogui.click(x=547, y=192)
            pyautogui.click(x=551, y=319)
            pyautogui.click(x=691, y=462)
            pyautogui.press('enter')
            time.sleep(2)
            pyautogui.click(x=673, y=284)
            pyautogui.press('enter')
            time.sleep(2)
            pyautogui.click(x=668, y=257)
            pyautogui.press('enter')
            time.sleep(2)
            pyautogui.click(x=670, y=260)
            pyautogui.click(x=1102, y=556)
            pyautogui.click(x=553, y=222)

            pyautogui.write(file_path)
            pyautogui.press('enter')
            time.sleep(5)
            logger.info("Importação concluída no CSLOG")
        except Exception as e:
            logger.error(f"Erro na automação do CSLOG: {str(e)}")

    def run(self):
        """Executa todo o processo"""
        try:
            self.setup_sftp_connection()
            logger.info(f"Processando diretório: {self.directory}")
            timeout = 3600  # Limite de tempo de espera (1 hora)
            start_time = time.time()
            while True:
                file_path = self.check_file_date()
                if file_path:
                    if self.wait_for_stable_file(file_path):
                        self.clear_local_directory()
                        local_path = os.path.join(self.local_base_dir, self.directory, os.path.basename(file_path))
                        self.download_file(file_path, local_path)
                        self.automate_cslog(local_path)
                        break
                elif time.time() - start_time > timeout:
                    logger.warning(f"Tempo limite atingido para {self.directory}. Encerrando verificação.")
                    break
                else:
                    logger.info("Nenhum arquivo encontrado. Verificando novamente em 2 minutos...")
                    time.sleep(120)
        finally:
            self.close_sftp_connection()

if __name__ == "__main__":
    process = AutomatedSFTPProcess('C:\\Users\\lucas.ribeiro\\Desktop\\Aut_RPA_Will\\config.json')
    process.run()
