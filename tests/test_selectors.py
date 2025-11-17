"""
Testes para módulo de seletores

Execute:
    pytest tests/test_selectors.py -v
"""

import pytest
from selenium.webdriver.common.by import By
from selectors.siach_selectors import SIACHSelectors, FasesProtocolo


class TestSIACHSelectors:
    """Testes para classe SIACHSelectors"""

    def test_selector_format(self):
        """Testa se seletores retornam tupla (By, valor)"""
        # Login
        assert len(SIACHSelectors.LOGIN_USERNAME) == 2
        assert SIACHSelectors.LOGIN_USERNAME[0] == By.NAME
        assert SIACHSelectors.LOGIN_USERNAME[1] == 'loginForm:username'

        # Protocolo
        assert len(SIACHSelectors.PROTOCOLO_FASE_TEXT) == 2
        assert SIACHSelectors.PROTOCOLO_FASE_TEXT[0] == By.XPATH

    def test_all_selectors_valid(self):
        """Testa se todos os seletores são válidos"""
        result = SIACHSelectors.validate_selectors()

        assert result['valid'] == True, f"Seletores inválidos: {result['errors']}"
        assert result['total'] >= 16, "Deve ter pelo menos 16 seletores"
        assert len(result['errors']) == 0

    def test_selector_categories(self):
        """Testa se seletores de cada categoria existem"""
        # LOGIN
        assert hasattr(SIACHSelectors, 'LOGIN_USERNAME')
        assert hasattr(SIACHSelectors, 'LOGIN_PASSWORD')
        assert hasattr(SIACHSelectors, 'LOGIN_BUTTON')

        # MENU
        assert hasattr(SIACHSelectors, 'MENU_SIACH_MODULE')
        assert hasattr(SIACHSelectors, 'MENU_ATENDER_OCORRENCIA')

        # FORM
        assert hasattr(SIACHSelectors, 'FORM_PROTOCOLO_INPUT')
        assert hasattr(SIACHSelectors, 'FORM_OCORRENCIA_INPUT')

        # PROTOCOLO
        assert hasattr(SIACHSelectors, 'PROTOCOLO_FASE_TEXT')

        # CLIENTE
        assert hasattr(SIACHSelectors, 'CLIENTE_NOME_PRIMARY')
        assert hasattr(SIACHSelectors, 'CLIENTE_NOME_FALLBACK')

        # FINALIZACAO
        assert hasattr(SIACHSelectors, 'FINALIZACAO_SALVAR_BUTTON')

    def test_get_selector_method(self):
        """Testa método get_selector()"""
        selector = SIACHSelectors.get_selector(SIACHSelectors.LOGIN_BUTTON)
        assert selector == SIACHSelectors.LOGIN_BUTTON
        assert isinstance(selector, tuple)


class TestFasesProtocolo:
    """Testes para classe FasesProtocolo"""

    def test_fases_processaveis(self):
        """Testa fases que podem ser finalizadas"""
        assert FasesProtocolo.pode_finalizar('ABERTA') == True
        assert FasesProtocolo.pode_finalizar('EM ANDAMENTO') == True
        assert FasesProtocolo.pode_finalizar('em andamento') == True  # case insensitive

    def test_fases_sem_acao(self):
        """Testa fases que não permitem ação"""
        assert FasesProtocolo.pode_finalizar('FINALIZADA') == False
        assert FasesProtocolo.pode_finalizar('REABERTA') == False

        assert FasesProtocolo.ja_finalizado('FINALIZADA') == True
        assert FasesProtocolo.ja_finalizado('REABERTA') == True

    def test_fases_desconhecidas(self):
        """Testa fases não mapeadas"""
        assert FasesProtocolo.pode_finalizar('CANCELADA') == False
        assert FasesProtocolo.ja_finalizado('CANCELADA') == False

    def test_case_insensitive(self):
        """Testa se validação é case-insensitive"""
        assert FasesProtocolo.pode_finalizar('aberta') == True
        assert FasesProtocolo.pode_finalizar('ABERTA') == True
        assert FasesProtocolo.pode_finalizar('Aberta') == True


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
