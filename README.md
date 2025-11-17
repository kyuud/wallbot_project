# WallBot SIACH v3.0.0-alpha.1

Automação RPA para sistema SIACH da Caixa com arquitetura modular.

[![Version](https://img.shields.io/badge/version-3.0.0--alpha.1-orange)](https://github.com/kyuud/wallbot_project)
[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)
[![Browser](https://img.shields.io/badge/browser-Chrome-green)](https://www.google.com/chrome/)
[![Tests](https://img.shields.io/badge/tests-62%20passing-brightgreen)](tests/)

---

## ⚠️ Status: ALPHA

Esta é uma versão **ALPHA** em desenvolvimento ativo. **NÃO usar em produção.**

Para produção, use: `v2.1.0-firefox-stable`

---

## 🚀 Início Rápido

### Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

### Exemplo Básico

```python
from drivers import DriverFactory

# Criar driver Chrome
driver_wrapper = DriverFactory.criar_driver()
driver = driver_wrapper.driver

# Usar o driver
driver.get('https://cartoes.extracaixa/')

# Fechar
driver_wrapper.fechar_seguro()
```

### Executar Testes

```bash
pytest tests/ -v -m "not slow"
```

---

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | Guia completo de uso |
| [examples/](examples/) | Exemplos práticos |
| [tests/README.md](tests/README.md) | Guia de testes |
| [CHANGELOG.md](CHANGELOG.md) | Histórico de versões |

---

## ✨ Novidades da v3.0.0

### Arquitetura Modular

- **config/** - Configurações centralizadas
- **drivers/** - Chrome + Firefox (Factory Pattern)
- **selectors/** - 16 XPaths organizados
- **validators/** - Validações de página/dados
- **tests/** - 62 testes automatizados
- **examples/** - 4 exemplos práticos

### Performance (Chrome vs Firefox)

| Métrica | Firefox | Chrome | Melhoria |
|---------|---------|--------|----------|
| Tempo/protocolo | 30.6s | 25.2s | **-18%** |
| RAM | 820MB | 580MB | **-29%** |
| Shutdown | 3s | 1s | **-67%** |

---

## 💡 Exemplos Práticos

```python
# Exemplo 1: Usar seletores
from selectors import SIACHSelectors
username = driver.find_element(*SIACHSelectors.LOGIN_USERNAME)

# Exemplo 2: Validar email
from validators import validar_email
valido, msg = validar_email("user@test.com")

# Exemplo 3: Configurar
from config.config import WallBotConfig
print(WallBotConfig.NAVEGADOR_PADRAO)  # 'chrome'
```

Ver [examples/](examples/) para mais exemplos.

---

## 🧪 Testes

**62 testes** cobrindo todos os módulos:

- `test_selectors.py` - 12 testes
- `test_validators.py` - 25 testes
- `test_config.py` - 10 testes
- `test_drivers.py` - 15 testes

```bash
pytest tests/ -v --cov=config --cov=selectors --cov=validators --cov=drivers
```

---

## 📦 Dependências

- selenium==4.15.2
- webdriver-manager==4.0.1
- openpyxl==3.1.2
- customtkinter==5.2.0
- pytest==7.4.3

---

## 🗺️ Roadmap

- **v3.0.0-alpha.2** - Refatoração do código principal
- **v3.0.0-beta.1** - Testes em produção
- **v3.0.0** - Release estável

Ver [CHANGELOG.md](CHANGELOG.md) para detalhes.

---

## 🔗 Links

- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Guia completo
- [CHANGELOG.md](CHANGELOG.md) - Histórico
- [examples/](examples/) - Exemplos
- [tests/](tests/) - Testes

---

**Versão:** v3.0.0-alpha.1 • **Status:** 🔬 ALPHA • **Data:** 2025-10-30