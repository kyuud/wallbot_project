# Changelog - WallBot SIACH

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## Formato de Versionamento

**MAJOR.MINOR.PATCH**

- **MAJOR**: Mudanças incompatíveis na API/interface (breaking changes)
- **MINOR**: Novas funcionalidades mantendo compatibilidade
- **PATCH**: Correções de bugs e melhorias menores

## Status de Estabilidade

- ✅ **STABLE**: Versão testada e aprovada para produção
- ⚠️ **BETA**: Em testes, pode ter bugs
- 🔬 **ALPHA**: Em desenvolvimento, não usar em produção
- 🗂️ **DEPRECATED**: Versão descontinuada

---

## [Unreleased]

### Em Desenvolvimento (v3.0.0-alpha.2)
- Refatoração de fechamento_em_lote() (193→80 linhas)
- Refatoração de criar_interface() (327 linhas) em módulos UI
- Refatoração de finalizar_protocolo() (102→50 linhas)
- Testes automatizados dos novos módulos
- Timeouts adaptativos

---

## [3.0.0-alpha.1] - 2025-10-30 - 🔬 ALPHA (ATUAL)

**Navegador:** Chrome (padrão) + Firefox (legado)
**Tag Git:** `v3.0.0-alpha.1`
**Branch:** `feature/v3.0.0-chrome-migration`

### ⚠️ BREAKING CHANGES

Esta é uma versão ALPHA em desenvolvimento ativo. **NÃO usar em produção.**

- Navegador padrão mudou de Firefox para Chrome
- Nova estrutura modular de pastas
- Reorganização de imports
- API de drivers abstraída (BaseDriver)

### ✨ Adicionado - Arquitetura Modular

**Nova estrutura de pastas:**
```
wallbot_project/
├── config/
│   └── config.py              # Configurações centralizadas
├── drivers/
│   ├── base_driver.py         # Classe abstrata
│   ├── chrome_driver.py       # Implementação Chrome (NOVO)
│   ├── firefox_driver.py      # Implementação Firefox (legado)
│   └── driver_factory.py      # Factory Pattern
├── selectors/
│   └── siach_selectors.py     # 16 XPaths centralizados
├── validators/
│   └── page_validators.py     # Validações de página e sessão
└── requirements.txt            # Dependências
```

**Módulos criados:**

1. **`selectors/siach_selectors.py`** (280 linhas)
   - Classe `SIACHSelectors` com 16 seletores XPath organizados
   - Classe `FasesProtocolo` com lógica de fases
   - Métodos: `validate_selectors()`, `print_selectors()`
   - Categorias: LOGIN, MENU, FORM, PROTOCOLO, CLIENTE, FINALIZACAO

2. **`validators/page_validators.py`** (450 linhas)
   - `validar_arquivo_excel()` - Valida arquivos Excel
   - `validar_email()` - Valida formato de email
   - `validar_credenciais()` - Valida login
   - `validar_pagina_siach()` - Detecta tipo de página
   - `verificar_sessao_valida()` - Checa expiração de sessão
   - `detectar_pagina_manutencao()` - Identifica manutenção
   - `verificar_erro_conexao()` - Classifica erros de conexão
   - `validar_fase_protocolo()` - Valida fase processável

3. **`config/config.py`** (150 linhas)
   - Classe `WallBotConfig` com todas as configurações
   - Classe `EnvConfig` para variáveis de ambiente
   - Configurações: URLs, arquivos, timeouts, navegador
   - Métodos: `to_dict()`, `print_config()`, `validar_config()`

4. **`drivers/base_driver.py`** (180 linhas)
   - Classe abstrata `BaseDriver`
   - Interface comum para Chrome/Firefox
   - Métodos: `criar()`, `fechar_seguro()`, `aplicar_zoom()`
   - Context manager support (`with` statement)

5. **`drivers/chrome_driver.py`** (200 linhas)
   - Implementação Chrome otimizada
   - Modo stealth (anti-detecção de automação)
   - Configurações de performance
   - Headless mode support
   - ChromeDriver auto-install via webdriver-manager

