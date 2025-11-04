"""
Exemplo 01: Criar e Usar Driver

Demonstra como criar drivers Chrome e Firefox usando a nova arquitetura.
"""

from drivers import DriverFactory, ChromeDriver, FirefoxDriver


def exemplo_factory_chrome():
    """Exemplo usando Factory para criar Chrome"""
    print("=" * 60)
    print("EXEMPLO 1: Factory - Chrome")
    print("=" * 60)

    # Criar driver Chrome usando Factory
    driver_wrapper = DriverFactory.criar_driver('chrome')
    driver = driver_wrapper.driver

    # Usar o driver
    driver.get('https://www.google.com')
    print(f"Título da página: {driver.title}")
    print(f"URL atual: {driver.current_url}")

    # Fechar
    driver_wrapper.fechar_seguro()
    print("Driver Chrome fechado com sucesso!\n")


def exemplo_factory_firefox():
    """Exemplo usando Factory para criar Firefox"""
    print("=" * 60)
    print("EXEMPLO 2: Factory - Firefox")
    print("=" * 60)

    # Criar driver Firefox usando Factory
    driver_wrapper = DriverFactory.criar_driver('firefox')
    driver = driver_wrapper.driver

    # Usar o driver
    driver.get('https://www.google.com')
    print(f"Título da página: {driver.title}")
    print(f"URL atual: {driver.current_url}")

    # Fechar (Firefox usa delay de 3s)
    driver_wrapper.fechar_seguro()
    print("Driver Firefox fechado com sucesso!\n")


def exemplo_instancia_direta():
    """Exemplo criando instância direta de ChromeDriver"""
    print("=" * 60)
    print("EXEMPLO 3: Instância Direta")
    print("=" * 60)

    # Criar instância direta
    driver_wrapper = ChromeDriver()
    driver = driver_wrapper.criar(headless=False, timeout=15)

    # Usar o driver
    driver.get('https://www.google.com')
    print(f"Título da página: {driver.title}")

    # Fechar
    driver_wrapper.fechar_seguro()
    print("Driver fechado com sucesso!\n")


def exemplo_context_manager():
    """Exemplo usando context manager (with statement)"""
    print("=" * 60)
    print("EXEMPLO 4: Context Manager")
    print("=" * 60)

    # Usar context manager (fecha automaticamente)
    with ChromeDriver() as driver_wrapper:
        driver = driver_wrapper.criar()
        driver.get('https://www.google.com')
        print(f"Título da página: {driver.title}")

    # Driver fechado automaticamente
    print("Driver fechado automaticamente pelo context manager!\n")


def exemplo_headless():
    """Exemplo em modo headless (sem interface gráfica)"""
    print("=" * 60)
    print("EXEMPLO 5: Modo Headless")
    print("=" * 60)

    # Criar driver em modo headless
    driver_wrapper = ChromeDriver()
    driver = driver_wrapper.criar(headless=True)

    print("Driver criado em modo headless (sem janela visível)")

    # Usar o driver
    driver.get('https://www.google.com')
    print(f"Título da página: {driver.title}")

    # Fechar
    driver_wrapper.fechar_seguro()
    print("Driver fechado!\n")


def exemplo_timeout_customizado():
    """Exemplo com timeout customizado"""
    print("=" * 60)
    print("EXEMPLO 6: Timeout Customizado")
    print("=" * 60)

    # Criar driver com timeout de 30 segundos
    driver_wrapper = DriverFactory.criar_driver(
        navegador='chrome',
        timeout=30
    )

    print("Driver criado com timeout de 30 segundos")

    driver = driver_wrapper.driver
    driver.get('https://www.google.com')
    print(f"Título: {driver.title}")

    driver_wrapper.fechar_seguro()
    print("Driver fechado!\n")


if __name__ == "__main__":
    print("\n" + "🚀 EXEMPLOS DE CRIAÇÃO DE DRIVERS".center(60))
    print()

    # Executar exemplos
    try:
        exemplo_factory_chrome()
        # exemplo_factory_firefox()  # Descomente se tiver Firefox instalado
        exemplo_instancia_direta()
        exemplo_context_manager()
        exemplo_headless()
        exemplo_timeout_customizado()

        print("=" * 60)
        print("✅ Todos os exemplos executados com sucesso!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        print("\nDica: Verifique se Chrome está instalado e requirements.txt foi instalado.")
