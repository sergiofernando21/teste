#!/usr/bin/env python3
import json
import os
import sys
from dataclasses import dataclass
from typing import List, Dict
from urllib import request, error


API = "https://api.github.com"


@dataclass
class BacklogItem:
    code: str
    title: str
    issue_type: str
    feature: str
    sprint: int
    sp: int
    hours: str
    status: str
    dependencies: List[str]
    objective: str
    value: str
    scope: List[str]
    acceptance: List[str]
    technical_notes: List[str]

    def full_title(self) -> str:
        return f"[{self.code}] {self.title}"


def build_items() -> List[BacklogItem]:
    common_notes = [
        "Frontend em React Native para fluxo do totem e entrega visual do bilhete.",
        "Backend em Python MVC com APIs REST para compra, confirmação e validação.",
        "Persistência em MySQL 8 com modelagem física aderente ao MVP.",
        "Cobrir testes unitários e integrados relevantes para o card.",
    ]

    return [
        BacklogItem("SETUP-01", "Configurar repositório", "setup", "atendimento-inicial", 1, 2, "6h", "ready", ["Sem dependências"],
                    "Como equipe de desenvolvimento, quero estruturar o repositório para iniciar o MVP com padrão único de trabalho.",
                    "Viabiliza colaboração, versionamento e base mínima para os próximos cards.",
                    ["Criar estrutura inicial de diretórios frontend/backend/database.", "Definir README inicial com convenções.", "Configurar templates básicos de issue e pull request."],
                    ["Repositório contém estrutura inicial versionada.", "README com instruções mínimas de execução e contribuição.", "Templates básicos de trabalho disponíveis."],
                    common_notes + ["Incluir revisão de documentação inicial."]),
        BacklogItem("DB-01", "Implantar modelo físico de banco de dados", "database", "atendimento-inicial", 1, 3, "12h", "ready", ["Depende de [ARCH-01] Definir arquitetura do MVP"],
                    "Como equipe técnica, queremos implantar o modelo físico no MySQL 8 para suportar pedidos, bilhetes e validações.",
                    "Cria base de dados consistente para o ciclo completo de compra e uso único do bilhete.",
                    ["Modelar tabelas de atendimento, pedido, pagamento, bilhete e validação.", "Criar scripts DDL e constraints.", "Configurar índices essenciais para consultas críticas."],
                    ["Scripts DDL executam sem erro no MySQL 8.", "Relacionamentos e constraints refletem regras do MVP.", "Modelo cobre uso único e histórico de tentativa de validação."],
                    common_notes + ["Avaliar necessidade de trigger para baixa automática de uso único."]),
        BacklogItem("ARCH-01", "Definir arquitetura do MVP", "architecture", "atendimento-inicial", 1, 2, "8h", "ready", ["Sem dependências"],
                    "Como equipe técnica, queremos definir arquitetura simples do MVP para orientar implementação frontend, backend e banco.",
                    "Reduz ambiguidades e acelera execução das histórias funcionais.",
                    ["Descrever módulos frontend React Native e backend Python MVC.", "Definir contratos iniciais de APIs REST.", "Definir estratégia de persistência MySQL 8 e fluxo de validação."],
                    ["Documento arquitetural publicado no repositório.", "Fluxos principais mapeados: compra Pix, emissão e validação.", "Responsabilidades de cada camada claras."],
                    common_notes + ["Sem mensageria, eventos ou componentes avançados fora do escopo."]),
        BacklogItem("US1.1", "Iniciar atendimento no totem", "user-story", "atendimento-inicial", 1, 2, "6h", "ready", ["Depende de [SETUP-01] Configurar repositório"],
                    "Como passageiro, quero iniciar o atendimento no totem para começar a compra do bilhete.",
                    "Dá início ao fluxo de autoatendimento sem apoio humano.",
                    ["Exibir tela inicial com botão de início.", "Criar estado de sessão de atendimento."],
                    ["Usuário consegue iniciar atendimento com um toque.", "Sessão é registrada com timestamp de início."],
                    common_notes),
        BacklogItem("US1.2", "Acessar a opção de compra do bilhete", "user-story", "atendimento-inicial", 1, 2, "6h", "ready", ["Depende de [US1.1] Iniciar atendimento no totem"],
                    "Como passageiro, quero acessar a opção de compra para seguir no fluxo do MVP.",
                    "Conecta atendimento inicial ao processo de compra unitária.",
                    ["Exibir opção de compra unitária.", "Direcionar para etapa de criação de pedido."],
                    ["Opção de compra aparece de forma destacada.", "Ao tocar, usuário avança para tela de compra."],
                    common_notes),
        BacklogItem("US1.3", "Utilizar interface adequada para toque", "user-story", "atendimento-inicial", 1, 3, "12h", "ready", ["Depende de [US1.1] Iniciar atendimento no totem"],
                    "Como passageiro, quero uma interface adequada para toque para concluir o processo sem erro operacional.",
                    "Melhora usabilidade no totem físico e reduz abandono.",
                    ["Aplicar componentes com área de toque adequada.", "Garantir contraste e legibilidade.", "Validar navegação sem teclado físico."],
                    ["Botões possuem tamanho mínimo para interação confortável.", "Fluxo principal é navegável apenas por toque.", "Textos críticos permanecem legíveis no display do totem."],
                    common_notes + ["Executar testes de usabilidade básicos do fluxo principal."]),
        BacklogItem("US1.4", "Registrar a abertura do atendimento", "user-story", "atendimento-inicial", 1, 2, "7h", "ready", ["Depende de [DB-01] Implantar modelo físico de banco de dados"],
                    "Como operação, quero registrar a abertura de atendimento para rastreabilidade e auditoria mínima.",
                    "Permite observar volume de uso e investigar falhas por sessão.",
                    ["Persistir evento de abertura de atendimento.", "Associar identificador da sessão ao fluxo."],
                    ["Cada atendimento iniciado gera registro único no banco.", "Dados de abertura podem ser consultados por API interna."],
                    common_notes),
        BacklogItem("US2.1", "Criar pedido de compra", "user-story", "compra-pix", 2, 3, "12h", "backlog", ["Depende da conclusão da Feature 1"],
                    "Como passageiro, quero criar um pedido para iniciar o pagamento do bilhete unitário.",
                    "Materializa a intenção de compra com dados rastreáveis.",
                    ["Criar endpoint para abertura de pedido.", "Persistir valor e status inicial do pedido.", "Vincular pedido à sessão de atendimento."],
                    ["Pedido é criado com status pendente.", "Pedido possui identificador único.", "Pedido referencia sessão válida."],
                    common_notes),
        BacklogItem("US2.2", "Gerar QR Code Pix para pagamento", "user-story", "compra-pix", 2, 5, "20h", "backlog", ["Depende de [US2.1] Criar pedido de compra"],
                    "Como passageiro, quero receber um QR Code Pix para pagar o bilhete.",
                    "Habilita pagamento digital no canal definido pelo MVP.",
                    ["Integrar serviço de geração de cobrança Pix.", "Exibir QR Code no totem.", "Persistir txid e dados de cobrança."],
                    ["QR Code válido é exibido após criação do pedido.", "Dados de cobrança ficam associados ao pedido.", "Erros de geração apresentam mensagem de contingência."],
                    common_notes + ["API REST deve abstrair provedor Pix para facilitar testes integrados."]),
        BacklogItem("US2.3", "Acompanhar o status do pagamento", "user-story", "compra-pix", 2, 5, "18h", "backlog", ["Depende de [US2.2] Gerar QR Code Pix para pagamento"],
                    "Como passageiro, quero que o totem acompanhe o pagamento para saber quando a compra foi confirmada.",
                    "Evita incerteza no atendimento e permite avançar para emissão do bilhete.",
                    ["Implementar consulta periódica do status da cobrança.", "Atualizar status do pedido no backend.", "Refletir estado na UI do totem."],
                    ["Pedido transita entre pendente, pago, expirado ou falha.", "Totem exibe estado atual sem recarga manual.", "Mudança para pago dispara próximo passo do fluxo."],
                    common_notes),
        BacklogItem("US2.4", "Encerrar corretamente a compra em estados finais", "user-story", "compra-pix", 2, 3, "10h", "backlog", ["Depende de [US2.3] Acompanhar o status do pagamento"],
                    "Como operação, quero encerrar a compra corretamente para evitar sessões presas.",
                    "Garante consistência do fluxo de compra e retorno previsível ao usuário.",
                    ["Tratar finalização para pago, expirado e cancelado.", "Registrar motivo de encerramento.", "Encaminhar fluxo para emissão apenas quando pago."],
                    ["Estados finais não permitem transições inválidas.", "Sessão é finalizada com motivo auditável.", "Fluxo pago segue para emissão de bilhete."],
                    common_notes),
        BacklogItem("US3.1", "Gerar bilhete eletrônico após pagamento confirmado", "user-story", "entrega-bilhete", 3, 3, "12h", "backlog", ["Depende da conclusão da Feature 2"],
                    "Como passageiro, quero que o bilhete eletrônico seja gerado após pagamento confirmado.",
                    "Converte transação financeira em direito de acesso.",
                    ["Criar entidade de bilhete com identificador único.", "Associar bilhete ao pedido pago.", "Gerar dados para QR Code do bilhete."],
                    ["Bilhete só é gerado para pedido pago.", "Bilhete contém status inicial não utilizado.", "Dados de bilhete ficam disponíveis para entrega."],
                    common_notes),
        BacklogItem("US3.2", "Exibir o bilhete no totem para captura", "user-story", "entrega-bilhete", 3, 2, "8h", "backlog", ["Depende de [US3.1] Gerar bilhete eletrônico após pagamento confirmado"],
                    "Como passageiro, quero visualizar o bilhete no totem para capturá-lo rapidamente.",
                    "Permite uso imediato do bilhete sem etapas extras.",
                    ["Renderizar QR Code do bilhete na tela do totem.", "Exibir instruções curtas de captura."],
                    ["Bilhete aparece na tela após geração.", "QR Code possui contraste e dimensão adequados para captura."],
                    common_notes),
        BacklogItem("US3.3", "Abrir o bilhete no navegador do celular", "user-story", "entrega-bilhete", 3, 3, "10h", "backlog", ["Depende de [US3.1] Gerar bilhete eletrônico após pagamento confirmado"],
                    "Como passageiro, quero abrir uma página web do bilhete no celular.",
                    "Entrega alternativa para consulta e uso do bilhete fora do totem.",
                    ["Gerar URL pública segura do bilhete.", "Exibir URL/QR para abertura no celular.", "Servir página responsiva com dados do bilhete."],
                    ["Página do bilhete abre em navegador móvel.", "Conteúdo inclui QR Code e status do bilhete.", "URL identifica bilhete válido."],
                    common_notes + ["Aplicar testes integrados entre API de bilhete e página web." ]),
        BacklogItem("US3.4", "Baixar a imagem do bilhete", "user-story", "entrega-bilhete", 3, 2, "7h", "backlog", ["Depende de [US3.3] Abrir o bilhete no navegador do celular"],
                    "Como passageiro, quero baixar a imagem do bilhete para acesso rápido offline.",
                    "Reduz fricção no uso do bilhete em áreas com conexão instável.",
                    ["Adicionar ação de download na página do bilhete.", "Gerar arquivo de imagem com QR Code legível."],
                    ["Usuário consegue baixar imagem no celular.", "Imagem baixada mantém legibilidade para leitura no acesso."],
                    common_notes),
        BacklogItem("US3.5", "Enviar o bilhete para outra pessoa", "user-story", "entrega-bilhete", 3, 2, "7h", "backlog", ["Depende de [US3.3] Abrir o bilhete no navegador do celular"],
                    "Como passageiro, quero compartilhar o bilhete para outra pessoa quando necessário.",
                    "Amplia flexibilidade de uso dentro do escopo de bilhete digital único.",
                    ["Adicionar ação de compartilhamento de link do bilhete.", "Registrar evento de compartilhamento para auditoria."],
                    ["Link do bilhete pode ser compartilhado pelo navegador móvel.", "Evento de compartilhamento fica registrado."],
                    common_notes),
        BacklogItem("US4.1", "Validar bilhete por API REST", "user-story", "controle-uso", 3, 5, "20h", "backlog", ["Depende da conclusão da Feature 3"],
                    "Como catraca/validador, quero validar o bilhete por API REST no acesso.",
                    "Permite autorização online no ponto de entrada com regra de uso único.",
                    ["Criar endpoint de validação.", "Verificar existência, status e elegibilidade do bilhete.", "Retornar resposta padronizada para autorizador."],
                    ["API responde em formato consistente para sucesso e falha.", "Bilhete inexistente ou inválido retorna negativa.", "Bilhete válido retorna autorização."],
                    common_notes + ["Cobrir testes unitários do domínio de validação." ]),
        BacklogItem("US4.2", "Registrar tentativa de validação do bilhete", "user-story", "controle-uso", 3, 3, "10h", "backlog", ["Depende de [US4.1] Validar bilhete por API REST"],
                    "Como operação, quero registrar cada tentativa de validação para rastreabilidade.",
                    "Viabiliza auditoria de uso e diagnóstico de incidentes.",
                    ["Persistir logs de tentativa com timestamp e resultado.", "Associar tentativa ao bilhete e ao canal de validação."],
                    ["Toda chamada de validação gera registro.", "Registros distinguem sucesso, recusa e erro técnico."],
                    common_notes),
        BacklogItem("US4.3", "Dar baixa automática no primeiro uso autorizado", "user-story", "controle-uso", 3, 3, "12h", "backlog", ["Depende de [US4.1] Validar bilhete por API REST", "Depende de [US4.2] Registrar tentativa de validação do bilhete"],
                    "Como operação, quero dar baixa automática no primeiro uso autorizado para garantir uso único.",
                    "Impede reutilização indevida do mesmo bilhete.",
                    ["Atualizar status do bilhete para utilizado na primeira autorização.", "Garantir atomicidade da operação de validação e baixa."],
                    ["Primeira validação autorizada marca bilhete como utilizado.", "Validações subsequentes retornam bilhete já utilizado.", "Não há condição de corrida que permita dupla autorização."],
                    common_notes + ["Pode utilizar trigger ou transação no MySQL 8 conforme desenho arquitetural."]),
        BacklogItem("US4.4", "Diferenciar bilhete válido, já utilizado, inválido e erro de comunicação", "user-story", "controle-uso", 3, 2, "8h", "backlog", ["Depende de [US4.1] Validar bilhete por API REST"],
                    "Como validador, quero respostas distintas para cada situação do bilhete.",
                    "Melhora decisão operacional e experiência na catraca.",
                    ["Definir códigos e mensagens de retorno por cenário.", "Padronizar payload de erro de comunicação."],
                    ["API diferencia explicitamente válido, utilizado, inválido e indisponível.", "Documentação de contrato atualizada com exemplos."],
                    common_notes),
        BacklogItem("US5.1", "Exibir mensagens de falha e contingência", "user-story", "excecoes-orientacao", 4, 2, "8h", "backlog", ["Depende da conclusão da Feature 1"],
                    "Como passageiro, quero mensagens claras de falha e contingência para saber como agir.",
                    "Reduz frustração em incidentes e orienta continuidade da jornada.",
                    ["Mapear falhas críticas do fluxo.", "Exibir mensagens objetivas e não técnicas.", "Padronizar tom e linguagem."],
                    ["Cenários de erro exibem orientação correspondente.", "Mensagens são legíveis e compreensíveis no totem."],
                    common_notes),
        BacklogItem("US5.2", "Orientar uso de canais alternativos", "user-story", "excecoes-orientacao", 4, 2, "6h", "backlog", ["Depende de [US5.1] Exibir mensagens de falha e contingência"],
                    "Como passageiro, quero orientação de canais alternativos quando o fluxo não puder prosseguir.",
                    "Mantém atendimento mesmo com indisponibilidade parcial do totem.",
                    ["Exibir orientações de guichê/app/canal oficial definido pelo negócio.", "Vincular orientações aos tipos de falha."],
                    ["Usuário recebe orientação acionável em casos de contingência.", "Mensagens não desviam do escopo do MVP."],
                    common_notes),
        BacklogItem("US5.3", "Retornar o totem ao estado inicial com segurança", "user-story", "excecoes-orientacao", 4, 3, "10h", "backlog", ["Depende de [US1.1] Iniciar atendimento no totem", "Depende de [US2.4] Encerrar corretamente a compra em estados finais"],
                    "Como operação, quero que o totem retorne ao estado inicial com segurança após cada atendimento.",
                    "Evita exposição de dados do usuário seguinte e prepara novo atendimento.",
                    ["Limpar sessão e dados sensíveis ao encerrar fluxo.", "Implementar timeout de inatividade com retorno automático."],
                    ["Após encerramento ou timeout, totem volta para tela inicial.", "Nenhum dado do usuário anterior permanece acessível."],
                    common_notes),
        BacklogItem("TEST-01", "Executar testes integrados finais das features completas", "test", "excecoes-orientacao", 4, 5, "20h", "backlog", ["Depende da conclusão das Features 1, 2, 3 e 4"],
                    "Como equipe de qualidade, quero executar testes integrados finais para validar fluxo ponta a ponta.",
                    "Reduz risco de falha sistêmica antes da demonstração do MVP.",
                    ["Executar cenários integrados de compra, emissão e validação.", "Registrar evidências de resultado."],
                    ["Cenários críticos passam sem bloqueadores.", "Relatório de testes integrados disponível."],
                    common_notes + ["Incluir casos de regressão dos fluxos de exceção."]),
        BacklogItem("TEST-02", "Executar testes de regressão após fechamento das features", "test", "excecoes-orientacao", 4, 3, "12h", "backlog", ["Depende de [TEST-01] Executar testes integrados finais das features completas"],
                    "Como equipe de qualidade, quero executar regressão para garantir estabilidade do MVP.",
                    "Assegura que correções finais não quebraram funcionalidades entregues.",
                    ["Rodar suíte de regressão priorizada.", "Documentar falhas e retestes."],
                    ["Suite de regressão executada com evidências.", "Não restam defeitos críticos abertos para MVP."],
                    common_notes),
        BacklogItem("DOC-01", "Revisar documentação final do MVP", "documentation", "excecoes-orientacao", 4, 2, "8h", "backlog", ["Depende da conclusão das Features 1 a 5"],
                    "Como equipe, queremos revisar a documentação final para transferência de conhecimento.",
                    "Facilita operação, manutenção e avaliação do MVP.",
                    ["Atualizar README técnico e de execução.", "Revisar contratos de API e modelo de dados.", "Consolidar limitações do MVP."],
                    ["Documentação técnica está consistente com implementação.", "Fluxos e endpoints possuem descrição atualizada."],
                    common_notes + ["Revisão de documentação é obrigatória antes da demo."]),
        BacklogItem("UX-01", "Ajustar responsividade e usabilidade final", "frontend", "excecoes-orientacao", 4, 3, "10h", "backlog", ["Depende da conclusão da Feature 3"],
                    "Como passageiro, quero uma interface final responsiva e clara no totem e no celular.",
                    "Melhora qualidade percebida e reduz erros de interação no uso real.",
                    ["Ajustar telas de totem para resolução alvo.", "Ajustar página de bilhete no celular.", "Refinar microtextos e feedbacks visuais."],
                    ["Telas principais se adaptam sem quebrar layout.", "Fluxo no celular mantém legibilidade e ação clara."],
                    common_notes),
        BacklogItem("DEMO-01", "Preparar ambiente de demonstração", "integration", "excecoes-orientacao", 4, 2, "6h", "backlog", ["Depende de [TEST-02] Executar testes de regressão após fechamento das features", "Depende de [DOC-01] Revisar documentação final do MVP"],
                    "Como equipe, queremos preparar ambiente de demonstração para apresentar o MVP funcional.",
                    "Viabiliza avaliação final do produto com roteiro reproduzível.",
                    ["Publicar build estável para demo.", "Configurar banco e backend com dados de teste controlados.", "Preparar roteiro de execução da demonstração."],
                    ["Ambiente de demo sobe sem erro.", "Roteiro reproduz compra, emissão e validação com uso único."],
                    common_notes + ["Executar checklist final antes da apresentação."]),
    ]


