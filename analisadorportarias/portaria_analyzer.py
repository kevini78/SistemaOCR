import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime, date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
import unicodedata

class PortariaAnalyzer:
    def __init__(self, planilha_historico_path=None):
        """
        Inicializa o analisador de portarias
        
        Args:
            planilha_historico_path (str): Caminho para a planilha com histórico de naturalizações (2018-2025)
        """
        self.planilha_historico_path = planilha_historico_path
        self.historico_df = None
        self.erros_encontrados = []
        self.paises_oficiais = set()
        self.estados_oficiais = [
            'Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo',
            'Goiás', 'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 'Paraíba',
            'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul',
            'Rondônia', 'Roraima', 'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins'
        ]
        self.estados_brasil = [
            'ACRE', 'ALAGOAS', 'AMAPÁ', 'AMAPA', 'AMAZONAS', 'BAHIA', 'CEARÁ', 'CEARA', 'DISTRITO FEDERAL',
            'ESPÍRITO SANTO', 'ESPIRITO SANTO', 'GOIÁS', 'GOIAS', 'MARANHÃO', 'MARANHAO', 'MATO GROSSO',
            'MATO GROSSO DO SUL', 'MINAS GERAIS', 'PARÁ', 'PARA', 'PARAÍBA', 'PARAIBA', 'PARANÁ', 'PARANA',
            'PERNAMBUCO', 'PIAUÍ', 'PIAUI', 'RIO DE JANEIRO', 'RIO GRANDE DO NORTE', 'RIO GRANDE DO SUL',
            'RONDÔNIA', 'RONDONIA', 'RORAIMA', 'SANTA CATARINA', 'SÃO PAULO', 'SAO PAULO', 'SERGIPE', 'TOCANTINS'
        ]
        self.carregar_paises_oficiais()
        if planilha_historico_path:
            self.carregar_historico(planilha_historico_path)
    
    def carregar_paises_oficiais(self):
        """Carrega lista de países oficiais"""
        self.paises_oficiais = {
            'AFEGANISTÃO', 'ÁFRICA DO SUL', 'ALBÂNIA', 'ALEMANHA', 'ANDORRA', 'ANGOLA', 
            'ANTÍGUA E BARBUDA', 'ARÁBIA SAUDITA', 'ARGÉLIA', 'ARGENTINA', 'ARMÊNIA', 
            'AUSTRÁLIA', 'ÁUSTRIA', 'AZERBAIJÃO', 'BAHAMAS', 'BAHREIN', 'BANGLADESH', 
            'BARBADOS', 'BELARUS', 'BÉLGICA', 'BELIZE', 'BENIN', 'BOLÍVIA', 'BÓSNIA E HERZEGOVINA', 
            'BOTSUANA', 'BRASIL', 'BRUNEI', 'BULGÁRIA', 'BURKINA FASO', 'BURUNDI', 'BUTÃO', 
            'CABO VERDE', 'CAMARÕES', 'CAMBOJA', 'CANADÁ', 'CATAR', 'CAZAQUISTÃO', 'CHADE', 
            'CHILE', 'CHINA', 'CHIPRE', 'COLÔMBIA', 'COMORES', 'CONGO', 'COREIA DO NORTE', 
            'COREIA DO SUL', 'COSTA DO MARFIM', 'COSTA RICA', 'CROÁCIA', 'CUBA', 'DINAMARCA', 
            'DJIBUTI', 'DOMINICA', 'EGITO', 'EL SALVADOR', 'EMIRADOS ÁRABES UNIDOS', 'EQUADOR', 
            'ERITREIA', 'ESLOVÁQUIA', 'ESLOVÊNIA', 'ESPANHA', 'ESTADOS UNIDOS', 'ESTÔNIA', 
            'ESWATINI', 'ETIÓPIA', 'FIJI', 'FILIPINAS', 'FINLÂNDIA', 'FRANÇA', 'FRANÇA METROPOLITANA', 'GABÃO', 
            'GÂMBIA', 'GANA', 'GEÓRGIA', 'GRANADA', 'GRÉCIA', 'GUATEMALA', 'GUIANA', 
            'GUINÉ', 'GUINÉ-BISSAU', 'GUINÉ EQUATORIAL', 'HAITI', 'HONDURAS', 'HUNGRIA', 
            'IÊMEN', 'ILHAS MARSHALL', 'ILHAS SALOMÃO', 'ÍNDIA', 'INDONÉSIA', 'IRÃ', 
            'IRAQUE', 'IRLANDA', 'ISLÂNDIA', 'ISRAEL', 'ITÁLIA', 'JAMAICA', 'JAPÃO', 
            'JORDÂNIA', 'KOSOVO', 'KUWAIT', 'LAOS', 'LESOTO', 'LETÔNIA', 'LÍBANO', 'LIBANO', 
            'LIBÉRIA', 'LÍBIA', 'LIECHTENSTEIN', 'LITUÂNIA', 'LUXEMBURGO', 'MACEDÔNIA DO NORTE', 
            'MADAGASCAR', 'MALÁSIA', 'MALAWI', 'MALDIVAS', 'MALI', 'MALTA', 'MARROCOS', 
            'MAURÍCIO', 'MAURITÂNIA', 'MÉXICO', 'MIANMAR', 'MICRONÉSIA', 'MOÇAMBIQUE', 
            'MOLDÁVIA', 'MÔNACO', 'MONGÓLIA', 'MONTENEGRO', 'NAMÍBIA', 'NAURU', 'NEPAL', 
            'NICARÁGUA', 'NÍGER', 'NIGÉRIA', 'NIGERIA', 'NORUEGA', 'NOVA ZELÂNDIA', 'OMÃ', 'PAÍSES BAIXOS', 
            'PALAU', 'PALESTINA', 'PANAMÁ', 'PAPUA-NOVA GUINÉ', 'PAQUISTÃO', 'PARAGUAI', 'PERU', 'POLÔNIA', 
            'PORTUGAL', 'QUÊNIA', 'QUIRGUIZISTÃO', 'REINO UNIDO', 'REPÚBLICA CENTRO-AFRICANA', 
            'REPÚBLICA DEMOCRÁTICA DO CONGO', 'REPÚBLICA DOMINICANA', 'REPÚBLICA TCHECA', 
            'ROMÊNIA', 'RUANDA', 'RÚSSIA', 'FEDERAÇÃO DA RÚSSIA', 'SAMOA', 'SAN MARINO', 'SANTA LÚCIA', 
            'SÃO CRISTÓVÃO E NEVIS', 'SÃO TOMÉ E PRÍNCIPE', 'SÃO VICENTE E GRANADINAS', 
            'SEICHELES', 'SENEGAL', 'SERRA LEOA', 'SÉRVIA', 'SINGAPURA', 'SÍRIA', 'SIRIA', 
            'SOMÁLIA', 'SRI LANKA', 'SUAZILÂNDIA', 'SUDÃO', 'SUDÃO DO SUL', 'SUÉCIA', 
            'SUÍÇA', 'SURINAME', 'TAILÂNDIA', 'TAIWAN', 'TAJIQUISTÃO', 'TANZÂNIA', 
            'TIMOR-LESTE', 'TOGO', 'TONGA', 'TRINIDAD E TOBAGO', 'TUNÍSIA', 'TURCOMENISTÃO', 
            'TURQUIA', 'TUVALU', 'UCRÂNIA', 'UGANDA', 'URUGUAI', 'UZBEQUISTÃO', 'VANUATU', 
            'VATICANO', 'VENEZUELA', 'VIETNÃ', 'ZÂMBIA', 'ZIMBÁBUE'
        }
    
    def carregar_historico(self, planilha_historico_path):
        """Carrega a planilha com histórico de naturalizações"""
        try:
            self.historico_df = pd.read_excel(planilha_historico_path)
            print(f"Histórico carregado: {len(self.historico_df)} registros")
        except Exception as e:
            print(f"Erro ao carregar histórico: {e}")
            self.historico_df = None
    
    def buscar_portaria_web(self, url_portaria):
        """
        Busca o conteúdo da portaria na web usando Selenium
        
        Args:
            url_portaria (str): URL da portaria
            
        Returns:
            str: Conteúdo HTML da portaria
        """
        print("Iniciando busca da portaria...")
        driver = None
        
        try:
            # Configurar Chrome
            print("Configurando Chrome WebDriver...")
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            # Tentar diferentes formas de inicializar o driver
            try:
                print("Tentando inicializar Chrome WebDriver...")
                driver = webdriver.Chrome(options=chrome_options)
                print("✅ Chrome WebDriver inicializado com sucesso!")
            except Exception as e1:
                print(f"❌ Erro ao inicializar Chrome: {e1}")
                
                # Tentar com service
                try:
                    print("Tentando com Service...")
                    service = Service()
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    print("✅ Chrome WebDriver inicializado com Service!")
                except Exception as e2:
                    print(f"❌ Erro com Service: {e2}")
                    
                    # Fallback para requests
                    print("Usando fallback com requests...")
                    return self.buscar_portaria_requests(url_portaria)
            
            # Acessar URL
            print(f"Acessando URL: {url_portaria}")
            driver.set_page_load_timeout(30)
            driver.get(url_portaria)
            
            print("Aguardando carregamento da página...")
            time.sleep(5)
            
            # Obter conteúdo
            print("Extraindo conteúdo...")
            content = driver.page_source
            
            print(f"✅ Conteúdo extraído! Tamanho: {len(content)} caracteres")
            
            return content
            
        except Exception as e:
            print(f"❌ Erro ao buscar portaria: {e}")
            print("Tentando método alternativo com requests...")
            return self.buscar_portaria_requests(url_portaria)
            
        finally:
            if driver:
                try:
                    driver.quit()
                    print("Chrome WebDriver fechado.")
                except:
                    pass
    
    def buscar_portaria_requests(self, url_portaria):
        """
        Método alternativo usando requests (fallback)
        """
        try:
            print("Usando método requests...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url_portaria, headers=headers, timeout=30)
            response.raise_for_status()
            
            print(f"✅ Conteúdo obtido via requests! Tamanho: {len(response.text)} caracteres")
            return response.text
            
        except Exception as e:
            print(f"❌ Erro com requests: {e}")
            return None
    
    def extrair_dados_portaria(self, html_content):
        """
        Extrai dados estruturados da portaria
        Args:
            html_content (str): Conteúdo HTML da portaria
        Returns:
            dict: Dados estruturados da portaria
        """
        print("Extraindo dados da portaria...")
        if not html_content:
            print("❌ Conteúdo HTML vazio")
            return None
        soup = BeautifulSoup(html_content, 'html.parser')
        # Encontrar o <p> do cabeçalho da portaria
        paragrafos = soup.find_all('p')
        idx_inicio = -1
        idx_fim = -1
        for i, p in enumerate(paragrafos):
            texto_p = p.get_text().strip()
            if re.search(r'PORTARIA\s*[NnNº°]?', texto_p):
                idx_inicio = i
                break
        if idx_inicio == -1:
            print("❌ Não encontrou o cabeçalho da portaria em <p>")
            texto_completo = soup.get_text()
        else:
            # Procurar o rodapé (primeiro <p> depois do início que começa com 'A pessoa referida' ou 'As pessoas referidas')
            for j in range(idx_inicio+1, len(paragrafos)):
                texto_p = paragrafos[j].get_text().strip()
                if texto_p.startswith('A pessoa referida') or texto_p.startswith('As pessoas referidas'):
                    idx_fim = j
                    break
            if idx_fim == -1:
                # Se não achou rodapé, pega até o fim
                blocos_pessoas = [p.get_text().strip() for p in paragrafos[idx_inicio:]]
            else:
                blocos_pessoas = [p.get_text().strip() for p in paragrafos[idx_inicio:idx_fim]]
            texto_completo = '\n'.join(blocos_pessoas)
        print(f"Texto extraído: {len(texto_completo)} caracteres")
        print(f"Início do texto: {texto_completo[:500]}...")
        # Extrair número e data da portaria
        match_portaria = re.search(r'PORTARIA\s*,?\s*[NnNº°]?\s*(\d+[\.,]?\d*)\s*,?\s*DE\s*(\d{1,2}\s+DE\s+\w+\s+DE\s+\d{4})', texto_completo, re.IGNORECASE)
        if not match_portaria:
            print("❌ Não foi possível extrair número/data da portaria")
            print("Tentando padrões alternativos...")
            patterns = [
                r'PORTARIA\s*N[º°]?\s*(\d+[\.,]?\d*)[,,\s]*DE\s*(\d{1,2}\s+DE\s+\w+\s+DE\s+\d{4})',
                r'PORTARIA\s*(\d+[\.,]?\d*)[,,\s]*DE\s*(\d{1,2}\s+DE\s+\w+\s+DE\s+\d{4})',
                r'Portaria\s*n[º°]?\s*(\d+[\.,]?\d*)[,,\s]*de\s*(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})'
            ]
            for pattern in patterns:
                match = re.search(pattern, texto_completo, re.IGNORECASE)
                if match:
                    match_portaria = match
                    break
            if not match_portaria:
                print("❌ Nenhum padrão de portaria encontrado")
                return None
        numero_portaria = match_portaria.group(1)
        data_portaria = match_portaria.group(2)
        print(f"✅ Portaria encontrada: {numero_portaria} de {data_portaria}")
        tipo_naturalizacao = self.identificar_tipo_naturalizacao(texto_completo)
        print(f"✅ Tipo identificado: {tipo_naturalizacao}")
        pessoas = self.extrair_pessoas(texto_completo)
        print(f"✅ Pessoas extraídas: {len(pessoas)}")
        return {
            'numero': numero_portaria,
            'data': data_portaria,
            'tipo': tipo_naturalizacao,
            'pessoas': pessoas,
            'texto_completo': texto_completo
        }
    
    def identificar_tipo_naturalizacao(self, texto):
        """Identifica o tipo de naturalização baseado no artigo e texto da portaria"""
        # Normalizar texto: remover acentos e converter para minúsculas
        import unicodedata
        
        # Normalizar caracteres especiais (ç -> c, ã -> a, etc.)
        texto_normalizado = unicodedata.normalize('NFD', texto)
        texto_normalizado = ''.join(c for c in texto_normalizado if not unicodedata.combining(c))
        texto_lower = texto_normalizado.lower()
        
        # 1. Provisória tem prioridade máxima - verificar várias variações
        if any(termo in texto_lower for termo in ['naturalizacao provisoria', 'naturalização provisória', 'naturalizacao provisória', 'naturalização provisoria']):
            return 'PROVISORIA'
        
        # 2. Definitiva só se não houver provisória
        if ('tornar definitiva' in texto_lower and 'art. 70' in texto_lower) or \
           ('tornar definitiva' in texto_lower and 'paragrafo unico' in texto_lower):
            return 'DEFINITIVA'
        
        # 3. Provisória (art. 70) - verificar se tem art. 70 E provisória
        if 'art. 70' in texto_lower and any(termo in texto_lower for termo in ['provisoria', 'provisória']):
            return 'PROVISORIA'
        
        # 4. Ordinária (art. 65) tem prioridade sobre extraordinária
        if 'art. 65' in texto_lower:
            print(f"[DEBUG] Encontrou 'art. 65' no texto")
            return 'ORDINARIA'
        
        # 5. Extraordinária (art. 67) só se não houver art. 65 ou art. 70
        if 'art. 67' in texto_lower and 'art. 65' not in texto_lower and 'art. 70' not in texto_lower:
            print(f"[DEBUG] Encontrou 'art. 67' no texto")
            return 'EXTRAORDINARIA'
        
        # 6. Fallbacks por contexto
        if 'tornar definitiva' in texto_lower:
            print(f"[DEBUG] Fallback: encontrou 'tornar definitiva' no texto")
            return 'DEFINITIVA'
        if 'extraordinaria' in texto_lower or 'extraordinária' in texto_lower:
            print(f"[DEBUG] Fallback: encontrou 'extraordinária' no texto")
            return 'EXTRAORDINARIA'
        if 'ordinaria' in texto_lower or 'ordinária' in texto_lower or 'por naturalizacao' in texto_lower:
            print(f"[DEBUG] Fallback: encontrou 'ordinária' ou 'por naturalização' no texto")
            return 'ORDINARIA'
        
        print(f"[DEBUG] Nenhum tipo identificado, retornando DESCONHECIDO")
        return 'DESCONHECIDO'
    
    def extrair_pessoas(self, texto, forcar_linha_por_bloco=False):
        """Extrai dados das pessoas da portaria, suportando múltiplos formatos"""
        print("Extraindo dados das pessoas (robusto)...")
        pessoas = []
        ignorados = []
        palavras_ignorar = {
            'PORTARIA', 'Nº', 'RESOLVE', 'CONCEDER', 'TORNAR', 'NACIONALIDADE', 
            'BRASILEIRA', 'NATURALIZAÇÃO', 'PESSOAS', 'RELACIONADAS', 'TERMOS', 'ART',
            'CONSTITUIÇÃO', 'FEDERAL', 'CONFORMIDADE', 'LEI', 'REGULAMENTADA', 'DECRETO',
            'COMPARECER', 'JUSTIÇA', 'ELEITORAL', 'CADASTRAMENTO',
            'COORDENADOR', 'COORDENADORA', 'DIRETOR', 'DIRETORA', 'PRESIDENTE', 'MINISTRO', 'MINISTRA',
            'SECRETÁRIO', 'SECRETÁRIA', 'DELEGADO', 'DELEGADA', 'CHEFE', 'SUPERINTENDENTE',
            'PROCURADOR', 'PROCURADORA', 'ADVOGADO', 'ADVOGADA', 'JUIZ', 'JUIZA',
            'DESEMBARGADOR', 'DESEMBARGADORA', 'PROCESSOS MIGRATÓRIOS', 'POLÍCIA FEDERAL',
            'MINISTÉRIO DA JUSTIÇA', 'DEPARTAMENTO', 'DIVISÃO', 'SEÇÃO', 'COORDENAÇÃO', 'GERÊNCIA'
        }
        expressoes_cargo = [
            'COORDENADOR', 'COORDENADORA', 'DIRETOR', 'DIRETORA', 'PRESIDENTE', 'MINISTRO', 'MINISTRA',
            'SECRETÁRIO', 'SECRETÁRIA', 'DELEGADO', 'DELEGADA', 'CHEFE', 'SUPERINTENDENTE',
            'PROCURADOR', 'PROCURADORA', 'ADVOGADO', 'ADVOGADA', 'JUIZ', 'JUIZA',
            'DESEMBARGADOR', 'DESEMBARGADORA', 'PROCESSOS MIGRATÓRIOS', 'POLÍCIA FEDERAL',
            'MINISTÉRIO DA JUSTIÇA', 'DEPARTAMENTO', 'DIVISÃO', 'SEÇÃO', 'COORDENAÇÃO', 'GERÊNCIA'
        ]
        palavras_lixo_site = [
            'ir para o conteúdo', 'acesso rápido', 'órgãos do governo', 'acesso à informação',
            'legislação', 'acessibilidade', 'mudar para o modo de alto contraste', 'acesso gov.br',
            'imprensa nacional', 'diário oficial da união', 'publicador de conteúdos', 'voltar',
            'compartilhe', 'facebook', 'twitter', 'linkedin', 'whatsapp', 'instagram', 'imagem não disponível',
            'versão certificada', 'diário completo', 'impressão', 'brasão do brasil', 'publicado em:',
            'edição:', 'seção:', 'página:', 'órgão:', 'caminho de navegação', 'serviços', 'leitura do jornal',
            'destaques do diário oficial', 'base de dados de publicações', 'verificação de autenticidade',
            'acesso ao sistema de envio', 'concursos e seleções', 'tutorial', 'termo de uso', 'política de privacidade',
            'portal da imprensa nacional', 'mega-menu'
        ]
        # Se forçar linha por bloco, cada linha é um bloco
        if forcar_linha_por_bloco:
            blocos = [b.strip() for b in texto.split('\n') if len(b.strip()) > 5]
        else:
            texto = re.sub(r'\)\s*e\s*([A-ZÁÉÍÓÚÃÕÂÊÎÔÛÇ])', r');\1', texto)
            texto = re.sub(r'\)\s*e\s*$', r');', texto, flags=re.MULTILINE)
            blocos = re.split(r';|\n\n', texto)
            blocos = [b.strip() for b in blocos if len(b.strip()) > 5]
        for bloco in blocos:
            bloco_lower = bloco.lower()
            if any(palavra in bloco_lower for palavra in palavras_lixo_site):
                ignorados.append({'motivo': 'bloco_lixo_site', 'bloco': bloco})
                continue
            m_doc = re.search(r'([A-Za-z]+\d+[-][A-Za-z0-9]+|Processo\s+[\d\./]+)', bloco)
            m_pais = re.search(r'natural\s+d[aeo]\s+([A-Za-zÀ-ú\s\-]+)', bloco, re.IGNORECASE)
            if not m_doc:
                ignorados.append({'motivo': 'sem_documento', 'bloco': bloco})
                continue
            if not m_pais:
                ignorados.append({'motivo': 'sem_pais', 'bloco': bloco})
                continue
            documento = m_doc.group(1).strip()
            pais_original = m_pais.group(1).strip()
            pais = self.normalizar_pais(pais_original)
            nome = ''
            nome_match = re.match(r'^\s*(.+?)[\s\-–—,:]+\s*' + re.escape(documento), bloco, re.IGNORECASE)
            if nome_match:
                nome = nome_match.group(1).strip()
            else:
                nome_match = re.search(r'(.+?)[\s\-–—,:]+\s*' + re.escape(documento), bloco, re.IGNORECASE)
                if nome_match:
                    nome = nome_match.group(1).strip()
                else:
                    nome_match = re.search(r'(.+?)\s*natural\s+d[aeo]', bloco, re.IGNORECASE)
                    if nome_match:
                        nome = nome_match.group(1).strip()
            if not nome:
                ignorados.append({'motivo': 'sem_nome', 'bloco': bloco})
                continue
            nome = re.sub(r'^\s*(.+?)\s*[-–—,:e\.]?\s*$', r'\1', nome.strip())
            nome_upper = nome.upper().strip()
            nome_palavras = nome_upper.split()
            # Verificações mais flexíveis
            if (
                nome_upper in palavras_ignorar
                or (len(nome_palavras) < 2 and any(exp in nome_upper for exp in expressoes_cargo))
                or nome_upper.startswith('PORTARIA N')
            ):
                ignorados.append({'motivo': 'palavra_ignorar', 'nome': nome, 'bloco': bloco})
                continue
            m_data = re.search(r'nascid[oa\(a\)]*\s*em\s*(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})', bloco, re.IGNORECASE)
            if not m_data:
                m_data = re.search(r'nascid[oa]?\s+em\s+(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})', bloco, re.IGNORECASE)
            data_nascimento = m_data.group(1).strip() if m_data else ''
            m_pai = re.search(r'filh[oa\(a\)]*\s+de\s+([A-ZÀ-Úa-zà-ú\s\'\-]+?)(?:\s+e\s+filh[oa\(a\)]*\s+de\s+[A-ZÀ-Úa-zà-ú\s\'\-]+)?', bloco, re.IGNORECASE)
            nome_pai = m_pai.group(1).strip() if m_pai else ''
            
            # Extrair documento (RNM, etc.)
            m_doc = re.search(r'([A-Za-z]\d{6,}-[A-Za-z0-9])', bloco)
            documento = m_doc.group(1).strip() if m_doc else ''
            tipo_documento = 'RNM' if documento else ''
            
            # Extrair processo
            m_processo = re.search(r'Processo\s*(n[ºo]\s*)?(\d{6,}\.[\d/]+)', bloco, re.IGNORECASE)
            processo = m_processo.group(2).strip() if m_processo else ''
            
            idade = self.calcular_idade(data_nascimento) if data_nascimento else None
            
            # Extrair estado brasileiro (mais flexível)
            m_estado = re.search(r'residente no estado [dodaas]{0,3}\s*([A-Za-zÀ-ú\s]+)', bloco, re.IGNORECASE)
            if not m_estado:
                m_estado = re.search(r'residente no Estado [dodaas]{0,3}\s*([A-Za-zÀ-ú\s]+)', bloco, re.IGNORECASE)
            estado = m_estado.group(1).strip() if m_estado else ''
            
            # Limpar "e " ou "E " do início, se houver
            estado = re.sub(r'^e\s+', '', estado, flags=re.IGNORECASE)
            
            pessoa = {
                'nome': nome,
                'documento': documento,
                'tipo_documento': tipo_documento,
                'processo': processo,
                'pais': pais,
                'data_nascimento': data_nascimento,
                'nome_pai': nome_pai,
                'idade': idade,
                'estado': estado
            }
            pessoas.append(pessoa)
            print(f"  - {nome} ({pais}) | Processo: {processo} | Estado: {estado}")
        print(f"Total de pessoas extraídas: {len(pessoas)}")
        if ignorados:
            print(f"⚠️ Blocos ignorados: {len(ignorados)}")
            for ign in ignorados[:5]:
                print(f"  Ignorado: {ign['motivo']} | {ign.get('nome','')} | {ign['bloco'][:80]}...")
        return pessoas
    
    def calcular_idade(self, data_nascimento_str):
        """Calcula idade baseada na data de nascimento em formato brasileiro"""
        try:
            # Converter data brasileira para datetime
            meses = {
                'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
                'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
                'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
            }
            
            partes = data_nascimento_str.lower().replace(' de ', ' ').split()
            dia = int(partes[0])
            mes = meses.get(partes[1], 1)
            ano = int(partes[2])
            
            data_nascimento = date(ano, mes, dia)
            hoje = date.today()
            
            idade = hoje.year - data_nascimento.year
            if hoje.month < data_nascimento.month or (hoje.month == data_nascimento.month and hoje.day < data_nascimento.day):
                idade -= 1
                
            return idade
        except:
            return None
    
    def verificar_erros(self, dados_portaria):
        """Verifica erros na portaria baseado nas regras"""
        erros = []
        
        if not dados_portaria:
            return [{'tipo': 'ERRO_PARSING', 'descrição': 'Não foi possível extrair dados da portaria'}]
        
        tipo = dados_portaria['tipo']
        pessoas = dados_portaria['pessoas']
        
        print(f"Verificando {len(pessoas)} pessoas para portaria tipo: {tipo}")
        
        # Verificar duplicatas na mesma portaria
        nomes_vistos = {}
        for pessoa in pessoas:
            nome_data = f"{pessoa['nome']}|{pessoa['data_nascimento']}"
            if nome_data in nomes_vistos:
                erros.append({
                    'tipo': 'DUPLICATA_MESMA_PORTARIA',
                    'pessoa': pessoa['nome'],
                    'descrição': f'{pessoa["nome"]} aparece mais de uma vez na mesma portaria'
                })
            nomes_vistos[nome_data] = True
        
        # Verificar cada pessoa
        for pessoa in pessoas:
            print(f"Verificando pessoa: {pessoa['nome']} (idade: {pessoa['idade']})")
            
            # Verificar idade conforme tipo de naturalização
            if tipo == 'ORDINARIA' and pessoa['idade'] and pessoa['idade'] < 18:
                erros.append({
                    'tipo': 'IDADE_INCORRETA_ORDINARIA',
                    'pessoa': pessoa['nome'],
                    'idade': pessoa['idade'],
                    'descrição': f'Naturalização ordinária (art. 65) com pessoa menor de 18 anos: {pessoa["nome"]} ({pessoa["idade"]} anos)'
                })
            
            elif tipo == 'EXTRAORDINARIA' and pessoa['idade'] and pessoa['idade'] < 15:
                erros.append({
                    'tipo': 'IDADE_INCORRETA_EXTRAORDINARIA',
                    'pessoa': pessoa['nome'],
                    'idade': pessoa['idade'],
                    'descrição': f'Naturalização extraordinária (art. 67) com pessoa menor de 15 anos: {pessoa["nome"]} ({pessoa["idade"]} anos)'
                })
            
            elif tipo == 'PROVISORIA' and pessoa['idade'] and pessoa['idade'] >= 18:
                erros.append({
                    'tipo': 'IDADE_INCORRETA_PROVISORIA',
                    'pessoa': pessoa['nome'],
                    'idade': pessoa['idade'],
                    'descrição': f'Naturalização provisória (art. 70) com pessoa maior ou igual a 18 anos: {pessoa["nome"]} ({pessoa["idade"]} anos)'
                })
            
            elif tipo == 'DEFINITIVA' and pessoa['idade'] and (pessoa['idade'] < 18 or pessoa['idade'] > 20):
                erros.append({
                    'tipo': 'IDADE_INCORRETA_DEFINITIVA',
                    'pessoa': pessoa['nome'],
                    'idade': pessoa['idade'],
                    'descrição': f'Naturalização definitiva com idade fora do intervalo 18-20 anos: {pessoa["nome"]} ({pessoa["idade"]} anos)'
                })
            
            # Verificar documento (Processo ou RNM)
            if pessoa['tipo_documento'] not in ['PROCESSO', 'RNM']:
                erros.append({
                    'tipo': 'DOCUMENTO_INVALIDO',
                    'pessoa': pessoa['nome'],
                    'descrição': f'Documento inválido para {pessoa["nome"]}: {pessoa["documento"]}'
                })
            
            # Verificar país
            pais_normalizado = self.normalizar_pais(pessoa['pais'])
            if pais_normalizado not in self.paises_oficiais:
                erros.append({
                    'tipo': 'PAIS_INVALIDO',
                    'pessoa': pessoa['nome'],
                    'pais': pessoa['pais'],
                    'descrição': f'País não reconhecido: {pessoa["pais"]} para {pessoa["nome"]}'
                })
            
            # Verificar estado brasileiro
            estado_normalizado = unicodedata.normalize('NFKD', pessoa.get('estado', '')).encode('ASCII', 'ignore').decode('ASCII').upper().strip()
            if pessoa.get('estado') and estado_normalizado not in self.estados_brasil:
                erros.append({
                    'tipo': 'ESTADO_INVALIDO',
                    'pessoa': pessoa['nome'],
                    'estado': pessoa['estado'],
                    'descrição': f'Estado brasileiro não reconhecido: {pessoa["estado"]} para {pessoa["nome"]}'
                })
            
            # Verificar histórico de naturalizações anteriores
            if self.historico_df is not None:
                print(f"\n🔍 Verificando histórico para {pessoa['nome']}...")
                resultado_historico = self.verificar_duplicata_historico(pessoa)
                print(f"   Resultado: {resultado_historico}")
                
                if resultado_historico == "HISTORICO_NAO_CARREGADO":
                    erros.append({
                        'tipo': 'HISTORICO_NAO_DISPONIVEL',
                        'pessoa': pessoa['nome'],
                        'descrição': f'Histórico de naturalizações não disponível para verificar {pessoa["nome"]}'
                    })
                elif resultado_historico == "COLUNAS_INEXISTENTES":
                    erros.append({
                        'tipo': 'HISTORICO_ESTRUTURA_INVALIDA',
                        'pessoa': pessoa['nome'],
                        'descrição': f'Estrutura da planilha de histórico inválida para verificar {pessoa["nome"]}'
                    })
                elif resultado_historico != "NAO_PUBLICADO_ANTERIORMENTE":
                    erros.append({
                        'tipo': 'JA_NATURALIZADO_ANTERIORMENTE',
                        'pessoa': pessoa['nome'],
                        'descrição': f'{pessoa["nome"]} já foi naturalizado anteriormente em {resultado_historico}'
                    })
                else:
                    print(f"   ✅ {pessoa['nome']} não encontrado no histórico")
                # Se não foi publicado anteriormente, não adiciona nada
            else:
                print(f"⚠️  Histórico não disponível para verificar {pessoa['nome']}")
        
        # NOVAS REGRAS DE ALERTA - APENAS PARA EXIBIÇÃO DE ERROS
        print("\n🔍 Verificando regras adicionais de validação...")
        for pessoa in pessoas:
            # 1. Alerta se processo ausente
            if not pessoa.get('processo'):
                erros.append({
                    'tipo': 'ALERTA_PROCESSO_AUSENTE',
                    'pessoa': pessoa['nome'],
                    'descrição': 'Processo ausente para esta pessoa'
                })
            
            # 2. Alerta se estado ausente
            if not pessoa.get('estado'):
                erros.append({
                    'tipo': 'ALERTA_ESTADO_AUSENTE',
                    'pessoa': pessoa['nome'],
                    'descrição': 'Estado ausente para esta pessoa'
                })
            
            # 3. Alerta se RNM sem dígito verificador
            if pessoa['tipo_documento'] == 'RNM':
                if not re.match(r'^[A-Z]\d{6,}-[A-Z0-9]$', pessoa['documento']):
                    erros.append({
                        'tipo': 'ALERTA_RNM_SEM_DIGITO_VERIFICADOR',
                        'pessoa': pessoa['nome'],
                        'descrição': f'RNM sem dígito verificador: {pessoa["documento"]}'
                    })
            
            # 4. Alerta se falta RNM nos tipos ordinária e extraordinária
            if tipo in ['ORDINARIA', 'EXTRAORDINARIA'] and pessoa['tipo_documento'] != 'RNM':
                erros.append({
                    'tipo': 'ALERTA_FALTA_RNM_ORDINARIA_EXTRAORDINARIA',
                    'pessoa': pessoa['nome'],
                    'descrição': f'Pessoa do tipo {tipo} sem RNM: {pessoa["documento"]}'
                })
            
            # 5. Alerta se falta país de nascimento
            if not pessoa['pais'] or not pessoa['pais'].strip():
                erros.append({
                    'tipo': 'ALERTA_FALTA_PAIS_NASCIMENTO',
                    'pessoa': pessoa['nome'],
                    'descrição': 'País de nascimento ausente'
                })
            
            # 6. Alerta se falta data de nascimento
            if not pessoa['data_nascimento'] or not pessoa['data_nascimento'].strip():
                erros.append({
                    'tipo': 'ALERTA_FALTA_DATA_NASCIMENTO',
                    'pessoa': pessoa['nome'],
                    'descrição': 'Data de nascimento ausente'
                })
        
        return erros
    
    def verificar_duplicata_historico(self, pessoa):
        """Verifica se a pessoa já foi naturalizada anteriormente - VERIFICAÇÃO RIGOROSA"""
        if self.historico_df is None:
            print(f"❌ Histórico não carregado para verificar {pessoa['nome']}")
            return "HISTORICO_NAO_CARREGADO"
        
        print(f"🔍 Verificando histórico para: {pessoa['nome']} (Data: {pessoa['data_nascimento']})")
        
        # Verificar se as colunas existem
        colunas_necessarias = ['NOME COMPLETO', 'DATA DE NASCIMENTO']
        colunas_faltando = [col for col in colunas_necessarias if col not in self.historico_df.columns]
        
        if colunas_faltando:
            print(f"❌ Colunas faltando no histórico: {colunas_faltando}")
            print(f"Colunas disponíveis: {list(self.historico_df.columns)}")
            return "COLUNAS_INEXISTENTES"
        
        # Limpar e normalizar o nome para busca
        nome_busca = pessoa['nome'].upper().strip()
        data_busca = pessoa['data_nascimento']
        
        print(f"   Nome para busca: '{nome_busca}'")
        print(f"   Data para busca: '{data_busca}'")
        
        # Se não tem data de nascimento, NÃO verificar duplicata
        if not data_busca:
            print(f"   ⚠️  Sem data de nascimento, não é possível verificar duplicata com segurança")
            return "NAO_PUBLICADO_ANTERIORMENTE"
        
        # Normalizar formato da data para comparação
        data_normalizada = self.normalizar_data(data_busca)
        print(f"   Data normalizada: '{data_normalizada}'")
        
        # BUSCA RIGOROSA: apenas nome EXATO E data EXATA
        mask_exato = (
            (self.historico_df['NOME COMPLETO'].str.upper() == nome_busca) &
            (self.historico_df['DATA DE NASCIMENTO'].astype(str).apply(self.normalizar_data_planilha) == data_normalizada)
        )
        resultados_exatos = self.historico_df[mask_exato]
        
        print(f"   Encontrados {len(resultados_exatos)} registros com nome E data EXATOS")
        
        if len(resultados_exatos) > 0:
            primeira_duplicata = resultados_exatos.iloc[0]
            portaria = primeira_duplicata.get('Nº da Portaria', 'N/A')
            mes = primeira_duplicata.get('Mês', 'N/A')
            ano = primeira_duplicata.get('Ano', 'N/A')
            
            resultado = f"Portaria {portaria} ({mes}/{ano})"
            print(f"   ✅ DUPLICATA CONFIRMADA: {resultado}")
            return resultado
        
        # Se não encontrou, verificar se há nome exato mas data diferente (para debug)
        mask_nome_exato = self.historico_df['NOME COMPLETO'].str.upper() == nome_busca
        resultados_nome_exato = self.historico_df[mask_nome_exato]
        
        if len(resultados_nome_exato) > 0:
            primeira_duplicata = resultados_nome_exato.iloc[0]
            data_historico = primeira_duplicata.get('DATA DE NASCIMENTO', 'N/A')
            print(f"   ⚠️  Nome encontrado mas data diferente: '{data_historico}' vs '{data_normalizada}'")
        
        print(f"   ✅ Nenhuma duplicata encontrada")
        return "NAO_PUBLICADO_ANTERIORMENTE"
    
    def normalizar_data(self, data_str):
        """Normaliza o formato da data para comparação"""
        if not data_str:
            return ""
        
        # Converter para string e limpar
        data_str = str(data_str).strip()
        
        # Se já está no formato correto, retornar
        if re.match(r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}', data_str, re.IGNORECASE):
            return data_str
        
        # Tentar converter outros formatos
        try:
            # Converter data brasileira para datetime e de volta para formato padrão
            meses = {
                'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
                'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
                'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
            }
            
            # Verificar se é formato DD/MM/YYYY ou DD/M/YYYY
            if re.match(r'\d{1,2}/\d{1,2}/\d{4}', data_str):
                partes = data_str.split('/')
                dia = int(partes[0])
                mes = int(partes[1])
                ano = int(partes[2])
                
                # Retornar no formato padrão
                meses_nomes = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
                              'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
                mes_nome = meses_nomes[mes - 1]
                
                return f"{dia} de {mes_nome} de {ano}"
            
            # Verificar se é formato DD de MES de YYYY
            partes = data_str.lower().replace(' de ', ' ').split()
            if len(partes) >= 3:
                dia = int(partes[0])
                mes = meses.get(partes[1], 1)
                ano = int(partes[2])
                
                # Retornar no formato padrão
                meses_nomes = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
                              'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
                mes_nome = meses_nomes[mes - 1]
                
                return f"{dia} de {mes_nome} de {ano}"
        except:
            pass
        
        return data_str
    
    def normalizar_data_planilha(self, data_str):
        """Normaliza o formato da data da planilha para comparação"""
        if not data_str:
            return ""
        
        # Converter para string e limpar
        data_str = str(data_str).strip()
        
        # Se já está no formato correto, retornar
        if re.match(r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}', data_str, re.IGNORECASE):
            return data_str
        
        # Verificar se é formato DD/MM/YYYY ou DD/M/YYYY
        if re.match(r'\d{1,2}/\d{1,2}/\d{4}', data_str):
            partes = data_str.split('/')
            dia = int(partes[0])
            mes = int(partes[1])
            ano = int(partes[2])
            
            # Retornar no formato padrão
            meses_nomes = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
                          'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
            mes_nome = meses_nomes[mes - 1]
            
            return f"{dia} de {mes_nome} de {ano}"
        
        # Verificar se é datetime
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
        
        return data_str
    
    def nomes_similares(self, nome1, nome2):
        """Verifica se dois nomes são similares"""
        nome1_clean = re.sub(r'\s+', ' ', nome1.upper().strip())
        nome2_clean = re.sub(r'\s+', ' ', nome2.upper().strip())
        
        # Verificar se são iguais
        if nome1_clean == nome2_clean:
            return True
        
        # Verificar se um contém o outro
        if nome1_clean in nome2_clean or nome2_clean in nome1_clean:
            return True
        
        # Verificar similaridade por palavras (pelo menos 2 palavras iguais)
        palavras1 = set(nome1_clean.split())
        palavras2 = set(nome2_clean.split())
        
        # Remover palavras muito comuns que podem causar falsos positivos
        palavras_comuns = {'DA', 'DE', 'DO', 'DAS', 'DOS', 'E'}
        palavras1 = palavras1 - palavras_comuns
        palavras2 = palavras2 - palavras_comuns
        
        palavras_comuns = palavras1.intersection(palavras2)
        
        # Para nomes com muitas palavras, exigir pelo menos 3 palavras iguais
        if len(palavras1) >= 4 or len(palavras2) >= 4:
            if len(palavras_comuns) >= 3:
                return True
        # Para nomes menores, 2 palavras iguais são suficientes
        elif len(palavras_comuns) >= 2:
            return True
        
        # Verificar se há pelo menos 70% de similaridade de caracteres
        if len(nome1_clean) > 10 and len(nome2_clean) > 10:
            from difflib import SequenceMatcher
            similaridade = SequenceMatcher(None, nome1_clean, nome2_clean).ratio()
            if similaridade >= 0.7:
                return True
        
        return False
    
    def gerar_relatorio_excel(self, dados_portaria, erros, nome_arquivo=None):
        """Gera relatório em Excel com os erros encontrados"""
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"relatorio_erros_portaria_{timestamp}.xlsx"
        
        wb = Workbook()
        
        # Aba 1: Resumo
        ws_resumo = wb.active
        if ws_resumo is not None:
            ws_resumo.title = "Resumo"
            ws_resumo['A1'] = "RELATÓRIO DE ANÁLISE DE PORTARIA"
            ws_resumo['A1'].font = Font(bold=True, size=14)
            ws_resumo['A3'] = "Número da Portaria:"
            ws_resumo['B3'] = dados_portaria.get('numero', 'N/A') if dados_portaria else "N/A"
            ws_resumo['A4'] = "Data:"
            ws_resumo['B4'] = dados_portaria.get('data', 'N/A') if dados_portaria else "N/A"
            ws_resumo['A5'] = "Tipo de Naturalização:"
            ws_resumo['B5'] = dados_portaria.get('tipo', 'N/A') if dados_portaria else "N/A"
            ws_resumo['A6'] = "Total de Pessoas:"
            ws_resumo['B6'] = len(dados_portaria.get('pessoas', [])) if dados_portaria else 0
            ws_resumo['A7'] = "Total de Erros:"
            ws_resumo['B7'] = len(erros)
        # Aba 2: Erros Detalhados
        ws_erros = wb.create_sheet(title="Erros")
        
        # Cabeçalhos
        headers_erros = ['Tipo de Erro', 'Pessoa', 'Idade', 'País', 'Descrição']
        for col, header in enumerate(headers_erros, 1):
            cell = ws_erros.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
        
        # Dados dos erros
        for row, erro in enumerate(erros, 2):
            ws_erros.cell(row=row, column=1, value=erro['tipo'])
            ws_erros.cell(row=row, column=2, value=erro.get('pessoa', ''))
            ws_erros.cell(row=row, column=3, value=erro.get('idade', ''))
            ws_erros.cell(row=row, column=4, value=erro.get('pais', ''))
            ws_erros.cell(row=row, column=5, value=erro['descrição'])
        
        # Aba 3: Pessoas da Portaria
        if dados_portaria and dados_portaria.get('pessoas'):
            ws_pessoas = wb.create_sheet(title="Pessoas")
            headers_pessoas = ['Nome', 'Documento', 'Tipo Doc', 'Processo', 'País', 'Data Nascimento', 'Idade', 'Nome do Pai', 'Estado']
            for col, header in enumerate(headers_pessoas, 1):
                cell = ws_pessoas.cell(row=1, column=col, value=header)
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
            for row, pessoa in enumerate(dados_portaria.get('pessoas', []), 2):
                ws_pessoas.cell(row=row, column=1, value=pessoa.get('nome', ''))
                ws_pessoas.cell(row=row, column=2, value=pessoa.get('documento', ''))
                ws_pessoas.cell(row=row, column=3, value=pessoa.get('tipo_documento', ''))
                ws_pessoas.cell(row=row, column=4, value=pessoa.get('processo', ''))
                ws_pessoas.cell(row=row, column=5, value=pessoa.get('pais', ''))
                ws_pessoas.cell(row=row, column=6, value=pessoa.get('data_nascimento', ''))
                ws_pessoas.cell(row=row, column=7, value=pessoa.get('idade', ''))
                ws_pessoas.cell(row=row, column=8, value=pessoa.get('nome_pai', ''))
                ws_pessoas.cell(row=row, column=9, value=pessoa.get('estado', ''))
        
        # Salvar arquivo
        wb.save(nome_arquivo)
        print(f"Relatório salvo em: {nome_arquivo}")
        
        return nome_arquivo
    
    def analisar_portaria(self, url_portaria, gerar_excel=True):
        """
        Método principal para analisar uma portaria
        
        Args:
            url_portaria (str): URL da portaria
            gerar_excel (bool): Se deve gerar relatório em Excel
            
        Returns:
            dict: Resultado da análise
        """
        print(f"Analisando portaria: {url_portaria}")
        
        # 1. Buscar conteúdo da portaria
        html_content = self.buscar_portaria_web(url_portaria)
        if not html_content:
            return {'erro': 'Não foi possível acessar a portaria'}
        
        # 2. Extrair texto dos parágrafos HTML corretamente
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Encontrar a div com class="texto-dou" que contém todas as portarias
        div_texto = soup.find('div', class_='texto-dou')
        if div_texto:
            # Extrair apenas os parágrafos da div texto-dou
            paragrafos = div_texto.find_all('p')
            texto_completo = '\n'.join([p.get_text().strip() for p in paragrafos])
        else:
            # Fallback: usar o método anterior
            texto_completo = soup.get_text()
        
        print(f"Texto extraído dos parágrafos: {len(texto_completo)} caracteres")
        
        # 3. Analisar múltiplas portarias
        resultados, arquivos_excel = self.analisar_multiplas_portarias(texto_completo, gerar_excel)
        
        # 4. Retornar resultado consolidado
        total_erros = sum(r['total_erros'] for r in resultados)
        
        return {
            'resultados': resultados,
            'arquivos_excel': arquivos_excel,
            'total_erros': total_erros,
            'total_portarias': len(resultados)
        }
    
    def analisar_texto_portaria(self, texto_portaria, gerar_excel=True):
        """
        Método para analisar uma portaria a partir do texto direto
        
        Args:
            texto_portaria (str): Texto da portaria
            gerar_excel (bool): Se deve gerar relatório em Excel
            
        Returns:
            dict: Resultado da análise
        """
        print(f"Analisando texto da portaria...")
        
        # 1. Extrair dados estruturados
        dados_portaria = self.extrair_dados_portaria_direto(texto_portaria)
        
        # 2. Verificar erros
        erros = self.verificar_erros(dados_portaria)
        
        # 3. Gerar relatório
        if gerar_excel:
            arquivo_excel = self.gerar_relatorio_excel(dados_portaria, erros)
        else:
            arquivo_excel = None
        
        # 4. Mostrar resumo
        print("\n" + "="*50)
        print("RESUMO DA ANÁLISE")
        print("="*50)
        
        if dados_portaria:
            print(f"Portaria: {dados_portaria['numero']}")
            print(f"Data: {dados_portaria['data']}")
            print(f"Tipo: {dados_portaria['tipo']}")
            print(f"Total de pessoas: {len(dados_portaria['pessoas'])}")
        
        print(f"Total de erros encontrados: {len(erros)}")
        
        if erros:
            print("\nERROS ENCONTRADOS:")
            for i, erro in enumerate(erros, 1):
                print(f"{i}. {erro['descrição']}")
        else:
            print("\n✅ Nenhum erro encontrado!")
        
        return {
            'dados_portaria': dados_portaria,
            'erros': erros,
            'arquivo_excel': arquivo_excel,
            'total_erros': len(erros)
        }
    
    def formatar_numero_portaria(self, numero):
        """
        Formata o número da portaria mantendo o formato original
        
        Args:
            numero (str): Número da portaria
            
        Returns:
            str: Número formatado
        """
        # Remover pontos e vírgulas temporariamente para converter para número
        numero_limpo = numero.replace('.', '').replace(',', '')
        numero_int = int(float(numero_limpo))
        
        # Formatar com pontos e vírgulas conforme o padrão oficial
        numero_formatado = format(numero_int, ',').replace(',', '.')
        return f"Nº {numero_formatado}".upper()

    def extrair_dados_portaria_direto(self, texto_portaria, forcar_linha_por_bloco=False):
        """
        Extrai dados estruturados da portaria a partir do texto direto
        Args:
            texto_portaria (str): Texto da portaria
            forcar_linha_por_bloco (bool): Se True, cada linha é um bloco de pessoa
        Returns:
            dict: Dados estruturados da portaria
        """
        print("Extraindo dados da portaria...")
        if not texto_portaria:
            print("❌ Texto da portaria vazio")
            return None
        texto_completo = texto_portaria
        print(f"Texto extraído: {len(texto_completo)} caracteres")
        print(f"Início do texto: {texto_completo[:500]}...")
        patterns_portaria = [
            r'PORTARIA\s*,?\s*Nº\s*(\d+[\.,]?\d*)\s*,?\s*DE\s*(\d{1,2}\s+DE\s+\w+\s+DE\s+\d{4})',
            r'PORTARIA\s*Nº\s*(\d+[\.,]?\d*)[,,\s]*DE\s*(\d{1,2}\s+DE\s+\w+\s+DE\s+\d{4})',
            r'PORTARIA\s*(\d+[\.,]?\d*)[,,\s]*DE\s*(\d{1,2}\s+DE\s+\w+\s+DE\s+\d{4})',
            r'PORTARIA\s*Nº\s*(\d+[\.,]?\d*)',
        ]
        match_portaria = None
        for i, pattern in enumerate(patterns_portaria):
            print(f"Tentando padrão {i+1}: {pattern}")
            match = re.search(pattern, texto_completo, re.IGNORECASE)
            if match:
                match_portaria = match
                print(f"✅ Padrão {i+1} encontrou match: {match.groups()}")
                break
        if not match_portaria:
            print("❌ Nenhum padrão de portaria encontrado")
            print("Debug: Procurando por 'PORTARIA' no texto...")
            if 'PORTARIA' in texto_completo.upper():
                print("✅ 'PORTARIA' encontrada no texto")
                match_numero = re.search(r'PORTARIA\s*[NnNº°]?\s*(\d+)', texto_completo, re.IGNORECASE)
                if match_numero:
                    numero_portaria = match_numero.group(1)
                    data_portaria = "Data não encontrada"
                    print(f"✅ Número extraído: {numero_portaria}")
                else:
                    return None
            else:
                print("❌ 'PORTARIA' não encontrada no texto")
                return None
        else:
            numero_portaria = match_portaria.group(1)
            data_portaria = match_portaria.group(2)
        numero_formatado = self.formatar_numero_portaria(numero_portaria)
        print(f"✅ Portaria encontrada: PORTARIA {numero_formatado}, DE {data_portaria}")
        tipo_naturalizacao = self.identificar_tipo_naturalizacao(texto_completo)
        print(f"✅ Tipo identificado: {tipo_naturalizacao}")
        pessoas = self.extrair_pessoas(texto_completo, forcar_linha_por_bloco=forcar_linha_por_bloco)
        print(f"✅ Pessoas extraídas: {len(pessoas)}")
        return {
            'numero': numero_formatado,
            'data': data_portaria,
            'tipo': tipo_naturalizacao,
            'pessoas': pessoas,
            'texto_completo': texto_completo
        }

    def analisar_multiplas_portarias(self, texto_completo, gerar_excel=True):
        """
        Analisa múltiplas portarias em um texto único, separando cada portaria e identificando o tipo corretamente.
        """
        # Padrão flexível para portarias de naturalização: PORTARIA[,] N[º°] [número], DE [data]
        # Corrigido para aceitar vírgula antes do Nº
        padrao_portaria = r'(PORTARIA\s*,?\s*N[º°]?\s*\d+[\.,]?\d*\s*,\s*DE\s*\d{1,2}\s+DE\s+\w+\s+DE\s+\d{4}[\s\S]*?)(?=PORTARIA\s*,?\s*N[º°]?\s*\d+[\.,]?\d*\s*,\s*DE\s*\d{1,2}\s+DE\s+\w+\s+DE\s+\d{4}|$)'
        blocos = re.findall(padrao_portaria, texto_completo, flags=re.IGNORECASE)
        blocos = [b.strip() for b in blocos if b.strip()]
        
        print(f"Regex encontrou {len(blocos)} blocos de portarias")
        for i, bloco in enumerate(blocos):
            print(f"Bloco {i+1}: {bloco[:100]}...")
        
        if not blocos:
            print("Nenhuma portaria de naturalização encontrada com o padrão específico.")
            # Fallback para o caso de ter apenas uma portaria colada sem o cabeçalho completo do DOU
            dados_portaria = self.extrair_dados_portaria_direto(texto_completo)
            if not dados_portaria or not dados_portaria.get('pessoas'):
                print("Não foi possível extrair dados ou pessoas da portaria única.")
                return [], []
            print("Analisando como portaria única (fallback).")
            erros = self.verificar_erros(dados_portaria)
            arquivo_excel = None
            if gerar_excel:
                arquivo_excel = self.gerar_relatorio_excel(dados_portaria, erros)
            return [{
                'dados_portaria': dados_portaria,
                'erros': erros,
                'arquivo_excel': arquivo_excel,
                'total_erros': len(erros)
            }], [arquivo_excel] if arquivo_excel else []
        
        print(f"Encontradas {len(blocos)} portarias de naturalização para análise.")
        todas_pessoas_documento = []
        resultados = []
        arquivos_excel = []
        
        for i, bloco in enumerate(blocos, 1):
            print(f"\n==============================")
            print(f"Analisando PORTARIA {i}...")
            print(f"Tamanho do bloco: {len(bloco)} caracteres")
            print(f"Primeiros 200 caracteres: {bloco[:200]}...")
            
            dados_portaria = self.extrair_dados_portaria_direto(bloco, forcar_linha_por_bloco=True)
            if not dados_portaria:
                print(f"❌ Não foi possível extrair dados da portaria {i}")
                continue
                
            erros = self.verificar_erros(dados_portaria)
            erros_duplicatas = self.verificar_duplicatas_entre_portarias(dados_portaria, todas_pessoas_documento)
            erros.extend(erros_duplicatas)
            
            for pessoa in dados_portaria['pessoas']:
                todas_pessoas_documento.append({
                    'nome': pessoa['nome'],
                    'data_nascimento': pessoa['data_nascimento'],
                    'portaria_origem': dados_portaria['numero']
                })
            
            arquivo_excel = None
            if gerar_excel:
                arquivo_excel = self.gerar_relatorio_excel(dados_portaria, erros)
                arquivos_excel.append(arquivo_excel)
            
            resultados.append({
                'dados_portaria': dados_portaria,
                'erros': erros,
                'arquivo_excel': arquivo_excel,
                'total_erros': len(erros)
            })
        
        return resultados, arquivos_excel

    def verificar_duplicatas_entre_portarias(self, dados_portaria_atual, todas_pessoas_documento):
        """
        Verifica se pessoas da portaria atual já apareceram em outras portarias do mesmo documento
        """
        erros = []
        
        for pessoa_atual in dados_portaria_atual['pessoas']:
            nome_atual = pessoa_atual['nome']
            data_atual = pessoa_atual['data_nascimento']
            
            # Verificar se esta pessoa já apareceu em outras portarias do documento
            for pessoa_anterior in todas_pessoas_documento:
                if (pessoa_anterior['nome'] == nome_atual and 
                    pessoa_anterior['data_nascimento'] == data_atual):
                    
                    erros.append({
                        'tipo': 'DUPLICATA_ENTRE_PORTARIAS',
                        'pessoa': nome_atual,
                        'descrição': f'{nome_atual} aparece em mais de uma portaria no mesmo documento: Portaria {pessoa_anterior["portaria_origem"]} e Portaria {dados_portaria_atual["numero"]}'
                    })
                    break  # Só precisa encontrar uma duplicata
        
        return erros

    def normalizar_pais(self, pais_str):
        """Normaliza o nome do país para corresponder aos nomes oficiais"""
        if not pais_str:
            return None
            
        # Remover palavras extras como "NASCIDO", "NASCIDA", etc.
        pais_limpo = re.sub(r'\s+(NASCIDO|NASCIDA|NATURAL|DE|DA|DO)\s*$', '', pais_str.strip(), flags=re.IGNORECASE)
        
        # Mapeamentos específicos
        mapeamentos = {
            'ARGENTINA NASCIDO': 'ARGENTINA',
            'VENEZUELA NASCIDO': 'VENEZUELA',
            'EGITO NASCIDO': 'EGITO',
            'URUGUAI NASCIDO': 'URUGUAI',
            'LIBANO': 'LÍBANO',
            'NIGERIA': 'NIGÉRIA',
            'SIRIA': 'SÍRIA',
            'FEDERAÇÃO DA RÚSSIA': 'RÚSSIA',
            'FRANÇA METROPOLITANA': 'FRANÇA'
        }
        
        # Verificar mapeamentos
        if pais_limpo.upper() in mapeamentos:
            return mapeamentos[pais_limpo.upper()]
        
        # Verificar se está na lista oficial
        if pais_limpo.upper() in self.paises_oficiais:
            return pais_limpo.upper()
        
        # Tentar encontrar correspondência aproximada
        for pais_oficial in self.paises_oficiais:
            if pais_limpo.upper() == pais_oficial.upper():
                return pais_oficial
        
        return pais_limpo.upper()  # Retornar como está se não encontrar correspondência

# Exemplo de uso - versão melhorada com diagnósticos
def main():
    print("="*60)
    print("🔍 ANALISADOR DE PORTARIAS DE NATURALIZAÇÃO")
    print("="*60)
    
    # Configurar analisador
    print("\n1. Configurando analisador...")
    
    # Verificar se há planilha de histórico
    arquivos_historico = [
        "historico_naturalizacoes.xlsx"
    ]
    
    caminho_historico = None
    for arquivo in arquivos_historico:
        if os.path.exists(arquivo):
            caminho_historico = arquivo
            break
    
    if not caminho_historico:
        print("⚠️  Nenhuma planilha de histórico encontrada.")
        print("   Procurados:", ", ".join(arquivos_historico))
        usar_historico = input("   Deseja informar o caminho manualmente? (s/n): ").lower() == 's'
        
        if usar_historico:
            caminho_historico = input("   Digite o caminho da planilha: ").strip()
            if not os.path.exists(caminho_historico):
                print("   ❌ Arquivo não encontrado. Continuando sem histórico...")
                caminho_historico = None
    else:
        print(f"✅ Planilha de histórico encontrada: {caminho_historico}")
    
    analyzer = PortariaAnalyzer(caminho_historico)
    
    print("\n2. Escolhendo método de análise...")
    print("1. Analisar por URL")
    print("2. Analisar texto direto")
    
    opcao = input("Escolha uma opção (1 ou 2): ").strip()
    
    if opcao == "1":
        print("\n3. Obtendo URL da portaria...")
        url_portaria = input("Digite a URL da portaria para análise: ").strip()
        
        if not url_portaria:
            print("❌ URL não fornecida!")
            return
        
        print(f"URL informada: {url_portaria}")
        
        print("\n4. Iniciando análise...")
        print("-" * 40)
        
        # Analisar por URL
        try:
            resultado = analyzer.analisar_portaria(url_portaria)
            
            if 'erro' in resultado:
                print(f"❌ Erro: {resultado['erro']}")
            else:
                print(f"\n🎉 Análise concluída!")
                print(f"📊 {resultado['total_erros']} erros encontrados em {resultado['total_portarias']} portarias.")
                
                if resultado['arquivos_excel']:
                    print(f"📄 Relatórios Excel: {', '.join(resultado['arquivos_excel'])}")
                
                # Coletar todos os erros de todas as portarias
                todos_erros = []
                todas_pessoas = []
                
                for idx, res in enumerate(resultado['resultados'], 1):
                    dados = res.get('dados_portaria') if isinstance(res, dict) else None
                    if dados:
                        todas_pessoas.extend(dados.get('pessoas', []))
                        # Adicionar informações da portaria aos erros
                        erros_res = res.get('erros') if isinstance(res, dict) else None
                        if erros_res:
                            for erro in erros_res:
                                erro_completo = erro.copy() if isinstance(erro, dict) else {}
                                erro_completo['portaria'] = dados.get('numero', 'N/A')
                                erro_completo['tipo_portaria'] = dados.get('tipo', 'N/A')
                                todos_erros.append(erro_completo)
                
                # Mostrar resumo consolidado
                print(f"\n{'='*80}")
                print("📋 RESUMO CONSOLIDADO DE TODOS OS ERROS ENCONTRADOS")
                print(f"{'='*80}")
                
                if todos_erros:
                    print(f"\n🔴 Total de {len(todos_erros)} erros encontrados:")
                    print("-" * 80)
                    
                    for i, erro in enumerate(todos_erros, 1):
                        pessoa = erro.get('pessoa', 'N/A')
                        tipo_erro = erro.get('tipo', 'ERRO DESCONHECIDO')
                        descricao = erro.get('descrição', '')
                        portaria = erro.get('portaria', 'N/A')
                        tipo_portaria = erro.get('tipo_portaria', 'N/A')
                        idade = erro.get('idade', '')
                        pais = erro.get('pais', '')
                        
                        print(f"{i:2d}. PESSOA: {pessoa}")
                        print(f"    📄 Portaria: {portaria} ({tipo_portaria})")
                        print(f"    ⚠️  Erro: {descricao}")
                        if idade:
                            print(f"    📅 Idade: {idade} anos")
                        if pais:
                            print(f"    🌍 País: {pais}")
                        print()
                else:
                    print("\n✅ Nenhum erro encontrado em nenhuma portaria!")
                
                # Mostrar estatísticas
                print(f"\n📊 ESTATÍSTICAS:")
                print(f"   • Total de portarias analisadas: {resultado['total_portarias']}")
                print(f"   • Total de pessoas processadas: {len(todas_pessoas)}")
                print(f"   • Total de erros encontrados: {len(todos_erros)}")
                
                # Contar tipos de erro
                tipos_erro = {}
                for erro in todos_erros:
                    tipo = erro.get('tipo', 'DESCONHECIDO')
                    tipos_erro[tipo] = tipos_erro.get(tipo, 0) + 1
                
                if tipos_erro:
                    print(f"\n📈 Tipos de erro encontrados:")
                    for tipo, quantidade in tipos_erro.items():
                        print(f"   • {tipo}: {quantidade}")
                
                print(f"\n{'='*80}")
        
        except KeyboardInterrupt:
            print("\n❌ Análise interrompida pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
    
    elif opcao == "2":
        print("\n3. Inserindo texto da portaria...")
        print("Cole o texto da portaria abaixo (pressione Ctrl+D ou Ctrl+Z quando terminar):")
        
        linhas = []
        try:
            while True:
                linha = input()
                linhas.append(linha)
        except (EOFError, KeyboardInterrupt):
            pass
        
        texto_portaria = '\n'.join(linhas)
        
        if not texto_portaria.strip():
            print("❌ Texto não fornecido!")
            return
        
        print(f"\nTexto recebido: {len(texto_portaria)} caracteres")
        
        print("\n4. Iniciando análise...")
        print("-" * 40)
        
        # Analisar múltiplas portarias
        try:
            resultados, arquivos_excel = analyzer.analisar_multiplas_portarias(texto_portaria)
            
            # Coletar todos os erros de todas as portarias
            todos_erros = []
            todas_pessoas = []
            total_portarias = 0
            
            for idx, resultado in enumerate(resultados, 1):
                if resultado['dados_portaria']:
                    dados = resultado['dados_portaria']
                    todas_pessoas.extend(dados['pessoas'])
                    total_portarias += 1
                    
                    # Adicionar informações da portaria aos erros
                    for erro in resultado['erros']:
                        erro_completo = erro.copy()
                        erro_completo['portaria'] = dados['numero']
                        erro_completo['tipo_portaria'] = dados['tipo']
                        todos_erros.append(erro_completo)
            
            # Mostrar resumo consolidado
            print(f"\n{'='*80}")
            print("📋 RESUMO CONSOLIDADO DE TODOS OS ERROS ENCONTRADOS")
            print(f"{'='*80}")
            
            if todos_erros:
                print(f"\n🔴 Total de {len(todos_erros)} erros encontrados:")
                print("-" * 80)
                
                for i, erro in enumerate(todos_erros, 1):
                    pessoa = erro.get('pessoa', 'N/A')
                    tipo_erro = erro.get('tipo', 'ERRO DESCONHECIDO')
                    descricao = erro.get('descrição', '')
                    portaria = erro.get('portaria', 'N/A')
                    tipo_portaria = erro.get('tipo_portaria', 'N/A')
                    idade = erro.get('idade', '')
                    pais = erro.get('pais', '')
                    
                    print(f"{i:2d}. PESSOA: {pessoa}")
                    print(f"    📄 Portaria: {portaria} ({tipo_portaria})")
                    print(f"    ⚠️  Erro: {descricao}")
                    if idade:
                        print(f"    📅 Idade: {idade} anos")
                    if pais:
                        print(f"    🌍 País: {pais}")
                    print()
            else:
                print("\n✅ Nenhum erro encontrado em nenhuma portaria!")
            
            # Mostrar estatísticas
            print(f"\n📊 ESTATÍSTICAS:")
            print(f"   • Total de portarias analisadas: {total_portarias}")
            print(f"   • Total de pessoas processadas: {len(todas_pessoas)}")
            print(f"   • Total de erros encontrados: {len(todos_erros)}")
            
            # Contar tipos de erro
            tipos_erro = {}
            for erro in todos_erros:
                tipo = erro.get('tipo', 'DESCONHECIDO')
                tipos_erro[tipo] = tipos_erro.get(tipo, 0) + 1
            
            if tipos_erro:
                print(f"\n📈 Tipos de erro encontrados:")
                for tipo, quantidade in tipos_erro.items():
                    print(f"   • {tipo}: {quantidade}")
            
            if arquivos_excel:
                print(f"\n📄 Relatórios Excel gerados: {', '.join(arquivos_excel)}")
            
            print(f"\n{'='*80}")
        except KeyboardInterrupt:
            print("\n❌ Análise interrompida pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
    
    else:
        print("❌ Opção inválida!")
        return
    
    print("\n" + "="*60)
    input("Pressione Enter para finalizar...")

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.10', port=9000)