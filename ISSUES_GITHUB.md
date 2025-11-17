# Issues para Abrir no GitHub - Projeto Necxt - Caixa

Este documento contém as issues que devem ser criadas no repositório GitHub para rastrear as falhas críticas identificadas na análise técnica.

---

## Issue #1: [CRÍTICO] Race Condition no Loop de Reconexão do WallBot

### Labels
`bug`, `priority: high`, `WallBot`, `Firefox`

### Título
🔴 [CRÍTICO] Race Condition no loop de reconexão automática causa vazamento de driver

### Descrição

**Arquivo:** `Necxt - Caixa/WallBot.py`
**Linhas:** 660-735
**Severidade:** ALTA

#### Problema

O loop de reconexão automática do WallBot possui uma race condition que pode causar:
- Vazamento de processos do Firefox (driver não fechado corretamente)
- Protocolos ficarem presos em loop infinito
- Estado inconsistente entre progresso salvo e real
- Consumo excessivo de memória

#### Cenário de Falha

**Cenário 1: Usuário clica "Parar" durante reconexão**
```
1. Erro de conexão detectado
2. tentativas_reconexao = 1
3. fechar_driver_seguro(driver) - OK
4. Loop de espera de 5s inicia
5. Usuário clica "Parar" no segundo 2
6. estado_app.parar() é chamado
7. Loop detecta e faz return
8. ❌ PROBLEMA: Driver novo pode estar sendo criado em segundo plano
9. ❌ PROBLEMA: Variável driver pode ficar dessincronizada
10. ❌ PROBLEMA: Nenhum cleanup é feito
```

**Cenário 2: Reconexão falha mas protocolo atual fica preso**
```
1. Protocolo #50 causa erro de conexão
2. tentativas_reconexao = 1
3. Reconexão falha (retorna None)
4. break é executado
5. ❌ PROBLEMA: Progresso NÃO é salvo
6. ❌ PROBLEMA: Protocolo #50 nunca será marcado como erro
7. ❌ RESULTADO: Loop infinito no protocolo #50 ao reiniciar
```

#### Código Problemático

```python
except WebDriverException as e:
    erro_msg = str(e)
    erros_conexao = ['HTTPConnectionPool', 'Read timed out', 'target frame detached',
                     'Connection refused', 'Reached error page', 'connection was refused']

    if any(erro in erro_msg for erro in erros_conexao):
        if tentativas_reconexao < CONFIG['MAX_TENTATIVAS_RECONEXAO']:
            tentativas_reconexao += 1

            # ⚠️ PROBLEMA: Driver pode ser usado por outra thread aqui
            fechar_driver_seguro(driver, logger)

            # ⚠️ PROBLEMA: Durante estes 5 segundos, o estado pode mudar
            for segundo in range(5):
                if not estado_app.esta_executando():
                    return  # ❌ Sai sem fechar driver!
                time.sleep(1)

            driver_novo, sipcs_novo, siach_novo = reconectar_driver(email, senha, logger)

            if driver_novo:
                driver = driver_novo  # ⚠️ Antiga referência pode ainda estar sendo usada
                # ...
                continue  # ❌ NÃO incrementa i - tenta novamente
```

#### Solução Proposta

1. **Adicionar locks ao atualizar `driver`:**
```python
with estado_app._lock:
    fechar_driver_seguro(driver, logger)
    driver = None
```

2. **Salvar progresso antes de retornar em cancelamento:**
```python
if not estado_app.esta_executando():
    logger.escrever("Reconexão cancelada pelo usuário")
    salvar_progresso(i)
    resultado = {
        'Protocolo': valor,
        'Status': 'Erro',
        'Mensagem': 'Reconexão cancelada pelo usuário',
        'DataHora': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    results.append(resultado)
    return
```

3. **Registrar erro quando reconexão falha:**
```python
else:
    logger.escrever("Falha na reconexão.")
    resultado = {
        'Protocolo': valor,
        'Status': 'Erro',
        'Mensagem': 'Falha na reconexão após erro de conexão',
        'DataHora': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    results.append(resultado)
    estatisticas.adicionar('Erro')
    stats_callback()
    salvar_progresso(i + 1)
    break
```