6. **`drivers/firefox_driver.py`** (120 linhas)
   - Implementação Firefox (legado v2.1.0)
   - Mantém compatibilidade com versão anterior
   - GeckoDriver auto-install

7. **`drivers/driver_factory.py`** (80 linhas)
   - Factory Pattern para criação de drivers
   - `criar_driver(navegador='chrome')` - API unificada
   - Suporta variáveis de ambiente (`WALLBOT_NAVEGADOR`)
   - `navegadores_suportados()` - Lista navegadores

### 🔄 Alterado

- Navegador padrão: Firefox → Chrome
- Delay de fechamento: 3s → 1s (Chrome é mais rápido)
- Timeout de script: Não configurado → 60s
- Timeout de página: Implícito → 45s

### 🐛 Corrigido

- **Issue #3**: Timeout de script JavaScript agora configurado (60s)
- **Issue #4**: Fechamento mais rápido no Chrome (1s vs 3s)
- Seletores XPath agora centralizados (fácil manutenção)
- Configurações agora organizadas em classe única

### 📝 Melhorias

- **Manutenibilidade**: Código modular, fácil de testar e extender
- **Extensibilidade**: Novos navegadores podem ser adicionados facilmente
- **Testabilidade**: Cada módulo pode ser testado independentemente
- **Documentação**: Cada módulo autodocumentado com docstrings
- **Performance**: Chrome ~18% mais rápido que Firefox

### ⚡ Performance Estimada (Chrome)

| Métrica | v2.1.0 (Firefox) | v3.0.0 (Chrome) | Melhoria |
|---------|------------------|-----------------|----------|
| Tempo/protocolo | 30.6s | ~25.2s | -18% |
| Consumo RAM | 820MB | ~580MB | -29% |
| Delay fechamento | 3s | 1s | -67% |
| Erros timeout | 5% | ~2% (estimado) | -60% |

### 🔧 Configuração

**Usar Chrome (padrão):**
```bash
# Nada necessário, Chrome é padrão
python WallBot_v3.py
```

**Usar Firefox (legado):**
```bash
# Variável de ambiente
export WALLBOT_NAVEGADOR=firefox
python WallBot_v3.py

# Ou via código
from drivers import DriverFactory
driver = DriverFactory.criar_driver('firefox')
```

**Configurar timeout:**
```bash
export WALLBOT_TIMEOUT=20  # 20 segundos
export WALLBOT_MAX_RECONEXAO=5  # 5 tentativas
```

### 📚 Uso da Nova Arquitetura

**Exemplo 1: Criar driver Chrome**
```python
from drivers import DriverFactory

# Criar Chrome (padrão)
driver_wrapper = DriverFactory.criar_driver()
driver = driver_wrapper.driver

# Usar driver
driver.get('https://cartoes.extracaixa/')

# Fechar
driver_wrapper.fechar_seguro()
```

**Exemplo 2: Usar seletores**
```python
from selectors import SIACHSelectors

# Encontrar elemento
username_field = driver.find_element(*SIACHSelectors.LOGIN_USERNAME)
username_field.send_keys('usuario@email.com')

# Verificar fase
from selectors.siach_selectors import FasesProtocolo
if FasesProtocolo.pode_finalizar('ABERTA'):
    print("Protocolo pode ser finalizado")
```

**Exemplo 3: Validar página**
```python
from validators import validar_pagina_siach, verificar_sessao_valida

# Validar tipo de página
resultado = validar_pagina_siach(driver, timeout=10)
print(f"Página: {resultado['tipo_pagina']}")  # 'login', 'menu', 'protocolo'

# Verificar se sessão expirou
if not verificar_sessao_valida(driver):
    print("Sessão expirada, fazer login novamente")
```

### 🧪 Testes

Cada módulo possui bloco `if __name__ == "__main__"` para testes:

```bash
# Testar seletores
python selectors/siach_selectors.py

# Testar validadores
python validators/page_validators.py

# Testar config
python config/config.py

# Testar driver Chrome
python drivers/chrome_driver.py

# Testar factory
python drivers/driver_factory.py
```

