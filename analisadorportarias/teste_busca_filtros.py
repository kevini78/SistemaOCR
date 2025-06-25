#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste da busca automática usando filtros específicos do DOU
Simula o processo manual: PORTARIA + Ministério da Justiça + Portaria + Secretaria Nacional de Justiça
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from busca_automatica_dou import BuscadorAutomaticoDOU

def testar_busca_com_filtros():
    """Testa a busca usando os filtros específicos do DOU"""
    print("🔍 TESTE DE BUSCA COM FILTROS ESPECÍFICOS DOU")
    print("=" * 60)
    print("Simulando: PORTARIA + Ministério da Justiça + Portaria + Secretaria Nacional de Justiça")
    print()
    
    buscador = BuscadorAutomaticoDOU()
    
    # Testar anos recentes onde sabemos que existem portarias
    anos_teste = [2024, 2023, 2022, 2021, 2020]
    
    for ano in anos_teste:
        print(f"\n📅 Testando ano {ano}")
        print("-" * 40)
        
        try:
            # Usar o novo método de busca por ano
            arquivo = buscador.buscar_portarias_por_ano(ano)
            
            if arquivo and os.path.exists(arquivo):
                print(f"✅ Sucesso! Arquivo gerado: {arquivo}")
                
                # Ler estatísticas
                import pandas as pd
                df = pd.read_excel(arquivo)
                print(f"📊 Total de registros: {len(df)}")
                
                if not df.empty:
                    print("📋 Amostra dos dados:")
                    print(df.head(2)[['nome', 'pais', 'estado', 'data_portaria']].to_string())
                
                return True  # Encontrou portarias, pode parar
            else:
                print(f"❌ Nenhuma portaria encontrada em {ano}")
                
        except Exception as e:
            print(f"❌ Erro no ano {ano}: {e}")
    
    return False

def testar_busca_especifica_periodo():
    """Testa busca específica em um período menor"""
    print("\n🔍 TESTE DE BUSCA ESPECÍFICA EM PERÍODO MENOR")
    print("=" * 60)
    
    buscador = BuscadorAutomaticoDOU()
    
    # Testar períodos menores onde é mais provável encontrar portarias
    periodos_teste = [
        ("2024-01-01", "2024-03-31", "Q1 2024"),
        ("2023-10-01", "2023-12-31", "Q4 2023"),
        ("2023-07-01", "2023-09-30", "Q3 2023"),
        ("2023-04-01", "2023-06-30", "Q2 2023"),
        ("2023-01-01", "2023-03-31", "Q1 2023"),
    ]
    
    for data_inicio, data_fim, descricao in periodos_teste:
        print(f"\n📅 Testando: {descricao}")
        print(f"   Período: {data_inicio} a {data_fim}")
        
        try:
            # Usar busca específica
            portarias = buscador.buscar_portarias_especificas(data_inicio, data_fim)
            
            if portarias:
                print(f"   ✅ Encontradas {len(portarias)} portarias")
                
                # Mostrar algumas portarias
                for i, portaria in enumerate(portarias[:2], 1):
                    print(f"      {i}. {portaria['titulo'][:80]}...")
                    print(f"         Data: {portaria['data_publicacao']}")
                
                # Testar análise
                print(f"   🔍 Analisando portarias...")
                df = buscador.analisar_portarias_encontradas(portarias)
                
                if not df.empty:
                    print(f"   ✅ Extraídos {len(df)} registros")
                    return True
                else:
                    print(f"   ⚠️ Nenhum dado extraído")
            else:
                print(f"   ❌ Nenhuma portaria encontrada")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    return False

def testar_api_querido_diario():
    """Testa se a API do Querido Diário está funcionando"""
    print("\n🔍 TESTE DE CONECTIVIDADE COM API")
    print("=" * 60)
    
    import requests
    
    try:
        # Teste simples da API
        url = "https://queridodiario.ok.org.br/api/gazettes"
        params = {
            'start_date': '2024-01-01',
            'end_date': '2024-01-31',
            'keywords': 'PORTARIA',
            'gazettes': 'DOU',
            'size': 10
        }
        
        print("🔗 Testando conexão com API do Querido Diário...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            print(f"✅ API funcionando! Status: {response.status_code}")
            print(f"📊 Resultados disponíveis: {len(dados.get('results', []))}")
            return True
        else:
            print(f"❌ Erro na API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TESTE COMPLETO DE BUSCA COM FILTROS")
    print("=" * 60)
    print("Este teste simula o processo manual de busca no DOU")
    print()
    
    # Teste 1: Conectividade
    api_ok = testar_api_querido_diario()
    
    if api_ok:
        # Teste 2: Busca por ano
        sucesso_ano = testar_busca_com_filtros()
        
        if not sucesso_ano:
            # Teste 3: Busca por período menor
            testar_busca_especifica_periodo()
    else:
        print("❌ API não está disponível. Verifique sua conexão com a internet.")
    
    print("\n✅ Testes concluídos!")
    print("\n💡 Dicas para melhorar os resultados:")
    print("   • Verifique se a API do Querido Diário está funcionando")
    print("   • Tente períodos menores (trimestres ou meses)")
    print("   • Considere que algumas portarias podem não estar indexadas")
    print("   • O sistema agora usa filtros específicos como no processo manual") 