def build_body(item: BacklogItem) -> str:
    deps = "\n".join([f"- {d}" for d in item.dependencies])
    scope = "\n".join([f"- {x}" for x in item.scope])
    acceptance = "\n".join([f"- {x}" for x in item.acceptance])
    notes = "\n".join([f"- {x}" for x in item.technical_notes])

    return f"""### História / Objetivo
{item.objective}

### Valor entregue
{item.value}

### Escopo
{scope}

### Critérios de aceite
{acceptance}

### Dependências
{deps}

### Metadados de planejamento
- Feature: {item.feature}
- Sprint: {item.sprint}
- Story Points: {item.sp}
- Estimativa em horas: {item.hours}
- Status inicial: {item.status}

### Observações técnicas
{notes}
"""


def labels_for(item: BacklogItem) -> List[str]:
    labels = [f"type:{item.issue_type}", f"feature:{item.feature}", f"sprint:{item.sprint}", item.status]
    return labels


def api_request(method: str, url: str, token: str, payload: Dict | None = None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if payload is not None:
        req.add_header("Content-Type", "application/json")
    with request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def graphql_request(token: str, query: str, variables: Dict | None = None):
    payload = {"query": query, "variables": variables or {}}
    return api_request("POST", f"{API}/graphql", token, payload)


def ensure_label(owner_repo: str, token: str, label: str):
    name = label
    color = "1d76db"
    if label.startswith("type:"):
        color = "5319e7"
    elif label.startswith("feature:"):
        color = "0e8a16"
    elif label.startswith("sprint:"):
        color = "fbca04"
    elif label in ["ready", "backlog"]:
        color = "0052cc" if label == "ready" else "b60205"
    payload = {"name": name, "color": color, "description": "Criada automaticamente para backlog MVP"}
    try:
        api_request("POST", f"{API}/repos/{owner_repo}/labels", token, payload)
    except error.HTTPError as e:
        if e.code != 422:
            raise


def create_issue(owner_repo: str, token: str, item: BacklogItem):
    payload = {"title": item.full_title(), "body": build_body(item), "labels": labels_for(item)}
    return api_request("POST", f"{API}/repos/{owner_repo}/issues", token, payload)


def load_project_fields(token: str, project_id: str):
    query = """
    query($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          fields(first: 50) {
            nodes {
              ... on ProjectV2FieldCommon { id name dataType }
              ... on ProjectV2SingleSelectField { options { id name } }
            }
          }
        }
      }
    }
    """
    data = graphql_request(token, query, {"projectId": project_id})
    fields = data["data"]["node"]["fields"]["nodes"]
    return {f["name"]: f for f in fields}


def pick_option_id(field: Dict, wanted: str):
    options = field.get("options", [])
    wanted_norm = wanted.strip().lower()
    candidates = [wanted_norm, f"sprint {wanted_norm}"]
    for opt in options:
        name = opt["name"].strip().lower()
        if name in candidates:
            return opt["id"]
    return None


def set_project_field(token: str, project_id: str, item_id: str, field: Dict, value):
    mutation = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: ProjectV2FieldValue!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId,
        itemId: $itemId,
        fieldId: $fieldId,
        value: $value
      }) {
        projectV2Item { id }
      }
    }
    """
    graphql_request(token, mutation, {
        "projectId": project_id,
        "itemId": item_id,
        "fieldId": field["id"],
        "value": value,
    })


def add_issue_to_project(token: str, project_id: str, content_id: str):
    mutation = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
        item { id }
      }
    }
    """
    data = graphql_request(token, mutation, {"projectId": project_id, "contentId": content_id})
    return data["data"]["addProjectV2ItemById"]["item"]["id"]


