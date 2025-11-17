# 📖 Guia de Uso - WallBot SIACH v3.0.0

Guia completo para usar a nova arquitetura modular do WallBot SIACH.

**Versão:** 3.0.0-alpha.1
**Data:** 2025-10-30
**Status:** ALPHA (não usar em produção)

---

## 📑 Índice

1. [Instalação](#instalação)
2. [Início Rápido](#início-rápido)
3. [Arquitetura](#arquitetura)
4. [Exemplos Práticos](#exemplos-práticos)
5. [Configuração](#configuração)
6. [Migração v2.1.0 → v3.0.0](#migração)
7. [Troubleshooting](#troubleshooting)
8. [Referência da API](#referência-da-api)

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8+
- Google Chrome instalado (para usar ChromeDriver)
- Firefox instalado (opcional, para modo legado)

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/kyuud/wallbot_project.git
cd wallbot_project
```

### Passo 2: Checkout da Branch v3.0.0

```bash
git checkout feature/v3.0.0-chrome-migration
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

**Dependências instaladas:**
- `selenium==4.15.2` - Automação web
- `webdriver-manager==4.0.1` - Gerenciamento automático de drivers
- `openpyxl==3.1.2` - Manipulação de Excel
- `customtkinter==5.2.0` - Interface gráfica
- `python-dotenv==1.0.0` - Variáveis de ambiente

### Passo 4: Verificar Instalação

```bash
python VERSION.py
```

**Saída esperada:**
```
WallBot v3.0.0-alpha.1 (Chrome) - ALPHA
```

---

## ⚡ Início Rápido

### Exemplo Mínimo

```python
from drivers import DriverFactory

# Criar driver Chrome (padrão)
driver_wrapper = DriverFactory.criar_driver()
driver = driver_wrapper.driver

# Usar o driver
driver.get('https://cartoes.extracaixa/')

# Fechar
driver_wrapper.fechar_seguro()
```

### Exemplo com Context Manager

```python
from drivers import ChromeDriver

# Usar context manager (fecha automaticamente)
with ChromeDriver() as chrome:
    driver = chrome.criar()
    driver.get('https://cartoes.extracaixa/')
    print(f"Título: {driver.title}")

# Driver fechado automaticamente
```

---

## 🏗️ Arquitetura

A v3.0.0 introduz arquitetura modular para melhor organização:

```
wallbot_project/
├── config/
│   └── config.py              # Configurações centralizadas
├── drivers/
│   ├── base_driver.py         # Classe abstrata
│   ├── chrome_driver.py       # Implementação Chrome
│   ├── firefox_driver.py      # Implementação Firefox
│   └── driver_factory.py      # Factory para criar drivers
├── selectors/
│   └── siach_selectors.py     # XPaths centralizados
├── validators/
│   └── page_validators.py     # Validações de página
├── tests/                      # Testes automatizados
└── examples/                   # Exemplos práticos
```

### Benefícios

✅ **Manutenibilidade** - XPaths centralizados, fácil atualizar
✅ **Extensibilidade** - Adicionar novo navegador = criar nova classe
✅ **Testabilidade** - Cada módulo testável independentemente
✅ **Performance** - Chrome 18% mais rápido que Firefox

---

## 📚 Exemplos Práticos

### 1. Criar Driver Chrome

```python
from drivers import DriverFactory

# Método 1: Factory (recomendado)
driver_wrapper = DriverFactory.criar_driver('chrome')

# Método 2: Instância direta
from drivers import ChromeDriver
driver_wrapper = ChromeDriver()
driver_wrapper.criar()

# Acessar driver Selenium
driver = driver_wrapper.driver

# Usar driver
driver.get('https://cartoes.extracaixa/')

# Fechar
driver_wrapper.fechar_seguro()
```

### 2. Criar Driver Firefox (Legado)

```python
from drivers import DriverFactory

# Usar Firefox ao invés de Chrome
driver_wrapper = DriverFactory.criar_driver('firefox')
driver = driver_wrapper.driver

# Fechar (Firefox usa delay de 3s)
driver_wrapper.fechar_seguro()  # delay=3s automático
```

### 3. Usar Seletores Centralizados

```python
from drivers import DriverFactory
from selectors import SIACHSelectors

driver_wrapper = DriverFactory.criar_driver()
driver = driver_wrapper.driver

driver.get('https://cartoes.extracaixa/')

# Login usando seletores
username_field = driver.find_element(*SIACHSelectors.LOGIN_USERNAME)
username_field.send_keys('usuario@email.com')

password_field = driver.find_element(*SIACHSelectors.LOGIN_PASSWORD)
password_field.send_keys('senha123')

login_button = driver.find_element(*SIACHSelectors.LOGIN_BUTTON)
login_button.click()

driver_wrapper.fechar_seguro()
```

### 4. Validar Páginas

```python
from drivers import DriverFactory
from validators import validar_pagina_siach, verificar_sessao_valida

driver_wrapper = DriverFactory.criar_driver()
driver = driver_wrapper.driver

driver.get('https://cartoes.extracaixa/')

# Validar tipo de página
resultado = validar_pagina_siach(driver, timeout=10)
print(f"Tipo de página: {resultado['tipo_pagina']}")  # 'login', 'menu', 'protocolo'
print(f"Página válida: {resultado['valido']}")

# Verificar se sessão está válida
if not verificar_sessao_valida(driver):
    print("Sessão expirada! Fazer login novamente.")
else:
    print("Sessão ativa!")

driver_wrapper.fechar_seguro()
```

### 5. Verificar Fase de Protocolo

```python
from selectors.siach_selectors import FasesProtocolo

fase_texto = "ABERTA"  # Extraído da página

# Verificar se pode finalizar
if FasesProtocolo.pode_finalizar(fase_texto):
    print("✅ Protocolo pode ser finalizado")
else:
    print("❌ Protocolo não pode ser finalizado")

# Verificar se já foi finalizado
if FasesProtocolo.ja_finalizado(fase_texto):
    print("Protocolo já está finalizado")
```

### 6. Validar Entrada de Dados

```python
from validators import validar_email, validar_arquivo_excel, validar_credenciais

# Validar email
valido, msg = validar_email("usuario@dominio.com")
if valido:
    print("✅ Email válido")
else:
    print(f"❌ Erro: {msg}")

# Validar arquivo Excel
valido, msg = validar_arquivo_excel("Base.xlsx")
if valido:
    print("✅ Arquivo válido")
else:
    print(f"❌ Erro: {msg}")

# Validar credenciais completas
valido, msg = validar_credenciais("user@test.com", "senha123")
if valido:
    print("✅ Credenciais válidas")
else:
    print(f"❌ Erro: {msg}")
```

### 7. Driver em Modo Headless

```python
from drivers import ChromeDriver

# Criar Chrome sem interface gráfica (headless)
driver_wrapper = ChromeDriver()
driver = driver_wrapper.criar(headless=True)

driver.get('https://cartoes.extracaixa/')
print(f"Título: {driver.title}")

driver_wrapper.fechar_seguro()
```

### 8. Configurar Timeouts Customizados

```python
from drivers import DriverFactory

# Criar driver com timeout customizado
driver_wrapper = DriverFactory.criar_driver(
    navegador='chrome',
    timeout=30  # 30 segundos
)

driver = driver_wrapper.driver
# Timeout de 30s aplicado automaticamente
```

---

## ⚙️ Configuração

### Configurações Padrão

O arquivo `config/config.py` contém todas as configurações:

```python
from config.config import WallBotConfig

# Ver todas as configurações
print(WallBotConfig.TIMEOUT_PADRAO)      # 15
print(WallBotConfig.NAVEGADOR_PADRAO)    # 'chrome'
print(WallBotConfig.URL_SIPCS)           # URL do SIACH
```

### Configuração via Variáveis de Ambiente

Criar arquivo `.env` na raiz do projeto:

```bash
# .env
WALLBOT_NAVEGADOR=chrome       # ou 'firefox'
WALLBOT_TIMEOUT=20             # timeout em segundos
WALLBOT_MAX_RECONEXAO=5        # tentativas de reconexão
WALLBOT_DEBUG=true             # modo debug
```

**Usar no código:**

```python
from config.config import EnvConfig

# Ler configurações do ambiente
navegador = EnvConfig.get_navegador()
timeout = EnvConfig.get_timeout_padrao()
max_tentativas = EnvConfig.get_max_tentativas_reconexao()
debug = EnvConfig.is_debug_mode()

print(f"Navegador: {navegador}")
print(f"Timeout: {timeout}s")
print(f"Max tentativas: {max_tentativas}")
print(f"Debug: {debug}")
```

### Configurações Disponíveis

| Configuração | Padrão | Descrição |
|--------------|--------|-----------|
| `NAVEGADOR_PADRAO` | `'chrome'` | Navegador padrão |
| `TIMEOUT_PADRAO` | `15` | Timeout geral (segundos) |
| `TIMEOUT_SALVAR` | `30` | Timeout para salvar (segundos) |
| `TIMEOUT_SCRIPT` | `60` | Timeout para scripts JS |
| `TIMEOUT_PAGINA` | `45` | Timeout para carregar página |
| `MAX_TENTATIVAS_RECONEXAO` | `3` | Tentativas de reconexão |
| `ESPERA_ENTRE_ACOES` | `1.0` | Delay entre ações (segundos) |
| `ZOOM_NIVEL` | `'0.67'` | Nível de zoom da página |
| `DELAY_FECHAR_DRIVER` | `1` | Delay ao fechar Chrome |

---

## 🔄 Migração v2.1.0 → v3.0.0 {#migração}

### Breaking Changes

⚠️ **Atenção:** v3.0.0 tem mudanças incompatíveis com v2.1.0

1. **Navegador padrão mudou:** Firefox → Chrome
2. **Estrutura de pastas:** Nova organização modular
3. **Imports:** Reorganizados em módulos

### Guia de Migração

#### Antes (v2.1.0)

```python
# Código antigo
from WallBot import criar_driver, fazer_login

driver = criar_driver()
fazer_login(driver, email, senha)
```

#### Depois (v3.0.0)

```python
# Novo código modular
from drivers import DriverFactory
from selectors import SIACHSelectors

driver_wrapper = DriverFactory.criar_driver()
driver = driver_wrapper.driver

# Login usando seletores
username = driver.find_element(*SIACHSelectors.LOGIN_USERNAME)
username.send_keys(email)
```

### Manter Firefox (Compatibilidade)

Se precisar continuar usando Firefox:

```python
# Opção 1: Via environment variable
import os
os.environ['WALLBOT_NAVEGADOR'] = 'firefox'

from drivers import DriverFactory
driver_wrapper = DriverFactory.criar_driver()

# Opção 2: Especificar diretamente
driver_wrapper = DriverFactory.criar_driver('firefox')
```

### Rollback para v2.1.0

Se encontrar problemas com v3.0.0:

```bash
# Voltar para versão estável
git checkout v2.1.0-firefox-stable

# Executar versão antiga
python WallBot.py
```

---

## 🔧 Troubleshooting

### Problema: ChromeDriver não encontrado

**Erro:**
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH.
```

**Solução:**
O `webdriver-manager` deve baixar automaticamente. Se falhar:

```bash
pip install --upgrade webdriver-manager
```

Ou manualmente:
```python
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
```

### Problema: Chrome não instalado

**Erro:**
```
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version XX
```

**Solução:**
- Instalar Google Chrome: https://www.google.com/chrome/
- Ou usar Firefox: `DriverFactory.criar_driver('firefox')`

### Problema: Imports não encontrados

**Erro:**
```
ModuleNotFoundError: No module named 'config'
```

**Solução:**
Verificar que está executando na raiz do projeto:

```bash
cd wallbot_project
python seu_script.py
```

Ou adicionar ao `sys.path`:

```python
import sys
sys.path.insert(0, 'f:/OneDrive/Documentos/Programacao/wallbot_project')

from config import WallBotConfig
```

### Problema: Seletores não encontram elementos

**Erro:**
```
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element
```

**Solução:**
1. Verificar se página carregou completamente
2. Adicionar espera explícita:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selectors import SIACHSelectors

wait = WebDriverWait(driver, 15)
element = wait.until(EC.presence_of_element_located(SIACHSelectors.LOGIN_BUTTON))
```

### Problema: Timeout expirado

**Erro:**
```
selenium.common.exceptions.TimeoutException: Message: timeout
```

**Solução:**
Aumentar timeout:

```python
# Via environment variable
os.environ['WALLBOT_TIMEOUT'] = '30'

# Ou diretamente no driver
driver_wrapper = DriverFactory.criar_driver(timeout=30)
```

### Problema: Versão errada

**Sintoma:** Código não funciona como esperado

**Solução:**
Verificar versão:

```bash
python VERSION.py
```

Deve mostrar: `WallBot v3.0.0-alpha.1 (Chrome) - ALPHA`

Se mostrar v2.1.0, fazer checkout correto:

```bash
git checkout feature/v3.0.0-chrome-migration
```

---

## 📖 Referência da API

### drivers.DriverFactory

```python
DriverFactory.criar_driver(
    navegador: Optional[str] = None,    # 'chrome' ou 'firefox'
    headless: bool = False,              # Modo sem interface
    timeout: Optional[int] = None,       # Timeout em segundos
    **kwargs                              # Argumentos adicionais
) -> BaseDriver
```

**Retorna:** Instância de `ChromeDriver` ou `FirefoxDriver`

### drivers.BaseDriver

**Métodos principais:**

```python
driver.criar(**kwargs) -> WebDriver
    # Cria e configura o WebDriver

driver.fechar_seguro(delay: int = 1) -> bool
    # Fecha o driver com segurança

driver.aplicar_zoom(nivel_zoom: str = '0.67') -> None
    # Aplica zoom à página

driver.abrir_url(url: str, timeout: Optional[int] = None) -> bool
    # Abre URL com tratamento de erro

driver.get_nome_navegador() -> str
    # Retorna 'Chrome' ou 'Firefox'
```

### selectors.SIACHSelectors

**Seletores principais:**

```python
# Login
SIACHSelectors.LOGIN_USERNAME         # Campo de usuário
SIACHSelectors.LOGIN_PASSWORD         # Campo de senha
SIACHSelectors.LOGIN_BUTTON           # Botão de login

# Menu
SIACHSelectors.MENU_SIACH_MODULE      # Link para SIACH
SIACHSelectors.MENU_ATENDER_OCORRENCIA # Menu "Atender Ocorrência"

# Formulário
SIACHSelectors.FORM_PROTOCOLO_INPUT   # Campo de protocolo
SIACHSelectors.FORM_OCORRENCIA_INPUT  # Campo de ocorrência
SIACHSelectors.FORM_CONSULTAR_BUTTON  # Botão "Consultar"

# Protocolo
SIACHSelectors.PROTOCOLO_FASE_TEXT    # Texto da fase

# Cliente
SIACHSelectors.CLIENTE_NOME_PRIMARY   # Nome do cliente
```

**Uso:**

```python
element = driver.find_element(*SIACHSelectors.LOGIN_USERNAME)
```

### selectors.FasesProtocolo

```python
FasesProtocolo.pode_finalizar(fase: str) -> bool
    # Verifica se fase permite finalização

FasesProtocolo.ja_finalizado(fase: str) -> bool
    # Verifica se protocolo já foi finalizado
```

**Fases:**
- `ABERTA` - Pode finalizar
- `EM ANDAMENTO` - Pode finalizar
- `FINALIZADA` - Não pode finalizar
- `REABERTA` - Não pode finalizar

### validators.page_validators

```python
validar_arquivo_excel(caminho: str) -> Tuple[bool, str]
    # Valida arquivo Excel

validar_email(email: str) -> Tuple[bool, str]
    # Valida formato de email

validar_credenciais(email: str, senha: str) -> Tuple[bool, str]
    # Valida credenciais de login

validar_pagina_siach(driver: WebDriver, timeout: int = 10) -> Dict
    # Valida e detecta tipo de página SIACH

verificar_sessao_valida(driver: WebDriver, timeout: int = 5) -> bool
    # Verifica se sessão está ativa

detectar_pagina_manutencao(driver: WebDriver) -> Tuple[bool, str]
    # Detecta página de manutenção

verificar_erro_conexao(exception_message: str) -> bool
    # Classifica erro como problema de conexão
```

### config.WallBotConfig

```python
# Acessar configurações
WallBotConfig.URL_SIPCS
WallBotConfig.TIMEOUT_PADRAO
WallBotConfig.NAVEGADOR_PADRAO

# Métodos
WallBotConfig.to_dict() -> Dict
    # Retorna todas as configurações

WallBotConfig.validar_config() -> Dict
    # Valida configurações

WallBotConfig.print_config() -> None
    # Imprime todas as configurações
```

---

## 🧪 Executar Testes

```bash
# Instalar pytest
pip install pytest

# Rodar todos os testes
pytest tests/ -v

# Rodar apenas testes rápidos (pular testes que criam drivers)
pytest tests/ -v -m "not slow"

# Rodar teste específico
pytest tests/test_selectors.py -v

# Ver cobertura
pip install pytest-cov
pytest tests/ --cov=config --cov=selectors --cov=validators --cov=drivers
```

---

## 📞 Suporte

- **Issues:** https://github.com/kyuud/wallbot_project/issues
- **Documentação:** [CHANGELOG.md](./CHANGELOG.md), [VERSION.py](./VERSION.py)
- **Exemplos:** Pasta `examples/`

---

## ⚠️ Notas Importantes

1. **ALPHA:** Esta é versão ALPHA, **não usar em produção**
2. **Produção:** Use `v2.1.0-firefox-stable` para produção
3. **Chrome:** Requer Google Chrome instalado
4. **Testes:** Execute testes antes de usar: `pytest tests/ -v`

---

**Última atualização:** 2025-10-30
**Versão do guia:** 1.0
**Compatível com:** WallBot v3.0.0-alpha.1

