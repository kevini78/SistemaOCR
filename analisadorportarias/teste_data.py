import pandas as pd
from datetime import datetime

def testar_normalizacao_data():
    """Testa a normalização de datas"""
    
    # Simular a função de normalização
    def normalizar_data_planilha(data_str):
        if not data_str:
            return ""
        
        data_str = str(data_str).strip()
        
        if '00:00:00' in data_str:
            try:
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
    
    # Testar diferentes formatos
    testes = [
        "29/4/1980",
        "2005-01-09 00:00:00",
        "2004-06-07 00:00:00",
        "1975-02-12 00:00:00",
        "15 de agosto de 1967",
        "31 de agosto de 1978",
        "27 de maio de 1985"
    ]
    
    print("Testando normalização de datas:")
    print("="*50)
    
    for teste in testes:
        resultado = normalizar_data_planilha(teste)
        print(f"'{teste}' -> '{resultado}'")
    
    # Testar com dados reais da planilha
    try:
        df = pd.read_excel('historico_naturalizacoes.xlsx')
        
        print(f"\nTestando com dados reais da planilha:")
        print("="*50)
        
        # Pegar algumas datas da planilha
        datas_planilha = df['DATA DE NASCIMENTO'].dropna().head(10)
        
        for data in datas_planilha:
            resultado = normalizar_data_planilha(data)
            print(f"'{data}' -> '{resultado}'")
            
    except Exception as e:
        print(f"Erro ao carregar planilha: {e}")

if __name__ == "__main__":
    testar_normalizacao_data() 