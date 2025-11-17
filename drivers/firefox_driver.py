"""
Firefox Driver para WallBot SIACH v2.1.0 (Legacy)

Mantém compatibilidade com versão 2.1.0
"""

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from .base_driver import BaseDriver
from typing import Optional


class FirefoxDriver(BaseDriver):
    """
    Driver Firefox (Legacy - v2.1.0)

    Mantido para compatibilidade com versão anterior
    """

    def __init__(self):
        super().__init__()
        self.options: Optional[FirefoxOptions] = None

    def configurar_opcoes(
        self,
        headless: bool = False,
        **kwargs
    ) -> FirefoxOptions:
        """
        Configura opções do Firefox

        Args:
            headless: Executar sem interface gráfica
            **kwargs: Argumentos adicionais

        Returns:
            FirefoxOptions configurado
        """
        options = FirefoxOptions()

        # Tamanho da janela
        options.add_argument(f'--width={self._window_width}')
        options.add_argument(f'--height={self._window_height}')

        # Modo headless
        if headless:
            options.add_argument('--headless')

        # Preferências Firefox (equivalente às do v2.1.0)
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        options.set_preference("network.http.connection-timeout", 90)
        options.set_preference("network.http.response.timeout", 90)

        self.options = options
        return options

    def criar(
        self,
        headless: bool = False,
        timeout: Optional[int] = None,
        **kwargs
    ) -> webdriver.Firefox:
        """
        Cria e configura driver Firefox

        Args:
            headless: Executar em modo headless
            timeout: Timeout padrão
            **kwargs: Argumentos adicionais

        Returns:
            WebDriver Firefox configurado
        """
        try:
            print("Inicializando Firefox...")

            if not self.options:
                self.configurar_opcoes(headless=headless, **kwargs)

            service = FirefoxService(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=service, options=self.options)

            timeout_final = timeout or self._timeout_padrao
            self.set_timeout_padrao(timeout_final)

            self.driver.set_window_size(self._window_width, self._window_height)

            print(f"Firefox iniciado com sucesso (Timeout: {timeout_final}s)")
            return self.driver

        except Exception as e:
            print(f"Erro ao criar Firefox driver: {e}")
            raise

    def get_nome_navegador(self) -> str:
        """Retorna 'Firefox'"""
        return "Firefox"

    def fechar_seguro(self, delay: int = 3) -> bool:
        """
        Fecha Firefox com delay maior (herança de v2.1.0)

        Firefox precisa de mais tempo para fechar completamente
        """
        return super().fechar_seguro(delay=delay)
