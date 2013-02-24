#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re

files = [
    './banks/banespa/layout.php',
    './banks/bb/layout.php',
    './banks/bradesco/layout.php',
    './banks/cef/layout.php',
    './banks/cef_sinco/layout.php',
    './banks/hsbc/layout.php',
    './banks/itau/layout.php',
    './banks/nossacaixa/layout.php',
    './banks/real/layout.php',
    './banks/santader/layout.php',
    './banks/unibanco/layout.php',
]

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def replace(file_path):
    fh = file(file_path, 'r')
    subject = fh.read()
    fh.close()

    lines = {
        """Instruções de Impressão""": """<?php _e( 'Instru&ccedil;&otilde;es de Impress&atilde;o', 'wcboleto' ); ?>""",
        """Imprima em impressora jato de tinta (ink jet) ou laser em qualidade normal ou alta (Não use modo econômico).""": """<?php _e( 'Imprima em impressora jato de tinta (ink jet) ou laser em qualidade normal ou alta (N&atilde;o use modo econ&ocirc;mico).', 'wcboleto' ); ?>""",
        """Utilize folha A4 (210 x 297 mm) ou Carta (216 x 279 mm) e margens mínimas à esquerda e à direita do formulário.""": """<?php _e( 'Utilize folha A4 (210 x 297 mm) ou Carta (216 x 279 mm) e margens m&iacute;nimas &agrave; esquerda e &agrave; direita do formul&aacute;rio.', 'wcboleto' ); ?>""",
        """Corte na linha indicada. Não rasure, risque, fure ou dobre a região onde se encontra o código de barras.""": """<?php _e( 'Corte na linha indicada. N&atilde;o rasure, risque, fure ou dobre a regi&atilde;o onde se encontra o c&oacute;digo de barras.', 'wcboleto' ); ?>""",
        """Caso não apareça o código de barras no final, clique em F5 para atualizar esta tela.""": """<?php _e( 'Caso n&atilde;o apare&ccedil;a o c&oacute;digo de barras no final, clique em F5 para atualizar esta tela.', 'wcboleto' ); ?>""",
        """Caso tenha problemas ao imprimir, copie a seqüencia numérica abaixo e pague no caixa eletrônico ou no internet banking:""": """<?php _e( 'Caso tenha problemas ao imprimir, copie a seq&uuml;encia num&eacute;rica abaixo e pague no caixa eletr&ocirc;nico ou no internet banking:', 'wcboleto' ); ?>""",
        """Linha Digitável:""": """<?php _e( 'Linha Digit&aacute;vel:', 'wcboleto' ); ?>""",
        """Recibo do Sacado""": """<?php _e( 'Recibo do Sacado', 'wcboleto' ); ?>""",
        """Agência/Código do Cedente""": """<?php _e( 'Ag&ecirc;ncia/C&oacute;digo do Cedente', 'wcboleto' ); ?>""",
        """Nosso número""": """<?php _e( 'Nosso n&uacute;mero', 'wcboleto' ); ?>""",
        """Número do documento""": """<?php _e( 'N&uacute;mero do documento', 'wcboleto' ); ?>""",
        """(=) Valor documento""": """<?php _e( '(=) Valor documento', 'wcboleto' ); ?>""",
        """(-) Desconto / Abatimentos""": """<?php _e( '(-) Desconto / Abatimentos', 'wcboleto' ); ?>""",
        """(-) Outras deduções""": """<?php _e( '(-) Outras dedu&ccedil;&otilde;es', 'wcboleto' ); ?>""",
        """(+) Mora / Multa""": """<?php _e( '(+) Mora / Multa', 'wcboleto' ); ?>""",
        """(+) Outros acréscimos""": """<?php _e( '(+) Outros acr&eacute;scimos', 'wcboleto' ); ?>""",
        """(=) Valor cobrado""": """<?php _e( '(=) Valor cobrado', 'wcboleto' ); ?>""",
        """(=) Valor cobrado""": """<?php _e( '(=) Valor cobrado', 'wcboleto' ); ?>""",
        """Sacador/Avalista""": """<?php _e( 'Sacador/Avalista', 'wcboleto' ); ?>""",
        """Instruções (Texto de responsabilidade do cedente)""": """<?php _e( 'Instru&ccedil;&otilde;es (Texto de responsabilidade do cedente)', 'wcboleto' ); ?>""",
        """Autenticação mecânica""": """<?php _e( 'Autentica&ccedil;&atilde;o mec&acirc;nica', 'wcboleto' ); ?>""",
        """Corte na linha pontilhada""": """<?php _e( 'Corte na linha pontilhada', 'wcboleto' ); ?>""",
        """Local de pagamento""": """<?php _e( 'Local de pagamento', 'wcboleto' ); ?>""",
        """Pagável em qualquer Banco até o vencimento""": """<?php _e( 'Pag&aacute;vel em qualquer Banco at&eacute; o vencimento', 'wcboleto' ); ?>""",
        """Agência/Código cedente""": """<?php _e( 'Ag&ecirc;ncia/C&oacute;digo cedente', 'wcboleto' ); ?>""",
        """Data do documento""": """<?php _e( 'Data do documento', 'wcboleto' ); ?>""",
        """N<u>o</u> documento""": """<?php _e( 'N<u>o</u> documento', 'wcboleto' ); ?>""",
        """Espécie doc.""": """<?php _e( 'Esp&eacute;cie doc.', 'wcboleto' ); ?>""",
        """Data processamento""": """<?php _e( 'Data processamento', 'wcboleto' ); ?>""",
        """Uso do banco""": """<?php _e( 'Uso do banco', 'wcboleto' ); ?>""",
        """Ficha de Compensação""": """<?php _e( 'Ficha de Compensa&ccedil;&atilde;o', 'wcboleto' ); ?>""",
        """Cód. baixa""": """<?php _e( 'C&oacute;d. baixa', 'wcboleto' ); ?>""",
        """Valor documento""": """<?php _e( 'Valor documento', 'wcboleto' ); ?>""",
        """Valor:""": """<?php _e( 'Valor:', 'wcboleto' ); ?>""",
        """Cedente""": """<?php _e( 'Cedente', 'wcboleto' ); ?>""",
        """Espécie""": """<?php _e( 'Esp&eacute;cie', 'wcboleto' ); ?>""",
        """Quantidade""": """<?php _e( 'Quantidade', 'wcboleto' ); ?>""",
        """CPF/CNPJ""": """<?php _e( 'CPF/CNPJ', 'wcboleto' ); ?>""",
        """Vencimento""": """<?php _e( 'Vencimento', 'wcboleto' ); ?>""",
        """Sacado""": """<?php _e( 'Sacado', 'wcboleto' ); ?>""",
        """Demonstrativo""": """<?php _e( 'Demonstrativo', 'wcboleto' ); ?>""",
        """Aceite""": """<?php _e( 'Aceite', 'wcboleto' ); ?>""",
        """Carteira""": """<?php _e( 'Carteira', 'wcboleto' ); ?>""",
    }

    result = replace_all(subject, lines)

    f_out = file(file_path, 'w')
    f_out.write(result)
    f_out.close()


for file_path in files:
    replace(file_path)
