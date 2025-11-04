# 📚 Exemplos - WallBot v3.0.0

Exemplos práticos demonstrando uso da nova arquitetura modular.

---

## 📑 Índice de Exemplos

| Exemplo | Descrição | Nível |
|---------|-----------|-------|
| [exemplo_01_criar_driver.py](exemplo_01_criar_driver.py) | Como criar drivers Chrome/Firefox | Básico |
| [exemplo_02_usar_seletores.py](exemplo_02_usar_seletores.py) | Usar seletores centralizados | Básico |
| [exemplo_03_validar_dados.py](exemplo_03_validar_dados.py) | Validar entradas (email, Excel, etc) | Intermediário |
| [exemplo_04_fases_protocolo.py](exemplo_04_fases_protocolo.py) | Validar fases de protocolo | Intermediário |

---

## 🚀 Como Executar

### Executar exemplo individual

```bash
# Navegar para a raiz do projeto
cd wallbot_project

# Executar exemplo
python examples/exemplo_01_criar_driver.py
```

### Executar todos os exemplos

```bash
# Windows
for %f in (examples\exemplo_*.py) do python %f

# Linux/Mac
for file in examples/exemplo_*.py; do python "$file"; done
```

---

## 📖 Descrição dos Exemplos

### 01 - Criar Driver
**Arquivo:** `exemplo_01_criar_driver.py`

**O que aprenderá:**
- ✅ Criar driver Chrome usando Factory
- ✅ Criar driver Firefox
- ✅ Instância direta vs Factory
- ✅ Context manager (`with` statement)
- ✅ Modo headless (sem interface)
- ✅ Timeout customizado

**Conceitos:**
- `DriverFactory.criar_driver()`
- `ChromeDriver()` e `FirefoxDriver()`
- Context managers
- Headless mode

---

### 02 - Usar Seletores
**Arquivo:** `exemplo_02_usar_seletores.py`

**O que aprenderá:**
- ✅ Acessar seletores centralizados
- ✅ Validar todos os seletores
- ✅ Listar seletores por categoria
- ✅ Usar seletores com WebDriver
- ✅ Esperas explícitas com seletores

**Conceitos:**
- `SIACHSelectors.LOGIN_USERNAME`
- `SIACHSelectors.validate_selectors()`
- `driver.find_element(*selector)`
- `WebDriverWait` com seletores

---

### 03 - Validar Dados
**Arquivo:** `exemplo_03_validar_dados.py`

**O que aprenderá:**
- ✅ Validar formato de email
- ✅ Validar arquivos Excel
- ✅ Validar credenciais completas
- ✅ Validar scripts de finalização
- ✅ Classificar erros de conexão
- ✅ Fluxo completo de validação

**Conceitos:**
- `validar_email()`
- `validar_arquivo_excel()`
- `validar_credenciais()`
- `validar_script_personalizacao()`
- `verificar_erro_conexao()`

---

### 04 - Fases de Protocolo
**Arquivo:** `exemplo_04_fases_protocolo.py`

**O que aprenderá:**
- ✅ Verificar se protocolo pode ser finalizado
- ✅ Validação case-insensitive
- ✅ Fluxo de decisão baseado em fase
- ✅ Coleta de estatísticas
- ✅ Constantes disponíveis

**Conceitos:**
- `FasesProtocolo.pode_finalizar()`
- `FasesProtocolo.ja_finalizado()`
- `FasesProtocolo.PROCESSAVEIS`
- `FasesProtocolo.SEM_ACAO`

---

## 🎯 Progressão Recomendada

### Nível 1: Básico (Iniciantes)
1. **exemplo_01** - Entender como criar drivers
2. **exemplo_02** - Aprender a usar seletores

### Nível 2: Intermediário
3. **exemplo_03** - Validar dados de entrada
4. **exemplo_04** - Trabalhar com fases de protocolo

---

## 💡 Dicas

### Executar com Tratamento de Erros

```python
try:
    # Seu código aqui
    from drivers import DriverFactory
    driver_wrapper = DriverFactory.criar_driver()
    # ...
except Exception as e:
    print(f"Erro: {e}")
finally:
    if 'driver_wrapper' in locals():
        driver_wrapper.fechar_seguro()
```

### Modo Debug

```python
# Ativar modo debug
import os
os.environ['WALLBOT_DEBUG'] = 'true'

from config.config import EnvConfig
if EnvConfig.is_debug_mode():
    print("Debug ativado!")
```

### Customizar Configurações

```python
# Via environment variables
os.environ['WALLBOT_NAVEGADOR'] = 'firefox'
os.environ['WALLBOT_TIMEOUT'] = '30'

# Ou diretamente
from config.config import WallBotConfig
WallBotConfig.TIMEOUT_PADRAO = 30
```

---

## ❓ Perguntas Frequentes

### Chrome não está instalado

**Erro:** `selenium.common.exceptions.SessionNotCreatedException`

**Solução:** Instale Chrome ou use Firefox:
```python
driver_wrapper = DriverFactory.criar_driver('firefox')
```

### Imports não funcionam

**Erro:** `ModuleNotFoundError: No module named 'config'`

**Solução:** Execute da raiz do projeto:
```bash
cd wallbot_project
python examples/exemplo_01_criar_driver.py
```

### Dependências faltando

**Erro:** `ModuleNotFoundError: No module named 'selenium'`

**Solução:** Instale dependências:
```bash
pip install -r requirements.txt
```

---

## 📞 Próximos Passos

Depois de dominar os exemplos:

1. Leia o [USAGE_GUIDE.md](../USAGE_GUIDE.md) completo
2. Execute os testes: `pytest tests/ -v`
3. Explore os módulos em `config/`, `drivers/`, `selectors/`, `validators/`
4. Consulte o [CHANGELOG.md](../CHANGELOG.md) para ver todas as features

---

## ⚠️ Notas

- **ALPHA:** Versão em desenvolvimento, não usar em produção
- **Produção:** Use `v2.1.0-firefox-stable`
- **Chrome:** Requer Google Chrome instalado
- **Testes:** Alguns exemplos criam drivers reais

---

**Última atualização:** 2025-10-30
**Versão:** 1.0
**Compatível com:** WallBot v3.0.0-alpha.1
