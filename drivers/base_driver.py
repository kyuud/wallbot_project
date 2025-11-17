"""
Base Driver abstrato para WallBot SIACH

Define interface comum para drivers Firefox e Chrome
"""

from abc import ABC, abstractmethod
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Optional
import time


class BaseDriver(ABC):
    """
    Classe base abstrata para drivers de navegador

    Define métodos que devem ser implementados por drivers concretos
    """

    def __init__(self):
        self.driver: Optional[WebDriver] = None
        self._timeout_padrao = 15
        self._window_width = 1920
        self._window_height = 1080

    @abstractmethod
    def criar(self, **kwargs) -> WebDriver:
        """
        Cria e configura o WebDriver

        Args:
            **kwargs: Argumentos específicos do driver

        Returns:
            WebDriver configurado

        Raises:
            Exception: Se houver erro na criação
        """
        pass

    @abstractmethod
    def configurar_opcoes(self, **kwargs) -> any:
        """
        Configura opções específicas do navegador

        Args:
            **kwargs: Opções específicas

        Returns:
            Objeto Options configurado
        """
        pass

    def aplicar_zoom(self, nivel_zoom: str = '0.67') -> None:
        """
        Aplica nível de zoom à página

        Args:
            nivel_zoom: Nível de zoom (ex: '0.67', '0.80')
        """
        if self.driver:
            self.driver.execute_script(f"document.body.style.zoom='{nivel_zoom}'")

    def fechar_seguro(self, delay: int = 1) -> bool:
        """
        Fecha o driver de forma segura

        Args:
            delay: Segundos de espera antes de fechar (padrão: 1s)

        Returns:
            True se fechou com sucesso, False caso contrário
        """
        if not self.driver:
            return True

        try:
            print(f"Fechando {self.get_nome_navegador()}...")
            time.sleep(delay)

            self.driver.quit()
            self.driver = None

            print(f"{self.get_nome_navegador()} fechado com sucesso")
            return True

        except Exception as e:
            print(f"Erro ao fechar {self.get_nome_navegador()}: {e}")
            self.driver = None
            return False

    @abstractmethod
    def get_nome_navegador(self) -> str:
        """
        Retorna nome do navegador

        Returns:
            Nome do navegador ('Chrome', 'Firefox', etc)
        """
        pass

    def configurar_tamanho_janela(self, width: int, height: int) -> None:
        """
        Configura tamanho da janela do navegador

        Args:
            width: Largura em pixels
            height: Altura em pixels
        """
        self._window_width = width
        self._window_height = height

        if self.driver:
            self.driver.set_window_size(width, height)

    def set_timeout_padrao(self, timeout: int) -> None:
        """
        Define timeout padrão para o driver

        Args:
            timeout: Timeout em segundos
        """
        self._timeout_padrao = timeout

        if self.driver:
            self.driver.set_page_load_timeout(timeout)
            self.driver.set_script_timeout(timeout)

    def maximizar_janela(self) -> None:
        """Maximiza a janela do navegador"""
        if self.driver:
            self.driver.maximize_window()

    def abrir_url(self, url: str, timeout: Optional[int] = None) -> bool:
        """
        Abre URL com tratamento de erro

        Args:
            url: URL a ser aberta
            timeout: Timeout opcional (usa padrão se None)

        Returns:
            True se sucesso, False caso contrário
        """
        if not self.driver:
            raise RuntimeError("Driver não inicializado")

        try:
            if timeout:
                self.driver.set_page_load_timeout(timeout)

            self.driver.get(url)
            return True

        except Exception as e:
            print(f"Erro ao abrir URL {url}: {e}")
            return False

    def __enter__(self):
        """Context manager: entrada"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager: saída"""
        self.fechar_seguro()
        return False
