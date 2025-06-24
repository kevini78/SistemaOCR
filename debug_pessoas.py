#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analisadorportarias.portaria_analyzer import PortariaAnalyzer

def debug_pessoas_faltantes():
    """Debuga por que algumas pessoas não estão sendo captadas"""
    
    # Ler o arquivo de teste
    with open('teste_portarias.txt', 'r', encoding='utf-8') as f:
        texto_completo = f.read()
    
    print("=== DEBUG PESSOAS FALTANTES ===")
    
    # Criar instância do analisador
    analyzer = PortariaAnalyzer()
    
    # Pessoas que sabemos que estão faltando
    pessoas_faltantes = [
        'ADAMA SANOGO',
        'AMALIA LAURA PASQUALINI', 
        'CLEETCHY CHOULOUTE',
        'OMAR SALLAM'
    ]
    
    # Verificar se essas pessoas estão no texto
    print("\n=== VERIFICANDO SE PESSOAS ESTÃO NO TEXTO ===")
    for pessoa in pessoas_faltantes:
        if pessoa in texto_completo:
            print(f"✅ {pessoa} - ENCONTRADA no texto")
        else:
            print(f"❌ {pessoa} - NÃO ENCONTRADA no texto")
    
    # Testar extração de pessoas em cada portaria individualmente
    print("\n=== TESTANDO EXTRAÇÃO POR PORTARIA ===")
    
    # Separar as portarias manualmente
    portarias = [
        ("PORTARIA 5.124", texto_completo[texto_completo.find("PORTARIA Nº 5.124"):texto_completo.find("PORTARIA Nº 5.125")]),
        ("PORTARIA 5.125", texto_completo[texto_completo.find("PORTARIA Nº 5.125"):texto_completo.find("PORTARIA Nº 5.126")]),
        ("PORTARIA 5.126", texto_completo[texto_completo.find("PORTARIA Nº 5.126"):texto_completo.find("PORTARIA Nº 5.127")]),
        ("PORTARIA 5.127", texto_completo[texto_completo.find("PORTARIA Nº 5.127"):])
    ]
    
    for nome_portaria, texto_portaria in portarias:
        print(f"\n--- {nome_portaria} ---")
        pessoas = analyzer.extrair_pessoas(texto_portaria)
        
        # Verificar se as pessoas faltantes estão nesta portaria
        for pessoa_faltante in pessoas_faltantes:
            if pessoa_faltante in texto_portaria:
                encontrada = any(p['nome'].upper() == pessoa_faltante.upper() for p in pessoas)
                if encontrada:
                    print(f"✅ {pessoa_faltante} - EXTRAÍDA")
                else:
                    print(f"❌ {pessoa_faltante} - NO TEXTO MAS NÃO EXTRAÍDA")
                    
                    # Debug: mostrar o contexto onde a pessoa aparece
                    pos = texto_portaria.find(pessoa_faltante)
                    if pos != -1:
                        inicio = max(0, pos - 100)
                        fim = min(len(texto_portaria), pos + 200)
                        contexto = texto_portaria[inicio:fim]
                        print(f"   Contexto: {contexto}")
                        
                        # Verificar se o padrão de documento está sendo encontrado
                        doc_match = re.search(r'([A-Za-z]+\d+[-][A-Za-z0-9]+|Processo\s+[\d\./]+)', contexto)
                        if doc_match:
                            print(f"   Documento encontrado: {doc_match.group(1)}")
                        else:
                            print(f"   ❌ Documento NÃO encontrado")
                        
                        # Verificar se o país está sendo encontrado
                        pais_match = re.search(r'natural\s+d[aeo]\s+([A-Za-zÀ-ú\s\-]+)', contexto, re.IGNORECASE)
                        if pais_match:
                            print(f"   País encontrado: {pais_match.group(1)}")
                        else:
                            print(f"   ❌ País NÃO encontrado")

if __name__ == "__main__":
    debug_pessoas_faltantes() 