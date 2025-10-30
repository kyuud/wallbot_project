"""
Chrome Driver para WallBot SIACH v3.0.0

Implementação do driver Chrome com otimizações
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from .base_driver import BaseDriver
from typing import Optional


class ChromeDriver(BaseDriver):
    """
    Driver Chrome otimizado para WallBot SIACH

    Features:
    - Configuração automática do ChromeDriver
    - Otimizações de performance
    - Modo headless opcional
    - Desativação de automação detectável
    """

    def __init__(self):
        super().__init__()
        self.options: Optional[ChromeOptions] = None

    def configurar_opcoes(
        self,
        headless: bool = False,
        desabilitar_gpu: bool = True,
        desabilitar_notificacoes: bool = True,
        **kwargs
    ) -> ChromeOptions:
        """
        Configura opções do Chrome

        Args:
            headless: Executar sem interface gráfica
            desabilitar_gpu: Desabilitar aceleração GPU
            desabilitar_notificacoes: Desabilitar notificações do navegador
            **kwargs: Argumentos adicionais

        Returns:
            ChromeOptions configurado
        """
        options = ChromeOptions()

        # Tamanho da janela
        options.add_argument(f'--window-size={self._window_width},{self._window_height}')

        # Modo headless (opcional)
        if headless:
            options.add_argument('--headless=new')  # Novo modo headless do Chrome

        # Desabilitar GPU (útil em ambientes de servidor)
        if desabilitar_gpu:
            options.add_argument('--disable-gpu')

        # Desabilitar notificações
        if desabilitar_notificacoes:
            options.add_argument('--disable-notifications')

        # Otimizações de performance
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Desabilitar extensões
        options.add_argument('--disable-extensions')

        # Desabilitar automação detectável
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        # Preferências adicionais
        prefs = {
            'profile.default_content_setting_values.notifications': 2,  # Bloquear notificações
            'profile.default_content_settings.popups': 0,  # Permitir popups (para SIACH)
            'download.prompt_for_download': False,  # Download automático
            'credentials_enable_service': False,  # Não salvar senhas
            'profile.password_manager_enabled': False  # Desabilitar gerenciador de senhas
        }
        options.add_experimental_option('prefs', prefs)

        # Argumentos customizados do usuário
        custom_args = kwargs.get('custom_arguments', [])
        for arg in custom_args:
            options.add_argument(arg)

        self.options = options
        return options

    def criar(
        self,
        headless: bool = False,
        timeout: Optional[int] = None,
        **kwargs
    ) -> webdriver.Chrome:
        """
        Cria e configura driver Chrome

        Args:
            headless: Executar em modo headless
            timeout: Timeout padrão em segundos
            **kwargs: Argumentos adicionais

        Returns:
            WebDriver Chrome configurado

        Raises:
            Exception: Se houver erro na criação
        """
        try:
            print("Inicializando Chrome...")

            # Configurar opções
            if not self.options:
                self.configurar_opcoes(headless=headless, **kwargs)

            # Criar serviço
            service = ChromeService(ChromeDriverManager().install())

            # Criar driver
            self.driver = webdriver.Chrome(service=service, options=self.options)

            # Configurar timeouts
            timeout_final = timeout or self._timeout_padrao
            self.set_timeout_padrao(timeout_final)

            # Configurar janela
            self.driver.set_window_size(self._window_width, self._window_height)

            print(f"Chrome iniciado com sucesso (Timeout: {timeout_final}s)")
            return self.driver

        except Exception as e:
            print(f"Erro ao criar Chrome driver: {e}")
            raise

    def get_nome_navegador(self) -> str:
        """
        Retorna nome do navegador

        Returns:
            'Chrome'
        """
        return "Chrome"

    def configurar_modo_stealth(self) -> None:
        """
        Configura modo stealth para evitar detecção de automação

        Executa scripts para mascarar propriedades do WebDriver
        """
        if not self.driver:
            raise RuntimeError("Driver não inicializado")

        # Script para remover propriedades que detectam WebDriver
        stealth_script = """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });

        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });

        Object.defineProperty(navigator, 'languages', {
            get: () => ['pt-BR', 'pt', 'en-US', 'en']
        });

        window.chrome = {
            runtime: {}
        };
        """

        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': stealth_script
        })

        print("Modo stealth ativado no Chrome")


if __name__ == "__main__":
    # Teste do Chrome Driver
    print("=" * 60)
    print("TESTE CHROME DRIVER")
    print("=" * 60)

    try:
        # Criar driver com context manager
        with ChromeDriver() as chrome:
            driver = chrome.criar(headless=False, timeout=15)

            print("\nTestando abertura de página...")
            sucesso = chrome.abrir_url("https://www.google.com", timeout=10)

            if sucesso:
                print(f"Título da página: {driver.title}")
                print(f"URL atual: {driver.current_url}")

            print("\nAplicando zoom...")
            chrome.aplicar_zoom('0.67')

            import time
            time.sleep(2)

            print("\nTeste concluído com sucesso!")

    except Exception as e:
        print(f"\nErro durante teste: {e}")

    print("\n" + "=" * 60)
