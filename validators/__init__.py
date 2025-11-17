"""
Módulo de Validadores para WallBot SIACH

Este módulo contém funções para validar estados de páginas,
sessões, e detectar condições especiais do sistema SIACH.
"""

from .page_validators import (
    validar_arquivo_excel,
    validar_email,
    validar_pagina_siach,
    verificar_sessao_valida,
    detectar_pagina_manutencao,
    verificar_erro_conexao
)

__all__ = [
    'validar_arquivo_excel',
    'validar_email',
    'validar_pagina_siach',
    'verificar_sessao_valida',
    'detectar_pagina_manutencao',
    'verificar_erro_conexao'
]
