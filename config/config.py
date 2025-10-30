"""
Configurações do WallBot SIACH v3.0.0

Centraliza todas as configurações do sistema.
"""

import os
from typing import Dict, Any


class WallBotConfig:
    """
    Classe de configuração centralizada para WallBot SIACH
    """

    # ==================== URLs ====================
    URL_SIPCS = 'https://cartoes.extracaixa/'

    # ==================== ARQUIVOS ====================
    ARQUIVO_PROGRESSO = 'progresso.txt'
    ARQUIVO_LOG = 'log_output.txt'
    ARQUIVO_RESULTADO = 'resultado_saida.xlsx'
    NOME_ABA_EXCEL = 'Planilha1'

    # ==================== NAVEGADOR ====================
    ZOOM_NIVEL = '0.67'
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080

    # Navegador padrão ('chrome' ou 'firefox')
    NAVEGADOR_PADRAO = 'chrome'

    # ==================== TIMEOUTS ====================
    TIMEOUT_PADRAO = 15  # segundos
    TIMEOUT_SALVAR = 30  # segundos
    TIMEOUT_SCRIPT = 60  # segundos (novo em v3.0.0)
    TIMEOUT_PAGINA = 45  # segundos (novo em v3.0.0)

    # ==================== RECONEXÃO ====================
    MAX_TENTATIVAS_RECONEXAO = 3
    ESPERA_ENTRE_TENTATIVAS = 2.0  # segundos
    ESPERA_ENTRE_ACOES = 1.0  # segundos

    # ==================== LOGGING ====================
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    # ==================== PERFORMANCE ====================
    # Limitar tentativas de StaleElement
    MAX_TENTATIVAS_STALE_ELEMENT = 3

    # Delay para fechamento do driver (segundos)
    DELAY_FECHAR_DRIVER = 1  # Reduzido de 3s para 1s (Chrome é mais rápido)

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """
        Retorna todas as configurações como dicionário

        Returns:
            Dict com todas as configurações públicas
        """
        return {
            key: value for key, value in vars(cls).items()
            if not key.startswith('_') and not callable(value)
        }

    @classmethod
    def print_config(cls) -> None:
        """
        Imprime todas as configurações
        """
        print("=" * 60)
        print("CONFIGURAÇÕES WALLBOT v3.0.0")
        print("=" * 60)

        categorias = {
            'URLs': ['URL_'],
            'Arquivos': ['ARQUIVO_', 'NOME_ABA'],
            'Navegador': ['ZOOM_', 'WINDOW_', 'NAVEGADOR_'],
            'Timeouts': ['TIMEOUT_', 'ESPERA_'],
            'Reconexão': ['MAX_TENTATIVAS', 'ESPERA_'],
            'Logging': ['LOG_'],
            'Performance': ['MAX_', 'DELAY_']
        }

        configs = cls.to_dict()

        for categoria, prefixos in categorias.items():
            print(f"\n{categoria}:")
            print("-" * 60)
            for key, value in configs.items():
                if any(key.startswith(p) for p in prefixos):
                    print(f"  {key}: {value}")

        print("\n" + "=" * 60)

    @classmethod
    def validar_config(cls) -> Dict[str, Any]:
        """
        Valida as configurações

        Returns:
            Dict com resultado da validação
        """
        erros = []

        # Validar URLs
        if not cls.URL_SIPCS.startswith('http'):
            erros.append("URL_SIPCS deve começar com http:// ou https://")

        # Validar timeouts
        if cls.TIMEOUT_PADRAO <= 0:
            erros.append("TIMEOUT_PADRAO deve ser maior que 0")

        if cls.TIMEOUT_SALVAR < cls.TIMEOUT_PADRAO:
            erros.append("TIMEOUT_SALVAR deve ser >= TIMEOUT_PADRAO")

        # Validar navegador
        if cls.NAVEGADOR_PADRAO not in ['chrome', 'firefox']:
            erros.append("NAVEGADOR_PADRAO deve ser 'chrome' ou 'firefox'")

        # Validar reconexão
        if cls.MAX_TENTATIVAS_RECONEXAO < 1:
            erros.append("MAX_TENTATIVAS_RECONEXAO deve ser >= 1")

        return {
            'valido': len(erros) == 0,
            'erros': erros
        }


# ==================== CONFIGURAÇÕES DE AMBIENTE ====================

class EnvConfig:
    """
    Configurações que podem ser sobrescritas por variáveis de ambiente
    """

    @staticmethod
    def get_navegador() -> str:
        """
        Retorna o navegador configurado (env ou config padrão)

        Returns:
            'chrome' ou 'firefox'
        """
        return os.getenv('WALLBOT_NAVEGADOR', WallBotConfig.NAVEGADOR_PADRAO).lower()

    @staticmethod
    def get_timeout_padrao() -> int:
        """
        Retorna timeout padrão (env ou config padrão)

        Returns:
            Timeout em segundos
        """
        try:
            return int(os.getenv('WALLBOT_TIMEOUT', str(WallBotConfig.TIMEOUT_PADRAO)))
        except ValueError:
            return WallBotConfig.TIMEOUT_PADRAO

    @staticmethod
    def get_max_tentativas_reconexao() -> int:
        """
        Retorna max tentativas de reconexão (env ou config padrão)

        Returns:
            Número de tentativas
        """
        try:
            return int(os.getenv('WALLBOT_MAX_RECONEXAO', str(WallBotConfig.MAX_TENTATIVAS_RECONEXAO)))
        except ValueError:
            return WallBotConfig.MAX_TENTATIVAS_RECONEXAO

    @staticmethod
    def is_debug_mode() -> bool:
        """
        Verifica se está em modo debug

        Returns:
            True se debug ativado
        """
        return os.getenv('WALLBOT_DEBUG', 'false').lower() in ['true', '1', 'yes']


if __name__ == "__main__":
    # Testes
    print("Validando configurações...")
    resultado = WallBotConfig.validar_config()

    print(f"\nVálido: {resultado['valido']}")

    if resultado['erros']:
        print("\nErros encontrados:")
        for erro in resultado['erros']:
            print(f"  - {erro}")
    else:
        print("\nConfiguração válida!")

    print("\n")
    WallBotConfig.print_config()

    print("\n\nConfiguração de Ambiente:")
    print(f"  Navegador: {EnvConfig.get_navegador()}")
    print(f"  Timeout: {EnvConfig.get_timeout_padrao()}s")
    print(f"  Max Reconexão: {EnvConfig.get_max_tentativas_reconexao()}")
    print(f"  Debug: {EnvConfig.is_debug_mode()}")
