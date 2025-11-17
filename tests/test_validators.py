"""
Testes para módulo de validadores

Execute:
    pytest tests/test_validators.py -v
"""

import pytest
import os
from validators.page_validators import (
    validar_arquivo_excel,
    validar_email,
    validar_credenciais,
    validar_script_personalizacao,
    verificar_erro_conexao
)


class TestValidarArquivoExcel:
    """Testes para validação de arquivos Excel"""

    def test_arquivo_valido(self):
        """Testa arquivo Excel válido"""
        # Criar arquivo temporário para teste
        test_file = "test_temp.xlsx"
        with open(test_file, 'w') as f:
            f.write("test")

        try:
            valido, msg = validar_arquivo_excel(test_file)
            assert valido == True
            assert msg == ""
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_arquivo_inexistente(self):
        """Testa arquivo que não existe"""
        valido, msg = validar_arquivo_excel("arquivo_inexistente.xlsx")
        assert valido == False
        assert "não encontrado" in msg.lower()

    def test_arquivo_vazio(self):
        """Testa string vazia"""
        valido, msg = validar_arquivo_excel("")
        assert valido == False
        assert "nenhum arquivo" in msg.lower()

    def test_extensao_invalida(self):
        """Testa arquivo com extensão inválida"""
        valido, msg = validar_arquivo_excel("arquivo.txt")
        assert valido == False
        assert "excel" in msg.lower()


class TestValidarEmail:
    """Testes para validação de email"""

    def test_email_valido(self):
        """Testa emails válidos"""
        emails_validos = [
            "usuario@dominio.com",
            "usuario@dominio.com.br",
            "user.name@example.co.uk",
            "test123@test.org"
        ]

        for email in emails_validos:
            valido, msg = validar_email(email)
            assert valido == True, f"Email '{email}' deveria ser válido"
            assert msg == ""

    def test_email_sem_arroba(self):
        """Testa email sem @"""
        valido, msg = validar_email("usuariodominio.com")
        assert valido == False
        assert "@" in msg

    def test_email_sem_dominio(self):
        """Testa email sem domínio"""
        valido, msg = validar_email("usuario@")
        assert valido == False
        assert "domínio" in msg.lower()

    def test_email_vazio(self):
        """Testa email vazio"""
        valido, msg = validar_email("")
        assert valido == False
        assert "vazio" in msg.lower()

    def test_email_sem_ponto(self):
        """Testa email sem ponto no domínio"""
        valido, msg = validar_email("usuario@dominio")
        assert valido == False


class TestValidarCredenciais:
    """Testes para validação de credenciais"""

    def test_credenciais_validas(self):
        """Testa credenciais válidas"""
        valido, msg = validar_credenciais("user@test.com", "senha123")
        assert valido == True
        assert msg == ""

    def test_email_invalido(self):
        """Testa com email inválido"""
        valido, msg = validar_credenciais("emailinvalido", "senha123")
        assert valido == False

    def test_senha_muito_curta(self):
        """Testa senha muito curta"""
        valido, msg = validar_credenciais("user@test.com", "12")
        assert valido == False
        assert "curta" in msg.lower()

    def test_campos_vazios(self):
        """Testa campos vazios"""
        valido, msg = validar_credenciais("", "")
        assert valido == False
        assert "obrigatório" in msg.lower()


class TestValidarScriptPersonalizacao:
    """Testes para validação de script"""

    def test_script_valido_sem_personalizacao(self):
        """Testa script válido sem personalização"""
        script = "Protocolo finalizado com sucesso"
        valido, msg = validar_script_personalizacao(script, usar_personalizacao=False)
        assert valido == True
        assert msg == ""

    def test_script_valido_com_personalizacao(self):
        """Testa script válido com personalização"""
        script = "Olá @NomeCliente@, protocolo finalizado"
        valido, msg = validar_script_personalizacao(script, usar_personalizacao=True)
        assert valido == True
        assert msg == ""

    def test_script_sem_placeholder(self):
        """Testa script sem placeholder mas com personalização ativa"""
        script = "Protocolo finalizado"
        valido, msg = validar_script_personalizacao(script, usar_personalizacao=True)
        assert valido == True  # Retorna True mas com aviso
        assert "@NomeCliente@" in msg

    def test_script_vazio(self):
        """Testa script vazio"""
        valido, msg = validar_script_personalizacao("", usar_personalizacao=False)
        assert valido == False
        assert "vazio" in msg.lower()


class TestVerificarErroConexao:
    """Testes para verificação de erros de conexão"""

    def test_erro_http_connection(self):
        """Testa detecção de HTTPConnectionPool"""
        assert verificar_erro_conexao("HTTPConnectionPool error") == True

    def test_erro_timeout(self):
        """Testa detecção de timeout"""
        assert verificar_erro_conexao("Read timed out") == True
        assert verificar_erro_conexao("Connection timeout") == True

    def test_erro_target_frame(self):
        """Testa detecção de target frame detached"""
        assert verificar_erro_conexao("target frame detached") == True

    def test_erro_connection_refused(self):
        """Testa detecção de connection refused"""
        assert verificar_erro_conexao("Connection refused") == True

    def test_erro_nao_conexao(self):
        """Testa que erro comum não é classificado como conexão"""
        assert verificar_erro_conexao("Element not found") == False
        assert verificar_erro_conexao("Invalid selector") == False

    def test_case_insensitive(self):
        """Testa detecção case-insensitive"""
        assert verificar_erro_conexao("httpconnectionpool error") == True
        assert verificar_erro_conexao("READ TIMED OUT") == True


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
