"""
Exemplo 02: Usar Seletores Centralizados

Demonstra como usar SIACHSelectors para localizar elementos.
"""

from drivers import DriverFactory
from selectors import SIACHSelectors
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def exemplo_seletores_basicos():
    """Demonstra uso básico de seletores"""
    print("=" * 60)
    print("EXEMPLO 1: Seletores Básicos")
    print("=" * 60)

    print("\nSeletores disponíveis:")
    print(f"  LOGIN_USERNAME: {SIACHSelectors.LOGIN_USERNAME}")
    print(f"  LOGIN_PASSWORD: {SIACHSelectors.LOGIN_PASSWORD}")
    print(f"  LOGIN_BUTTON: {SIACHSelectors.LOGIN_BUTTON}")
    print()


def exemplo_validar_seletores():
    """Valida todos os seletores"""
    print("=" * 60)
    print("EXEMPLO 2: Validar Seletores")
    print("=" * 60)

    resultado = SIACHSelectors.validate_selectors()

    print(f"\nTotal de seletores: {resultado['total']}")
    print(f"Todos válidos: {resultado['valid']}")

    if resultado['errors']:
        print("\nErros encontrados:")
        for erro in resultado['errors']:
            print(f"  - {erro}")
    else:
        print("\n✅ Todos os seletores estão válidos!")

    print()


def exemplo_imprimir_seletores():
    """Imprime todos os seletores organizados"""
    print("=" * 60)
    print("EXEMPLO 3: Listar Todos os Seletores")
    print("=" * 60)
    print()

    SIACHSelectors.print_selectors()


def exemplo_usar_com_driver():
    """Demonstra uso de seletores com driver real"""
    print("=" * 60)
    print("EXEMPLO 4: Usar Seletores com Driver")
    print("=" * 60)

    # Criar driver
    driver_wrapper = DriverFactory.criar_driver()
    driver = driver_wrapper.driver

    try:
        # Abrir página de teste (Google)
        driver.get('https://www.google.com')
        print("\n✅ Página aberta com sucesso")

        # Exemplo: buscar elemento (não irá encontrar pois não é página SIACH)
        print("\n⚠️ Nota: Seletores são específicos para SIACH")
        print("Para testar com página real do SIACH, ajuste o código abaixo:")
        print()
        print("# driver.get('https://cartoes.extracaixa/')")
        print("# username = driver.find_element(*SIACHSelectors.LOGIN_USERNAME)")
        print("# username.send_keys('seu_email@email.com')")
        print()

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        driver_wrapper.fechar_seguro()
        print("Driver fechado\n")


def exemplo_usar_com_espera():
    """Demonstra uso de seletores com espera explícita"""
    print("=" * 60)
    print("EXEMPLO 5: Seletores com Espera Explícita")
    print("=" * 60)

    print("\nExemplo de código com espera explícita:")
    print()
    print("```python")
    print("from selenium.webdriver.support.ui import WebDriverWait")
    print("from selenium.webdriver.support import expected_conditions as EC")
    print()
    print("# Esperar até elemento estar presente")
    print("wait = WebDriverWait(driver, 15)")
    print("element = wait.until(")
    print("    EC.presence_of_element_located(SIACHSelectors.LOGIN_BUTTON)")
    print(")")
    print("element.click()")
    print("```")
    print()


def exemplo_categorias_seletores():
    """Mostra seletores por categoria"""
    print("=" * 60)
    print("EXEMPLO 6: Seletores por Categoria")
    print("=" * 60)

    categorias = {
        'LOGIN': ['LOGIN_USERNAME', 'LOGIN_PASSWORD', 'LOGIN_BUTTON'],
        'MENU': ['MENU_SIACH_MODULE', 'MENU_ATENDER_OCORRENCIA'],
        'FORM': ['FORM_PROTOCOLO_INPUT', 'FORM_OCORRENCIA_INPUT', 'FORM_CONSULTAR_BUTTON'],
        'PROTOCOLO': ['PROTOCOLO_FASE_TEXT'],
        'CLIENTE': ['CLIENTE_NOME_PRIMARY', 'CLIENTE_NOME_FALLBACK'],
        'FINALIZACAO': ['FINALIZACAO_SALVAR_BUTTON', 'FINALIZACAO_CONFIRMAR_BUTTON']
    }

    for categoria, seletores in categorias.items():
        print(f"\n{categoria}:")
        for nome in seletores:
            if hasattr(SIACHSelectors, nome):
                print(f"  ✅ {nome}")
            else:
                print(f"  ❌ {nome} (não encontrado)")

    print()


if __name__ == "__main__":
    print("\n" + "📍 EXEMPLOS DE USO DE SELETORES".center(60))
    print()

    try:
        exemplo_seletores_basicos()
        exemplo_validar_seletores()
        exemplo_categorias_seletores()
        exemplo_usar_com_driver()
        exemplo_usar_com_espera()
        exemplo_imprimir_seletores()

        print("\n" + "=" * 60)
        print("✅ Todos os exemplos executados com sucesso!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
