# ------------------------------------------------------------------
# MONITOR DE REQUISIÇÕES HTTP (VERSÃO COM LOG)
# ------------------------------------------------------------------

# 1. Importações necessárias
from playwright.sync_api import sync_playwright, Request
import json
import logging # <-- MUDANÇA: Importamos o módulo de logging

# --- NOVA SEÇÃO: Configuração do Logging ---
# Configura o sistema de logging para escrever em um arquivo.
logging.basicConfig(
    filename='http_requests.log',  # Nome do arquivo de log
    level=logging.INFO,            # Nível mínimo de mensagem a ser registrada
    filemode='a',                  # 'a' para adicionar (append), 'w' para sobrescrever a cada execução
    format='%(asctime)s - %(levelname)s - %(message)s', # Formato da linha de log
    encoding='utf-8'               # Garante a compatibilidade com caracteres especiais
)
# -----------------------------------------


# 2. Função que será executada para cada requisição detectada
def monitorar_requisicao(req: Request):
    """
    Esta função agora constrói uma mensagem e a envia para o arquivo de log.
    """
    
    # Constrói a mensagem de log como uma lista de strings
    log_message = [
        "-----------------------------------------------------------",
        "🚀 NOVA REQUISIÇÃO DETECTADA!",
        f"   - Método: {req.method}",
        f"   - URL: {req.url}"
    ]

    # Adiciona os cabeçalhos à mensagem
    headers = req.headers
    headers_str = "\n".join([f"     - {key}: {value}" for key, value in headers.items()])
    log_message.append(f"   - Cabeçalhos (Headers):\n{headers_str}")

    # Se a requisição for do tipo POST, tenta adicionar o corpo (payload)
    if req.method == "POST":
        try:
            post_data = req.post_data_json
            payload_str = json.dumps(post_data, indent=4, ensure_ascii=False)
            log_message.append(f"   - Corpo da Requisição (Payload): \n{payload_str}")
        except Exception:
            log_message.append(f"   - Corpo da Requisição (Payload): {req.post_data}")
            
    log_message.append("-----------------------------------------------------------\n")

    # MUDANÇA: Em vez de 'print', usamos 'logging.info' para registrar no arquivo.
    # Juntamos todas as partes da mensagem com quebras de linha.
    logging.info("\n".join(log_message))
    
    # Também vamos manter um print no console para saber que algo foi capturado
    print(f"✅ Requisição para {req.url[:70]}... registrada no log.")


# 3. Bloco principal do nosso script
def main():
    # O 'with' garante que os recursos do Playwright serão fechados corretamente
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()

        page.on("request", monitorar_requisicao)

        # MUDANÇA: Usamos logging para registrar os eventos do script
        logging.info("Iniciando o monitoramento.")
        print(">>> Iniciando o monitoramento. As requisições serão salvas em 'http_requests.log'.")
        
        try:
            # !!! ALTERE ESTE URL PARA O SITE DESEJADO !!!
            page.goto("https://www.google.com", timeout=60000)
        except Exception as e:
            error_message = f"Não foi possível carregar a página. Erro: {e}"
            logging.error(error_message)
            print(error_message)
            browser.close()
            return

        print("\n✅ Monitoramento ativo!")
        print("Interaja com o site no navegador. Feche a janela para encerrar.")
        
        try:
            page.wait_for_timeout(300000)
        except Exception:
            print("Navegador fechado pelo usuário.")
            
        browser.close()
        logging.info("Monitoramento encerrado.")
        print("\n>>> Monitoramento encerrado. Verifique o arquivo 'http_requests.log'.")

if __name__ == "__main__":
    main()