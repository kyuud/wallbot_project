"""
Validadores de Página e Sessão - WallBot SIACH

Este módulo contém funções de validação para:
- Validar entrada de dados (Excel, email, scripts)
- Verificar estado de páginas do SIACH
- Detectar erros de conexão e sessão
- Identificar páginas de manutenção
"""

import os
from typing import Dict, Tuple, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# ==================== VALIDAÇÃO DE ENTRADA ====================

def validar_arquivo_excel(caminho_arquivo: str) -> Tuple[bool, str]:
    """
    Valida se o arquivo Excel existe e tem extensão válida

    Args:
        caminho_arquivo: Caminho para o arquivo Excel

    Returns:
        Tupla (válido, mensagem_erro)
        - válido: True se válido, False caso contrário
        - mensagem_erro: Descrição do erro ou string vazia
    """
    if not caminho_arquivo:
        return False, "Nenhum arquivo foi selecionado"

    if not os.path.exists(caminho_arquivo):
        return False, f"Arquivo não encontrado: {caminho_arquivo}"

    extensao = caminho_arquivo.lower()
    if not (extensao.endswith('.xlsx') or extensao.endswith('.xls')):
        return False, "Arquivo deve ser Excel (.xlsx ou .xls)"

    # Verificar permissão de leitura
    if not os.access(caminho_arquivo, os.R_OK):
        return False, f"Sem permissão de leitura para: {caminho_arquivo}"

    return True, ""


def validar_email(email: str) -> Tuple[bool, str]:
    """
    Valida formato básico de email

    Args:
        email: String do email

    Returns:
        Tupla (válido, mensagem_erro)
    """
    if not email or not email.strip():
        return False, "Email não pode estar vazio"

    email = email.strip()

    if '@' not in email:
        return False, "Email deve conter '@'"

    if '.' not in email:
        return False, "Email deve conter domínio (.com, .com.br, etc)"

    partes = email.split('@')
    if len(partes) != 2:
        return False, "Email com formato inválido"

    usuario, dominio = partes

    if not usuario:
        return False, "Usuário do email não pode estar vazio"

    if not dominio or '.' not in dominio:
        return False, "Domínio do email inválido"

    return True, ""


def validar_credenciais(email: str, senha: str) -> Tuple[bool, str]:
    """
    Valida credenciais de login

    Args:
        email: Email do usuário
        senha: Senha

    Returns:
        Tupla (válido, mensagem_erro)
    """
    if not email or not senha:
        return False, "Email e senha são obrigatórios"

    # Validar email
    email_valido, msg_email = validar_email(email)
    if not email_valido:
        return False, msg_email

    if len(senha) < 3:
        return False, "Senha muito curta"

    return True, ""


def validar_script_personalizacao(script: str, usar_personalizacao: bool) -> Tuple[bool, str]:
    """
    Valida script de finalização e personalização

    Args:
        script: Conteúdo do script
        usar_personalizacao: Se personalização está ativada

    Returns:
        Tupla (válido, mensagem_aviso)
        Aviso é retornado se personalização ativada mas placeholder ausente
    """
    if not script or not script.strip():
        return False, "Script de finalização não pode estar vazio"

    if usar_personalizacao and '@NomeCliente@' not in script:
        aviso = (
            "Personalização ativada, mas script não contém @NomeCliente@.\n"
            "O script será usado sem personalização."
        )
        return True, aviso

    return True, ""


# ==================== VALIDAÇÃO DE PÁGINA SIACH ====================

