"""
Módulo de Seletores para WallBot SIACH

Este módulo centraliza todos os seletores (XPath, CSS, Name) usados
para localizar elementos nas páginas do sistema SIACH.

Também garante compatibilidade com o módulo padrão `selectors` da
biblioteca padrão do Python. Fizemos isso porque Selenium importa o
módulo padrão e, como o nosso pacote tem o mesmo nome, precisamos
re-exportar as classes originais (DefaultSelector, BaseSelector etc.)
para evitar conflitos.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import os
import sys
from pathlib import Path


def _load_stdlib_selectors():
    """Carrega o módulo `selectors` da biblioteca padrão em um alias seguro."""
    module_name = "_stdlib_selectors"
    if module_name in sys.modules:
        return sys.modules[module_name]

    stdlib_dir = Path(os.__file__).resolve().parent
    selectors_path = stdlib_dir / "selectors.py"

    loader = importlib.machinery.SourceFileLoader(module_name, str(selectors_path))
    spec = importlib.util.spec_from_loader(module_name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    sys.modules[module_name] = module
    return module


_stdlib_selectors = _load_stdlib_selectors()

# Re-exporta todos os símbolos públicos do módulo padrão
for _name in getattr(_stdlib_selectors, "__all__", dir(_stdlib_selectors)):
    if _name.startswith("_"):
        continue
    globals()[_name] = getattr(_stdlib_selectors, _name)

from .siach_selectors import SIACHSelectors

__all__ = list(getattr(_stdlib_selectors, "__all__", []))
__all__.append("SIACHSelectors")
