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

### Em Planejamento
- Migração de Firefox para Chrome
- Centralização de seletores XPath
- Sistema de validação de páginas
- Timeouts adaptativos
- Refatoração e simplificação de código

---

## [2.1.0] - 2025-10-23 - ✅ STABLE (ATUAL)

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