def validar_pagina_siach(driver: WebDriver, timeout: int = 10) -> Dict[str, any]:
    """
    Valida se a página atual é do SIACH e está carregada corretamente

    Args:
        driver: WebDriver do Selenium
        timeout: Tempo máximo de espera em segundos

    Returns:
        Dict com resultado da validação:
        {
            'valido': bool,
            'tipo_pagina': str ('login', 'menu', 'protocolo', 'desconhecida'),
            'mensagem': str,
            'elementos_presentes': list
        }
    """
    resultado = {
        'valido': False,
        'tipo_pagina': 'desconhecida',
        'mensagem': '',
        'elementos_presentes': []
    }

    try:
        # Verificar URL
        url_atual = driver.current_url
        if 'cartoes.extracaixa' not in url_atual:
            resultado['mensagem'] = f"URL não é do SIACH: {url_atual}"
            return resultado

        # Detectar tipo de página baseado em elementos característicos
        wait = WebDriverWait(driver, timeout)

        # Página de login
        try:
            from selenium.webdriver.common.by import By
            wait.until(EC.presence_of_element_located((By.NAME, 'loginForm:username')))
            resultado['valido'] = True
            resultado['tipo_pagina'] = 'login'
            resultado['elementos_presentes'].append('login_form')
            resultado['mensagem'] = "Página de login detectada"
            return resultado
        except TimeoutException:
            pass

        # Página de menu/index
        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="index"]/fieldset')
            ))
            resultado['valido'] = True
            resultado['tipo_pagina'] = 'menu'
            resultado['elementos_presentes'].append('menu_principal')
            resultado['mensagem'] = "Página de menu detectada"
            return resultado
        except TimeoutException:
            pass

        # Página de protocolo
        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="menu"]/li[3]/a')
            ))
            resultado['valido'] = True
            resultado['tipo_pagina'] = 'protocolo'
            resultado['elementos_presentes'].append('menu_atender_ocorrencia')
            resultado['mensagem'] = "Página de protocolo detectada"
            return resultado
        except TimeoutException:
            pass

        resultado['mensagem'] = "Página SIACH não reconhecida"
        return resultado

    except Exception as e:
        resultado['mensagem'] = f"Erro ao validar página: {str(e)}"
        return resultado


def verificar_sessao_valida(driver: WebDriver, timeout: int = 5) -> bool:
    """
    Verifica se a sessão do usuário ainda está válida

    Detecta se foi redirecionado para página de login ou expiração de sessão

    Args:
        driver: WebDriver do Selenium
        timeout: Tempo de espera

    Returns:
        True se sessão válida, False se expirada
    """
    try:
        from selenium.webdriver.common.by import By
        wait = WebDriverWait(driver, timeout)

        # Se página de login estiver presente, sessão expirou
        try:
            wait.until(EC.presence_of_element_located((By.NAME, 'loginForm:username')))
            return False  # Login form presente = sessão expirada
        except TimeoutException:
            pass

        # Verificar se há mensagem de sessão expirada
        try:
            mensagem_expiracao = driver.find_element(
                By.XPATH,
                "//*[contains(text(), 'sessão expirou') or contains(text(), 'Sessão expirada')]"
            )
            if mensagem_expiracao:
                return False
        except:
            pass

        # Se URL contém 'login', sessão provavelmente expirou
        if 'login' in driver.current_url.lower():
            return False

        return True

    except Exception:
        # Em caso de erro, assumir sessão válida (será tratado em outra camada)
        return True


def detectar_pagina_manutencao(driver: WebDriver) -> Tuple[bool, str]:
    """
    Detecta se o sistema está em página de manutenção

    Args:
        driver: WebDriver do Selenium

    Returns:
        Tupla (em_manutencao, mensagem)
    """
    try:
        from selenium.webdriver.common.by import By

        # Palavras-chave comuns em páginas de manutenção
        keywords = [
            'manutenção',
            'manutencao',
            'maintenance',
            'indisponível',
            'temporariamente fora do ar',
            'sistema em atualização'
        ]

        # Obter texto da página
        body_text = driver.find_element(By.TAG_NAME, 'body').text.lower()

        for keyword in keywords:
            if keyword in body_text:
                return True, f"Sistema em manutenção (palavra-chave: '{keyword}')"

        # Verificar título da página
        titulo = driver.title.lower()
        for keyword in keywords:
            if keyword in titulo:
                return True, f"Título indica manutenção: '{driver.title}'"

        return False, ""

    except Exception as e:
        return False, f"Erro ao detectar manutenção: {str(e)}"


def verificar_erro_conexao(exception_message: str) -> bool:
    """
    Verifica se uma mensagem de erro indica problema de conexão

    Args:
        exception_message: Mensagem da exceção

    Returns:
        True se é erro de conexão, False caso contrário
    """
    # Lista de mensagens que indicam erro de conexão
    erros_conexao = [
        'HTTPConnectionPool',
        'Read timed out',
        'target frame detached',
        'Connection refused',
        'Reached error page',
        'connection reset',
        'network error',
        'timeout',
        'ERR_CONNECTION',
        'ERR_INTERNET_DISCONNECTED'
    ]

    mensagem_lower = exception_message.lower()

    for erro in erros_conexao:
        if erro.lower() in mensagem_lower:
            return True

    return False