#### Referência

Ver análise completa em: `Necxt - Caixa/ANALISE_WallBot.md` (seção 3, CRÍTICA 1)

---

## Issue #2: [CRÍTICO] Versões v1 possuem recursão infinita e credenciais hardcoded

### Labels
`bug`, `priority: critical`, `security`, `WallBot`, `v1`

### Título
🔴 [CRÍTICO] Versões v1 contêm credenciais hardcoded e recursão infinita

### Descrição

**Arquivos:**
- `Necxt - Caixa/Fechamento em lote - Ocorrências.py`
- `Necxt - Caixa/Fechamento em lote - Protocolos.py`

**Severidade:** CRÍTICA
**Impacto:** Segurança + Estabilidade

#### Problema 1: Credenciais Hardcoded (SEGURANÇA)

**Linhas:** 72-73

```python
usuario.send_keys('wbsouza1@stefanini.com')
senha.send_keys('Barbara05')
```

**Riscos:**
- ❌ Violação crítica de segurança
- ❌ Credenciais expostas no código fonte
- ❌ Credenciais no histórico do Git
- ❌ Risco de comprometimento de contas
- ❌ Impossível de usar por outros usuários

#### Problema 2: Recursão Infinita em TimeoutException

**Linhas:** 268-281

```python
except TimeoutException as e:
    mensagem = f'TimeoutException: Protocolo {valor}'
    print(mensagem)
    driver.quit()
    fechamento_em_lote()  # ❌ CHAMA A FUNÇÃO NOVAMENTE - RECURSÃO INFINITA!
    return
```

**Impacto:**
- ❌ Stack overflow após múltiplos timeouts
- ❌ Consumo excessivo de memória
- ❌ Perda de contexto de progresso
- ❌ Aplicação trava completamente

#### Problema 3: Loop Infinito sem Limite de Tentativas

**Linhas:** 60-86

```python
while True:  # ❌ Sem limite de tentativas!
    try:
        driver = webdriver.Chrome(...)
        # Login
        break
    except Exception as e:
        driver.quit()
        mensagem_erro = "Erro de comunicação. Tentando novamente..."
        # Tenta eternamente!
```

**Impacto:**
- ❌ Se o sistema estiver fora do ar, fica tentando eternamente
- ❌ Usuário não pode cancelar facilmente
- ❌ Consumo desnecessário de recursos

#### Solução Recomendada

**Imediato:**
1. ❌ **REMOVER** credenciais hardcoded do código
2. ❌ **REMOVER** credenciais do histórico do Git usando `git filter-branch`
3. ❌ **RESETAR** senha da conta `wbsouza1@stefanini.com`
4. ✅ **MIGRAR** usuários para versões v2 (Chrome ou Firefox)
5. ✅ **DEPRECAR** versões v1 completamente

**Médio Prazo:**
- Adicionar `.env` para variáveis sensíveis
- Implementar autenticação via interface (já existe em v2)
- Adicionar validação de credenciais antes de iniciar

#### Referência