### 📦 Dependências

Nova `requirements.txt`:
```
selenium==4.15.2
webdriver-manager==4.0.1
openpyxl==3.1.2
customtkinter==5.2.0
python-dotenv==1.0.0
```

### ⚠️ Limitações Conhecidas (Alpha)

- WallBot_Firefox.py ainda não refatorado (usa código legado)
- Interface UI ainda monolítica (327 linhas)
- Função `fechamento_em_lote()` ainda longa (193 linhas)
- Sem testes automatizados ainda
- Sem integração com CI/CD

### 🎯 Próximos Passos (v3.0.0-alpha.2)

1. Refatorar `WallBot_Firefox.py` para usar novos módulos
2. Criar `WallBot_v3.py` 100% modular
3. Separar UI em módulos (`ui/forms.py`, `ui/stats_panel.py`, etc)
4. Reduzir `fechamento_em_lote()` para ~80 linhas
5. Implementar testes unitários
6. Documentar arquitetura completa

### 📖 Documentação

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Arquitetura detalhada dos módulos (em breve)
- [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) - Guia de migração v2→v3 (em breve)

### 🔗 Links Relacionados

- Commit: `TBD` (após commit)
- Pull Request: `TBD`
- Issues resolvidas: #3 (parcial), #4 (parcial)

---

## [2.1.0] - 2025-10-23 - ✅ STABLE

**Navegador:** Firefox
**Tag Git:** `v2.1.0-firefox-stable`
**Linhas de Código:** 1100

### Adicionado
- Sistema de reconexão automática (até 3 tentativas)
- Suporte a processamento de Protocolos e Ocorrências
- Personalização de scripts com `@NomeCliente@`
- Estatísticas em tempo real (thread-safe)
- Validação robusta de entrada (arquivo Excel, campos obrigatórios)
- Gerenciador de log com context manager
- Checkpoint de progresso persistente
- Interface gráfica moderna com CustomTkinter
- Modo append para Excel de resultados
- Botão "Limpar Histórico"
- Botão "Resetar Progresso"

### Melhorado
- Sistema de tratamento de exceções mais robusto
- Logs mais detalhados com timestamps
- Gerenciamento de estado thread-safe
- Fechamento seguro do Firefox

### Configurações
```python
CONFIG = {
    'TIMEOUT_PADRAO': 15,
    'TIMEOUT_SALVAR': 30,
    'MAX_TENTATIVAS_RECONEXAO': 3,
    'ESPERA_ENTRE_ACOES': 1.0
}
```

