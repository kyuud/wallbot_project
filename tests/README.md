# 🧪 Testes - WallBot v3.0.0

Suite completa de testes para a nova arquitetura modular.

---

## 📊 Cobertura de Testes

| Módulo | Arquivo de Teste | Testes | Status |
|--------|------------------|--------|--------|
| `selectors/` | [test_selectors.py](test_selectors.py) | 12 | ✅ |
| `validators/` | [test_validators.py](test_validators.py) | 25 | ✅ |
| `config/` | [test_config.py](test_config.py) | 10 | ✅ |
| `drivers/` | [test_drivers.py](test_drivers.py) | 15 | ✅ |
| **Total** | **4 arquivos** | **62** | **✅** |

---

## 🚀 Executar Testes

### Pré-requisitos

```bash
pip install pytest
# ou
pip install -r requirements-dev.txt
```

### Comandos Básicos

```bash
# Rodar todos os testes
pytest tests/ -v

# Rodar apenas testes rápidos (pular testes que criam drivers reais)
pytest tests/ -v -m "not slow"

# Rodar teste específico
pytest tests/test_selectors.py -v

# Rodar com output detalhado
pytest tests/ -vv

# Rodar e parar no primeiro erro
pytest tests/ -x
```

### Comandos Avançados

```bash
# Ver cobertura de testes
pytest tests/ --cov=config --cov=selectors --cov=validators --cov=drivers

# Gerar relatório HTML de cobertura
pytest tests/ --cov=config --cov=selectors --cov=validators --cov=drivers --cov-report=html

# Rodar apenas uma classe de teste
pytest tests/test_selectors.py::TestSIACHSelectors -v

# Rodar apenas um teste específico
pytest tests/test_selectors.py::TestSIACHSelectors::test_selector_format -v

# Rodar com modo verboso + mostrar prints
pytest tests/ -v -s

# Rodar em paralelo (requer pytest-xdist)
pip install pytest-xdist
pytest tests/ -n auto
```

---

## 📁 Estrutura dos Testes

```
tests/
├── __init__.py                # Inicialização do pacote de testes
├── test_selectors.py          # Testes de seletores (12 testes)
├── test_validators.py         # Testes de validadores (25 testes)
├── test_config.py             # Testes de configuração (10 testes)
├── test_drivers.py            # Testes de drivers (15 testes)
└── README.md                  # Este arquivo
```

---

## 📖 Descrição dos Arquivos de Teste

### test_selectors.py
**Testa:** `selectors/siach_selectors.py`

**Classes de Teste:**
- `TestSIACHSelectors` - Valida seletores XPath
  - `test_selector_format()` - Formato das tuplas (By, valor)
  - `test_all_selectors_valid()` - Todos os seletores são válidos
  - `test_selector_categories()` - Seletores por categoria
  - `test_get_selector_method()` - Método get_selector()

- `TestFasesProtocolo` - Valida lógica de fases
  - `test_fases_processaveis()` - Fases que podem finalizar
  - `test_fases_sem_acao()` - Fases que não permitem ação
  - `test_fases_desconhecidas()` - Fases não mapeadas
  - `test_case_insensitive()` - Validação case-insensitive

**Executar:**
```bash
pytest tests/test_selectors.py -v
```

---

### test_validators.py
**Testa:** `validators/page_validators.py`

**Classes de Teste:**
- `TestValidarArquivoExcel` - Validação de arquivos Excel
  - `test_arquivo_valido()` - Arquivo válido
  - `test_arquivo_inexistente()` - Arquivo não encontrado
  - `test_arquivo_vazio()` - String vazia
  - `test_extensao_invalida()` - Extensão errada

- `TestValidarEmail` - Validação de emails
  - `test_email_valido()` - Emails válidos
  - `test_email_sem_arroba()` - Sem @
  - `test_email_sem_dominio()` - Sem domínio
  - `test_email_vazio()` - String vazia
  - `test_email_sem_ponto()` - Sem ponto

- `TestValidarCredenciais` - Validação de login
  - `test_credenciais_validas()` - Credenciais OK
  - `test_email_invalido()` - Email errado
  - `test_senha_muito_curta()` - Senha < 3 chars
  - `test_campos_vazios()` - Campos vazios