Ver análise completa em: `Necxt - Caixa/ANALISE_TECNICA.md` (seção 4, problemas #1, #2 e #3)

---

## Issue #3: [MÉDIA] Timeout de script JavaScript não configurado no Firefox

### Labels
`enhancement`, `priority: medium`, `WallBot`, `Firefox`

### Título
🟡 Firefox driver não tem timeout de script configurado

### Descrição

**Arquivo:** `Necxt - Caixa/WallBot.py`
**Linha:** 234 (`criar_driver`)
**Severidade:** MÉDIA

#### Problema

O driver do Firefox não tem `set_script_timeout()` configurado, o que pode causar:
- Scripts JavaScript executarem indefinidamente
- Driver travar em páginas com AJAX pesado
- Timeout padrão do Firefox é muito longo (30 minutos!)

#### Código Atual

```python
def criar_driver():
    firefox_options = Options()
    # ... configurações ...

    driver = webdriver.Firefox(...)
    driver.maximize_window()
    driver.set_page_load_timeout(60)  # ✅ OK
    # ❌ FALTA: driver.set_script_timeout()
    return driver
```

#### Solução

```python
def criar_driver():
    # ... código existente ...

    driver = webdriver.Firefox(...)
    driver.maximize_window()
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(30)   # ✅ ADICIONAR: Timeout para scripts
    driver.implicitly_wait(5)       # ✅ ADICIONAR: Espera implícita

    return driver
```

#### Benefícios

- ✅ Evita travamento em JavaScript pesado
- ✅ Melhor controle sobre timeouts
- ✅ Comportamento mais previsível

#### Referência

Ver análise completa em: `Necxt - Caixa/ANALISE_WallBot.md` (seção 3, MÉDIA 1)

---

## Issue #4: [MÉDIA] Fechamento do Firefox pode travar indefinidamente

### Labels
`bug`, `priority: medium`, `WallBot`, `Firefox`

### Título
🟡 `fechar_driver_seguro()` pode travar indefinidamente no Firefox

### Descrição

**Arquivo:** `Necxt - Caixa/WallBot.py`
**Linhas:** 247-256
**Severidade:** MÉDIA

#### Problema

A função `fechar_driver_seguro()` pode travar indefinidamente se o Firefox não responder ao `driver.quit()`.

#### Código Atual

```python
def fechar_driver_seguro(driver, logger):
    try:
        if driver:
            logger.escrever("Fechando conexão com Firefox...")
            driver.quit()  # ❌ PODE TRAVAR INDEFINIDAMENTE!
            time.sleep(3)
            logger.escrever("Firefox fechado com sucesso")
    except Exception as e:
        logger.escrever(f"Erro ao fechar Firefox: {e}")
```

#### Cenários de Falha

1. **Firefox travado:** `driver.quit()` nunca retorna
2. **Processo zombie:** Firefox não finaliza corretamente
3. **Múltiplos drivers:** Referências antigas ainda abertas

#### Impacto

- ❌ Aplicação pode travar ao fechar
- ❌ Processos do Firefox podem acumular (vazamento de processos)
- ❌ Usuário precisa matar processos manualmente usando Task Manager

#### Solução Proposta

Implementar timeout forçado usando thread + psutil:

```python
import threading
import psutil  # pip install psutil

def fechar_driver_seguro(driver, logger, timeout=10):
    """
    Fecha o driver com timeout forçado
    """
    try:
        if driver:
            logger.escrever("Fechando conexão com Firefox...")

            # Obter PID do processo
            try:
                service_pid = driver.service.process.pid
            except:
                service_pid = None

            # Usar thread com timeout
            def close_driver():
                try:
                    driver.quit()
                except:
                    pass

            close_thread = threading.Thread(target=close_driver, daemon=True)
            close_thread.start()
            close_thread.join(timeout=timeout)

            if close_thread.is_alive():
                logger.escrever(f"⚠ driver.quit() travou após {timeout}s. Forçando encerramento...")

                # Matar processo manualmente
                if service_pid:
                    try:
                        parent = psutil.Process(service_pid)
                        children = parent.children(recursive=True)

                        for child in children:
                            child.kill()

                        parent.kill()
                        logger.escrever("✓ Processos encerrados forçadamente")
                    except Exception as e:
                        logger.escrever(f"Erro ao matar processos: {e}")
            else:
                logger.escrever("✓ Firefox fechado com sucesso")

            time.sleep(2)

    except Exception as e:
        logger.escrever(f"Erro ao fechar Firefox: {e}")
```

#### Referência

Ver análise completa em: `Necxt - Caixa/ANALISE_WallBot.md` (seção 3, MÉDIA 2)

---

## Issue #5: [MÉDIA] Tentativas de login duplicadas na reconexão (3x3 = 9 tentativas)

### Labels
`enhancement`, `priority: medium`, `WallBot`, `Firefox`, `performance`

### Título
🟡 Reconexão causa 9 tentativas de login ao invés de 3

### Descrição

**Arquivo:** `Necxt - Caixa/WallBot.py`
**Linhas:** 258-294 (`reconectar_driver`)
**Severidade:** MÉDIA

#### Problema

A função `reconectar_driver()` chama `fazer_login()`, que tem seu próprio sistema de retry interno (3 tentativas). Como a reconexão também tem 3 tentativas, o resultado é 3×3 = **9 tentativas de login**.

#### Fluxo Atual

```
1. reconectar_driver() é chamado (tentativa 1 de 3)
2. criar_driver() OK - driver1 criado
3. fazer_login() é chamado
   3.1. Tentativa 1 de login - FALHA
   3.2. Tentativa 2 de login - FALHA
   3.3. Tentativa 3 de login - FALHA
4. Exception é lançada
5. driver1 é fechado
6. return None

7. reconectar_driver() é chamado (tentativa 2 de 3)
8. Repete passos 2-6

9. reconectar_driver() é chamado (tentativa 3 de 3)
10. Repete passos 2-6

TOTAL: 3 tentativas × 3 retries = 9 tentativas de login!
```

#### Impacto

- ⚠️ Tempo de espera muito maior que o esperado
- ⚠️ Pode parecer que o sistema travou
- ⚠️ Logs ficam poluídos com muitos erros
- ⚠️ Pode ser bloqueado por rate limiting do servidor

#### Solução

Criar versão simplificada de `fazer_login()` para usar na reconexão:

```python
def fazer_login_simples(driver, email, senha, logger, max_tentativas=1):
    """
    Versão simplificada sem retry interno (para reconexão)
    """
    for tentativa in range(max_tentativas):
        try:
            driver.get(CONFIG['URL_SIPCS'])

            usuario_input = WebDriverWait(driver, CONFIG['TIMEOUT_PADRAO']).until(
                EC.presence_of_element_located((By.NAME, 'loginForm:username'))
            )
            senha_input = driver.find_element(By.NAME, 'loginForm:password')

            usuario_input.clear()
            senha_input.clear()
            usuario_input.send_keys(email)
            senha_input.send_keys(senha)

            botao_login = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div/input')
            botao_login.click()

            time.sleep(3)
            logger.escrever("Login realizado com sucesso")
            return True

        except Exception as e:
            if tentativa < max_tentativas - 1:
                logger.escrever(f"Tentativa {tentativa + 1} falhou. Tentando novamente...")
                time.sleep(2)
            else:
                raise

def reconectar_driver(email, senha, logger):
    try:
        logger.escrever("Iniciando reconexão...")
        driver = criar_driver()

        # ✅ Usar versão sem retry
        fazer_login_simples(driver, email, senha, logger, max_tentativas=1)

        # ... resto do código ...
    except Exception as e:
        # ...
```

#### Benefícios

- ✅ 3 tentativas totais ao invés de 9
- ✅ Mais rápido
- ✅ Logs mais limpos
- ✅ Comportamento mais previsível

#### Referência

Ver análise completa em: `Necxt - Caixa/ANALISE_WallBot.md` (seção 3, MÉDIA 3)

---

## Resumo de Prioridades

### 🔴 CRÍTICO (Implementar Imediatamente)
1. **Issue #1**: Race condition no loop de reconexão
2. **Issue #2**: Credenciais hardcoded e recursão infinita (v1)

### 🟡 MÉDIO (Implementar em Breve)
3. **Issue #3**: Timeout de script JavaScript não configurado
4. **Issue #4**: Fechamento do Firefox pode travar
5. **Issue #5**: Tentativas de login duplicadas

### Documentação Completa

- `Necxt - Caixa/ANALISE_TECNICA.md` - Análise geral de todos os arquivos
- `Necxt - Caixa/ANALISE_WallBot.md` - Análise detalhada do Firefox

---

**Documento gerado por:** Claude Code
**Data:** 29/10/2025

