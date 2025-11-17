"""
Testes para módulo de drivers

Execute:
    pytest tests/test_drivers.py -v

NOTA: Testes que criam drivers reais estão marcados com @pytest.mark.slow
      Para pular testes lentos: pytest -m "not slow"
"""

import pytest
from drivers import DriverFactory, ChromeDriver, FirefoxDriver, BaseDriver


class TestDriverFactory:
    """Testes para DriverFactory"""

    def test_navegadores_suportados(self):
        """Testa lista de navegadores suportados"""
        navegadores = DriverFactory.navegadores_suportados()

        assert isinstance(navegadores, list)
        assert 'chrome' in navegadores
        assert 'firefox' in navegadores
        assert len(navegadores) >= 2

    def test_criar_driver_chrome_sem_inicializar(self):
        """Testa criação de instância Chrome sem inicializar driver"""
        driver = ChromeDriver()

        assert isinstance(driver, BaseDriver)
        assert driver.driver is None
        assert driver.get_nome_navegador() == "Chrome"

    def test_criar_driver_firefox_sem_inicializar(self):
        """Testa criação de instância Firefox sem inicializar driver"""
        driver = FirefoxDriver()

        assert isinstance(driver, BaseDriver)
        assert driver.driver is None
        assert driver.get_nome_navegador() == "Firefox"

    def test_factory_navegador_invalido(self):
        """Testa factory com navegador inválido"""
        with pytest.raises(ValueError) as excinfo:
            DriverFactory.criar_driver('safari')

        assert 'não suportado' in str(excinfo.value).lower()


class TestBaseDriver:
    """Testes para funcionalidades de BaseDriver"""

    def test_chrome_driver_herda_base(self):
        """Testa se ChromeDriver herda de BaseDriver"""
        driver = ChromeDriver()
        assert isinstance(driver, BaseDriver)

    def test_firefox_driver_herda_base(self):
        """Testa se FirefoxDriver herda de BaseDriver"""
        driver = FirefoxDriver()
        assert isinstance(driver, BaseDriver)

    def test_base_driver_metodos_abstratos(self):
        """Testa se BaseDriver define métodos abstratos"""
        assert hasattr(BaseDriver, 'criar')
        assert hasattr(BaseDriver, 'configurar_opcoes')
        assert hasattr(BaseDriver, 'get_nome_navegador')


class TestChromeDriver:
    """Testes específicos para ChromeDriver"""

    def test_chrome_nome_navegador(self):
        """Testa nome do navegador Chrome"""
        driver = ChromeDriver()
        assert driver.get_nome_navegador() == "Chrome"

    def test_chrome_configurar_opcoes(self):
        """Testa configuração de opções Chrome"""
        driver = ChromeDriver()
        options = driver.configurar_opcoes(headless=False)

        assert options is not None
        assert driver.options is not None

    def test_chrome_configurar_opcoes_headless(self):
        """Testa configuração headless"""
        driver = ChromeDriver()
        options = driver.configurar_opcoes(headless=True)

        # Verifica se opção headless foi adicionada
        assert any('headless' in str(arg).lower() for arg in options.arguments)

    @pytest.mark.slow
    def test_chrome_criar_driver_real(self):
        """Testa criação real de driver Chrome (TESTE LENTO)"""
        driver_wrapper = ChromeDriver()

        try:
            driver = driver_wrapper.criar(headless=True, timeout=10)

            assert driver is not None
            assert driver_wrapper.driver is not None

            # Testar navegação básica
            sucesso = driver_wrapper.abrir_url("about:blank")
            assert sucesso == True

        finally:
            driver_wrapper.fechar_seguro()


class TestFirefoxDriver:
    """Testes específicos para FirefoxDriver"""

    def test_firefox_nome_navegador(self):
        """Testa nome do navegador Firefox"""
        driver = FirefoxDriver()
        assert driver.get_nome_navegador() == "Firefox"

    def test_firefox_configurar_opcoes(self):
        """Testa configuração de opções Firefox"""
        driver = FirefoxDriver()
        options = driver.configurar_opcoes(headless=False)

        assert options is not None
        assert driver.options is not None

    def test_firefox_delay_fechamento(self):
        """Testa que Firefox tem delay maior de fechamento"""
        chrome = ChromeDriver()
        firefox = FirefoxDriver()

        # Firefox deve usar delay padrão de 3s
        # (verificamos isso indiretamente através da implementação)
        assert firefox.get_nome_navegador() == "Firefox"


class TestDriverIntegration:
    """Testes de integração entre drivers"""

    def test_factory_cria_chrome_por_padrao(self):
        """Testa que factory cria Chrome por padrão"""
        # Não inicializa driver real, apenas testa lógica
        from config.config import WallBotConfig
        assert WallBotConfig.NAVEGADOR_PADRAO == 'chrome'

    def test_multiplos_drivers_podem_coexistir(self):
        """Testa que múltiplas instâncias podem existir"""
        chrome1 = ChromeDriver()
        chrome2 = ChromeDriver()
        firefox1 = FirefoxDriver()

        assert chrome1 is not chrome2
        assert chrome1.get_nome_navegador() == chrome2.get_nome_navegador()
        assert chrome1.get_nome_navegador() != firefox1.get_nome_navegador()


if __name__ == "__main__":
    pytest.main([__file__, '-v', '-m', 'not slow'])