- `TestValidarScriptPersonalizacao` - Validação de scripts
  - `test_script_valido_sem_personalizacao()` - Sem @NomeCliente@
  - `test_script_valido_com_personalizacao()` - Com placeholder
  - `test_script_sem_placeholder()` - Aviso se falta placeholder
  - `test_script_vazio()` - Script vazio

- `TestVerificarErroConexao` - Classificação de erros
  - `test_erro_http_connection()` - HTTPConnectionPool
  - `test_erro_timeout()` - Read timed out
  - `test_erro_target_frame()` - target frame detached
  - `test_erro_connection_refused()` - Connection refused
  - `test_erro_nao_conexao()` - Erros comuns
  - `test_case_insensitive()` - Case insensitive

**Executar:**
```bash
pytest tests/test_validators.py -v
```

---

### test_config.py
**Testa:** `config/config.py`

**Classes de Teste:**
- `TestWallBotConfig` - Configurações padrão
  - `test_config_defaults()` - Valores padrão
  - `test_urls()` - URLs configuradas
  - `test_arquivos()` - Arquivos configurados
  - `test_timeouts()` - Timeouts configurados
  - `test_navegador_config()` - Config do navegador
  - `test_to_dict()` - Conversão para dict
  - `test_validar_config()` - Validação de config

- `TestEnvConfig` - Configurações de ambiente
  - `test_get_navegador_default()` - Navegador padrão
  - `test_get_timeout_default()` - Timeout padrão
  - `test_get_max_tentativas_default()` - Max tentativas
  - `test_is_debug_mode_default()` - Modo debug

**Executar:**
```bash
pytest tests/test_config.py -v
```

---

### test_drivers.py
**Testa:** `drivers/`

**Classes de Teste:**
- `TestDriverFactory` - Factory de drivers
  - `test_navegadores_suportados()` - Lista navegadores
  - `test_criar_driver_chrome_sem_inicializar()` - Instância Chrome
  - `test_criar_driver_firefox_sem_inicializar()` - Instância Firefox
  - `test_factory_navegador_invalido()` - Navegador inválido

- `TestBaseDriver` - Classe base
  - `test_chrome_driver_herda_base()` - Herança Chrome
  - `test_firefox_driver_herda_base()` - Herança Firefox
  - `test_base_driver_metodos_abstratos()` - Métodos abstratos

- `TestChromeDriver` - Driver Chrome
  - `test_chrome_nome_navegador()` - Nome do navegador
  - `test_chrome_configurar_opcoes()` - Configurar opções
  - `test_chrome_configurar_opcoes_headless()` - Modo headless
  - `test_chrome_criar_driver_real()` - ⚠️ Cria driver real (LENTO)

- `TestFirefoxDriver` - Driver Firefox
  - `test_firefox_nome_navegador()` - Nome do navegador
  - `test_firefox_configurar_opcoes()` - Configurar opções
  - `test_firefox_delay_fechamento()` - Delay de 3s

- `TestDriverIntegration` - Integração
  - `test_factory_cria_chrome_por_padrao()` - Padrão Chrome
  - `test_multiplos_drivers_podem_coexistir()` - Múltiplas instâncias

**Executar:**
```bash
# Todos os testes (pula testes lentos)
pytest tests/test_drivers.py -v -m "not slow"

# Incluindo testes lentos (cria drivers reais)
pytest tests/test_drivers.py -v
```

---

## 🏷️ Markers de Testes

### @pytest.mark.slow

Marca testes que demoram mais (criam drivers reais).

**Uso:**
```python
@pytest.mark.slow
def test_chrome_criar_driver_real():
    # Teste que cria driver real
    pass
```

**Executar sem testes lentos:**
```bash
pytest tests/ -m "not slow"
```

**Executar apenas testes lentos:**
```bash
pytest tests/ -m "slow"
```

---

## 📊 Ver Cobertura de Testes

### Instalar pytest-cov

```bash
pip install pytest-cov
```

### Gerar Relatório

```bash
# Relatório no terminal
pytest tests/ --cov=config --cov=selectors --cov=validators --cov=drivers

# Relatório HTML (cria pasta htmlcov/)
pytest tests/ --cov=config --cov=selectors --cov=validators --cov=drivers --cov-report=html

# Abrir relatório HTML
# Windows: start htmlcov/index.html
# Linux: xdg-open htmlcov/index.html
# Mac: open htmlcov/index.html
```

