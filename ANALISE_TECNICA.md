# Análise Técnica - Projeto Necxt - Caixa

**Data:** 29 de Outubro de 2025
**Repositório:** Python-Projects/Necxt - Caixa

---

## ÍNDICE
1. [Visão Geral do Projeto](#visão-geral-do-projeto)
2. [Estrutura de Arquivos](#estrutura-de-arquivos)
3. [Análise Detalhada por Arquivo](#análise-detalhada-por-arquivo)
4. [Possíveis Falhas de Fluxo](#possíveis-falhas-de-fluxo)
5. [Problemas de Segurança](#problemas-de-segurança)
6. [Recomendações de Melhoria](#recomendações-de-melhoria)

---

## 1. VISÃO GERAL DO PROJETO

O projeto **Necxt - Caixa** é uma coleção de ferramentas de automação RPA (Robotic Process Automation) desenvolvidas para processar protocolos e ocorrências no sistema SIACH da Caixa Econômica Federal.

### Objetivo Principal
Automatizar o fechamento em lote de:
- **Protocolos** (requisições/tickets)
- **Ocorrências** (casos/problemas)

### Tecnologias Utilizadas
- **Python 3.x**
- **Selenium WebDriver** (Chrome)
- **CustomTkinter** (Interface gráfica moderna)
- **OpenPyXL** (Manipulação de planilhas Excel)
- **Threading** (Processamento assíncrono)
- **PyAutoGUI** (Automação de interface)
- **Playwright** (Monitor HTTP)

---

## 2. ESTRUTURA DE ARQUIVOS

```
Necxt - Caixa/
├── Ocorrencias v2.py                          # Automação de ocorrências (versão 2)
├── Protocolos v2.py                           # Automação de protocolos (versão 2)
├── Fechamento em lote - Ocorrências.py        # Automação de ocorrências (versão 1)
├── Fechamento em lote - Protocolos.py         # Automação de protocolos (versão 1)
├── processamento projeto.py                   # Automação com PyAutoGUI
├── processamento projeto G15.py               # (não lido)
├── posição do mouse.py                        # (não lido)
├── Projeto - Emails Desacordo/
│   └── monitor_http.py                        # Monitor de requisições HTTP
├── Base.xlsx                                  # Planilha de dados de entrada
├── resultado_saida.xlsx                       # Planilha de resultados
├── log_output.txt                             # Log de execução
├── progresso.txt                              # Arquivo de checkpoint
├── *.spec                                     # Arquivos de build PyInstaller
├── build/                                     # Builds compilados
└── dist/                                      # Executáveis (.exe)
```

---

## 3. ANÁLISE DETALHADA POR ARQUIVO

### 3.1. **Ocorrencias v2.py** (845 linhas)
**Título:** WallBot - Finalização de Ocorrências SIACH v2.0
**Status:** Versão mais recente e robusta

#### Funcionalidades:
- Interface gráfica com **CustomTkinter** (modo escuro)
- Login no sistema SIPCS com retry (3 tentativas)
- Processamento em lote de ocorrências do SIACH
- Sistema de **estatísticas em tempo real**:
  - Concluídos
  - Sem ação
  - Fase desconhecida
  - Erros
- **Personalização de scripts** com substituição de `@NomeCliente@`
- Gerenciamento de progresso (checkpoint)
- Logs detalhados com timestamps
- Salvamento de resultados em Excel (modo append)

#### Arquitetura:
- **Gerenciamento de Estado** (thread-safe com locks)
- **Gerenciador de Log** (context manager)
- **Configurações centralizadas** (dicionário CONFIG)
- **Tratamento robusto de exceções**

#### Fluxo de Execução:
```
1. Login no SIPCS
2. Acesso ao módulo SIACH (nova aba)
3. Para cada ocorrência:
   a. Consultar fase da ocorrência
   b. Se ABERTA ou EM ANDAMENTO:
      - Abrir detalhes
      - Clicar em Finalizar
      - Preencher campos (justificativa, resposta, informação técnica)
      - Salvar e confirmar
   c. Se REABERTA ou FINALIZADA: pular
   d. Outras fases: registrar como desconhecida
4. Salvar resultados em Excel
5. Exibir estatísticas finais
```

---

### 3.2. **Protocolos v2.py** (845 linhas)
**Título:** WallBot - Finalização de Protocolos SIACH v2.0
**Status:** Versão mais recente e robusta

#### Diferenças em relação a Ocorrencias v2.py:
- **Campo de entrada:** Protocolo (linha 339) vs Ocorrência (linha 135 em Ocorrencias v2)
  ```python
  # Protocolos v2.py
  campo_texto = driver.find_element(By.XPATH,
      '/html/body/div[2]/div/div/div[2]/div[1]/form/div[1]/div[1]/div[3]/div/input')

  # Ocorrencias v2.py
  campo_texto = driver.find_element(By.XPATH,
      '/html/body/div[2]/div/div/div[2]/div[1]/form/div[1]/div[1]/div[2]/div/input')
  ```

**Funcionalidades:** Idênticas ao Ocorrencias v2.py

---

### 3.3. **Fechamento em lote - Ocorrências.py** (395 linhas)
**Título:** WallBot - Finalização de Ocorrências SIACH v1.1
**Status:** Versão anterior, mais simples

#### Diferenças em relação à v2:
- ❌ Sem sistema de estatísticas
- ❌ Sem personalização de scripts
- ❌ Sem gerenciamento de estado thread-safe
- ❌ Sem validações avançadas
- ✅ Mais compacto (395 vs 845 linhas)
- ✅ **CRÍTICO:** Credenciais hardcoded (linhas 72-73)
  ```python
  usuario.send_keys('wbsouza1@stefanini.com')
  senha.send_keys('Barbara05')
  ```

#### Problema de Fluxo Crítico:
**Linha 280:** Recursão infinita em caso de timeout
```python
except TimeoutException as e:
    mensagem = f'TimeoutException: Protocolo {valor}'
    print(mensagem)
    driver.quit()
    fechamento_em_lote()  # ⚠️ RECURSÃO SEM LIMITE!
    return
```

---

### 3.4. **Fechamento em lote - Protocolos.py** (395 linhas)
Idêntico ao "Fechamento em lote - Ocorrências.py", mas processa protocolos.

**Mesmos problemas:**
- Credenciais hardcoded
- Recursão infinita em TimeoutException (linha 280)

---

### 3.5. **processamento projeto.py** (93 linhas)
**Título:** Message Sender
**Finalidade:** Automação de formulários com PyAutoGUI

#### Funcionalidades:
- Envio automatizado de mensagens aleatórias
- Sequência de teclas programada
- Interface gráfica simples (Tkinter)
- Controle de iterações

#### Fluxo:
```
1. Aguardar carregamento da página (10s)
2. Enviar sequência de teclas (1,1,1,1,4 ou 1,1,1,1,3)
3. Aguardar 5s
4. Clicar na posição (160, 720)
5. Colar mensagem aleatória
6. Pressionar TAB + SPACE
7. Aguardar 65s
8. Finalizar com SPACE
```

#### Problemas:
- **Coordenadas fixas** (160, 720) - pode quebrar em diferentes resoluções
- **Sem validação** de posição do cursor
- **Sem tratamento de erros**
- **Timings fixos** (não adaptativos)

---

### 3.6. **monitor_http.py** (96 linhas)
**Finalidade:** Capturar requisições HTTP com Playwright

#### Funcionalidades:
- Interceptar todas as requisições HTTP
- Logar método, URL, headers e payload
- Salvar em arquivo `http_requests.log`
- Navegador em modo não-headless (visível)

#### Uso:
Útil para reverse engineering de APIs e debugging de aplicações web.

---

## 4. POSSÍVEIS FALHAS DE FLUXO

### 4.1. CRÍTICAS (Alta Prioridade)

#### 🔴 1. **Recursão Infinita em TimeoutException**
**Arquivos:** Fechamento em lote - Ocorrências.py, Fechamento em lote - Protocolos.py
**Linhas:** 268-281

**Problema:**
```python
except TimeoutException as e:
    driver.quit()
    fechamento_em_lote()  # Chama a função novamente!
    return
```

**Impacto:**
- Stack overflow após múltiplos timeouts
- Consumo excessivo de memória
- Perda de contexto de progresso
- Múltiplas instâncias do driver podem ser criadas

**Solução:**
```python
except TimeoutException as e:
    mensagem = f'TimeoutException: Protocolo {valor}'
    logger.escrever(mensagem)
    driver.quit()
    # NÃO chamar fechamento_em_lote() novamente!
    # Simplesmente continue ou break
    continue  # ou break, dependendo do comportamento desejado
```

---

#### 🔴 2. **Credenciais Hardcoded**
**Arquivos:** Fechamento em lote - Ocorrências.py, Fechamento em lote - Protocolos.py
**Linhas:** 72-73

**Problema:**
```python
usuario.send_keys('wbsouza1@stefanini.com')
senha.send_keys('Barbara05')
```

**Riscos:**
- **Violação de segurança** (credenciais expostas no código)
- Impossibilidade de uso por múltiplos usuários
- Credenciais no histórico do Git

**Solução:**
- Remover credenciais do código
- Usar variáveis de ambiente
- Implementar login via interface (já existe nas versões v2)

---

#### 🔴 3. **Gerenciamento de Arquivo de Log Aberto**
**Arquivos:** Fechamento em lote - Ocorrências.py, Fechamento em lote - Protocolos.py
**Linha:** 38

**Problema:**
```python
log_file = open('log_output.txt', 'a', encoding='utf-8')
# ...
# Arquivo só é fechado no finally (linha 291)
```

**Risco:**
- Se ocorrer exceção antes do `finally`, o arquivo pode não ser fechado corretamente
- Perda de dados do log em buffer

**Solução:**
Usar context manager (já implementado nas versões v2):
```python
with open('log_output.txt', 'a', encoding='utf-8') as log_file:
    # código aqui
```

---

### 4.2. MÉDIAS (Prioridade Moderada)

#### 🟡 4. **Loop Infinito sem Limite de Tentativas**
**Arquivos:** Fechamento em lote - Ocorrências.py, Fechamento em lote - Protocolos.py
**Linhas:** 60-86

**Problema:**
```python
while True:
    try:
        driver = webdriver.Chrome(...)
        # ...
        break
    except Exception as e:
        driver.quit()
        mensagem_erro = "Erro de comunicação. Tentando novamente..."
        # Tenta indefinidamente!
```

**Impacto:**
- Se o sistema estiver fora do ar, ficará tentando eternamente
- Usuário não pode cancelar facilmente
- Consome recursos desnecessariamente

**Solução:**
```python
MAX_TENTATIVAS_LOGIN = 5
for tentativa in range(MAX_TENTATIVAS_LOGIN):
    try:
        # ...
        break
    except Exception as e:
        if tentativa < MAX_TENTATIVAS_LOGIN - 1:
            logger.escrever(f"Tentativa {tentativa+1} falhou. Tentando novamente...")
            time.sleep(3)
        else:
            raise Exception("Falha ao conectar após 5 tentativas")
```

---

#### 🟡 5. **XPaths Frágeis e Absolutos**
**Todos os arquivos de automação**

**Problema:**
```python
campo_texto = driver.find_element(By.XPATH,
    '/html/body/div[2]/div/div/div[2]/div[1]/form/div[1]/div[1]/div[2]/div/input')
```

**Impacto:**
- Quebra facilmente com mudanças mínimas no HTML
- Difícil manutenção
- XPaths muito longos e difíceis de ler

**Solução:**
Usar seletores relativos ou IDs/classes:
```python
# Melhor:
campo_texto = driver.find_element(By.ID, 'campo_ocorrencia')

# Ou XPath relativo:
campo_texto = driver.find_element(By.XPATH,
    "//form[@id='formConsulta']//input[@name='ocorrencia']")
```

---

#### 🟡 6. **Timeouts Fixos (time.sleep)**
**Todos os arquivos de automação**

**Problema:**
```python
time.sleep(3)  # Espera fixa de 3 segundos
```

**Impacto:**
- Desperdiça tempo quando elementos carregam rapidamente
- Pode falhar se elementos demorarem mais que o esperado
- Não adapta a variações de velocidade da rede

**Solução:**
Usar `WebDriverWait` com expected_conditions:
```python
elemento = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, xpath))
)
```

---

### 4.3. BAIXAS (Melhorias Gerais)

#### 🟢 7. **Falta de Validação de Entrada**
**Arquivos:** Versões v1 (linhas 34-35)

**Problema:**
```python
caminho_arquivo = entrada_arquivo.get()
script = entrada_script.get("1.0", "end-1c")
# Nenhuma validação se os campos estão vazios!
```

**Solução:**
As versões v2 já implementam validação (linhas 734-742)

---

#### 🟢 8. **Falta de Tratamento de StaleElementReferenceException**
**Arquivos:** Versões v1

**Problema:**
Só trata `StaleElementReferenceException` em um local específico.

**Solução:**
As versões v2 melhoraram isso com tratamentos mais abrangentes.

---

#### 🟢 9. **Coordenadas Fixas em PyAutoGUI**
**Arquivo:** processamento projeto.py (linha 20)

**Problema:**
```python
COORD_X, COORD_Y = 160, 720  # Só funciona em uma resolução específica!
```

**Solução:**
- Usar reconhecimento de imagem (pyautogui.locateOnScreen)
- Ou tornar as coordenadas configuráveis
- Ou usar automação baseada em acessibilidade

---

#### 🟢 10. **Falta de Backup Antes de Sobrescrever**
**Arquivo:** Fechamento em lote - Ocorrências.py (linha 306)

**Problema:**
```python
workbook.save('resultado_saida.xlsx')  # Sempre sobrescreve!
```

**Solução:**
As versões v2 implementam modo append (linha 153-183)

---

## 5. PROBLEMAS DE SEGURANÇA

### 🔒 1. **Credenciais em Texto Plano**
- **Severidade:** CRÍTICA
- **Arquivo:** Fechamento em lote - Ocorrências.py, Fechamento em lote - Protocolos.py
- **Linhas:** 72-73
- **Mitigação:** Usar variáveis de ambiente ou prompt de senha

### 🔒 2. **Ignorar Erros de Certificado SSL**
- **Severidade:** MÉDIA
- **Todos os arquivos**
- **Linha:** chrome_options.add_argument('--ignore-certificate-errors')
- **Risco:** Man-in-the-middle attacks
- **Justificativa:** Pode ser necessário para ambientes corporativos com certificados autoassinados

### 🔒 3. **Credenciais no Histórico do Git**
- **Severidade:** CRÍTICA
- **Ação:** Verificar histórico do Git e remover commits com credenciais
- **Comando:**
  ```bash
  git filter-branch --force --index-filter \
    "git rm --cached --ignore-unmatch 'Fechamento em lote - Ocorrências.py'" \
    --prune-empty --tag-name-filter cat -- --all
  ```

---

## 6. RECOMENDAÇÕES DE MELHORIA

### 6.1. PRIORIDADE ALTA

1. **Migrar completamente para as versões v2**
   - As versões v2 são significativamente superiores
   - Considerar deprecar as versões v1

2. **Remover credenciais hardcoded**
   - Implementar .env para variáveis sensíveis
   - Adicionar .env ao .gitignore

3. **Corrigir recursão infinita**
   - Substituir chamadas recursivas por loops controlados

4. **Implementar limite de tentativas**
   - Adicionar MAX_RETRIES em todas as operações de rede

### 6.2. PRIORIDADE MÉDIA

5. **Melhorar seletores XPath**
   - Migrar para seletores relativos
   - Documentar motivo de cada seletor

6. **Implementar retry pattern**
   - Usar decorators para retry automático
   - Exemplo: `@retry(max_attempts=3, delay=2)`

7. **Adicionar testes automatizados**
   - Testes unitários para funções de processamento
   - Testes de integração para fluxos completos

8. **Implementar logging estruturado**
   - Usar biblioteca `logging` do Python
   - Níveis: DEBUG, INFO, WARNING, ERROR, CRITICAL

### 6.3. PRIORIDADE BAIXA

9. **Refatorar código duplicado**
   - Criar módulo compartilhado entre Ocorrencias e Protocolos
   - Herança ou composição para reutilização

10. **Documentação**
    - Adicionar docstrings em todas as funções
    - Criar README.md com instruções de uso
    - Documentar APIs e fluxos

11. **Interface aprimorada**
    - Adicionar preview do Excel antes de processar
    - Gráficos de estatísticas em tempo real
    - Dark/Light mode toggle

---

## 7. COMPARATIVO DE VERSÕES

| Aspecto | Versão v1 | Versão v2 |
|---------|-----------|-----------|
| **Linhas de código** | 395 | 845 |
| **Estatísticas** | ❌ Não | ✅ Sim (tempo real) |
| **Personalização de script** | ❌ Não | ✅ Sim (@NomeCliente@) |
| **Thread-safety** | ❌ Não | ✅ Sim (locks) |
| **Gerenciamento de log** | ⚠️ Manual | ✅ Context manager |
| **Validação de entrada** | ❌ Não | ✅ Sim |
| **Modo append Excel** | ❌ Sobrescreve | ✅ Append |
| **Credenciais** | ❌ Hardcoded | ✅ Via interface |
| **Recursão infinita** | ❌ Sim (bug) | ✅ Não |
| **Arquitetura** | Procedural | OOP + Procedural |
| **Manutenibilidade** | Baixa | Alta |

**Recomendação:** Descontinuar versões v1 e focar nas v2.

---

## 8. NOTA SOBRE WallBot.py

⚠️ **ARQUIVO NÃO ENCONTRADO**

Durante a análise, foi solicitado examinar o arquivo `WallBot.py`, porém este arquivo **não existe** no repositório.

**Possibilidades:**
1. O arquivo foi renomeado ou removido
2. Está em outro repositório
3. Ainda não foi criado
4. O nome pode estar diferente

**Arquivos encontrados relacionados:**
- `Ocorrencias v2.py` - WallBot para Ocorrências (Chrome)
- `Protocolos v2.py` - WallBot para Protocolos (Chrome)
- Versões v1 equivalentes

**Observação:** Todos os arquivos WallBot encontrados utilizam **Chrome** via Selenium, não Firefox.

Se a intenção é criar uma versão para Firefox, seria necessário:
```python
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(
    service=FirefoxService(GeckoDriverManager().install()),
    options=firefox_options
)
```

---

## 9. CONCLUSÃO

O projeto **Necxt - Caixa** possui uma estrutura sólida de automação RPA, especialmente nas versões v2. No entanto, existem **falhas críticas de fluxo** nas versões v1 que precisam ser corrigidas urgentemente:

### Falhas Críticas:
1. ❌ Recursão infinita em TimeoutException
2. ❌ Credenciais hardcoded
3. ❌ Loop infinito de tentativas sem limite

### Pontos Positivos:
1. ✅ Interface gráfica moderna (CustomTkinter)
2. ✅ Sistema de checkpoint (progresso.txt)
3. ✅ Logs detalhados
4. ✅ Tratamento de exceções robusto (v2)
5. ✅ Estatísticas em tempo real (v2)

### Próximos Passos:
1. **Imediato:** Remover credenciais e corrigir recursão
2. **Curto prazo:** Migrar usuários para v2
3. **Médio prazo:** Refatorar XPaths e implementar testes
4. **Longo prazo:** Criar versão Firefox (se necessário)

---

**Documento gerado por:** Claude Code
**Versão:** 1.0
**Última atualização:** 29/10/2025

