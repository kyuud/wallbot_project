"""
Seletores do Sistema SIACH

Centraliza todos os XPaths e seletores usados para interagir com
as páginas do sistema SIACH da Caixa.

Organização:
- LOGIN: Elementos da página de login
- MENU: Navegação e menu principal
- FORMULARIO: Campos de formulário de entrada
- PROTOCOLO: Elementos de protocolo/ocorrência
- FINALIZACAO: Elementos da tela de finalização
- CLIENTE: Dados do cliente
"""

from selenium.webdriver.common.by import By
from typing import Tuple


class SIACHSelectors:
    """
    Classe que centraliza todos os seletores do sistema SIACH.

    Cada seletor retorna uma tupla (By.ESTRATEGIA, "valor") para uso
    direto com WebDriver.find_element()

    Exemplo:
        driver.find_element(*SIACHSelectors.LOGIN_BUTTON)
    """

    # ==================== LOGIN ====================

    # Campos de entrada de credenciais
    LOGIN_USERNAME: Tuple[str, str] = (By.NAME, 'loginForm:username')
    LOGIN_PASSWORD: Tuple[str, str] = (By.NAME, 'loginForm:password')

    # Botão de envio do formulário de login
    LOGIN_BUTTON: Tuple[str, str] = (
        By.XPATH,
        '//*[@id="loginForm"]/div/div/input'
    )

    # ==================== MENU E NAVEGAÇÃO ====================

    # Link para acessar o módulo SIACH a partir do menu principal
    MENU_SIACH_MODULE: Tuple[str, str] = (
        By.XPATH,
        '//*[@id="index"]/fieldset/div[1]/table/tbody/tr[1]/td[2]/a'
    )

    # Menu "Atender Ocorrência"
    MENU_ATENDER_OCORRENCIA: Tuple[str, str] = (
        By.XPATH,
        '//*[@id="menu"]/li[3]/a'
    )

    # ==================== FORMULÁRIO DE BUSCA ====================

    # Campo de entrada para PROTOCOLO
    FORM_PROTOCOLO_INPUT: Tuple[str, str] = (
        By.XPATH,
        '/html/body/div[2]/div/div/div[2]/div[1]/form/div[1]/div[1]/div[3]/div/input'
    )

    # Campo de entrada para OCORRÊNCIA
    FORM_OCORRENCIA_INPUT: Tuple[str, str] = (
        By.XPATH,
        '/html/body/div[2]/div/div/div[2]/div[1]/form/div[1]/div[1]/div[2]/div/input'
    )

    # Botão "Consultar" para buscar protocolo/ocorrência
    FORM_CONSULTAR_BUTTON: Tuple[str, str] = (
        By.XPATH,
        '/html/body/div[2]/div/div/div[2]/div[1]/form/div[2]/a[1]'
    )

    # ==================== PROTOCOLO/OCORRÊNCIA ====================

    # Elemento que exibe a fase atual do protocolo
    PROTOCOLO_FASE_TEXT: Tuple[str, str] = (
        By.XPATH,
        '/html/body/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div/table/tbody/tr/td/div/div[1]/div/div[2]/p[3]/span'
    )

    # Seletor alternativo para fase (usado em retry de StaleElement)
    PROTOCOLO_FASE_TEXT_RETRY: Tuple[str, str] = PROTOCOLO_FASE_TEXT

    # ==================== DADOS DO CLIENTE ====================

    # Nome do cliente (seletor primário)
    CLIENTE_NOME_PRIMARY: Tuple[str, str] = (
        By.XPATH,
        '//*[@id="dados_cliente_2"]/div/div[2]/span'
    )

    # Nome do cliente (seletor alternativo/fallback)
    CLIENTE_NOME_FALLBACK: Tuple[str, str] = (
        By.XPATH,
        '/html/body/div[2]/div/div/div[6]/div/div[2]/fieldset[2]/div[2]/div[1]/div/div[2]/span'
    )

    # ==================== FINALIZAÇÃO ====================

    # Botão de lupa/magnifier para visualizar detalhes da ocorrência
    FINALIZACAO_DETALHE_BUTTON: Tuple[str, str] = (
        By.XPATH,
        '//*[@id="detalhe_ocorrencia"]/span'
    )

    # Botão "Finalizar" protocolo/ocorrência
    FINALIZACAO_FINALIZAR_BUTTON: Tuple[str, str] = (
        By.XPATH,
        '//*[@id="content"]/div/div[6]/div/div[3]/form/a[6]'
    )

    # Campo "Justificativa"
    FINALIZACAO_JUSTIFICATIVA_INPUT: Tuple[str, str] = (
        By.XPATH,
        '/html/body/div[2]/div/div/div[2]/div[1]/form/div[1]/fieldset[1]/div/div[2]/div/input'
    )

    # Campo "Resposta ao Cliente"
    FINALIZACAO_RESPOSTA_CLIENTE_INPUT: Tuple[str, str] = (
        By.XPATH,
        '/html/body/div[2]/div/div/div[2]/div[1]/form/div[1]/fieldset[1]/div/div[4]/div/textarea'
    )

    # Campo "Informação Técnica"
    FINALIZACAO_INFO_TECNICA_INPUT: Tuple[str, str] = (
        By.XPATH,
        '/html/body/div[2]/div/div/div[2]/div[1]/form/div[1]/fieldset[1]/div/div[7]/div/textarea'
    )

    # Botão "Salvar" (Angular data-ng-click)
    FINALIZACAO_SALVAR_BUTTON: Tuple[str, str] = (
        By.XPATH,
        "//a[@data-ng-click='tratarOcorrenciaCtrl.form.submit()']"
    )

    # Botão de confirmação na modal (CSS Selector)
    FINALIZACAO_CONFIRMAR_BUTTON: Tuple[str, str] = (
        By.CSS_SELECTOR,
        'button.btn.btn-default'
    )

    # ==================== MÉTODOS AUXILIARES ====================

    @staticmethod
    def get_selector(selector_tuple: Tuple[str, str]) -> Tuple[str, str]:
        """
        Retorna o seletor como tupla (By, valor)

        Args:
            selector_tuple: Tupla com estratégia e valor do seletor

        Returns:
            Tupla (By.ESTRATEGIA, "valor") pronta para uso
        """
        return selector_tuple

    @classmethod
    def validate_selectors(cls) -> dict:
        """
        Valida que todos os seletores estão no formato correto

        Returns:
            Dict com resultado da validação:
            {
                'valid': bool,
                'total': int,
                'errors': list
            }
        """
        errors = []
        valid_strategies = {By.XPATH, By.CSS_SELECTOR, By.ID, By.NAME, By.CLASS_NAME}

        selectors = {
            name: value for name, value in vars(cls).items()
            if not name.startswith('_') and isinstance(value, tuple)
        }

        for name, selector in selectors.items():
            if len(selector) != 2:
                errors.append(f"{name}: deve ter exatamente 2 elementos")
                continue

            strategy, value = selector

            if strategy not in valid_strategies:
                errors.append(f"{name}: estratégia '{strategy}' inválida")

            if not isinstance(value, str) or not value.strip():
                errors.append(f"{name}: valor do seletor deve ser string não-vazia")

        return {
            'valid': len(errors) == 0,
            'total': len(selectors),
            'errors': errors
        }

    @classmethod
    def print_selectors(cls) -> None:
        """
        Imprime todos os seletores organizados por categoria
        """
        print("=" * 60)
        print("SELETORES SIACH - WallBot v3.0.0")
        print("=" * 60)

        categories = {
            'LOGIN': [],
            'MENU': [],
            'FORM': [],
            'PROTOCOLO': [],
            'CLIENTE': [],
            'FINALIZACAO': []
        }

        for name, value in vars(cls).items():
            if not name.startswith('_') and isinstance(value, tuple):
                for category in categories:
                    if name.startswith(category):
                        categories[category].append((name, value))
                        break

        for category, selectors in categories.items():
            if selectors:
                print(f"\n{category}:")
                print("-" * 60)
                for name, (strategy, value) in selectors:
                    print(f"  {name}")
                    print(f"    Estratégia: {strategy}")
                    print(f"    Valor: {value[:50]}..." if len(value) > 50 else f"    Valor: {value}")

        print("\n" + "=" * 60)