---

## ✍️ Escrever Novos Testes

### Template Básico

```python
"""
Testes para novo_modulo

Execute:
    pytest tests/test_novo_modulo.py -v
"""

import pytest
from novo_modulo import MinhaClasse


class TestMinhaClasse:
    """Testes para MinhaClasse"""

    def test_funcionalidade_basica(self):
        """Testa funcionalidade básica"""
        obj = MinhaClasse()
        resultado = obj.metodo()

        assert resultado == "esperado"

    def test_com_parametros(self):
        """Testa com parâmetros"""
        obj = MinhaClasse()
        resultado = obj.metodo_com_param(10)

        assert resultado > 0

    def test_excecao(self):
        """Testa se exceção é lançada"""
        obj = MinhaClasse()

        with pytest.raises(ValueError):
            obj.metodo_invalido()


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
```

### Fixtures

```python
import pytest

@pytest.fixture
def driver_chrome():
    """Fixture para criar driver Chrome"""
    from drivers import ChromeDriver

    driver = ChromeDriver()
    driver.criar()

    yield driver

    driver.fechar_seguro()


def test_com_fixture(driver_chrome):
    """Teste que usa fixture"""
    driver = driver_chrome.driver
    driver.get('https://www.google.com')
    assert 'Google' in driver.title
```

---

## 🐛 Debugging de Testes

### Ver prints durante testes

```bash
pytest tests/ -v -s
```

### Parar no primeiro erro

```bash
pytest tests/ -x
```

### Executar último teste que falhou

```bash
pytest tests/ --lf
```

### Executar com pdb (debugger)

```bash
pytest tests/ --pdb
```

### Ver tempo de execução

```bash
pytest tests/ --durations=10
```

---

## 🎯 Boas Práticas

### ✅ DO

- ✅ Um teste testa uma coisa
- ✅ Nomes descritivos: `test_email_valido_retorna_true()`
- ✅ Usar fixtures para setup/teardown
- ✅ Isolar testes (não dependem uns dos outros)
- ✅ Testar edge cases e erros
- ✅ Marcar testes lentos com `@pytest.mark.slow`

### ❌ DON'T

- ❌ Testes que dependem de ordem de execução
- ❌ Testes que dependem de estado global
- ❌ Testes sem assertions
- ❌ Testes com muitas responsabilidades
- ❌ Testes sem documentação (docstring)

---

## 📞 Troubleshooting

### Testes não encontrados

**Erro:** `collected 0 items`

**Solução:** Certifique-se de estar na raiz do projeto:
```bash
cd wallbot_project
pytest tests/ -v
```

### Import errors

**Erro:** `ModuleNotFoundError`

**Solução:** Adicione raiz do projeto ao PYTHONPATH:
```bash
# Windows
set PYTHONPATH=%CD%
pytest tests/ -v

# Linux/Mac
export PYTHONPATH=$(pwd)
pytest tests/ -v
```

### Testes lentos travando

**Sintoma:** Teste nunca termina

**Solução:** Pule testes lentos:
```bash
pytest tests/ -m "not slow"
```

---

## 📈 Métricas de Qualidade

### Metas

- ✅ Cobertura de testes: ≥ 80%
- ✅ Todos os testes passam
- ✅ Tempo de execução < 30s (sem testes lentos)
- ✅ Zero warnings

### Verificar Qualidade

```bash
# Rodar testes + cobertura + warnings
pytest tests/ -v --cov=config --cov=selectors --cov=validators --cov=drivers --cov-report=term-missing -W error
```

---

## 🔄 Integração Contínua

Para configurar CI/CD (GitHub Actions, GitLab CI, etc):

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest tests/ -v -m "not slow" --cov=config --cov=selectors --cov=validators --cov=drivers
```

---

## 📞 Próximos Passos

1. Execute todos os testes: `pytest tests/ -v`
2. Veja cobertura: `pytest tests/ --cov=...`
3. Escreva novos testes para features novas
4. Consulte [USAGE_GUIDE.md](../USAGE_GUIDE.md) para uso dos módulos

---

**Última atualização:** 2025-10-30
**Versão:** 1.0
**Compatível com:** WallBot v3.0.0-alpha.1
