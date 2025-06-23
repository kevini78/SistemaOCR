import pandas as pd
import re

def testar_mariana_rigoroso():
    """Testa a verificação rigorosa para MARIANA DA CONCEICAO MATIAS NGUNZA"""
    
    try:
        # Carregar planilha
        df = pd.read_excel('historico_naturalizacoes.xlsx')
        print(f"Planilha carregada: {len(df)} registros")
        
        # Dados da pessoa para testar
        nome_teste = "MARIANA DA CONCEICAO MATIAS NGUNZA"
        data_teste = "29 de abril de 1980"  # Data que está na planilha
        
        print(f"\n🔍 Testando verificação rigorosa para:")
        print(f"   Nome: {nome_teste}")
        print(f"   Data: {data_teste}")
        print("="*60)
        
        # Simular a função de normalização
        def normalizar_data_planilha(data_str):
            if not data_str:
                return ""
            
            data_str = str(data_str).strip()
            
            if '00:00:00' in data_str:
                try:
                    from datetime import datetime
                    dt = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
                    meses_nomes = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
                                  'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
                    mes_nome = meses_nomes[dt.month - 1]
                    return f"{dt.day} de {mes_nome} de {dt.year}"
                except:
                    pass
            
            if '/' in data_str:
                try:
                    partes = data_str.split('/')
                    dia = int(partes[0])
                    mes = int(partes[1])
                    ano = int(partes[2])
                    
                    meses_nomes = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
                                  'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
                    mes_nome = meses_nomes[mes - 1]
                    
                    return f"{dia} de {mes_nome} de {ano}"
                except:
                    pass
            
            return data_str
        
        # Busca rigorosa: nome EXATO E data EXATA
        mask_exato = (
            (df['NOME COMPLETO'].str.upper() == nome_teste) &
            (df['DATA DE NASCIMENTO'].astype(str).apply(normalizar_data_planilha) == data_teste)
        )
        resultados_exatos = df[mask_exato]
        
        print(f"1. Busca rigorosa (nome EXATO E data EXATA): {len(resultados_exatos)} resultados")
        
        if len(resultados_exatos) > 0:
            for _, row in resultados_exatos.iterrows():
                print(f"   ✅ ENCONTRADA: {row['NOME COMPLETO']}")
                print(f"      Data: {row.get('DATA DE NASCIMENTO', 'N/A')}")
                print(f"      Portaria: {row.get('Nº da Portaria', 'N/A')}")
                print(f"      Mês/Ano: {row.get('Mês', 'N/A')}/{row.get('Ano', 'N/A')}")
        else:
            print("   ❌ NÃO ENCONTRADA")
            
            # Verificar por que não encontrou
            print(f"\n2. Debug - Verificando separadamente:")
            
            # Verificar nome
            mask_nome = df['NOME COMPLETO'].str.upper() == nome_teste
            resultados_nome = df[mask_nome]
            print(f"   Nome exato encontrado: {len(resultados_nome)}")
            
            if len(resultados_nome) > 0:
                for _, row in resultados_nome.iterrows():
                    data_historico = row.get('DATA DE NASCIMENTO', 'N/A')
                    data_normalizada = normalizar_data_planilha(data_historico)
                    print(f"      - Data original: '{data_historico}'")
                    print(f"      - Data normalizada: '{data_normalizada}'")
                    print(f"      - Data esperada: '{data_teste}'")
                    print(f"      - Datas iguais: {data_normalizada == data_teste}")
            
            # Verificar data
            mask_data = df['DATA DE NASCIMENTO'].astype(str).apply(normalizar_data_planilha) == data_teste
            resultados_data = df[mask_data]
            print(f"   Data exata encontrada: {len(resultados_data)}")
            
            if len(resultados_data) > 0:
                for _, row in resultados_data.iterrows():
                    nome_historico = row.get('NOME COMPLETO', 'N/A')
                    print(f"      - Nome: '{nome_historico}'")
                    print(f"      - Nome esperado: '{nome_teste}'")
                    print(f"      - Nomes iguais: {nome_historico.upper() == nome_teste}")
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_mariana_rigoroso() 