#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste da busca automática com períodos reais onde existem portarias
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from busca_automatica_dou import BuscadorAutomaticoDOU
from datetime import datetime, timedelta

def testar_periodos_reais():
    """Testa busca em períodos onde realmente existem portarias"""
    print("🔍 TESTE COM PERÍODOS REAIS")
    print("=" * 50)
    
    buscador = BuscadorAutomaticoDOU()
    
    # Períodos onde sabemos que existem portarias de naturalização
    periodos_teste = [
        ("2024-01-01", "2024-12-31", "2024 (ano completo)"),
        ("2023-01-01", "2023-12-31", "2023 (ano completo)"),
        ("2022-01-01", "2022-12-31", "2022 (ano completo)"),
        ("2021-01-01", "2021-12-31", "2021 (ano completo)"),
        ("2020-01-01", "2020-12-31", "2020 (ano completo)"),
        ("2019-01-01", "2019-12-31", "2019 (ano completo)"),
        ("2018-01-01", "2018-12-31", "2018 (ano completo)"),
        ("2024-06-01", "2024-06-30", "Junho 2024"),
        ("2024-05-01", "2024-05-31", "Maio 2024"),
        ("2024-04-01", "2024-04-30", "Abril 2024"),
    ]
    
    for data_inicio, data_fim, descricao in periodos_teste:
        print(f"\n📅 Testando: {descricao}")
        print(f"   Período: {data_inicio} a {data_fim}")
        
        try:
            # Buscar portarias
            portarias = buscador.buscar_portarias_periodo(
                data_inicio=data_inicio,
                data_fim=data_fim
            )
            
            if portarias:
                print(f"   ✅ Encontradas {len(portarias)} portarias")
                
                # Mostrar algumas portarias encontradas
                for i, portaria in enumerate(portarias[:2], 1):
                    print(f"      {i}. {portaria['titulo'][:80]}...")
                    print(f"         Data: {portaria['data_publicacao']}")
                
                # Testar análise com a primeira portaria
                if portarias:
                    print(f"   🔍 Analisando primeira portaria...")
                    df = buscador.analisar_portarias_encontradas(portarias[:1])
                    
                    if not df.empty:
                        print(f"   ✅ Extraídos {len(df)} registros")
                        print(f"   📊 Amostra: {df['nome'].iloc[0] if len(df) > 0 else 'N/A'}")
                        return True  # Encontrou portarias, pode parar
                    else:
                        print(f"   ⚠️ Nenhum dado extraído")
            else:
                print(f"   ❌ Nenhuma portaria encontrada")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    return False

def testar_palavras_chave_especificas():
    """Testa com palavras-chave mais específicas"""
    print("\n🔍 TESTE COM PALAVRAS-CHAVE ESPECÍFICAS")
    print("=" * 50)
    
    buscador = BuscadorAutomaticoDOU()
    
    # Período mais amplo
    data_inicio = "2023-01-01"
    data_fim = "2023-12-31"
    
    # Palavras-chave mais específicas
    palavras_chave = [
        "PORTARIA",
        "naturalização",
        "nacionalidade brasileira",
        "art. 65",
        "art. 67",
        "art. 70",
        "deferimento",
        "naturalizacao"
    ]
    
    print(f"📅 Período: {data_inicio} a {data_fim}")
    print(f"🔑 Palavras-chave: {', '.join(palavras_chave)}")
    
    try:
        portarias = buscador.buscar_portarias_periodo(
            data_inicio=data_inicio,
            data_fim=data_fim,
            palavras_chave=palavras_chave
        )
        
        if portarias:
            print(f"✅ Encontradas {len(portarias)} portarias")
            for portaria in portarias[:3]:
                print(f"   - {portaria['titulo'][:100]}...")
                print(f"     Palavra: {portaria['palavra_encontrada']}")
                print(f"     Data: {portaria['data_publicacao']}")
        else:
            print("❌ Nenhuma portaria encontrada")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def testar_busca_por_mes():
    """Testa busca por mês específico"""
    print("\n🔍 TESTE POR MÊS ESPECÍFICO")
    print("=" * 50)
    
    buscador = BuscadorAutomaticoDOU()
    
    # Testar alguns meses específicos
    meses_teste = [
        ("2023-12-01", "2023-12-31", "Dezembro 2023"),
        ("2023-11-01", "2023-11-30", "Novembro 2023"),
        ("2023-10-01", "2023-10-31", "Outubro 2023"),
        ("2023-09-01", "2023-09-30", "Setembro 2023"),
        ("2023-08-01", "2023-08-31", "Agosto 2023"),
    ]
    
    for data_inicio, data_fim, descricao in meses_teste:
        print(f"\n📅 Testando: {descricao}")
        
        try:
            portarias = buscador.buscar_portarias_periodo(
                data_inicio=data_inicio,
                data_fim=data_fim
            )
            
            if portarias:
                print(f"   ✅ Encontradas {len(portarias)} portarias")
                return True
            else:
                print(f"   ❌ Nenhuma portaria encontrada")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    return False

if __name__ == "__main__":
    print("🚀 TESTE DE BUSCA COM PERÍODOS REAIS")
    print("=" * 60)
    print("Este teste busca em períodos onde realmente existem portarias")
    print()
    
    # Teste 1: Períodos reais
    sucesso = testar_periodos_reais()
    
    if not sucesso:
        # Teste 2: Palavras-chave específicas
        testar_palavras_chave_especificas()
        
        # Teste 3: Por mês
        testar_busca_por_mes()
    
    print("\n✅ Testes concluídos!")
    print("\n💡 Se nenhuma portaria foi encontrada:")
    print("   • Verifique sua conexão com a internet")
    print("   • A API do Querido Diário pode estar temporariamente indisponível")
    print("   • Tente períodos diferentes")
    print("   • Considere usar palavras-chave mais específicas") 