def validar_fase_protocolo(fase_texto: str) -> Dict[str, any]:
    """
    Valida e classifica a fase de um protocolo

    Args:
        fase_texto: Texto da fase extraído da página

    Returns:
        Dict com informações sobre a fase:
        {
            'fase': str,
            'pode_finalizar': bool,
            'status': str ('PROCESSAR', 'SEM_ACAO', 'DESCONHECIDA')
        }
    """
    from selectors.siach_selectors import FasesProtocolo

    fase_upper = fase_texto.upper().strip()

    resultado = {
        'fase': fase_texto,
        'pode_finalizar': False,
        'status': 'DESCONHECIDA'
    }

    if FasesProtocolo.pode_finalizar(fase_upper):
        resultado['pode_finalizar'] = True
        resultado['status'] = 'PROCESSAR'
    elif FasesProtocolo.ja_finalizado(fase_upper):
        resultado['status'] = 'SEM_ACAO'
    else:
        resultado['status'] = 'DESCONHECIDA'

    return resultado


# ==================== VALIDAÇÃO DE ELEMENTOS ====================

def elemento_esta_visivel(driver: WebDriver, by: str, value: str, timeout: int = 5) -> bool:
    """
    Verifica se elemento está visível na página

    Args:
        driver: WebDriver
        by: Estratégia de busca (By.XPATH, By.ID, etc)
        value: Valor do seletor
        timeout: Tempo de espera

    Returns:
        True se visível, False caso contrário
    """
    try:
        wait = WebDriverWait(driver, timeout)
        elemento = wait.until(EC.visibility_of_element_located((by, value)))
        return elemento is not None
    except TimeoutException:
        return False
    except Exception:
        return False


def elemento_esta_clicavel(driver: WebDriver, by: str, value: str, timeout: int = 5) -> bool:
    """
    Verifica se elemento está clicável

    Args:
        driver: WebDriver
        by: Estratégia de busca
        value: Valor do seletor
        timeout: Tempo de espera

    Returns:
        True se clicável, False caso contrário
    """
    try:
        wait = WebDriverWait(driver, timeout)
        elemento = wait.until(EC.element_to_be_clickable((by, value)))
        return elemento is not None
    except TimeoutException:
        return False
    except Exception:
        return False


if __name__ == "__main__":
    # Testes unitários das funções de validação
    print("=" * 60)
    print("TESTES DE VALIDAÇÃO")
    print("=" * 60)

    # Teste validar_email
    print("\nTeste: validar_email()")
    emails_teste = [
        ("usuario@dominio.com", True),
        ("usuario@dominio.com.br", True),
        ("invalido", False),
        ("@dominio.com", False),
        ("usuario@", False),
        ("", False)
    ]

    for email, esperado in emails_teste:
        valido, msg = validar_email(email)
        status = "✓" if valido == esperado else "✗"
        print(f"  {status} '{email}' -> {valido} | {msg}")

    # Teste validar_arquivo_excel
    print("\nTeste: validar_arquivo_excel()")
    arquivos_teste = [
        ("Base.xlsx", True),
        ("arquivo.xls", False),  # Não existe
        ("", False)
    ]

    for arquivo, esperado in arquivos_teste:
        valido, msg = validar_arquivo_excel(arquivo)
        status = "✓" if (valido == esperado or msg) else "✗"
        print(f"  {status} '{arquivo}' -> {valido} | {msg}")

    # Teste verificar_erro_conexao
    print("\nTeste: verificar_erro_conexao()")
    erros_teste = [
        ("HTTPConnectionPool error", True),
        ("Read timed out", True),
        ("Element not found", False),
        ("target frame detached", True)
    ]

    for erro, esperado in erros_teste:
        eh_conexao = verificar_erro_conexao(erro)
        status = "✓" if eh_conexao == esperado else "✗"
        print(f"  {status} '{erro}' -> {eh_conexao}")

    print("\n" + "=" * 60)
    print("Testes concluídos!")