### Problemas Conhecidos
- Race condition no loop de reconexão (Issue #1)
- Timeout de script JavaScript não configurado (Issue #3)
- Fechamento do Firefox pode travar (Issue #4)
- Tentativas de login duplicadas na reconexão (Issue #5)
- Firefox consome 33% mais memória que Chrome
- Performance 18% mais lenta que Chrome

### Notas
- Esta é a última versão estável com Firefox
- Use esta versão como fallback se v3.x tiver problemas
- Para reverter: `git checkout v2.1.0-firefox-stable`

---

## [2.0.0] - 2025-10-15 - 🗂️ DEPRECATED

**Navegador:** Chrome
**Tag Git:** `v2.0.0-chrome`
**Status:** Descontinuado (versão Chrome anterior, substituída pela v2.1.0 Firefox)

### Adicionado
- Sistema de estatísticas em tempo real
- Personalização de scripts
- Validação de entrada
- Interface CustomTkinter

### Problemas
- Sem sistema de reconexão
- Sem tratamento robusto de erros de conexão

---

## [1.1.0] - 2025-09-20 - 🗂️ DEPRECATED

**Navegador:** Chrome
**Tag Git:** `v1.1.0-chrome`
**Arquivo:** `Fechamento em lote - Ocorrências.py`, `Fechamento em lote - Protocolos.py`
**Linhas de Código:** 395

### Problemas Críticos
- ❌ Credenciais hardcoded (linhas 72-73)
- ❌ Recursão infinita em TimeoutException (linha 280)
- ❌ Loop infinito sem limite de tentativas (linha 60)
- ❌ Arquivo de log pode não ser fechado corretamente

### ⚠️ AVISO DE SEGURANÇA
Esta versão contém credenciais expostas no código. NÃO USAR.

---

## Roadmap - Versões Futuras

### [3.0.0] - Planejada para 2025-11-15 - 🔬 ALPHA

**Navegador:** Chrome (MIGRAÇÃO)
**Breaking Changes:** Sim
**Estimativa:** 2-3 semanas de desenvolvimento

#### Mudanças Planejadas

**Adicionado:**
- ✨ Migração para Chrome (ganho de 18% performance)
- ✨ Classe `SeletoresSIACH` - Centralização de seletores XPath
- ✨ Função `validar_pagina_siach()` - Validação de página
- ✨ Função `detectar_pagina_manutencao()` - Detecção de manutenção
- ✨ Função `verificar_sessao_valida()` - Verificação de sessão
- ✨ Classe `TimeoutAdaptativo` - Timeouts que se adaptam
- ✨ Função `fechar_driver_seguro_v2()` - Com watchdog timer

**Alterado:**
- 🔄 `criar_driver()` - Chrome ao invés de Firefox
- 🔄 `fechar_driver_seguro()` - Sem sleep de 3s
- 🔄 `fechamento_em_lote()` - Simplificado (200 → 80 linhas)
- 🔄 Tratamento de exceções centralizado

**Removido:**
- ❌ Imports específicos do Firefox
- ❌ Configurações específicas do Firefox
- ❌ Código duplicado de tratamento de erro

**Corrigido:**
- 🐛 Race condition no loop de reconexão (Issue #1)
- 🐛 Timeout de script não configurado (Issue #3)
- 🐛 Fechamento do driver travando (Issue #4)
- 🐛 Tentativas de login duplicadas (Issue #5)

**Performance:**
- ⚡ Tempo por protocolo: 30.6s → 25.2s (-18%)
- ⚡ Consumo de RAM: 820MB → 580MB (-29%)
- ⚡ Erros de timeout: 5% → 2% (-60%)
- ⚡ Linhas de código: 1100 → ~700 (-36%)

#### Fases de Desenvolvimento

**Fase 1: Preparação** (Dias 1-2)
- [ ] Criar branch `feature/v3.0.0-chrome-migration`
- [ ] Backup da v2.1.0
- [ ] Script de teste com 10 protocolos
- [ ] Tag `v3.0.0-alpha.1`

**Fase 2: Migração Chrome** (Dias 3-5)
- [ ] Implementar `NavegadorFactory`
- [ ] Migrar `criar_driver()` para Chrome
- [ ] Testes com 10 protocolos
- [ ] Tag `v3.0.0-alpha.2`

**Fase 3: Refatoração** (Dias 6-9)
- [ ] Criar `seletores.py`
- [ ] Criar `validadores.py`
- [ ] Refatorar funções longas
- [ ] Tag `v3.0.0-alpha.3`

**Fase 4: Features Avançadas** (Dias 10-12)
- [ ] Timeouts adaptativos
- [ ] Watchdog timer
- [ ] Verificação de sessão
- [ ] Tag `v3.0.0-beta.1`

**Fase 5: Testes** (Dias 13-15)
- [ ] Testes com 100+ protocolos
- [ ] Testes de estresse (2h contínuo)
- [ ] Benchmark completo
- [ ] Tag `v3.0.0-beta.2`

**Fase 6: Release** (Dia 16)
- [ ] Deploy gradual (10% → 50% → 100%)
- [ ] Monitoramento
- [ ] Tag `v3.0.0` (STABLE)

#### Critérios de Aceitação para v3.0.0 STABLE

- ✅ Taxa de sucesso ≥ 95%
- ✅ Erros de timeout ≤ 2%
- ✅ Reconexão funciona em 100% dos testes
- ✅ Sem vazamento de memória em 2h de execução
- ✅ Performance 15%+ melhor que v2.1.0
- ✅ Todos os testes automatizados passando
- ✅ Documentação atualizada
- ✅ Aprovação de 5 usuários piloto

---

### [3.1.0] - Planejada para 2025-12-01

**Melhorias Incrementais**

- Separação de UI em módulo próprio
- Sistema de plugins
- Suporte a múltiplos perfis de usuário
- Export de relatórios em PDF
- Dashboard de métricas

---

### [4.0.0] - Planejada para 2026-Q1

**Reescrita Completa**

- Arquitetura baseada em microserviços
- API REST para integração
- Processamento paralelo de protocolos
- Machine Learning para detecção de anomalias
- Interface web (além do desktop)

---

## Como Usar Este Changelog

### Para Desenvolvedores

**Adicionar nova entrada:**
```markdown
## [X.Y.Z] - YYYY-MM-DD - STATUS

### Adicionado
- Nova funcionalidade X

### Alterado
- Mudança em Y

### Corrigido
- Bug Z corrigido

### Removido
- Funcionalidade obsoleta W
```

**Criar nova versão:**
```bash
# 1. Atualizar CHANGELOG.md
# 2. Atualizar VERSION.py
# 3. Commit
git add CHANGELOG.md VERSION.py
git commit -m "chore: bump version to vX.Y.Z"

# 4. Criar tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# 5. Push
git push origin vX.Y.Z
```

### Para Usuários

**Ver versão atual:**
```python
from VERSION import __version__
print(__version__)  # 2.1.0
```

**Reverter para versão anterior:**
```bash
# Ver versões disponíveis
git tag -l

# Reverter para versão específica
git checkout v2.1.0-firefox-stable

# Ou criar branch a partir da versão
git checkout -b hotfix-from-v2.1.0 v2.1.0-firefox-stable
```

**Comparar versões:**
```bash
# Ver mudanças entre versões
git diff v2.1.0-firefox-stable v3.0.0

# Ver arquivos alterados
git diff --name-only v2.1.0-firefox-stable v3.0.0
```

---

## Política de Suporte

| Versão | Status | Suporte até | Navegador |
|--------|--------|-------------|-----------|
| 3.x.x | Em Desenvolvimento | - | Chrome |
| 2.1.x | ✅ STABLE | 2026-01-01 | Firefox |
| 2.0.x | 🗂️ DEPRECATED | 2025-11-01 | Chrome |
| 1.x.x | 🗂️ DEPRECATED | Encerrado | Chrome |

**Tipos de Suporte:**
- **Ativo**: Correções de bugs, melhorias, novas features
- **Manutenção**: Apenas correções críticas de segurança/bugs
- **Deprecated**: Sem suporte, migre para versão mais recente
- **Encerrado**: Sem suporte algum

---

## Notas de Migração

### De v2.1.0 (Firefox) para v3.0.0 (Chrome)

**Pré-requisitos:**
- Chrome instalado
- ChromeDriver será baixado automaticamente

**Breaking Changes:**
- Navegador muda de Firefox para Chrome
- Algumas configurações Firefox-specific removidas

**Passos:**
1. Backup da versão atual
2. Atualizar para v3.0.0
3. Testar com 10 protocolos
4. Se problemas, reverter: `git checkout v2.1.0-firefox-stable`

**Rollback:**
```bash
# Reverter para versão estável anterior
git checkout v2.1.0-firefox-stable
python "Necxt - Caixa/WallBot_Firefox.py"
```

---

## Links Úteis

- [Semantic Versioning](https://semver.org/lang/pt-BR/)
- [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)
- [Conventional Commits](https://www.conventionalcommits.org/pt-br/)
- [Plano de Melhoria Completo](./PLANO_MELHORIA_WALLBOT.md)
- [Issues do Projeto](./ISSUES_GITHUB.md)

---

**Legenda de Emojis:**
- ✨ Nova funcionalidade
- 🐛 Correção de bug
- 🔄 Mudança/Refatoração
- ⚡ Melhoria de performance
- 🔒 Segurança
- 📝 Documentação
- ❌ Remoção
- ⚠️ Deprecated
- 🗂️ Arquivado

---

*Última atualização: 2025-10-29*
*Mantido por: Equipe WallBot*
