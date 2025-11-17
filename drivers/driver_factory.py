"""
Factory para criação de drivers

Cria drivers Chrome ou Firefox baseado em configuração
"""

from typing import Union, Optional
from .base_driver import BaseDriver
from .chrome_driver import ChromeDriver
from .firefox_driver import FirefoxDriver
from config.config import WallBotConfig, EnvConfig


class DriverFactory:
    """
    Factory para criar drivers de navegador

    Exemplo:
        factory = DriverFactory()
        driver = factory.criar_driver('chrome')
        # ou
        driver = factory.criar_driver()  # Usa configuração padrão
    """

    @staticmethod
    def criar_driver(
        navegador: Optional[str] = None,
        headless: bool = False,
        timeout: Optional[int] = None,
        **kwargs
    ) -> BaseDriver:
        """
        Cria driver baseado no navegador especificado

        Args:
            navegador: 'chrome' ou 'firefox' (None = usa config)
            headless: Executar sem interface gráfica
            timeout: Timeout em segundos (None = usa config)
            **kwargs: Argumentos adicionais específicos do driver

        Returns:
            BaseDriver configurado (ChromeDriver ou FirefoxDriver)

        Raises:
            ValueError: Se navegador não for suportado
        """
        # Determinar navegador
        if navegador is None:
            navegador = EnvConfig.get_navegador()

        navegador = navegador.lower().strip()

        # Determinar timeout
        if timeout is None:
            timeout = EnvConfig.get_timeout_padrao()

        # Criar driver apropriado
        if navegador == 'chrome':
            print(f"Criando Chrome driver (headless={headless}, timeout={timeout}s)")
            driver_instance = ChromeDriver()

        elif navegador == 'firefox':
            print(f"Criando Firefox driver (headless={headless}, timeout={timeout}s)")
            driver_instance = FirefoxDriver()

        else:
            raise ValueError(
                f"Navegador '{navegador}' não suportado. "
                f"Use 'chrome' ou 'firefox'"
            )

        # Configurar e criar
        driver_instance.criar(headless=headless, timeout=timeout, **kwargs)

        return driver_instance

    @staticmethod
    def navegadores_suportados() -> list:
        """
        Retorna lista de navegadores suportados

        Returns:
            Lista de strings com nomes dos navegadores
        """
        return ['chrome', 'firefox']


if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DRIVER FACTORY")
    print("=" * 60)

    # Listar navegadores suportados
    print("\nNavegadores suportados:")
    for nav in DriverFactory.navegadores_suportados():
        print(f"  - {nav}")

    # Testar criação de driver padrão
    print("\nCriando driver padrão (configuração)...")
    try:
        driver = DriverFactory.criar_driver()
        print(f"Driver criado: {driver.get_nome_navegador()}")
        driver.fechar_seguro()
    except Exception as e:
        print(f"Erro: {e}")

    print("\n" + "=" * 60)
