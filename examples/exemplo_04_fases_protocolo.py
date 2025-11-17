"""
Exemplo 04: Validar Fases de Protocolo

Demonstra uso de FasesProtocolo para validar estado de protocolos.
"""

from selectors.siach_selectors import FasesProtocolo


def exemplo_fases_basicas():
    """Demonstra validação básica de fases"""
    print("=" * 60)
    print("EXEMPLO 1: Fases Básicas")
    print("=" * 60)

    fases_teste = [
        "ABERTA",
        "EM ANDAMENTO",
        "FINALIZADA",
        "REABERTA",
        "CANCELADA"
    ]

    print("\nTestando fases:")
    for fase in fases_teste:
        pode = FasesProtocolo.pode_finalizar(fase)
        ja_finalizado = FasesProtocolo.ja_finalizado(fase)

        print(f"\n  Fase: {fase}")
        print(f"    Pode finalizar? {'✅ Sim' if pode else '❌ Não'}")
        print(f"    Já finalizado? {'✅ Sim' if ja_finalizado else '❌ Não'}")

    print()


def exemplo_case_insensitive():
    """Demonstra que validação é case-insensitive"""
    print("=" * 60)
    print("EXEMPLO 2: Case Insensitive")
    print("=" * 60)

    variacoes = [
        "ABERTA",
        "aberta",
        "Aberta",
        "aBerTa"
    ]

    print("\nTestando variações de case:")
    for fase in variacoes:
        pode = FasesProtocolo.pode_finalizar(fase)
        print(f"  '{fase}' -> Pode finalizar: {'✅ Sim' if pode else '❌ Não'}")

    print("\n✅ Todas as variações retornam o mesmo resultado!")
    print()


def exemplo_fluxo_decisao():
    """Demonstra fluxo de decisão baseado na fase"""
    print("=" * 60)
    print("EXEMPLO 3: Fluxo de Decisão")
    print("=" * 60)

    def processar_protocolo(numero, fase):
        """Simula processamento de protocolo baseado na fase"""
        print(f"\nProtocolo: {numero}")
        print(f"Fase atual: {fase}")

        if FasesProtocolo.pode_finalizar(fase):
            print("  ✅ Ação: FINALIZAR protocolo")
            return "PROCESSAR"

        elif FasesProtocolo.ja_finalizado(fase):
            print("  ⏭️ Ação: PULAR (já finalizado)")
            return "PULAR"

        else:
            print("  ⚠️ Ação: FASE DESCONHECIDA (registrar)")
            return "DESCONHECIDO"

    # Testar com diferentes protocolos
    protocolos_teste = [
        ("123456", "ABERTA"),
        ("123457", "FINALIZADA"),
        ("123458", "EM ANDAMENTO"),
        ("123459", "REABERTA"),
        ("123460", "CANCELADA")
    ]

    print("\nProcessando protocolos:")
    resultados = {}
    for numero, fase in protocolos_teste:
        resultado = processar_protocolo(numero, fase)
        resultados[resultado] = resultados.get(resultado, 0) + 1

    print("\n" + "-" * 60)
    print("Resumo:")
    for acao, qtd in resultados.items():
        print(f"  {acao}: {qtd} protocolo(s)")

    print()


def exemplo_estatisticas():
    """Demonstra coleta de estatísticas por fase"""
    print("=" * 60)
    print("EXEMPLO 4: Estatísticas de Fases")
    print("=" * 60)

    # Simular processamento de lote
    fases_encontradas = [
        "ABERTA", "ABERTA", "FINALIZADA", "EM ANDAMENTO",
        "REABERTA", "ABERTA", "FINALIZADA", "CANCELADA",
        "EM ANDAMENTO", "ABERTA"
    ]

    estatisticas = {
        'processadas': 0,
        'puladas': 0,
        'desconhecidas': 0
    }

    print("\nProcessando lote de 10 protocolos:")

    for i, fase in enumerate(fases_encontradas, 1):
        print(f"  [{i:2d}] Fase: {fase:15s} ", end="")

        if FasesProtocolo.pode_finalizar(fase):
            estatisticas['processadas'] += 1
            print("-> ✅ Processar")

        elif FasesProtocolo.ja_finalizado(fase):
            estatisticas['puladas'] += 1
            print("-> ⏭️ Pular")

        else:
            estatisticas['desconhecidas'] += 1
            print("-> ⚠️ Desconhecida")

    # Exibir estatísticas
    print("\n" + "-" * 60)
    print("Estatísticas Finais:")
    print(f"  ✅ Processadas: {estatisticas['processadas']}")
    print(f"  ⏭️ Puladas: {estatisticas['puladas']}")
    print(f"  ⚠️ Desconhecidas: {estatisticas['desconhecidas']}")
    print(f"  📊 Total: {len(fases_encontradas)}")

    # Calcular percentuais
    total = len(fases_encontradas)
    print(f"\nPercentuais:")
    print(f"  Processadas: {(estatisticas['processadas'] / total * 100):.1f}%")
    print(f"  Puladas: {(estatisticas['puladas'] / total * 100):.1f}%")
    print(f"  Desconhecidas: {(estatisticas['desconhecidas'] / total * 100):.1f}%")

    print()


def exemplo_constantes_disponiveis():
    """Mostra as constantes disponíveis"""
    print("=" * 60)
    print("EXEMPLO 5: Constantes Disponíveis")
    print("=" * 60)

    print("\nFases que PODEM ser finalizadas:")
    for fase in FasesProtocolo.PROCESSAVEIS:
        print(f"  ✅ {fase}")

    print("\nFases que NÃO podem ser finalizadas:")
    for fase in FasesProtocolo.SEM_ACAO:
        print(f"  ❌ {fase}")

    print("\nConstantes individuais:")
    print(f"  FasesProtocolo.ABERTA = '{FasesProtocolo.ABERTA}'")
    print(f"  FasesProtocolo.EM_ANDAMENTO = '{FasesProtocolo.EM_ANDAMENTO}'")
    print(f"  FasesProtocolo.FINALIZADA = '{FasesProtocolo.FINALIZADA}'")
    print(f"  FasesProtocolo.REABERTA = '{FasesProtocolo.REABERTA}'")

    print()


if __name__ == "__main__":
    print("\n" + "📋 EXEMPLOS DE VALIDAÇÃO DE FASES".center(60))
    print()

    try:
        exemplo_fases_basicas()
        exemplo_case_insensitive()
        exemplo_fluxo_decisao()
        exemplo_estatisticas()
        exemplo_constantes_disponiveis()

        print("=" * 60)
        print("✅ Todos os exemplos executados com sucesso!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
