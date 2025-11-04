"""
Exemplo 03: Validar Dados de Entrada

Demonstra uso de validadores para entrada de dados.
"""

from validators import (
    validar_email,
    validar_arquivo_excel,
    validar_credenciais,
    validar_script_personalizacao,
    verificar_erro_conexao
)


def exemplo_validar_emails():
    """Valida diferentes formatos de email"""
    print("=" * 60)
    print("EXEMPLO 1: Validar Emails")
    print("=" * 60)

    emails_teste = [
        "usuario@dominio.com",
        "user.name@example.co.uk",
        "invalido",
        "@dominio.com",
        "usuario@",
        "",
        "teste123@test.org"
    ]

    print("\nTestando emails:")
    for email in emails_teste:
        valido, msg = validar_email(email)
        status = "✅" if valido else "❌"
        print(f"  {status} '{email}' -> {msg if msg else 'Válido'}")

    print()


def exemplo_validar_arquivos():
    """Valida arquivos Excel"""
    print("=" * 60)
    print("EXEMPLO 2: Validar Arquivos Excel")
    print("=" * 60)

    arquivos_teste = [
        "Base.xlsx",
        "arquivo_inexistente.xlsx",
        "arquivo.txt",
        ""
    ]

    print("\nTestando arquivos:")
    for arquivo in arquivos_teste:
        valido, msg = validar_arquivo_excel(arquivo)
        status = "✅" if valido else "❌"
        resultado = msg if msg else "Válido"
        print(f"  {status} '{arquivo}' -> {resultado}")

    print()


def exemplo_validar_credenciais():
    """Valida credenciais de login"""
    print("=" * 60)
    print("EXEMPLO 3: Validar Credenciais")
    print("=" * 60)

    credenciais_teste = [
        ("usuario@test.com", "senha123"),
        ("emailinvalido", "senha123"),
        ("user@test.com", "12"),  # Senha muito curta
        ("", ""),  # Campos vazios
        ("user@domain.com", "senhavalida")
    ]

    print("\nTestando credenciais:")
    for email, senha in credenciais_teste:
        valido, msg = validar_credenciais(email, senha)
        status = "✅" if valido else "❌"
        print(f"  {status} Email: '{email}', Senha: '{senha}'")
        if msg:
            print(f"      -> {msg}")

    print()


def exemplo_validar_scripts():
    """Valida scripts de finalização"""
    print("=" * 60)
    print("EXEMPLO 4: Validar Scripts")
    print("=" * 60)

    scripts_teste = [
        ("Protocolo finalizado com sucesso", False),
        ("Olá @NomeCliente@, protocolo finalizado", True),
        ("Protocolo finalizado", True),  # Com personalização mas sem placeholder
        ("", False)
    ]

    print("\nTestando scripts:")
    for script, usar_personalizacao in scripts_teste:
        valido, msg = validar_script_personalizacao(script, usar_personalizacao)
        status = "✅" if valido else "❌"
        pers = "COM" if usar_personalizacao else "SEM"
        print(f"  {status} {pers} personalização: '{script[:40]}...'")
        if msg:
            print(f"      ⚠️ {msg}")

    print()


def exemplo_verificar_erros_conexao():
    """Verifica se erros são de conexão"""
    print("=" * 60)
    print("EXEMPLO 5: Verificar Erros de Conexão")
    print("=" * 60)

    erros_teste = [
        "HTTPConnectionPool error occurred",
        "Read timed out after 30 seconds",
        "target frame detached from window",
        "Connection refused by server",
        "Element not found",  # Não é erro de conexão
        "Invalid selector syntax",  # Não é erro de conexão
        "ERR_INTERNET_DISCONNECTED"
    ]

    print("\nClassificando erros:")
    for erro in erros_teste:
        eh_conexao = verificar_erro_conexao(erro)
        tipo = "🌐 Conexão" if eh_conexao else "🔧 Outro"
        print(f"  {tipo}: {erro}")

    print()


def exemplo_fluxo_completo():
    """Demonstra fluxo completo de validação"""
    print("=" * 60)
    print("EXEMPLO 6: Fluxo Completo de Validação")
    print("=" * 60)

    print("\nSimulando entrada de dados do usuário:")

    # Dados de entrada simulados
    email = "usuario@necxt.com"
    senha = "senha123"
    arquivo = "Base.xlsx"
    script = "Olá @NomeCliente@, seu protocolo foi finalizado."
    usar_personalizacao = True

    print(f"\n  Email: {email}")
    print(f"  Senha: {'*' * len(senha)}")
    print(f"  Arquivo: {arquivo}")
    print(f"  Script: {script}")
    print(f"  Personalização: {usar_personalizacao}")

    # Validar tudo
    print("\nValidando...")

    # 1. Validar credenciais
    cred_validas, msg_cred = validar_credenciais(email, senha)
    if not cred_validas:
        print(f"  ❌ Credenciais inválidas: {msg_cred}")
        return
    print("  ✅ Credenciais válidas")

    # 2. Validar arquivo
    arquivo_valido, msg_arquivo = validar_arquivo_excel(arquivo)
    if not arquivo_valido:
        print(f"  ❌ Arquivo inválido: {msg_arquivo}")
        return
    print("  ✅ Arquivo válido")

    # 3. Validar script
    script_valido, msg_script = validar_script_personalizacao(script, usar_personalizacao)
    if not script_valido:
        print(f"  ❌ Script inválido: {msg_script}")
        return
    print("  ✅ Script válido")

    if msg_script:
        print(f"  ⚠️ Aviso: {msg_script}")

    print("\n✅ Todas as validações passaram! Pode prosseguir com o processamento.")
    print()


if __name__ == "__main__":
    print("\n" + "✔️ EXEMPLOS DE VALIDAÇÃO DE DADOS".center(60))
    print()

    try:
        exemplo_validar_emails()
        exemplo_validar_arquivos()
        exemplo_validar_credenciais()
        exemplo_validar_scripts()
        exemplo_verificar_erros_conexao()
        exemplo_fluxo_completo()

        print("=" * 60)
        print("✅ Todos os exemplos executados com sucesso!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
