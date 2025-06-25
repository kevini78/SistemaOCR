#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para busca automática de portarias de naturalização no DOU
Baseado no conceito do Ro-DOU (https://github.com/gestaogovbr/Ro-dou)
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import json
import os
from typing import List, Dict, Optional
from portaria_analyzer import PortariaAnalyzer

class BuscadorAutomaticoDOU:
    def __init__(self):
        """Inicializa o buscador automático do DOU"""
        self.base_url = "https://queridodiario.ok.org.br/api"
        self.analyzer = PortariaAnalyzer()
        
    def buscar_portarias_periodo(self, data_inicio: str, data_fim: str, 
                                palavras_chave: List[str] = None) -> List[Dict]:
        """
        Busca portarias de naturalização em um período específico
        
        Args:
            data_inicio: Data de início (YYYY-MM-DD)
            data_fim: Data de fim (YYYY-MM-DD)
            palavras_chave: Lista de palavras-chave para busca
            
        Returns:
            Lista de portarias encontradas
        """
        if palavras_chave is None:
            palavras_chave = [
                "naturalização",
                "naturalizacao", 
                "PORTARIA",
                "nacionalidade brasileira",
                "art. 65",
                "art. 67", 
                "art. 70",
                "deferimento",
                "naturalizar",
                "naturalizado",
                "naturalizada",
                "cidadania brasileira",
                "brasileiro nato",
                "brasileira nata",
                "processo de naturalização",
                "concessão de nacionalidade",
                "concessao de nacionalidade"
            ]
        
        print(f"🔍 Buscando portarias de {data_inicio} até {data_fim}")
        print(f"📝 Palavras-chave: {', '.join(palavras_chave)}")
        
        portarias_encontradas = []
        
        try:
            # Buscar no DOU usando a API do Querido Diário
            for palavra in palavras_chave:
                print(f"Buscando por: {palavra}")
                
                # Parâmetros da busca
                params = {
                    'start_date': data_inicio,
                    'end_date': data_fim,
                    'keywords': palavra,
                    'gazettes': 'DOU',  # Apenas Diário Oficial da União
                    'size': 100  # Máximo de resultados por busca
                }
                
                response = requests.get(f"{self.base_url}/gazettes", params=params)
                
                if response.status_code == 200:
                    dados = response.json()
                    
                    if 'results' in dados:
                        for resultado in dados['results']:
                            # Verificar se é uma portaria de naturalização
                            if self._eh_portaria_naturalizacao(resultado):
                                portaria_info = {
                                    'url': resultado.get('url'),
                                    'data_publicacao': resultado.get('date'),
                                    'titulo': resultado.get('title', ''),
                                    'conteudo': resultado.get('content', ''),
                                    'palavra_encontrada': palavra
                                }
                                portarias_encontradas.append(portaria_info)
                                print(f"✅ Encontrada: {resultado.get('title', 'Sem título')}")
                
                # Pausa para não sobrecarregar a API
                time.sleep(1)
                
        except Exception as e:
            print(f"❌ Erro na busca: {e}")
        
        # Remover duplicatas baseado na URL
        portarias_unicas = []
        urls_vistas = set()
        
        for portaria in portarias_encontradas:
            if portaria['url'] not in urls_vistas:
                portarias_unicas.append(portaria)
                urls_vistas.add(portaria['url'])
        
        print(f"📊 Total de portarias únicas encontradas: {len(portarias_unicas)}")
        return portarias_unicas
    
    def _eh_portaria_naturalizacao(self, resultado: Dict) -> bool:
        """
        Verifica se o resultado é uma portaria de naturalização
        
        Args:
            resultado: Dicionário com dados do resultado da busca
            
        Returns:
            True se for portaria de naturalização
        """
        titulo = resultado.get('title', '').lower()
        conteudo = resultado.get('content', '').lower()
        
        # Palavras-chave que indicam portaria de naturalização
        indicadores = [
            'portaria',
            'naturalização',
            'naturalizacao',
            'nacionalidade brasileira',
            'art. 65',
            'art. 67',
            'art. 70',
            'deferimento',
            'naturalizar',
            'naturalizado',
            'naturalizada',
            'cidadania brasileira',
            'brasileiro nato',
            'brasileira nata',
            'processo de naturalização',
            'concessão de nacionalidade',
            'concessao de nacionalidade'
        ]
        
        # Verificar se contém pelo menos 1 indicador (mais flexível)
        contadores = 0
        for indicador in indicadores:
            if indicador in titulo or indicador in conteudo:
                contadores += 1
        
        # Se contém pelo menos 1 indicador, é provavelmente uma portaria de naturalização
        return contadores >= 1
    
    def analisar_portarias_encontradas(self, portarias: List[Dict]) -> pd.DataFrame:
        """
        Analisa as portarias encontradas e retorna um DataFrame com os dados
        
        Args:
            portarias: Lista de portarias encontradas
            
        Returns:
            DataFrame com dados das pessoas naturalizadas
        """
        print(f"🔍 Analisando {len(portarias)} portarias encontradas...")
        
        todas_pessoas = []
        
        for i, portaria in enumerate(portarias, 1):
            print(f"\n📋 Analisando portaria {i}/{len(portarias)}")
            print(f"📅 Data: {portaria['data_publicacao']}")
            print(f"🔗 URL: {portaria['url']}")
            
            try:
                # Analisar a portaria usando nosso sistema
                if portaria.get('conteudo'):
                    # Usar o conteúdo direto se disponível
                    resultados, _ = self.analyzer.analisar_multiplas_portarias(
                        portaria['conteudo'], 
                        gerar_excel=False
                    )
                else:
                    # Tentar buscar o conteúdo da URL
                    resultados, _ = self.analyzer.analisar_portaria(
                        portaria['url'], 
                        gerar_excel=False
                    )
                
                # Processar resultados
                if isinstance(resultados, list):
                    for resultado in resultados:
                        if resultado.get('dados_portaria'):
                            dados = resultado['dados_portaria']
                            for pessoa in dados.get('pessoas', []):
                                pessoa_info = {
                                    'nome': pessoa.get('nome', ''),
                                    'documento': pessoa.get('documento', ''),
                                    'tipo_documento': pessoa.get('tipo_documento', ''),
                                    'processo': pessoa.get('processo', ''),
                                    'pais': pessoa.get('pais', ''),
                                    'estado': pessoa.get('estado', ''),
                                    'idade': pessoa.get('idade', ''),
                                    'data_nascimento': pessoa.get('data_nascimento', ''),
                                    'nome_pai': pessoa.get('nome_pai', ''),
                                    'numero_portaria': dados.get('numero', ''),
                                    'data_portaria': dados.get('data', ''),
                                    'tipo_naturalizacao': dados.get('tipo', ''),
                                    'data_publicacao_dou': portaria['data_publicacao'],
                                    'url_portaria': portaria['url']
                                }
                                todas_pessoas.append(pessoa_info)
                
            except Exception as e:
                print(f"❌ Erro ao analisar portaria: {e}")
                continue
        
        # Criar DataFrame
        if todas_pessoas:
            df = pd.DataFrame(todas_pessoas)
            print(f"✅ Total de pessoas extraídas: {len(df)}")
            return df
        else:
            print("❌ Nenhuma pessoa foi extraída")
            return pd.DataFrame()
    
    def gerar_planilha_periodo(self, data_inicio: str, data_fim: str, 
                              nome_arquivo: str = None) -> str:
        """
        Busca portarias de um período e gera planilha com os dados
        
        Args:
            data_inicio: Data de início (YYYY-MM-DD)
            data_fim: Data de fim (YYYY-MM-DD)
            nome_arquivo: Nome do arquivo de saída
            
        Returns:
            Caminho do arquivo gerado
        """
        print(f"🚀 Iniciando busca automática de {data_inicio} até {data_fim}")
        
        # Primeiro tentar busca específica (mais eficiente)
        print("🔍 Tentando busca específica (PORTARIA + Ministério da Justiça + Secretaria Nacional de Justiça)...")
        portarias = self.buscar_portarias_especificas(data_inicio, data_fim)
        
        # Se não encontrar nada, tentar busca geral
        if not portarias:
            print("⚠️ Busca específica não retornou resultados, tentando busca geral...")
            portarias = self.buscar_portarias_periodo(data_inicio, data_fim)
        
        if not portarias:
            print("❌ Nenhuma portaria encontrada no período")
            return None
        
        # Analisar portarias
        df = self.analisar_portarias_encontradas(portarias)
        
        if df.empty:
            print("❌ Nenhum dado foi extraído")
            return None
        
        # Gerar arquivo
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"naturalizacoes_{data_inicio}_a_{data_fim}_{timestamp}.xlsx"
        
        # Salvar planilha
        df.to_excel(nome_arquivo, index=False, engine='openpyxl')
        
        print(f"✅ Planilha gerada: {nome_arquivo}")
        print(f"📊 Total de registros: {len(df)}")
        
        return nome_arquivo

    def buscar_portarias_especificas(self, data_inicio: str, data_fim: str) -> List[Dict]:
        """
        Busca portarias de naturalização usando filtros específicos do DOU
        Simula o processo manual: PORTARIA + Ministério da Justiça + Portaria + Secretaria Nacional de Justiça
        
        Args:
            data_inicio: Data de início (YYYY-MM-DD)
            data_fim: Data de fim (YYYY-MM-DD)
            
        Returns:
            Lista de portarias encontradas
        """
        print(f"🔍 Busca específica: PORTARIA + Ministério da Justiça + Secretaria Nacional de Justiça")
        print(f"📅 Período: {data_inicio} até {data_fim}")
        
        portarias_encontradas = []
        
        try:
            # Busca específica usando os filtros do DOU
            params = {
                'start_date': data_inicio,
                'end_date': data_fim,
                'keywords': 'PORTARIA',
                'gazettes': 'DOU',
                'size': 200,  # Aumentar para pegar mais resultados
                'organization': 'ministerio-da-justica-e-seguranca-publica',  # Ministério da Justiça
                'sub_organization': 'secretaria-nacional-de-justica',  # Secretaria Nacional de Justiça
                'act_type': 'portaria'  # Tipo de ato: Portaria
            }
            
            print("🔍 Fazendo busca com filtros específicos...")
            response = requests.get(f"{self.base_url}/gazettes", params=params)
            
            if response.status_code == 200:
                dados = response.json()
                
                if 'results' in dados:
                    print(f"📊 Encontrados {len(dados['results'])} resultados")
                    
                    for resultado in dados['results']:
                        # Verificar se é uma portaria de naturalização
                        if self._eh_portaria_naturalizacao_especifica(resultado):
                            portaria_info = {
                                'url': resultado.get('url'),
                                'data_publicacao': resultado.get('date'),
                                'titulo': resultado.get('title', ''),
                                'conteudo': resultado.get('content', ''),
                                'palavra_encontrada': 'PORTARIA (filtro específico)',
                                'organizacao': resultado.get('organization', ''),
                                'sub_organizacao': resultado.get('sub_organization', '')
                            }
                            portarias_encontradas.append(portaria_info)
                            print(f"✅ Encontrada: {resultado.get('title', 'Sem título')}")
                else:
                    print("❌ Nenhum resultado encontrado na API")
            else:
                print(f"❌ Erro na API: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erro na busca específica: {e}")
        
        print(f"📊 Total de portarias de naturalização encontradas: {len(portarias_encontradas)}")
        return portarias_encontradas
    
    def _eh_portaria_naturalizacao_especifica(self, resultado: Dict) -> bool:
        """
        Verifica se é uma portaria de naturalização usando critérios mais específicos
        
        Args:
            resultado: Dicionário com dados do resultado da busca
            
        Returns:
            True se for portaria de naturalização
        """
        titulo = resultado.get('title', '').lower()
        conteudo = resultado.get('content', '').lower()
        
        # Palavras-chave específicas para naturalização
        palavras_naturalizacao = [
            'naturalização',
            'naturalizacao',
            'nacionalidade brasileira',
            'art. 65',
            'art. 67',
            'art. 70',
            'deferimento',
            'naturalizar',
            'naturalizado',
            'naturalizada',
            'cidadania brasileira',
            'brasileiro nato',
            'brasileira nata',
            'processo de naturalização',
            'concessão de nacionalidade',
            'concessao de nacionalidade',
            'estrangeiro',
            'estrangeira',
            'residente',
            'residente no brasil'
        ]
        
        # Verificar se contém palavras relacionadas à naturalização
        for palavra in palavras_naturalizacao:
            if palavra in titulo or palavra in conteudo:
                return True
        
        return False
    
    def buscar_portarias_por_ano(self, ano: int) -> str:
        """
        Busca portarias de naturalização de um ano específico
        
        Args:
            ano: Ano para buscar (ex: 2024)
            
        Returns:
            Caminho do arquivo gerado
        """
        data_inicio = f"{ano}-01-01"
        data_fim = f"{ano}-12-31"
        
        print(f"🔍 Buscando portarias de {ano}")
        
        # Primeiro tentar busca específica
        portarias = self.buscar_portarias_especificas(data_inicio, data_fim)
        
        # Se não encontrar nada, tentar busca geral
        if not portarias:
            print("⚠️ Busca específica não retornou resultados, tentando busca geral...")
            portarias = self.buscar_portarias_periodo(data_inicio, data_fim)
        
        if portarias:
            # Analisar portarias encontradas
            df = self.analisar_portarias_encontradas(portarias)
            
            if not df.empty:
                # Gerar arquivo
                nome_arquivo = f"naturalizacoes_{ano}.xlsx"
                df.to_excel(nome_arquivo, index=False, engine='openpyxl')
                
                print(f"✅ Planilha gerada: {nome_arquivo}")
                print(f"📊 Total de registros: {len(df)}")
                
                return nome_arquivo
            else:
                print("❌ Nenhum dado foi extraído das portarias")
                return None
        else:
            print(f"❌ Nenhuma portaria encontrada em {ano}")
            return None

def main():
    """Função principal para teste"""
    print("🔍 SISTEMA DE BUSCA AUTOMÁTICA DOU")
    print("=" * 50)
    
    buscador = BuscadorAutomaticoDOU()
    
    # Exemplo: buscar portarias de 2024
    data_inicio = "2024-01-01"
    data_fim = "2024-12-31"
    
    arquivo = buscador.gerar_planilha_periodo(data_inicio, data_fim)
    
    if arquivo:
        print(f"\n🎉 Busca concluída! Arquivo: {arquivo}")
    else:
        print("\n❌ Busca não retornou resultados")

if __name__ == "__main__":
    main() 