def fill_project_fields(token: str, project_id: str, project_item_id: str, fields_by_name: Dict, item: BacklogItem):
    mapping = {
        "Feature": item.feature,
        "Sprint": str(item.sprint),
        "Story Points": item.sp,
        "Horas Estimadas": item.hours,
        "Status": item.status,
    }
    for field_name, raw_value in mapping.items():
        field = fields_by_name.get(field_name)
        if not field:
            continue
        data_type = field.get("dataType", "")
        if data_type == "SINGLE_SELECT":
            option_id = pick_option_id(field, str(raw_value))
            if option_id:
                set_project_field(token, project_id, project_item_id, field, {"singleSelectOptionId": option_id})
        elif data_type == "NUMBER":
            if isinstance(raw_value, int):
                number_value = float(raw_value)
            else:
                number_value = float(str(raw_value).split("h")[0])
            set_project_field(token, project_id, project_item_id, field, {"number": number_value})
        elif data_type == "TEXT":
            set_project_field(token, project_id, project_item_id, field, {"text": str(raw_value)})


def main():
    items = build_items()
    if len(items) != 28:
        print("Esperado 28 itens.", file=sys.stderr)
        sys.exit(1)

    if "--dry-run" in sys.argv:
        summary = []
        for idx, item in enumerate(items, start=1):
            summary.append({
                "ordem": idx,
                "titulo": item.full_title(),
                "feature": item.feature,
                "sprint": item.sprint,
                "story_points": item.sp,
                "horas": item.hours,
                "labels": labels_for(item),
                "status": item.status,
            })
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    token = os.getenv("GITHUB_TOKEN")
    owner_repo = os.getenv("GITHUB_REPOSITORY")
    project_id = os.getenv("GITHUB_PROJECT_ID")
    if not token or not owner_repo:
        print("Defina GITHUB_TOKEN e GITHUB_REPOSITORY (owner/repo).", file=sys.stderr)
        sys.exit(2)

    all_labels = set()
    for item in items:
        all_labels.update(labels_for(item))

    for label in sorted(all_labels):
        ensure_label(owner_repo, token, label)

    fields_by_name = load_project_fields(token, project_id) if project_id else {}

    created = []
    for item in items:
        issue = create_issue(owner_repo, token, item)
        if project_id:
            project_item_id = add_issue_to_project(token, project_id, issue["node_id"])
            fill_project_fields(token, project_id, project_item_id, fields_by_name, item)
        created.append({"number": issue["number"], "title": issue["title"], "url": issue["html_url"]})
        print(f"Criada #{issue['number']} - {issue['title']}")

    print(json.dumps(created, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
