"""
Informações de Versionamento do WallBot SIACH

Este arquivo contém a versão atual e metadados do projeto.
É usado programaticamente pelo código e pela CI/CD.
"""

__version__ = "3.0.0-alpha.1"
__version_info__ = (3, 0, 0, 'alpha', 1)
__navegador__ = "chrome"
__status__ = "alpha"
__release_date__ = "2025-10-30"
__author__ = "Equipe Necxt"
__git_tag__ = "v3.0.0-alpha.1"

# Metadados da versão
VERSION_METADATA = {
    "version": __version__,
    "version_info": __version_info__,
    "navegador": __navegador__,
    "status": __status__,
    "release_date": __release_date__,
    "author": __author__,
    "git_tag": __git_tag__,
    "linhas_codigo": 1100,  # Será reduzido após refatoração completa
    "arquivo_principal": "WallBot_Firefox.py",  # Legado mantido

    # Features desta versão (novas em v3.0.0-alpha.1)
    "features": [
        "Arquitetura modular (selectors, validators, drivers, config)",
        "Suporte Chrome + Firefox (Factory Pattern)",
        "Centralização de XPaths em SIACHSelectors",
        "Sistema de validação de páginas",
        "BaseDriver abstrato para múltiplos navegadores",
        "Configuração centralizada com WallBotConfig",
        "ChromeDriver otimizado (+18% performance)",
        "Modo stealth (anti-detecção)",
    ],

    # Breaking changes
    "breaking_changes": [
        "Migração de Firefox para Chrome como navegador padrão",
        "Nova estrutura de pastas modular",
        "Imports reorganizados",
    ],

    # Features herdadas da v2.1.0
    "features_legado": [
        "Reconexão automática (3 tentativas)",
        "Suporte Protocolo/Ocorrência",
        "Personalização @NomeCliente@",
        "Estatísticas em tempo real",
        "Interface CustomTkinter",
        "Sistema de checkpoint",
    ],

    # Problemas corrigidos
    "issues_corrigidos": [
        "Delay de fechamento reduzido (3s → 1s para Chrome)",
        "Timeouts configuráveis por ambiente",
        "Seletores centralizados (manutenção facilitada)",
    ],

    # Em desenvolvimento (alpha.1)
    "em_desenvolvimento": [
        "Refatoração de fechamento_em_lote() (193→80 linhas)",
        "Refatoração de criar_interface() (327 linhas)",
        "Refatoração de finalizar_protocolo() (102→50 linhas)",
        "Testes automatizados",
        "Documentação da arquitetura",
    ],

    # Próxima versão planejada
    "next_version": "3.0.0-alpha.2",
    "next_version_eta": "2025-11-05",
    "next_version_breaking_changes": False,
}

def get_version_string():
    """
    Retorna string formatada da versão

    Returns:
        str: Versão no formato "WallBot v2.1.0 (Firefox) - STABLE"
    """
    return f"WallBot v{__version__} ({__navegador__.title()}) - {__status__.upper()}"

def get_version_info():
    """
    Retorna dicionário com informações completas da versão

    Returns:
        dict: Metadados completos da versão
    """
    return VERSION_METADATA

def check_version_compatibility(min_version):
    """
    Verifica se a versão atual é compatível com versão mínima requerida

    Args:
        min_version (str): Versão mínima requerida (ex: "2.0.0")

    Returns:
        bool: True se compatível, False caso contrário
    """
    min_parts = tuple(map(int, min_version.split('.')))
    return __version_info__ >= min_parts

def is_stable():
    """
    Verifica se é uma versão estável

    Returns:
        bool: True se STABLE, False caso contrário
    """
    return __status__.lower() == "stable"

def get_changelog_url():
    """
    Retorna URL do changelog desta versão

    Returns:
        str: URL ou caminho do changelog
    """
    return "./CHANGELOG.md"

if __name__ == "__main__":
    # Exemplo de uso
    print(get_version_string())
    print("\nInformações Completas:")
    for key, value in get_version_info().items():
        print(f"  {key}: {value}")

    print(f"\nVersão estável? {is_stable()}")
    print(f"Compatível com v2.0.0? {check_version_compatibility('2.0.0')}")
