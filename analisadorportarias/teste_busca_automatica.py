#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste da funcionalidade de busca automática no DOU
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from busca_automatica_dou import BuscadorAutomaticoDOU
from datetime import datetime, timedelta

def testar_busca_automatica():
    """Testa a funcionalidade de busca automática"""
    print("🔍 TESTE DA BUSCA AUTOMÁTICA DOU")
    print("=" * 50)
    
    # Inicializar buscador
    buscador = BuscadorAutomaticoDOU()
    
    # Definir período de teste (últimos 30 dias)
    data_fim = datetime.now()
    data_inicio = data_fim - timedelta(days=30)
    
    data_inicio_str = data_inicio.strftime("%Y-%m-%d")
    data_fim_str = data_fim.strftime("%Y-%m-%d")
    
    print(f"📅 Período de teste: {data_inicio_str} a {data_fim_str}")
    print()
    
    try:
        # Testar busca de portarias
        print("1️⃣ Testando busca de portarias...")
        portarias = buscador.buscar_portarias_periodo(
            data_inicio=data_inicio_str,
            data_fim=data_fim_str
        )
        
        if portarias:
            print(f"✅ Encontradas {len(portarias)} portarias")
            
            # Mostrar algumas portarias encontradas
            for i, portaria in enumerate(portarias[:3], 1):
                print(f"   {i}. {portaria['titulo'][:100]}...")
                print(f"      Data: {portaria['data_publicacao']}")
                print(f"      URL: {portaria['url']}")
                print()
            
            # Testar análise das portarias
            print("2️⃣ Testando análise das portarias...")
            df = buscador.analisar_portarias_encontradas(portarias[:2])  # Analisar apenas 2 para teste
            
            if not df.empty:
                print(f"✅ Extraídos {len(df)} registros de pessoas")
                print("\n📊 Amostra dos dados:")
                print(df.head(3).to_string())
                
                # Testar geração de planilha
                print("\n3️⃣ Testando geração de planilha...")
                arquivo = buscador.gerar_planilha_periodo(
                    data_inicio=data_inicio_str,
                    data_fim=data_fim_str,
                    nome_arquivo="teste_busca_automatica.xlsx"
                )
                
                if arquivo and os.path.exists(arquivo):
                    print(f"✅ Planilha gerada: {arquivo}")
                    print(f"📊 Total de registros: {len(df)}")
                else:
                    print("❌ Erro ao gerar planilha")
            else:
                print("❌ Nenhum dado foi extraído das portarias")
        else:
            print("❌ Nenhuma portaria encontrada no período")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

def testar_busca_especifica():
    """Testa busca com palavras-chave específicas"""
    print("\n🔍 TESTE COM PALAVRAS-CHAVE ESPECÍFICAS")
    print("=" * 50)
    
    buscador = BuscadorAutomaticoDOU()
    
    # Definir período (últimos 7 dias)
    data_fim = datetime.now()
    data_inicio = data_fim - timedelta(days=7)
    
    data_inicio_str = data_inicio.strftime("%Y-%m-%d")
    data_fim_str = data_fim.strftime("%Y-%m-%d")
    
    # Palavras-chave específicas
    palavras_chave = ["PORTARIA", "naturalização"]
    
    print(f"📅 Período: {data_inicio_str} a {data_fim_str}")
    print(f"🔑 Palavras-chave: {', '.join(palavras_chave)}")
    print()
    
    try:
        portarias = buscador.buscar_portarias_periodo(
            data_inicio=data_inicio_str,
            data_fim=data_fim_str,
            palavras_chave=palavras_chave
        )
        
        if portarias:
            print(f"✅ Encontradas {len(portarias)} portarias")
            for portaria in portarias:
                print(f"   - {portaria['titulo'][:80]}...")
                print(f"     Palavra encontrada: {portaria['palavra_encontrada']}")
        else:
            print("❌ Nenhuma portaria encontrada")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando testes da busca automática...")
    print()
    
    # Teste principal
    testar_busca_automatica()
    
    # Teste com palavras-chave específicas
    testar_busca_especifica()
    
    print("\n✅ Testes concluídos!") 