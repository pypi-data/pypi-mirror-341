"""
Interface de linha de comando para o framework OrNexus
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
import asyncio
import re
import subprocess
import getpass
import json
import datetime
from dotenv import load_dotenv
import hashlib
import yaml
from pydantic import BaseModel, Field

# Verificar se motor está instalado e instalar se necessário
try:
    import motor
except ImportError:
    print("⚠️ Pacote 'motor' não encontrado. Instalando...")
    subprocess.run([sys.executable, "-m", "pip", "install", "motor"], check=True)
    import motor

# Verificar se hashlib está instalado
try:
    import hashlib
except ImportError:
    print("⚠️ Pacote 'hashlib' não encontrado. Instalando...")
    subprocess.run([sys.executable, "-m", "pip", "install", "hashlib"], check=True)
    import hashlib

from ornexus.database import MongoDBAsyncIntegration, md5_hash

# Carregar variáveis de ambiente do .env (se existir)
load_dotenv()

def normalize_class_name(project_name):
    """
    Normaliza o nome do projeto para usar como nome de classe
    
    Args:
        project_name: Nome do projeto
        
    Returns:
        Nome da classe normalizado (PascalCase)
    """
    # Remover caracteres não alfanuméricos e substituir por espaços
    normalized = re.sub(r'[^a-zA-Z0-9]', ' ', project_name)
    # Dividir em palavras, capitalizar cada palavra e juntar
    return ''.join(word.capitalize() for word in normalized.split())

def create_project_structure(project_name):
    """
    Cria a estrutura básica de um novo projeto baseado no Agno
    
    Args:
        project_name: Nome do projeto a ser criado
    """
    # Obter o diretório do pacote ornexus
    package_dir = Path(__file__).parent.absolute()
    
    # Normalizar o nome do projeto para nome de classe
    class_name = normalize_class_name(project_name)
    
    # Criar o diretório do projeto com caminho absoluto para evitar problemas
    project_dir = Path(project_name).absolute()
    if project_dir.exists():
        print(f"Erro: O diretório {project_name} já existe.")
        return False
    
    # Criar estrutura de diretórios
    dirs = [
        project_dir,
        project_dir / "config",
        project_dir / "knowledge",
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Criado diretório: {dir_path.name if dir_path == project_dir else str(dir_path).replace(str(project_dir) + '/', '')}")
    
    # Copiar arquivos de template
    templates = {
        package_dir / "config" / "agents.yaml": project_dir / "config" / "agents.yaml",
        package_dir / "config" / "tasks.yaml": project_dir / "config" / "tasks.yaml",
    }
    
    for src, dest in templates.items():
        shutil.copy2(src, dest)
        # Solução: usar uma string formatada em vez de relative_to
        dest_path = str(dest).replace(str(project_dir) + '/', '')
        print(f"✅ Copiado: {src.name} -> {dest_path}")
    
    # Criar arquivo __init__.py do projeto
    with open(project_dir / "__init__.py", "w") as f:
        f.write('"""Projeto gerado pelo framework OrNexus"""\n\n')
    print(f"✅ Criado arquivo: {project_name}/__init__.py")

    with open(project_dir / ".env", "w") as f:
        f.write('ANONYMIZED_TELEMETRY=true\n')
        f.write('CREWAI_DISABLE_TELEMETRY=true\n')
        f.write('OTEL_SDK_DISABLED=true\n')
        f.write('OPENAI_API_KEY=\n')
        f.write('ANTHROPIC_API_KEY=\n')
        f.write('MONGODB_CONN=\n')
        f.write('SERPAPI_API_KEY=\n')
        f.write('SERPER_API_KEY=\n')
    print(f"✅ Criado arquivo: {project_name}/.env")
    
    # Criar arquivo main.py do projeto com método correto para execução assíncrona
    with open(project_dir / f"{project_name}.py", "w") as f:
        f.write(f'''from typing import Dict, Any, Optional
from pathlib import Path
import os
from datetime import datetime
import json
import yaml
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.team import Team
from agno.models.anthropic import Claude
from agno.models.openai import OpenAIChat
from agno.tools.crawl4ai import Crawl4aiTools
from agno.tools.serpapi import SerpApiTools

# Classe Pydantic para gerenciar os inputs da aplicação
class AppInputs(BaseModel):
    topico: str = Field(
        default="Impactos da política monetária dos bancos centrais em mercados emergentes",
        description="Tópico principal da pesquisa"
    )
    tema: str = Field(
        default="Como as decisões do FED afetam economias emergentes em 2024",
        description="Tema específico a ser explorado"
    )
    datenow: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d"),
        description="Data atual para contextualização"
    )
    
    def __str__(self) -> str:
        """Converte os inputs para string em formato JSON para passar ao agente"""
        return json.dumps(self.model_dump())

#===============================================================================#
# Configuração de conhecimento para o OrNexus
# Para mais informações sobre como configurar e utilizar bases de conhecimento,
# consulte a documentação oficial do Agno em: https://docs.agno.com/knowledge/introduction
#===============================================================================#

# from agno.knowledge.text import TextKnowledgeBase
# from agno.document.chunking.recursive import RecursiveChunking
# from agno.vectordb.mongodb import MongoDb

# # Exemplo de conexão do MongoDB Atlas
# mongodb_uri = os.getenv("MONGODB_CONN")
# print(f"Usando MongoDB URI: {{mongodb_uri}}")

# # Exemplo de inicialização do TextKnowledgeBase com MongoDB e RecursiveChunking
# knowledge = TextKnowledgeBase(
#     path=str(knowledge_dir),  # Caminho para a pasta knowledge com arquivos .txt
#     vector_db=MongoDb(
#         database="ornexus_knw",
#         collection_name="knowledge", 
#         db_url=mongodb_uri,
#         wait_until_index_ready=60,
#         wait_after_insert=300
#     ),
#     chunking_strategy=RecursiveChunking()
# )

class {class_name}:
    """Aplicação baseada no framework OrNexus"""
    
    def __init__(self, recreate=False):
        # self.knowledge = knowledge        
        # if recreate:
        #     self.knowledge.load(recreate=True)
        # else:
        #     self.knowledge.load(recreate=False)

        with open('config/agents.yaml', 'r') as f:
            self.config_agents = yaml.safe_load(f)

        with open('config/tasks.yaml', 'r') as f:
            self.config_tasks = yaml.safe_load(f)

        self.sonnet3_7 = Claude(
            id="claude-3-7-sonnet-20250219",
            temperature=0.0,
            max_tokens=8000
        )
        
        self.gpt4o = OpenAIChat(
            id="gpt-4o",
            temperature=0.0,
        )

    def pesquisador(self) -> Agent:
        return Agent(
            name="Pesquisador Econômico",
            role=self.config_agents['researcher']['role'],
            goal=self.config_agents['researcher']['goal'],
            description=self.config_agents['researcher']['backstory'],
            instructions=self.config_tasks['pesquisador']['description'],
            expected_output=self.config_tasks['pesquisador']['expected_output'],
            model=self.sonnet3_7,
            debug_mode=True,
            telemetry=False,
            tools=[
                Crawl4aiTools(),
                SerpApiTools()
            ],
            show_tool_calls=True,
            # knowledge=self.knowledge
        )
    
    def redator_twitter(self) -> Agent:
        return Agent(
            name="Redator de Conteúdo para Twitter",
            role=self.config_agents['content_writer']['role'],
            goal=self.config_agents['content_writer']['goal'],
            description=self.config_agents['content_writer']['backstory'],
            instructions=self.config_tasks['redator_twitter']['description'],
            expected_output=self.config_tasks['redator_twitter']['expected_output'],
            model=self.sonnet3_7,
            debug_mode=True,
            telemetry=False,
            # knowledge=self.knowledge
        )
    
    def team(self) -> Team:
        return Team(
            mode="collaborate",
            members=[
                self.pesquisador(),
                self.redator_twitter()
            ],
            model=self.sonnet3_7,
            debug_mode=True,
            success_criteria="Uma análise econômica completa com conteúdo pronto para redes sociais.",
            expected_output="Uma análise econômica completa com conteúdo pronto para redes sociais.",
            telemetry=False
        )

def main(inputs: Optional[AppInputs] = None):
    if not inputs:
        inputs = AppInputs()
    
    app = {class_name}(recreate=True)
    team = app.team()
    
    result = team.print_response(str(inputs))
    return result

if __name__ == "__main__":
    inputs = AppInputs(
        topico = "Escolha um tópico",
        tema = "Escolha um tema",
        datenow = datetime.now().strftime("%Y-%m-%d"),
    )
    main()
''')
    print(f"✅ Criado arquivo: {project_name}/{project_name}.py")
    
    # Criar requirements.txt
    with open(project_dir / "requirements.txt", "w") as f:
        f.write('agno\n')
        f.write('ornexus\n')
        f.write('openai\n')
        f.write('anthropic\n')
        f.write('pymongo\n')
        f.write('pyyaml\n')
        f.write('crawl4ai\n')
        f.write('google-search-results\n')
    print(f"✅ Criado arquivo: {project_name}/requirements.txt")
    
    # Instalar o UV se não estiver instalado
    try:
        subprocess.run(["uv", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("✅ UV já está instalado.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("🔄 Instalando o UV...")
        try:
            subprocess.run(["pip", "install", "--user", "uv"], check=True)
            print("✅ UV instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar o UV: {e}")
            print("⚠️ Ambiente virtual não será criado. Por favor, instale o UV manualmente: pip install uv")
            print(f"\nProjeto '{project_name}' criado com sucesso!")
            print(f"Classe principal: {class_name}")
            print("\nPara executar o projeto, use:")
            print(f"  cd {project_name}")
            print(f"  python -m {project_name}")
            return True
    
    # Criar ambiente virtual com UV
    print(f"🔄 Criando ambiente virtual com UV em {project_name}/.venv...")
    os.chdir(project_dir)
    try:
        subprocess.run(["uv", "venv", ".venv"], check=True)
        print("✅ Ambiente virtual criado.")
        
        # Instalar dependências usando UV global (não o do ambiente virtual)
        print("🔄 Instalando dependências no ambiente virtual...")
        
        try:
            # Usar o UV global para instalar no venv
            subprocess.run(["uv", "pip", "install", "--python", ".venv/bin/python", "-r", "requirements.txt"], check=True)
            print("✅ Dependências instaladas no ambiente virtual.")
            
            # Instruções para ativar o ambiente
            if sys.platform == "win32":
                activate_instr = f"  .venv\\Scripts\\activate"
            else:
                activate_instr = f"  source .venv/bin/activate"
            
            print(f"\nProjeto '{project_name}' baseado em Agno criado com sucesso!")
            print(f"Classe principal: {class_name}")
            print("\nPara usar o ambiente virtual e executar o projeto:")
            print(f"  cd {project_name}")
            print(activate_instr)
            print(f"  python -m {project_name}")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            print("Por favor, instale manualmente:")
            print(f"  cd {project_name}")
            if sys.platform == "win32":
                print(f"  .venv\\Scripts\\activate")
            else:
                print(f"  source .venv/bin/activate")
            print(f"  pip install -r requirements.txt")
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar ambiente virtual: {e}")
        print("Por favor, crie manualmente:")
        print(f"  cd {project_name}")
        print(f"  python -m venv .venv")
        print(f"  source .venv/bin/activate  # ou .venv\\Scripts\\activate no Windows")
        print(f"  pip install -r requirements.txt")
    
    # Voltar ao diretório original
    os.chdir(str(project_dir.parent))
    return True

def create_crewai_flow_project(project_name):
    """
    Cria a estrutura básica de um novo projeto baseado em CrewAI
    
    Args:
        project_name: Nome do projeto a ser criado
    """
    # Verificar se o crewai está instalado
    try:
        import importlib.util
        crewai_spec = importlib.util.find_spec("crewai")
        if crewai_spec is None:
            print("⚠️ CrewAI não está instalado. Instalando...")
            subprocess.run([sys.executable, "-m", "pip", "install", "crewai[tools]>=0.28.6"], check=True)
            print("✅ CrewAI instalado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao verificar/instalar CrewAI: {e}")
        return False
    
    # Executar o comando crewai create flow
    try:
        print(f"🚀 Criando projeto CrewAI Flow: {project_name}")
        subprocess.run(["crewai", "create", "flow", project_name], check=True)
        print(f"\n✅ Projeto '{project_name}' baseado em CrewAI flow criado com sucesso!")
        print(f"\nPara executar o projeto, use:")
        print(f"  cd {project_name}")
        print(f"  crewai run")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar projeto CrewAI flow: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

async def authenticate_user(email, password):
    """
    Autentica um usuário via API
    
    Args:
        email: Email do usuário
        password: Senha do usuário
    
    Returns:
        Dicionário com informações do usuário ou None se autenticação falhar
    """
    try:
        # Usar a API para autenticação
        from ornexus.database import AUTH_SERVICE_URL
        import requests
        
        # Calcular hash MD5 da senha
        password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
        
        # Fazer requisição de login para a API
        login_url = f"{AUTH_SERVICE_URL}/login"
        response = requests.post(
            login_url,
            data={"username": email, "password": password_md5, "password_is_hashed": "true"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            
            return {
                "email": email,
                "token": token
            }
        
        return None
        
    except Exception as e:
        print(f"❌ Erro ao conectar com o servidor: {str(e)}")
        return None

def check_login_status():
    """
    Verifica se o usuário está logado
    
    Returns:
        True se o usuário estiver logado, False caso contrário
    """
    # Verificar o arquivo auth.json (onde o token é armazenado)
    auth_file = Path.home() / ".ornexus" / "auth.json"
    
    if auth_file.exists():
        try:
            with open(auth_file, "r") as f:
                config = json.load(f)
            
            # Verificar se há um token
            if "token" in config and config["token"]:
                return True
        except:
            pass
            
    # Se chegou aqui, não está logado
    return False

async def login_command():
    """
    Executa o comando de login
    """
    print("🔑 Login OrNexus")
    
    if check_login_status():
        print("✅ Você já está logado.")
        return True
    
    email = input("Email: ")
    password = getpass.getpass("Senha: ")
    
    print("🔄 Autenticando...")
    
    try:
        # Usar a função de login via API
        from ornexus.database import api_login
        
        token = await api_login(email, password)
        
        if token:
            # Salvar token no arquivo de configuração
            config_dir = Path.home() / ".ornexus"
            config_dir.mkdir(exist_ok=True)
            
            with open(config_dir / "auth.json", "w") as f:
                json.dump({"token": token}, f)
            
            print("✅ Login bem-sucedido!")
            return True
        
        print("❌ Falha na autenticação. Verifique suas credenciais.")
        return False
        
    except Exception as e:
        print(f"❌ Erro ao autenticar: {str(e)}")
        print("Verifique se o servidor da API está disponível.")
        return False

def logout_command():
    """
    Executa o logout do usuário
    """
    auth_file = Path.home() / ".ornexus" / "auth.json"
    
    if not auth_file.exists():
        print("❌ Você não está logado.")
        return
    
    try:
        # Remover arquivo de autenticação
        auth_file.unlink()
        print("✅ Logout realizado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao fazer logout: {str(e)}")

def main():
    """Função principal da CLI"""
    parser = argparse.ArgumentParser(description="OrNexus CLI - Framework para criação de agentes")
    subparsers = parser.add_subparsers(dest="command", help="Comando a ser executado")
    
    # Comando 'login'
    login_parser = subparsers.add_parser("login", help="Autenticar na plataforma OrNexus")
    
    # Comando 'logout'
    logout_parser = subparsers.add_parser("logout", help="Sair da plataforma OrNexus")
    
    # Comando 'create'
    create_parser = subparsers.add_parser("create", help="Cria um novo projeto")
    create_subparsers = create_parser.add_subparsers(dest="create_type", help="Tipo de projeto a ser criado")
    
    # Subcomando 'create agno'
    agno_parser = create_subparsers.add_parser("agno", help="Cria projeto baseado em Agno")
    agno_parser.add_argument("project_name", help="Nome do projeto a ser criado")
    
    # Subcomando 'create flow'
    flow_parser = create_subparsers.add_parser("flow", help="Cria projeto baseado em CrewAI flow")
    flow_parser.add_argument("project_name", help="Nome do projeto a ser criado")
    
    # Comando 'run'
    run_parser = subparsers.add_parser("run", help="Executa um projeto existente")
    run_parser.add_argument("project_path", help="Caminho para o projeto")
    run_parser.add_argument("--input", "-i", help="Arquivo JSON com os inputs")
    
    # Comando 'deploy'
    deploy_parser = subparsers.add_parser("deploy", help="Cria estrutura de API no projeto")
    deploy_parser.add_argument("--path", "-p", help="Caminho para o projeto (opcional)")
    deploy_parser.add_argument("--force", "-f", action="store_true", help="Forçar criação mesmo sem ser projeto OrNexus")
    
    # Comando 'version'
    version_parser = subparsers.add_parser("version", help="Mostra a versão do framework")
    
    args = parser.parse_args()
    
    if args.command == "login":
        asyncio.run(login_command())
    
    elif args.command == "logout":
        logout_command()
    
    elif args.command == "create":
        # Verificar se o usuário está logado
        if not check_login_status():
            print("❌ Você precisa estar logado para criar projetos.")
            print("   Use 'ornexus login' para autenticar.")
            return
            
        if args.create_type == "agno":
            create_project_structure(args.project_name)
        elif args.create_type == "flow":
            create_crewai_flow_project(args.project_name)
        else:
            create_parser.print_help()
    
    elif args.command == "run":
        # Verificar se o usuário está logado
        if not check_login_status():
            print("❌ Você precisa estar logado para executar projetos.")
            print("   Use 'ornexus login' para autenticar.")
            return
            
        # Implementar a execução direta de projetos
        print("Execução direta de projetos não implementada ainda.")
    
    elif args.command == "deploy":
        # Verificar se o usuário está logado
        if not check_login_status():
            print("❌ Você precisa estar logado para fazer deploy.")
            print("   Use 'ornexus login' para autenticar.")
            return
            
        # Sempre usar força=True por padrão, independentemente da flag --force
        deploy_api_structure(args.path, force=True)
    
    elif args.command == "version":
        try:
            # Método 1: Tentar obter a versão instalada via pip
            import subprocess
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", "ornexus"], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                # Extrair a versão da saída do pip show
                for line in result.stdout.splitlines():
                    if line.startswith("Version:"):
                        version = line.split(":", 1)[1].strip()
                        print(f"OrNexus v{version}")
                        break
                else:
                    # Fallback 1: Tentar ler setup.cfg
                    try:
                        import configparser
                        cfg_path = Path(__file__).resolve().parent.parent / "setup.cfg"
                        if cfg_path.exists():
                            config = configparser.ConfigParser()
                            config.read(cfg_path)
                            if 'metadata' in config and 'version' in config['metadata']:
                                version = config['metadata']['version']
                                print(f"OrNexus v{version}")
                            else:
                                # Fallback 2: Usar pkg_resources
                                import pkg_resources
                                version = pkg_resources.get_distribution("ornexus").version
                                print(f"OrNexus v{version}")
                        else:
                            # Fallback 2: Usar pkg_resources
                            import pkg_resources
                            version = pkg_resources.get_distribution("ornexus").version
                            print(f"OrNexus v{version}")
                    except Exception:
                        # Fallback 3: Usar importlib.metadata
                        try:
                            import importlib.metadata
                            version = importlib.metadata.version("ornexus")
                            print(f"OrNexus v{version}")
                        except Exception:
                            # Fallback 4: Usar a versão do módulo (potencialmente desatualizada)
                            from ornexus import __version__
                            print(f"OrNexus v{__version__}")
            else:
                # Se pip show falhar, tentar outras abordagens
                try:
                    import pkg_resources
                    version = pkg_resources.get_distribution("ornexus").version
                    print(f"OrNexus v{version}")
                except Exception:
                    try:
                        import importlib.metadata
                        version = importlib.metadata.version("ornexus")
                        print(f"OrNexus v{version}")
                    except Exception:
                        from ornexus import __version__
                        print(f"OrNexus v{__version__}")
        except Exception as e:
            # Último recurso: use a versão do módulo com um aviso
            from ornexus import __version__
            print(f"OrNexus v{__version__} (aviso: pode não refletir a versão instalada)")
    
    else:
        parser.print_help()

def init_project():
    """
    Inicializa o projeto OrNexus:
    - Cria diretório knowledge
    """
    # Criar diretório knowledge se não existir
    knowledge_dir = Path("knowledge")
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Diretório {knowledge_dir} criado!")


def show_knowledge_summary():
    """
    Exibe um resumo dos arquivos de conhecimento
    """
    try:
        # 1. Verifique se o diretório knowledge existe
        knowledge_dir = Path("knowledge")
        if not knowledge_dir.exists():
            print(f"❌ Diretório {knowledge_dir} não encontrado!")
            return
            
        # Contador de arquivos de texto na pasta principal
        txt_files = list(knowledge_dir.glob('*.txt'))
        print(f"Encontrados {len(txt_files)} arquivos de texto (.txt) em {knowledge_dir}")
        
    except Exception as e:
        print(f"Erro ao exibir resumo dos arquivos de conhecimento: {e}") 

def deploy_api_structure(project_path=None, force=True):
    """
    Cria a estrutura de API completa para um projeto executando o script
    install_api_structure.sh na pasta do projeto
    
    Args:
        project_path: Caminho para o projeto (opcional, usa diretório atual se não fornecido)
        force: Se True, ignora a verificação de projeto válido (agora True por padrão)
    """
    import subprocess
    import os
    
    # Determinar o caminho do projeto
    if project_path:
        project_dir = Path(project_path)
    else:
        project_dir = Path.cwd()
    
    # Criar o diretório se não existir
    if not project_dir.exists():
        print(f"📁 Criando diretório do projeto: {project_dir}")
        try:
            project_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"❌ Erro ao criar diretório: {e}")
            return False
    
    print(f"📁 Criando estrutura de API em: {project_dir}")
    
    # Verificações para diferentes tipos de projetos (opcional agora)
    is_valid_project = any([
        (project_dir / "knowledge").exists(),  # Verificação para Agno
        (project_dir / "flows").exists(),      # Verificação para CrewAI (flow)
        (project_dir / "crews").exists(),      # Verificação para CrewAI (crew)
        force                                  # Se force=True, sempre é válido
    ])
    
    if not is_valid_project:
        print(f"⚠️ Aviso: Criando API em um diretório que não parece ser um projeto OrNexus reconhecido.")
    
    # Localizar o script install_api_structure.sh no pacote
    package_dir = Path(__file__).parent.absolute()
    script_path = package_dir / "deploy" / "install_api_structure.sh"
    
    if not script_path.exists():
        print(f"❌ Erro: Script de instalação não encontrado.")
        return False
    
    # Garantir que o script tem permissões de execução
    script_path.chmod(0o755)
    
    # Mudar para o diretório do projeto antes de executar o script
    original_dir = os.getcwd()
    os.chdir(project_dir)
    
    try:
        print(f"⚙️ Executando script de instalação...")
        result = subprocess.run(["bash", str(script_path)], check=True)
        
        if result.returncode == 0:
            print(f"✅ Estrutura de API criada com sucesso em {project_dir}")
            return True
        else:
            print(f"❌ Erro ao executar o script de instalação (código: {result.returncode})")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar o script: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    finally:
        # Voltar ao diretório original
        os.chdir(original_dir) 