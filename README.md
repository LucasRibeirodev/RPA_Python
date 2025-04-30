# RPA_Python
Documentação Técnica: Automação de Processo RPA em Python
Resumo do Projeto
Este projeto implementa uma solução de RPA (Robotic Process Automation) em Python para extrair arquivos de um servidor SFTP, validar e processar esses arquivos, automatizar a importação no sistema CSLOG, e registrar logs detalhados. O código foi configurado para funcionar de maneira totalmente automática, rodando diariamente via Agendador de Tarefas do Windows.

Arquitetura
O script utiliza as seguintes bibliotecas:

os: Gerenciamento de arquivos e diretórios locais.

json: Manipulação de arquivos de configuração.

time: Controle de espera e validação de tempos.

logging: Registro de eventos e logs de execução.

paramiko: Interação com servidores SFTP.

pyautogui: Automação de entrada do teclado e mouse.

Path: Manipulação de caminhos com a biblioteca pathlib.

datetime: Manipulação de data e hora.

O script está dividido em múltiplos métodos que lidam com conexões SFTP, validações de arquivos, automação no CSLOG e outros processos.

Fluxo de Execução
Configurações Carregadas:

Um arquivo config.json é usado para armazenar credenciais do SFTP, informações do CSLOG e o diretório local de extração.

Conexão ao SFTP:

O script inicia uma conexão ao servidor SFTP, acessa o diretório especificado e verifica arquivos disponíveis.

Validação de Arquivos:

Verifica se existe um arquivo com a data atual. Caso não exista, realiza verificações em intervalos de 2 minutos.

Confirma a estabilidade do arquivo ao validar seu tamanho em intervalos de 1 minuto.

Extração de Arquivos:

Após a validação, o script limpa a pasta local de destino e faz o download do arquivo mais recente.

Automação CSLOG:

Utiliza pyautogui para interagir com a interface do CSLOG, realizando login e navegando até o módulo de importação para processar o arquivo.

Logs Detalhados:

Cada etapa e erro são registrados no arquivo de logs rpa_process.log para auditoria e depuração.

Encerramento:

A conexão SFTP é fechada ao final do processo.

Configuração do Ambiente
Requisitos
Python: Certifique-se de ter o Python instalado (versão 3.9+ recomendada).

Bibliotecas Necessárias: Execute o seguinte comando para instalar todas as dependências:

bash
pip install paramiko pyautogui
Arquivo de Configuração (config.json): Este arquivo deve ser formatado como:

json
{
  "sftp": {
    "host": "ftp-8a6fe4-prod.owill.com.br",
    "port": 22,
    "username": "trctaborda",
    "password": "XgHMD5F85pwd3Dw8",
    "base_dir": "/ftp-will-assessorias-prod/trctaborda"
  },
  "cslog": {
    "exe_path": "C:\\Program Files (x86)\\CSLog\\Administrativo\\startsiscob.exe",
    "username": "lucas.ribeiro",
    "password": "Luc17021988"
  },
  "local_base_dir": "C:\\Users\\lucas.ribeiro\\Desktop\\Aut_RPA_Will\\Extração SFTP"
}
Estrutura do Código
Classe AutomatedSFTPProcess
A classe encapsula todo o fluxo de automação e está dividida nos seguintes métodos principais:

__init__(config_file):

Carrega configurações do arquivo config.json.

Configura variáveis globais como sftp_config e local_base_dir.

setup_sftp_connection():

Estabelece conexão ao servidor SFTP utilizando paramiko.

Lança exceção caso a conexão falhe.

close_sftp_connection():

Fecha a conexão ao servidor SFTP.

check_file_date():

Verifica se existe um arquivo com a data atual no diretório remoto.

Retorna o caminho remoto do arquivo ou None.

wait_for_stable_file(file_path):

Aguarda até que o arquivo estabilize seu tamanho.

Retorna True quando o tamanho do arquivo é constante.

clear_local_directory():

Remove arquivos existentes no diretório local de extração.

download_file(remote_path, local_path):

Baixa o arquivo do servidor SFTP para o diretório local.

automate_cslog(file_path):

Utiliza pyautogui para realizar login e importação no CSLOG.

Simula cliques e entradas de texto conforme as coordenadas definidas.

run():

Executa o fluxo completo:

Conecta ao SFTP.

Processa diretório e arquivo.

Executa automação do CSLOG.

Fecha conexão.

Configuração do Agendador de Tarefas (Windows)
Criar uma Tarefa:

Acesse o Agendador de Tarefas no Windows.

Clique em Criar Tarefa.

Configurações:

Defina um nome para a tarefa, como "Automação RPA".

Configure para executar diariamente às 5:30 da manhã.

Ação:

Escolha a opção Iniciar um Programa.

Caminho do programa: C:\Users\lucas.ribeiro\Desktop\Aut_RPA_Will\rpa_will.exe.

Concluir:

Salve a tarefa e teste para garantir que está funcionando.

Tratamento de Erros
Logs
Todos os eventos e erros são registrados no arquivo rpa_process.log. Exemplos:

Sucesso: Conexão SFTP estabelecida com sucesso.

Erro: Erro ao conectar ao servidor SFTP: Connection Timeout.

Exceções
O código utiliza try e except para capturar erros críticos:

JSONDecodeError: Erro no formato do arquivo config.json.

FileNotFoundError: Arquivo de configuração não encontrado.

Exception: Captura erros gerais durante execução.

Conclusão
Este projeto de automação utiliza práticas robustas para interações com servidores SFTP e sistemas GUI, garantindo confiabilidade e desempenho. Ele está configurado para rodar automaticamente e registrar todas as ações, tornando-o ideal para processos repetitivos e críticos.

Se necessário, futuras extensões podem incluir:

Suporte para múltiplos diretórios.

Integração com APIs de sistemas ao invés de automação GUI.

Documentação concluída. 🚀
