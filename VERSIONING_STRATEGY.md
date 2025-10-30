# Estratégia de Versionamento - WallBot SIACH

Este documento descreve a estratégia de versionamento, release e rollback do projeto WallBot.

---

## 📋 Índice

1. [Versionamento Semântico](#versionamento-semântico)
2. [Estrutura de Branches](#estrutura-de-branches)
3. [Sistema de Tags](#sistema-de-tags)
4. [Processo de Release](#processo-de-release)
5. [Estratégia de Rollback](#estratégia-de-rollback)
6. [Testes por Versão](#testes-por-versão)
7. [Comunicação de Mudanças](#comunicação-de-mudanças)

---

## 1. Versionamento Semântico

Seguimos o padrão **Semantic Versioning 2.0.0** (SemVer):

### Formato: `MAJOR.MINOR.PATCH`

```
v3.2.1
│ │ │
│ │ └─ PATCH: Correção de bugs (backward compatible)
│ └─── MINOR: Novas funcionalidades (backward compatible)
└───── MAJOR: Mudanças incompatíveis (breaking changes)
```

### Regras de Incremento

| Tipo de Mudança | Versão | Exemplo |
|-----------------|--------|---------|
| Breaking change (muda navegador, API, interface) | MAJOR | 2.1.0 → 3.0.0 |
| Nova funcionalidade (mantém compatibilidade) | MINOR | 3.0.0 → 3.1.0 |
| Correção de bug | PATCH | 3.1.0 → 3.1.1 |
| Correção crítica de segurança | PATCH | 3.1.1 → 3.1.2 |

### Exemplos Práticos

**MAJOR (Breaking Change):**
```python
# v2.1.0 → v3.0.0
# Mudança: Firefox → Chrome
# Motivo: Usuário precisa ter Chrome instalado (breaking)

# v3.5.0 → v4.0.0
# Mudança: Interface desktop → Interface web
# Motivo: Muda completamente como o usuário acessa (breaking)
```

**MINOR (Nova Feature):**
```python
# v3.0.0 → v3.1.0
# Adicionado: Export de relatórios em PDF
# Motivo: Nova funcionalidade, mas não quebra nada existente

# v3.1.0 → v3.2.0
# Adicionado: Suporte a temas claro/escuro
# Motivo: Nova feature opcional
```

**PATCH (Bug Fix):**
```python
# v3.0.0 → v3.0.1
# Corrigido: Race condition no loop de reconexão
# Motivo: Apenas correção, sem novas features

# v3.0.1 → v3.0.2
# Corrigido: Vazamento de memória após 100 protocolos
# Motivo: Bug fix crítico
```

---

## 2. Estrutura de Branches

### Branches Principais

```
main (produção)
├── develop (desenvolvimento)
├── release/v3.0.0 (preparação de release)
├── feature/chrome-migration (features)
├── hotfix/v2.1.1-memory-leak (correções urgentes)
└── stable/v2.1.x (versão estável anterior)
```

### Descrição das Branches

#### `main`
- **Propósito:** Código em produção
- **Proteção:** Apenas merges de `release/*` ou `hotfix/*`
- **Tags:** Todas as versões stable (`v3.0.0`, `v3.1.0`, etc.)

#### `develop`
- **Propósito:** Integração de features
- **Base:** Sempre sincronizada com `main`
- **Merges:** De `feature/*` branches

#### `release/vX.Y.Z`
- **Propósito:** Preparação de nova versão
- **Criada de:** `develop`
- **Merge para:** `main` e `develop`
- **Duração:** Temporária (deletada após merge)

#### `feature/nome-da-feature`
- **Propósito:** Desenvolvimento de nova funcionalidade
- **Criada de:** `develop`
- **Merge para:** `develop`
- **Nomenclatura:** `feature/chrome-migration`, `feature/pdf-export`

#### `hotfix/vX.Y.Z-descricao`
- **Propósito:** Correção urgente em produção
- **Criada de:** `main`
- **Merge para:** `main` e `develop`
- **Nomenclatura:** `hotfix/v2.1.1-memory-leak`

#### `stable/vX.Y.x`
- **Propósito:** Manter versão estável anterior para rollback
- **Criada de:** Tag da última versão estável
- **Proteção:** Read-only (exceto hotfixes críticos)
- **Exemplo:** `stable/v2.1.x` (última versão Firefox estável)

### Fluxo de Trabalho

```
┌─────────┐
│  main   │ ◄─── Produção
└────┬────┘
     │
     │ tag v3.0.0
     │
┌────▼────────┐
│ release/v3  │ ◄─── Release Candidate
└────┬────────┘
     │
     │ merge
     │
┌────▼────────┐
│   develop   │ ◄─── Integração
└─┬──┬──┬─────┘
  │  │  │
  │  │  └─ feature/timeouts-adaptativos
  │  └──── feature/validacao-pagina
  └─────── feature/chrome-migration
```

---

## 3. Sistema de Tags

### Formato de Tags

```
vMAJOR.MINOR.PATCH[-PRE_RELEASE][+BUILD_METADATA]
```

### Tipos de Tags

#### Stable Release
```bash
v3.0.0              # Release estável
v3.1.0              # Minor update
v3.1.1              # Patch
```

#### Pre-Release
```bash
v3.0.0-alpha.1      # Alpha 1
v3.0.0-alpha.2      # Alpha 2
v3.0.0-beta.1       # Beta 1
v3.0.0-beta.2       # Beta 2
v3.0.0-rc.1         # Release Candidate 1
```

#### Com Build Metadata
```bash
v3.0.0-beta.1+20251029    # Beta com data
v3.0.0+chrome             # Build específico
v2.1.0-firefox-stable     # Tag descritiva
```

### Criando Tags

**Stable Release:**
```bash
git tag -a v3.0.0 -m "Release v3.0.0 - Migração para Chrome

- Migração de Firefox para Chrome
- Performance +18%
- Memória -29%
- 700 linhas de código (-36%)

Breaking Changes:
- Navegador mudou de Firefox para Chrome

Veja CHANGELOG.md para detalhes completos."

git push origin v3.0.0
```

**Pre-Release:**
```bash
git tag -a v3.0.0-alpha.1 -m "Alpha 1 - Migração Chrome inicial"
git push origin v3.0.0-alpha.1
```

**Versão Estável para Rollback:**
```bash
git tag -a v2.1.0-firefox-stable -m "Última versão estável Firefox

Esta tag marca a última versão estável com Firefox.
Use para rollback se v3.x tiver problemas críticos.

Rollback: git checkout v2.1.0-firefox-stable"

git push origin v2.1.0-firefox-stable
```

### Listando Tags

```bash
# Todas as tags
git tag -l

# Tags de uma versão específica
git tag -l "v3.0.*"

# Tags stable
git tag -l "*-stable"

# Tags com mensagens
git tag -l -n9
```

---

## 4. Processo de Release

### Ciclo de Vida de uma Release

```
1. Planejamento
   ↓
2. Desenvolvimento (feature branches)
   ↓
3. Integração (develop)
   ↓
4. Release Candidate (release/vX.Y.Z)
   ↓
5. Testes (alpha → beta → rc)
   ↓
6. Release Stable (main + tag)
   ↓
7. Monitoramento
```

### Passo a Passo Detalhado

#### Fase 1: Planejamento

```bash
# 1. Criar issue de planejamento
# - Listar features/bugs a serem incluídos
# - Definir breaking changes
# - Estimar data de release

# 2. Atualizar CHANGELOG.md seção [Unreleased]
```

#### Fase 2: Desenvolvimento

```bash
# Para cada feature:

# 1. Criar feature branch
git checkout develop
git pull origin develop
git checkout -b feature/chrome-migration

# 2. Desenvolver

# 3. Commit seguindo Conventional Commits
git commit -m "feat: adiciona suporte a Chrome

- Implementa NavegadorFactory
- Migra criar_driver() para Chrome
- Remove dependências Firefox

BREAKING CHANGE: Navegador mudou de Firefox para Chrome"

# 4. Push e criar Pull Request
git push origin feature/chrome-migration

# 5. Code Review

# 6. Merge para develop
git checkout develop
git merge feature/chrome-migration
git push origin develop
```

#### Fase 3: Release Candidate

```bash
# 1. Criar branch de release
git checkout develop
git pull origin develop
git checkout -b release/v3.0.0

# 2. Atualizar VERSION.py
__version__ = "3.0.0"
__navegador__ = "chrome"
__status__ = "rc"

# 3. Atualizar CHANGELOG.md
# Mover [Unreleased] para [3.0.0] - YYYY-MM-DD

# 4. Commit
git commit -m "chore: prepare release v3.0.0"

# 5. Criar tag RC
git tag -a v3.0.0-rc.1 -m "Release Candidate 1"
git push origin v3.0.0-rc.1

# 6. Deploy para ambiente de testes
```

#### Fase 4: Testes

```bash
# Alpha (testes internos)
git tag -a v3.0.0-alpha.1 -m "Alpha 1"

# Beta (testes com usuários selecionados)
git tag -a v3.0.0-beta.1 -m "Beta 1"

# Release Candidate (candidato a produção)
git tag -a v3.0.0-rc.1 -m "Release Candidate 1"
```

**Checklist de Testes:**
- [ ] Testes funcionais (10 protocolos)
- [ ] Testes de carga (100 protocolos)
- [ ] Testes de estresse (2h contínuo)
- [ ] Testes de reconexão
- [ ] Testes de memória
- [ ] Testes de rollback
- [ ] Validação com usuários piloto

#### Fase 5: Release Stable

```bash
# 1. Merge para main
git checkout main
git pull origin main
git merge --no-ff release/v3.0.0 -m "Release v3.0.0"

# 2. Criar tag stable
git tag -a v3.0.0 -m "Release v3.0.0 - Migração Chrome"

# 3. Merge de volta para develop
git checkout develop
git merge --no-ff main

# 4. Push tudo
git push origin main develop
git push origin v3.0.0

# 5. Deletar branch de release
git branch -d release/v3.0.0
git push origin --delete release/v3.0.0

# 6. Criar branch stable para versão anterior
git checkout v2.1.0-firefox-stable
git checkout -b stable/v2.1.x
git push origin stable/v2.1.x

# 7. Atualizar VERSION.py no develop para próxima versão
git checkout develop
# Editar VERSION.py: __version__ = "3.1.0-dev"
git commit -m "chore: bump version to v3.1.0-dev"
git push origin develop
```

#### Fase 6: Deploy e Monitoramento

```bash
# 1. Deploy gradual
# - 10% dos usuários
# - Monitorar por 24h
# - 50% dos usuários
# - Monitorar por 48h
# - 100% dos usuários

# 2. Monitorar métricas
# - Taxa de sucesso
# - Erros de timeout
# - Consumo de memória
# - Performance

# 3. Se problemas críticos → Rollback
# Se OK → Comunicar release
```

---

## 5. Estratégia de Rollback

### Cenários de Rollback

1. **Bug Crítico em Produção**
2. **Performance Inaceitável**
3. **Muitos Usuários Reportando Problemas**
4. **Incompatibilidade Não Prevista**

### Níveis de Rollback

#### Nível 1: Rollback para Última Tag Stable

**Quando:** Bug menor em PATCH

```bash
# Cenário: v3.0.1 tem bug, voltar para v3.0.0
git checkout v3.0.0
git checkout -b hotfix/v3.0.2-fix-bug
# Corrigir bug
git commit -m "fix: corrige bug X"
git checkout main
git merge hotfix/v3.0.2-fix-bug
git tag -a v3.0.2 -m "Hotfix v3.0.2"
git push origin main v3.0.2
```

**Tempo estimado:** 1-2 horas

#### Nível 2: Rollback para Versão Estável Anterior

**Quando:** Problemas graves em nova MAJOR version

```bash
# Cenário: v3.0.0 (Chrome) tem problemas sérios
# Voltar para v2.1.0 (Firefox)

# 1. Checkout da versão estável anterior
git checkout v2.1.0-firefox-stable

# 2. Criar branch temporária
git checkout -b rollback-to-v2.1.0

# 3. Merge para main (force)
git checkout main
git reset --hard v2.1.0-firefox-stable

# 4. Push (requer force)
git push origin main --force-with-lease

# 5. Comunicar rollback
# 6. Investigar problemas da v3.0.0
```

**Tempo estimado:** 15-30 minutos

⚠️ **ATENÇÃO:** Rollback com `--force` é perigoso. Comunicar toda a equipe antes.

#### Nível 3: Rollback Progressivo

**Quando:** Problemas afetam apenas alguns usuários

```bash
# Manter v3.0.0 no main
# Mas distribuir v2.1.0 para usuários afetados

# 1. Disponibilizar v2.1.0 como download alternativo
# 2. Documentar workaround
# 3. Corrigir v3.0.0 em paralelo
# 4. Release v3.0.1 com correções
```

**Tempo estimado:** Variável

### Processo de Decisão de Rollback

```
Problema Identificado
         ↓
    Severidade?
    /    |    \
Baixa  Média  Alta
  ↓      ↓      ↓
PATCH  MINOR  ROLLBACK
```

**Severidade:**

- **Baixa:** <5% usuários afetados, workaround disponível → Patch
- **Média:** 5-20% usuários afetados, workaround complexo → Hotfix urgente
- **Alta:** >20% usuários afetados, sem workaround → Rollback imediato

### Checklist de Rollback

**Antes do Rollback:**
- [ ] Confirmar severidade do problema
- [ ] Documentar o problema
- [ ] Verificar se há workaround
- [ ] Avisar stakeholders
- [ ] Backup dos dados atuais

**Durante o Rollback:**
- [ ] Executar rollback
- [ ] Testar versão restaurada
- [ ] Monitorar logs
- [ ] Confirmar que problema foi resolvido

**Após o Rollback:**
- [ ] Comunicar usuários
- [ ] Atualizar documentação
- [ ] Criar post-mortem
- [ ] Planejar correção
- [ ] Implementar testes para prevenir regressão

---

## 6. Testes por Versão

### Matriz de Testes

| Tipo de Teste | PATCH | MINOR | MAJOR |
|---------------|-------|-------|-------|
| Unitários | ✅ | ✅ | ✅ |
| Integração | ⚠️ | ✅ | ✅ |
| Regressão | ❌ | ⚠️ | ✅ |
| Performance | ❌ | ⚠️ | ✅ |
| Estresse | ❌ | ❌ | ✅ |
| Usuário Piloto | ❌ | ⚠️ | ✅ |

✅ Obrigatório | ⚠️ Recomendado | ❌ Opcional

### Plano de Testes para v3.0.0 (MAJOR)

**Fase Alpha:**
```bash
# Testes Internos
- Funcional: 10 protocolos
- Verificar: login, processamento, salvamento

# Critério de Passagem:
- 100% funcionalidades básicas OK
```

**Fase Beta:**
```bash
# Testes com 5 Usuários Piloto
- Carga: 50-100 protocolos cada
- Cenários: protocolos normais + edge cases

# Critério de Passagem:
- 90% taxa de sucesso
- <5% erros de timeout
- Feedback positivo de 4/5 usuários
```

**Fase RC:**
```bash
# Testes Pré-Produção
- Estresse: 2h contínuo (200+ protocolos)
- Memória: monitorar vazamentos
- Reconexão: forçar desconexões

# Critério de Passagem:
- 95% taxa de sucesso
- <2% erros
- Sem vazamento de memória
- Reconexão 100% funcional
```

### Automação de Testes

```python
# tests/test_version_compatibility.py

def test_version_backward_compatibility():
    """
    Testa se nova versão lê dados da versão anterior
    """
    # Carregar dados salvos por v2.1.0
    data_v2 = load_results("resultado_v2.1.0.xlsx")

    # Processar com v3.0.0
    # ...

    assert can_read(data_v2)

def test_performance_regression():
    """
    Garante que performance não piorou
    """
    tempo_v3 = processar_10_protocolos()
    tempo_v2_referencia = 306  # 30.6s por protocolo

    assert tempo_v3 < tempo_v2_referencia
```

---

## 7. Comunicação de Mudanças

### Canais de Comunicação

1. **CHANGELOG.md** - Registro técnico detalhado
2. **Release Notes** - Comunicado aos usuários
3. **Email** - Notificação de releases importantes
4. **README.md** - Versão atual e instruções de instalação

### Template de Release Notes

```markdown
# 🚀 WallBot v3.0.0 - Migração para Chrome

**Data de Release:** 15 de novembro de 2025
**Status:** STABLE
**Tipo:** MAJOR (Breaking Changes)

## 🎯 Destaques

- **18% mais rápido** que versão anterior
- **29% menos memória** utilizada
- **60% menos erros** de timeout
- **Mais estável** e confiável

## ✨ Novidades

- Migração de Firefox para Chrome (melhor performance)
- Validação automática de páginas SIACH
- Detecção de sistema em manutenção
- Timeouts adaptativos (se adapta à velocidade)
- Código 36% mais simples e manutenível

## 🔄 Mudanças que Afetam Você

- **IMPORTANTE:** Agora usa Chrome ao invés de Firefox
- **Requisito:** Chrome deve estar instalado
- **Compatibilidade:** Arquivos de resultados compatíveis com v2.x

## 🐛 Correções

- Corrigida race condition no sistema de reconexão
- Corrigido timeout de script JavaScript
- Corrigido vazamento de memória em longas sessões
- Melhorado tratamento de erros

## ⬆️ Como Atualizar

```bash
# Backup da versão atual
git checkout v2.1.0-firefox-stable
# Salvar em local seguro

# Atualizar para v3.0.0
git checkout v3.0.0

# Testar com poucos protocolos primeiro
python "Necxt - Caixa/WallBot_Chrome.py"
```

## 🔙 Rollback (Se Necessário)

Se encontrar problemas, você pode voltar para versão anterior:

```bash
git checkout v2.1.0-firefox-stable
```

## 📊 Benchmark

| Métrica | v2.1.0 | v3.0.0 | Melhoria |
|---------|--------|--------|----------|
| Tempo/100 protocolos | 51 min | 42 min | -18% |
| Memória | 820MB | 580MB | -29% |
| Erros | 5% | 2% | -60% |

## 🙋 Suporte

- Dúvidas: abrir issue no GitHub
- Bugs: reportar com logs anexados
- Melhorias: sugerir na issue de feedback

## 📚 Documentação

- [CHANGELOG Completo](./CHANGELOG.md)
- [Plano de Melhoria](./PLANO_MELHORIA_WALLBOT.md)
- [Guia de Migração](./MIGRATION_GUIDE.md)

---

**Agradecimentos** à equipe de testes e usuários piloto!
```

---

## Resumo - Quick Reference

### Criar Nova Versão

```bash
# 1. Feature → develop
git checkout develop
git merge feature/xyz

# 2. develop → release
git checkout -b release/vX.Y.Z
# Atualizar VERSION.py, CHANGELOG.md
git commit -m "chore: prepare release vX.Y.Z"

# 3. release → main
git checkout main
git merge --no-ff release/vX.Y.Z
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# 4. Push
git push origin main develop vX.Y.Z
```

### Rollback Rápido

```bash
# Para versão anterior
git checkout vX.Y.Z-1
git checkout -b rollback
git checkout main
git reset --hard vX.Y.Z-1
git push origin main --force-with-lease
```

### Ver Versão Atual

```python
from VERSION import get_version_string
print(get_version_string())
# "WallBot v3.0.0 (Chrome) - STABLE"
```

---

*Documento mantido por: Equipe DevOps WallBot*
*Última atualização: 2025-10-29*
