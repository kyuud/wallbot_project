"""
Informações de Versionamento do WallBot SIACH

Este arquivo contém a versão atual e metadados do projeto.
É usado programaticamente pelo código e pela CI/CD.
"""

__version__ = "2.1.0"
__version_info__ = (2, 1, 0)
__navegador__ = "firefox"
__status__ = "stable"
__release_date__ = "2025-10-23"
__author__ = "Equipe Necxt"
__git_tag__ = "v2.1.0-firefox-stable"

# Metadados da versão
VERSION_METADATA = {
    "version": __version__,
    "version_info": __version_info__,
    "navegador": __navegador__,
    "status": __status__,
    "release_date": __release_date__,
    "author": __author__,
    "git_tag": __git_tag__,
    "linhas_codigo": 1100,
    "arquivo_principal": "WallBot_Firefox.py",

    # Features desta versão
    "features": [
        "Reconexão automática (3 tentativas)",
        "Suporte Protocolo/Ocorrência",
        "Personalização @NomeCliente@",
        "Estatísticas em tempo real",
        "Interface CustomTkinter",
        "Sistema de checkpoint",
    ],

    # Problemas conhecidos
    "known_issues": [
        "Race condition no loop de reconexão",
        "Timeout de script não configurado",
        "Fechamento pode travar",
        "Consumo de RAM alto (820MB)",
    ],

    # Próxima versão planejada
    "next_version": "3.0.0",
    "next_version_eta": "2025-11-15",
    "next_version_breaking_changes": True,
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
