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
        """    Instruções de Impressão\n""": """    <?php _e( 'Instru&ccedil;&otilde;es de Impress&atilde;o', 'wcboleto' ); ?>\n""",
        """<li>Imprima em impressora jato de tinta (ink jet) ou laser em qualidade normal ou alta (Não use modo econômico).<br>""": """<li><?php _e( 'Imprima em impressora jato de tinta (ink jet) ou laser em qualidade normal ou alta (N&atilde;o use modo econ&ocirc;mico).', 'wcboleto' ); ?><br>""",
        """<li>Utilize folha A4 (210 x 297 mm) ou Carta (216 x 279 mm) e margens mínimas à esquerda e à direita do formulário.<br>""": """<li><?php _e( 'Utilize folha A4 (210 x 297 mm) ou Carta (216 x 279 mm) e margens m&iacute;nimas &agrave; esquerda e &agrave; direita do formul&aacute;rio.', 'wcboleto' ); ?><br>""",
        """<li>Corte na linha indicada. Não rasure, risque, fure ou dobre a região onde se encontra o código de barras.<br>""": """<li><?php _e( 'Corte na linha indicada. N&atilde;o rasure, risque, fure ou dobre a regi&atilde;o onde se encontra o c&oacute;digo de barras.', 'wcboleto' ); ?><br>""",
        """<li>Caso não apareça o código de barras no final, clique em F5 para atualizar esta tela.\n""": """<li><?php _e( 'Caso n&atilde;o apare&ccedil;a o c&oacute;digo de barras no final, clique em F5 para atualizar esta tela.', 'wcboleto' ); ?>\n""",
        """<li>Caso tenha problemas ao imprimir, copie a seqüencia numérica abaixo e pague no caixa eletrônico ou no internet banking:<br>""": """<li><?php _e( 'Caso tenha problemas ao imprimir, copie a seq&uuml;encia num&eacute;rica abaixo e pague no caixa eletr&ocirc;nico ou no internet banking:', 'wcboleto' ); ?><br>""",
        """&nbsp;Linha Digitável: &nbsp;""": """&nbsp;<?php _e( 'Linha Digit&aacute;vel:', 'wcboleto' ); ?> &nbsp;""",
        """<b class="cp">Recibo do Sacado</b>""": """<b class="cp"><?php _e( 'Recibo do Sacado', 'wcboleto' ); ?></b>""",
        """    Agência/Código do Cedente\n""": """    <?php _e( 'Ag&ecirc;ncia/C&oacute;digo do Cedente', 'wcboleto' ); ?>\n""",
        """    Nosso número\n""": """    <?php _e( 'Nosso n&uacute;mero', 'wcboleto' ); ?>\n""",
        """    Número do documento\n""": """    <?php _e( 'N&uacute;mero do documento', 'wcboleto' ); ?>\n""",
        """    (=) Valor documento\n""": """    <?php _e( '(=) Valor documento', 'wcboleto' ); ?>\n""",
        """    (-) Desconto / Abatimentos\n""": """    <?php _e( '(-) Desconto / Abatimentos', 'wcboleto' ); ?>\n""",
        """    (-) Outras deduções\n""": """    <?php _e( '(-) Outras dedu&ccedil;&otilde;es', 'wcboleto' ); ?>\n""",
        """    (+) Mora / Multa\n""": """    <?php _e( '(+) Mora / Multa', 'wcboleto' ); ?>\n""",
        """    (+) Outros acréscimos\n""": """    <?php _e( '(+) Outros acr&eacute;scimos', 'wcboleto' ); ?>\n""",
        """    (=) Valor cobrado\n""": """    <?php _e( '(=) Valor cobrado', 'wcboleto' ); ?>\n""",
        """    (=) Valor cobrado\n""": """    <?php _e( '(=) Valor cobrado', 'wcboleto' ); ?>\n""",
        """    Sacador/Avalista\n""": """    <?php _e( 'Sacador/Avalista', 'wcboleto' ); ?>\n""",
        """<font class="ct">Instruções (Texto de responsabilidade do cedente)</font><br>""": """<font class="ct"><?php _e( 'Instru&ccedil;&otilde;es (Texto de responsabilidade do cedente)', 'wcboleto' ); ?></font><br>""",
        """    Autenticação mecânica - <b class="cp">""": """    <?php _e( 'Autentica&ccedil;&atilde;o mec&acirc;nica', 'wcboleto' ); ?> - <b class="cp">""",
        """    Corte na linha pontilhada\n""": """    <?php _e( 'Corte na linha pontilhada', 'wcboleto' ); ?>\n""",
        """    Local de pagamento\n""": """    <?php _e( 'Local de pagamento', 'wcboleto' ); ?>\n""",
        """    Pagável em qualquer Banco até o vencimento\n""": """    <?php _e( 'Pag&aacute;vel em qualquer Banco at&eacute; o vencimento', 'wcboleto' ); ?>\n""",
        """    Agência/Código cedente\n""": """    <?php _e( 'Ag&ecirc;ncia/C&oacute;digo cedente', 'wcboleto' ); ?>\n""",
        """    Data do documento\n""": """    <?php _e( 'Data do documento', 'wcboleto' ); ?>\n""",
        """    N<u>o</u> documento\n""": """    <?php _e( 'N<u>o</u> documento', 'wcboleto' ); ?>\n""",
        """    Espécie doc.\n""": """    <?php _e( 'Esp&eacute;cie doc.', 'wcboleto' ); ?>\n""",
        """    Data processamento\n""": """    <?php _e( 'Data processamento', 'wcboleto' ); ?>\n""",
        """    Uso do banco\n""": """    <?php _e( 'Uso do banco', 'wcboleto' ); ?>\n""",
        """<b class="cp">Ficha de Compensação</b>""": """<b class="cp"><?php _e( 'Ficha de Compensa&ccedil;&atilde;o', 'wcboleto' ); ?></b>""",
        """    Cód. baixa\n""": """    <?php _e( 'C&oacute;d. baixa', 'wcboleto' ); ?>\n""",
        """    Valor documento\n""": """    <?php _e( 'Valor documento', 'wcboleto' ); ?>\n""",
        """    Valor Documento\n""": """    <?php _e( 'Valor Documento', 'wcboleto' ); ?>\n""",
        """&nbsp;Valor: &nbsp;""": """&nbsp;<?php _e( 'Valor:', 'wcboleto' ); ?>&nbsp;""",
        """    Cedente\n""": """    <?php _e( 'Cedente', 'wcboleto' ); ?>\n""",
        """    Espécie\n""": """    <?php _e( 'Esp&eacute;cie', 'wcboleto' ); ?>\n""",
        """    Quantidade\n""": """    <?php _e( 'Quantidade', 'wcboleto' ); ?>\n""",
        """    CPF/CNPJ\n""": """    <?php _e( 'CPF/CNPJ', 'wcboleto' ); ?>\n""",
        """    Vencimento\n""": """    <?php _e( 'Vencimento', 'wcboleto' ); ?>\n""",
        """    Sacado\n""": """    <?php _e( 'Sacado', 'wcboleto' ); ?>\n""",
        """    Demonstrativo\n""": """    <?php _e( 'Demonstrativo', 'wcboleto' ); ?>\n""",
        """    Aceite\n""": """    <?php _e( 'Aceite', 'wcboleto' ); ?>\n""",
        """    Carteira\n""": """    <?php _e( 'Carteira', 'wcboleto' ); ?>\n""",
        """<?=""": """<?php echo """,
    }

    result = replace_all(subject, lines)

    f_out = file(file_path, 'w')
    f_out.write(result)
    f_out.close()


for file_path in files:
    replace(file_path)
