# ORQUESTRADOR
Threat Intelligence Orchestrator for collecting, correlating, and scoring external security indicators (OSINT, breaches, attack surface) with reporting and MISP/OpenCTI integration.
# Threat Intelligence Orchestrator

Pipeline de Threat Intelligence desenvolvido para coletar, correlacionar, enriquecer e classificar indicadores externos relacionados à superfície de exposição de uma organização.

---

## Visão Geral

A maioria dos ataques cibernéticos não começa dentro da organização.

Credenciais comprometidas, ativos expostos e dados vazados podem circular em fontes externas por longos períodos antes de serem explorados.

Este projeto tem como objetivo fornecer visibilidade sobre esses sinais iniciais, permitindo antecipação de riscos e apoio a decisões de segurança.

---

## Funcionalidades

- Coleta de dados externos (OSINT e fontes de vazamento)
- Normalização de indicadores em modelo padronizado
- Classificação de risco (confidence e severity)
- Deduplicação e correlação de dados
- Geração de relatórios em múltiplos formatos (JSON, CSV, HTML)
- Preparado para integração com plataformas de Threat Intelligence

---

## Arquitetura

Targets → Connectors → Indicators → Scoring → Deduplicação → Relatórios → Exportação

---

## Estrutura do Projeto

.
├── main.py  
├── models.py  
├── scoring.py  
├── utils.py  
├── report.py  
├── config.yaml  
├── targets.txt  
├── requirements.txt  
└── README.md  

---

## Execução

### Instalar dependências

pip install -r requirements.txt

### Definir alvos

Editar o arquivo targets.txt com os domínios, e-mails ou IPs que deseja analisar.

Exemplo:

example.com  
usuario@example.com  

### Executar

python main.py --targets targets.txt

---

## Saídas Geradas

Após a execução, os arquivos serão gerados em:

outputs/latest/

Incluindo:

- findings.json  
- findings.csv  
- report.html  
- summary.json  

---

## Casos de Uso

- Monitoramento de exposição de credenciais  
- Análise de superfície de ataque externa  
- Suporte a atividades de Threat Hunting  
- Enriquecimento de dados para SOC  
- Identificação antecipada de riscos  

---

## Conectores Suportados

- theHarvester  
- Holehe  
- SpiderFoot  
- DeHashed (requer API Key)  

---

## Integrações

- MISP  
- OpenCTI  

---

## Requisitos

- Python 3.10 ou superior  
- Ferramentas externas instaladas conforme conectores utilizados  
- Variáveis de ambiente configuradas para integrações  

---

## Melhorias Futuras

- Monitoramento em tempo real  
- Integração com SIEM (Wazuh, Sentinel)  
- Detecção de anomalias com Machine Learning  
- Dashboard interativo  

---

## Autor

Ubirajara Prado  
Cybersecurity | Threat Intelligence | Cloud | DevSecOps