# ==================== FASES VÁLIDAS ====================

class FasesProtocolo:
    """
    Enumeração das fases válidas de um protocolo no SIACH
    """
    # Fases que permitem finalização
    ABERTA = "ABERTA"
    EM_ANDAMENTO = "EM ANDAMENTO"

    # Fases que NÃO permitem ação
    REABERTA = "REABERTA"
    FINALIZADA = "FINALIZADA"

    # Lista de fases processáveis
    PROCESSAVEIS = [ABERTA, EM_ANDAMENTO]
    SEM_ACAO = [REABERTA, FINALIZADA]

    @classmethod
    def pode_finalizar(cls, fase: str) -> bool:
        """
        Verifica se uma fase permite finalização

        Args:
            fase: Texto da fase do protocolo

        Returns:
            True se pode finalizar, False caso contrário
        """
        return fase.upper() in cls.PROCESSAVEIS

    @classmethod
    def ja_finalizado(cls, fase: str) -> bool:
        """
        Verifica se protocolo já foi finalizado

        Args:
            fase: Texto da fase do protocolo

        Returns:
            True se já finalizado, False caso contrário
        """
        return fase.upper() in cls.SEM_ACAO


if __name__ == "__main__":
    # Testes e validação dos seletores
    print("Validando seletores...")
    result = SIACHSelectors.validate_selectors()

    print(f"\nTotal de seletores: {result['total']}")
    print(f"Válidos: {result['valid']}")

    if result['errors']:
        print("\nErros encontrados:")
        for error in result['errors']:
            print(f"  - {error}")
    else:
        print("\nTodos os seletores estão válidos!")

    print("\n")
    SIACHSelectors.print_selectors()

    # Testar fases
    print("\n\nTestando FasesProtocolo:")
    print(f"'ABERTA' pode finalizar? {FasesProtocolo.pode_finalizar('ABERTA')}")
    print(f"'FINALIZADA' pode finalizar? {FasesProtocolo.pode_finalizar('FINALIZADA')}")
    print(f"'REABERTA' já finalizado? {FasesProtocolo.ja_finalizado('REABERTA')}")
