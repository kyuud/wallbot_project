"""
Testes para módulo de configuração

Execute:
    pytest tests/test_config.py -v
"""

import pytest
from config.config import WallBotConfig, EnvConfig


class TestWallBotConfig:
    """Testes para classe WallBotConfig"""

    def test_config_defaults(self):
        """Testa valores padrão da configuração"""
        assert WallBotConfig.NAVEGADOR_PADRAO == 'chrome'
        assert WallBotConfig.TIMEOUT_PADRAO == 15
        assert WallBotConfig.TIMEOUT_SALVAR == 30
        assert WallBotConfig.MAX_TENTATIVAS_RECONEXAO == 3
        assert WallBotConfig.ZOOM_NIVEL == '0.67'

    def test_urls(self):
        """Testa configuração de URLs"""
        assert WallBotConfig.URL_SIPCS.startswith('https://')
        assert 'cartoes.extracaixa' in WallBotConfig.URL_SIPCS

    def test_arquivos(self):
        """Testa configuração de arquivos"""
        assert WallBotConfig.ARQUIVO_PROGRESSO == 'progresso.txt'
        assert WallBotConfig.ARQUIVO_LOG == 'log_output.txt'
        assert WallBotConfig.ARQUIVO_RESULTADO == 'resultado_saida.xlsx'

    def test_timeouts(self):
        """Testa configuração de timeouts"""
        assert WallBotConfig.TIMEOUT_PADRAO > 0
        assert WallBotConfig.TIMEOUT_SALVAR >= WallBotConfig.TIMEOUT_PADRAO
        assert WallBotConfig.TIMEOUT_SCRIPT == 60
        assert WallBotConfig.TIMEOUT_PAGINA == 45

    def test_navegador_config(self):
        """Testa configuração de navegador"""
        assert WallBotConfig.WINDOW_WIDTH == 1920
        assert WallBotConfig.WINDOW_HEIGHT == 1080
        assert WallBotConfig.NAVEGADOR_PADRAO in ['chrome', 'firefox']

    def test_to_dict(self):
        """Testa conversão para dicionário"""
        config_dict = WallBotConfig.to_dict()

        assert isinstance(config_dict, dict)
        assert 'URL_SIPCS' in config_dict
        assert 'TIMEOUT_PADRAO' in config_dict
        assert 'NAVEGADOR_PADRAO' in config_dict

    def test_validar_config(self):
        """Testa validação da configuração"""
        result = WallBotConfig.validar_config()

        assert isinstance(result, dict)
        assert 'valido' in result
        assert 'erros' in result
        assert result['valido'] == True, f"Erros: {result['erros']}"
        assert len(result['erros']) == 0


class TestEnvConfig:
    """Testes para classe EnvConfig"""

    def test_get_navegador_default(self):
        """Testa navegador padrão"""
        navegador = EnvConfig.get_navegador()
        assert navegador in ['chrome', 'firefox']

    def test_get_timeout_default(self):
        """Testa timeout padrão"""
        timeout = EnvConfig.get_timeout_padrao()
        assert isinstance(timeout, int)
        assert timeout > 0

    def test_get_max_tentativas_default(self):
        """Testa max tentativas padrão"""
        max_tentativas = EnvConfig.get_max_tentativas_reconexao()
        assert isinstance(max_tentativas, int)
        assert max_tentativas >= 1

    def test_is_debug_mode_default(self):
        """Testa modo debug padrão"""
        debug = EnvConfig.is_debug_mode()
        assert isinstance(debug, bool)


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
