import streamlit as st
import pandas as pd # ✅ Importação necessária para o Dashboard
import matplotlib.pyplot as plt
import plotly.express as px
import json
import os
from datetime import datetime

# Configuração inicial do Dashboard
st.set_page_config(page_title="DYL - Dash Your Life", layout="wide")

# Caminho do arquivo JSON
DATA_FILE = "dashboard_data.json"

def carregar_dados():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"projetos": {}, "tarefas_diarias": {}, "configuracoes": {
        "lembretes_ativos": False,
        "modo_lembrete": "Texto",
        "resumo_diario": True,
        "resumo_semanal": True,
        "resumo_mensal": True
    }}

def salvar_dados():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Carregar dados do JSON
data = carregar_dados()

# Garante que a chave "agendamentos" existe
if "agendamentos" not in data:
    data["agendamentos"] = []


def mudar_pagina(pagina, projeto=None, tarefa=None):
    st.session_state["pagina"] = pagina
    if projeto is not None:
        st.session_state["projeto_selecionado"] = projeto
    if tarefa is not None:
        st.session_state["tarefa_selecionada"] = tarefa
    st.rerun()


# Estado inicial das páginas
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "inicio"
    st.session_state["projeto_selecionado"] = None
    st.session_state["tarefa_selecionada"] = None

pagina_atual = st.session_state["pagina"]


if pagina_atual == "inicio" and data["configuracoes"].get("lembretes_ativos", False):
    from datetime import datetime

    agora = datetime.now()
    dia_atual = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"][agora.weekday()]
    hora_atual = agora.strftime("%H:%M")

    lembretes_do_dia = []

    # Tarefas Diárias
    for tarefa, agendamentos in data.get("tarefas_diarias", {}).items():
        for agendamento in agendamentos:
         dias = agendamento.get("dias", [])
         if dia_atual in dias:
          lembretes_do_dia.append(("diaria", tarefa, agendamento.get("horario", "Sem horário")))

    # Tarefas de Projetos
    for projeto_nome, projeto_info in data.get("projetos", {}).items():
        for etapa_nome, etapa_info in projeto_info.get("etapas", {}).items():
            for tarefa_nome, detalhes in etapa_info.get("tarefas", {}).items():
                if detalhes.get("data_limite") == agora.strftime("%Y-%m-%d"):
                    lembretes_do_dia.append(("projeto", tarefa_nome, projeto_nome))

    if lembretes_do_dia:
        st.markdown("### ⏰ **Lembretes para hoje**")
        for tipo, nome, info in lembretes_do_dia:
            modo = data["configuracoes"].get("modo_lembrete", "Texto")
            if tipo == "diaria":
                if modo == "Texto":
                    st.info(f"📌 Tarefa diária: **{nome}** às **{info}**")
                else:
                    st.success(f"🤖 Senhor, às {info} está agendada a tarefa diária: {nome}")
            else:
                st.warning(f"📌 Tarefa do Projeto **{info}**: {nome} (vencendo hoje!)")


if pagina_atual == "inicio":
    st.title("Dash your Life - O que você deseja fazer agora?")

    # Estilos para os botões coloridos
    st.markdown("""
    <style>
    .botao-amarelo button {
        background-color: #FFD700 !important;
        color: black !important;
        font-weight: bold;
        border-radius: 8px;
    }
    .botao-vermelho button {
        background-color: #FF6961 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
    }
    .botao-azul button {
        background-color: #87CEEB !important;
        color: black !important;
        font-weight: bold;
        border-radius: 8px;
    }
    .botao-cinza button {
        background-color: #D3D3D3 !important;
        color: black !important;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    lembretes_ativos = data["configuracoes"].get("lembretes_ativos", False)

    # =====================
    # 🟨 Projetos
    # =====================
    st.subheader("📁 Projetos")
    if st.button("Criar novo projeto", key="btn_proj_criar"):
        mudar_pagina("inserir_projeto")

    with st.container():
        st.markdown('<div class="botao-amarelo">', unsafe_allow_html=True)
        if st.button("Projetos Criados", key="btn_proj_lista"):
            mudar_pagina("lista_projetos")
        st.markdown('</div>', unsafe_allow_html=True)
    # 📊 Novo botão de Dashboard
    with st.container():
     st.markdown('<div class="botao-amarelo">', unsafe_allow_html=True)
    if st.button("📊 Dashboard dos Projetos", key="btn_dashboard_proj"):
        mudar_pagina("dashboard_projetos")
    st.markdown('</div>', unsafe_allow_html=True)    

    st.markdown("---")

    # =====================
    # 🟥 Agendamentos
    # =====================
    st.subheader("📅 Agendamentos")
    with st.container():
        st.markdown('<div class="botao-vermelho">', unsafe_allow_html=True)
        if st.button("Adicionar Agendamento", key="btn_ag_criar"):
            mudar_pagina("inserir_agendamento")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="botao-vermelho">', unsafe_allow_html=True)
        if st.button("Compromissos Agendados", key="btn_ag_lista"):
            mudar_pagina("lista_agendamentos")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # =====================
    # 🟦 Tarefas Diárias
    # =====================
    st.subheader("🔁 Tarefas Diárias")
    with st.container():
        st.markdown('<div class="botao-azul">', unsafe_allow_html=True)
        if st.button("Adicionar Tarefa Diária", key="btn_td_criar"):
            mudar_pagina("inserir_tarefa_diaria")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="botao-azul">', unsafe_allow_html=True)
        if st.button("Tarefas Diárias", key="btn_td_lista"):
            mudar_pagina("lista_tarefas_diarias")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # =====================
    # ⚙️ Lembretes
    # =====================
    st.subheader("🔔 Lembretes")
    with st.container():
        if st.button("🔔 Lembretes: Ligado" if lembretes_ativos else "🔕 Lembretes: Desligado", key="btn_lembretes_toggle"):
            data["configuracoes"]["lembretes_ativos"] = not lembretes_ativos
            salvar_dados()
            mudar_pagina("inicio")

        if st.button("⚙️ Configuração de Lembretes", key="btn_config_lembretes"):
            mudar_pagina("config_lembretes")
                
        if st.button("📆 Agendamentos da Semana", key="btn_semana"):
            mudar_pagina("lembretes_semana")
        
        if st.button("🌙 Agendamentos do Mês", key="btn_mes"):
            mudar_pagina("lembretes_mes")
    



elif pagina_atual == "inserir_projeto":
    st.title("Adicionar/Editar Projeto")

    nome_projeto = st.session_state.get("projeto_selecionado", "")
    nome_projeto = st.text_input("Nome do Projeto", nome_projeto)

    if nome_projeto not in data["projetos"]:
        data_inicio = st.date_input("Data de Início do Projeto")
        data_fim = st.date_input("Data de Término do Projeto")

        if st.button("Salvar Projeto"):
            data["projetos"][nome_projeto] = {
                "data_inicio": str(data_inicio),
                "data_fim": str(data_fim),
                "etapas": {}
            }
            salvar_dados()
            mudar_pagina("inserir_etapa", projeto=nome_projeto)
    else:
        mudar_pagina("inserir_etapa", projeto=nome_projeto)

elif pagina_atual == "inserir_etapa":
    nome_projeto = st.session_state.get("projeto_selecionado")
    st.title(f"Projeto: {nome_projeto}")

    etapas = data["projetos"][nome_projeto].get("etapas", {})

    # 🔄 Resetar campo da etapa se necessário (antes do text_input!)
    if "reset_etapa" in st.query_params:
        st.query_params.clear()
        st.session_state["nova_etapa"] = ""

    # 🧾 Campo de texto da etapa
    nova_etapa = st.text_input("Nome da Etapa", key="nova_etapa")

    # 💾 Botão de salvar etapa
    if st.button("Salvar Etapa") and nova_etapa:
        if nova_etapa not in etapas:
            etapas[nova_etapa] = {"tarefas": {}}
            data["projetos"][nome_projeto]["etapas"] = etapas
            salvar_dados()
            st.success("Etapa adicionada")
            st.query_params["reset_etapa"] = "true"
            st.rerun()

    # 📚 Mostrar etapas já cadastradas
    if etapas:
        st.markdown("### Etapas cadastradas:")
        for etapa in etapas:
            st.markdown(f"- {etapa}")

    # ➡️ Avançar para tarefas
    if st.button("Criar Tarefa"):
        mudar_pagina("inserir_tarefa", projeto=nome_projeto)

    # 🔙 Voltar ao início
    if st.button("Início", key="inicio_projeto"):
     mudar_pagina("inicio") #teladeetapas
 
        
elif pagina_atual == "inserir_tarefa":
    nome_projeto = st.session_state.get("projeto_selecionado")
    st.title(f"Tarefas do Projeto: {nome_projeto}")

    etapas = data["projetos"][nome_projeto].get("etapas", {})
    data_fim_projeto = datetime.strptime(data["projetos"][nome_projeto]["data_fim"], "%Y-%m-%d").date()

    # ⏮ Resetar antes de renderizar o campo
    if "reset_tarefa" in st.query_params:
        st.query_params.clear()
        st.session_state["nova_tarefa"] = ""

    # 🧾 Campo de entrada (dentro de form para evitar múltiplos botões)
    with st.form("form_tarefa"):
        nome_tarefa = st.text_input("Nome da Tarefa", key="nova_tarefa")
        etapa_selecionada = st.selectbox("Selecionar Etapa", list(etapas.keys()), key="etapa_tarefa")
        data_limite = st.date_input("Data limite da tarefa")
        status = st.selectbox("Situação da tarefa", ["Não iniciado", "Em andamento", "OK"])
        submit = st.form_submit_button("Salvar Tarefa")

        if submit:
            if data_limite > data_fim_projeto:
                st.error("A data limite da tarefa não pode ultrapassar a data de término do projeto!")
            elif nome_tarefa.strip() == "":
                st.warning("O nome da tarefa não pode estar vazio!")
            else:
                etapas[etapa_selecionada]["tarefas"][nome_tarefa] = {
                    "data_limite": str(data_limite),
                    "status": status
                }
                data["projetos"][nome_projeto]["etapas"] = etapas
                salvar_dados()
                st.success("Tarefa salva com sucesso!")
                st.query_params["reset_tarefa"] = "true"
                st.rerun()

    # Botões finais
    if st.button("Estruturar Projeto"):
        mudar_pagina("estrutura_projeto", projeto=nome_projeto)

    if st.button("Início", key="inicio_tarefa"):
     mudar_pagina("inicio")  #botãodastarefas

# PÁGINA: Detalhes do Projeto (estrutura em árvore)
elif pagina_atual == "detalhes_projeto":
    nome_projeto = st.session_state.get("projeto_selecionado")
    if not nome_projeto or nome_projeto not in data["projetos"]:
        st.warning("Projeto não encontrado.")
        st.stop()

    st.title(f"📁 Estrutura do Projeto: {nome_projeto}")
    projeto = data["projetos"][nome_projeto]

    etapas = projeto.get("etapas", {})

    for etapa_nome, etapa_info in etapas.items():
        st.markdown(f"- ├── **{etapa_nome}**")
        tarefas = etapa_info.get("tarefas", {})
        for tarefa_nome, detalhes in tarefas.items():
            if isinstance(detalhes, dict):
                status = detalhes.get("status", "Não iniciado")
                data_limite = detalhes.get("data_limite", "Sem data")
            else:
                status = detalhes
                data_limite = "Sem data"

            if st.button(f"📌 {tarefa_nome} — 🕓 {data_limite} — *{status}*", key=f"tarefa_{etapa_nome}_{tarefa_nome}"):
                st.session_state["tarefa_selecionada"] = tarefa_nome
                mudar_pagina("inserir_tarefa", projeto=nome_projeto)

    st.markdown("---")
    if st.button("Editar Projeto", key="editar_detalhes_projeto"):
        mudar_pagina("inserir_projeto", projeto=nome_projeto)

    if st.button("Excluir Projeto", key="excluir_detalhes_projeto"):
        del data["projetos"][nome_projeto]
        salvar_dados()
        mudar_pagina("lista_projetos")

    if st.button("🏠 Voltar ao Início", key="inicio_detalhes_projeto"):
        mudar_pagina("inicio")

# ============================
# 🗂️  PÁGINAS DE TAREFAS DIÁRIAS
# ============================

elif pagina_atual == "inserir_tarefa_diaria":
    st.title("Adicionar/Editar Tarefa Diária")

    nome_tarefa = st.text_input("Nome da Tarefa Diária", key="nome_tarefa_diaria")
    dias_semana = st.multiselect("Dias da Semana", ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"], key="dias_tarefa_diaria")
    horario = st.time_input("Horário da Tarefa", key="horario_tarefa_diaria")

    if st.button("Salvar Agendamento"):
        if nome_tarefa and dias_semana:
            if nome_tarefa not in data["tarefas_diarias"]:
                data["tarefas_diarias"][nome_tarefa] = []

            for dia in dias_semana:
                novo = {
                    "dias": [dia],  # manter como lista
                    "horario": horario.strftime("%H:%M")
                }
                if not any(
                    isinstance(ag, dict) and
                    ag.get("dias") == novo["dias"] and
                    ag.get("horario") == novo["horario"]
                    for ag in data["tarefas_diarias"][nome_tarefa]
                ):
                    data["tarefas_diarias"][nome_tarefa].append(novo)

            salvar_dados()
            st.success("✅ Agendamento salvo com sucesso!")
            mudar_pagina("lista_tarefas_diarias")
        else:
            st.warning("⚠️ Informe o nome da tarefa e selecione ao menos um dia.")

    if st.button("Início", key="inicio_tarefa_diaria"):
        mudar_pagina("inicio")


# PÁGINA: Lista de Tarefas Diárias
elif pagina_atual == "lista_tarefas_diarias":
    st.title("Tarefas Diárias Cadastradas")

    for tarefa, agendamentos in list(data["tarefas_diarias"].items()):
        st.subheader(f"📌 {tarefa}")

        if isinstance(agendamentos, list):
            for idx, agendamento in enumerate(agendamentos):
                if isinstance(agendamento, dict) and "dias" in agendamento and "horario" in agendamento:
                    dias = ", ".join(agendamento["dias"])
                    horario = agendamento["horario"]

                    col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
                    with col1:
                        st.write(f"- Dias: {dias} | Horário: {horario}")
                    with col2:
                        if st.button("✏️", key=f"edit_{tarefa}_{idx}"):
                            st.session_state["tarefa_editando"] = tarefa
                            st.session_state["idx_editando"] = idx
                            st.session_state["dias_editando"] = agendamento["dias"]
                            st.session_state["horario_editando"] = agendamento["horario"]
                            mudar_pagina("editar_tarefa_diaria")
                    with col3:
                        if st.button("❌", key=f"del_{tarefa}_{idx}"):
                            data["tarefas_diarias"][tarefa].pop(idx)
                            if not data["tarefas_diarias"][tarefa]:
                                del data["tarefas_diarias"][tarefa]
                            salvar_dados()
                            st.rerun()
                else:
                    st.warning(f"⚠️ Agendamento com formato inválido: {agendamento}")
        else:
            st.warning(f"⚠️ Esta tarefa está com estrutura incorreta: {agendamentos}")

    if st.button("Início", key="inicio_lista_tarefas_diarias"):
        mudar_pagina("inicio")
        


# PÁGINA: Inserir Agendamento Comum
elif pagina_atual == "inserir_agendamento":
    st.title("📅 Adicionar Agendamento Comum")

    titulo = st.text_input("Título do Agendamento")
    data_agendada = st.date_input("Data")
    hora_agendada = st.time_input("Horário")

    if st.button("Salvar Agendamento"):
        if titulo:
            data["agendamentos"].append({
                "titulo": titulo,
                "data": str(data_agendada),
                "hora": hora_agendada.strftime("%H:%M")
            })
            salvar_dados()
            st.success(f"✅ Agendamento salvo: {titulo} em {data_agendada} às {hora_agendada.strftime('%H:%M')}")
        else:
            st.warning("⚠️ Informe um título para o agendamento.")

    if st.button("Início", key="inicio_agendamento"):
        mudar_pagina("inicio")

# PÁGINA: Lista de Agendamentos
elif pagina_atual == "lista_agendamentos":
    st.title("📅 Agendamentos Salvos")

    if not data["agendamentos"]:
        st.info("Nenhum agendamento foi cadastrado ainda.")
    else:
        for idx, item in enumerate(data["agendamentos"]):
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                st.write(f"📌 {item['titulo']} — {item['data']} às {item['hora']}")
            with col2:
                if st.button("❌", key=f"excluir_agendamento_{idx}"):
                    del data["agendamentos"][idx]
                    salvar_dados()
                    st.rerun()

    if st.button("Início", key="inicio_lista_agendamentos"):
        mudar_pagina("inicio")

# PÁGINA: Lembretes da Semana
elif pagina_atual == "lembretes_semana":
    st.title("📆 Lembretes da Semana")

    from datetime import datetime, timedelta

    hoje = datetime.now().date()
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
    dias_futuros = [(hoje + timedelta(days=i)) for i in range(7)]
    dias_futuros_str = [d.strftime("%Y-%m-%d") for d in dias_futuros]
    dias_semana_futuros = [dias_semana[d.weekday()] for d in dias_futuros]

    lembretes_semana = {
        "tarefas_diarias": [],
        "agendamentos": [],
        "projetos": []
    }

    # Tarefas Diárias
    for tarefa, agendamentos in data.get("tarefas_diarias", {}).items():
        for ag in agendamentos:
            dias = ag.get("dias", [])
            if any(dia in dias for dia in dias_semana_futuros):
                lembretes_semana["tarefas_diarias"].append(f"{tarefa} — {', '.join(dias)} às {ag['horario']}")

    # Agendamentos comuns
    for ag in data.get("agendamentos", []):
        if ag["data"] in dias_futuros_str:
            lembretes_semana["agendamentos"].append(f"{ag['titulo']} — {ag['data']} às {ag['hora']}")

    # Tarefas de projetos
    for projeto, info in data.get("projetos", {}).items():
        for etapa, etapa_info in info.get("etapas", {}).items():
            for tarefa_nome, detalhes in etapa_info.get("tarefas", {}).items():
                if detalhes.get("data_limite") in dias_futuros_str:
                    lembretes_semana["projetos"].append(f"{tarefa_nome} (Projeto: {projeto}) — até {detalhes['data_limite']}")

    # Exibição
    if not any(lembretes_semana.values()):
        st.info("✅ Nenhum lembrete para os próximos 7 dias.")
    else:
        if lembretes_semana["tarefas_diarias"]:
            st.subheader("🔁 Tarefas Diárias")
            for item in lembretes_semana["tarefas_diarias"]:
                st.markdown(f"- {item}")

        if lembretes_semana["agendamentos"]:
            st.subheader("📅 Agendamentos")
            for item in lembretes_semana["agendamentos"]:
                st.markdown(f"- {item}")

        if lembretes_semana["projetos"]:
            st.subheader("📁 Tarefas de Projetos")
            for item in lembretes_semana["projetos"]:
                st.markdown(f"- {item}")

    if st.button("Início", key="inicio_lembretes_semana"):
        mudar_pagina("inicio")
        

# 🆕 PÁGINA: Lembretes do Mês
elif pagina_atual == "lembretes_mes":
    st.title("🌙 Lembretes do Mês")

    from datetime import datetime, timedelta

    hoje = datetime.now().date()
    fim_mes = (hoje.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    intervalo = [(hoje + timedelta(days=i)) for i in range((fim_mes - hoje).days + 1)]
    datas_mes_str = [d.strftime("%Y-%m-%d") for d in intervalo]
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
    dias_semana_mes = [dias_semana[d.weekday()] for d in intervalo]

    lembretes_mes = {
        "tarefas_diarias": [],
        "agendamentos": [],
        "projetos": []
    }

    # Tarefas Diárias
    for tarefa, agendamentos in data.get("tarefas_diarias", {}).items():
        for ag in agendamentos:
            dias = ag.get("dias", [])
            if any(dia in dias for dia in dias_semana_mes):
                lembretes_mes["tarefas_diarias"].append(f"{tarefa} — {', '.join(dias)} às {ag['horario']}")

    # Agendamentos comuns
    for ag in data.get("agendamentos", []):
        if ag["data"] in datas_mes_str:
            lembretes_mes["agendamentos"].append(f"{ag['titulo']} — {ag['data']} às {ag['hora']}")

    # Tarefas de projetos
    for projeto, info in data.get("projetos", {}).items():
        for etapa, etapa_info in info.get("etapas", {}).items():
            for tarefa_nome, detalhes in etapa_info.get("tarefas", {}).items():
                if detalhes.get("data_limite") in datas_mes_str:
                    lembretes_mes["projetos"].append(f"{tarefa_nome} (Projeto: {projeto}) — até {detalhes['data_limite']}")

    # Exibição
    if not any(lembretes_mes.values()):
        st.info("✅ Nenhum lembrete para o restante do mês.")
    else:
        if lembretes_mes["tarefas_diarias"]:
            st.subheader("🔁 Tarefas Diárias")
            for item in lembretes_mes["tarefas_diarias"]:
                st.markdown(f"- {item}")

        if lembretes_mes["agendamentos"]:
            st.subheader("📅 Agendamentos")
            for item in lembretes_mes["agendamentos"]:
                st.markdown(f"- {item}")

        if lembretes_mes["projetos"]:
            st.subheader("📁 Tarefas de Projetos")
            for item in lembretes_mes["projetos"]:
                st.markdown(f"- {item}")

    if st.button("Início", key="inicio_lembretes_mes"):
        mudar_pagina("inicio")
        


# PÁGINA: Configuração de Lembretes
elif pagina_atual == "config_lembretes":
    st.title("Configurações de Lembretes")

    # Remove seleção de modo (fixo em Texto)
    st.markdown("Modo de Lembrete: **Texto**")

    resumo_diario = st.checkbox("Mostrar resumo diário?", value=data["configuracoes"].get("resumo_diario", True))
    resumo_semanal = st.checkbox("Mostrar resumo semanal nas segundas?", value=data["configuracoes"].get("resumo_semanal", True))
    resumo_mensal = st.checkbox("Mostrar resumo mensal no 1º dia de cada mês?", value=data["configuracoes"].get("resumo_mensal", True))

    if st.button("Salvar Configurações"):
        data["configuracoes"]["modo_lembrete"] = "Texto"
        data["configuracoes"]["resumo_diario"] = resumo_diario
        data["configuracoes"]["resumo_semanal"] = resumo_semanal
        data["configuracoes"]["resumo_mensal"] = resumo_mensal
        salvar_dados()
        st.success("Configurações salvas com sucesso!")

    if st.button("Início"):
        mudar_pagina("inicio")


        

# PÁGINA: Editar Tarefa Diária
elif pagina_atual == "editar_tarefa_diaria":
    st.title("Editar Agendamento da Tarefa Diária")

    tarefa = st.session_state.get("tarefa_editando")
    idx = st.session_state.get("idx_editando")
    dias_orig = st.session_state.get("dias_editando", [])
    horario_orig = st.session_state.get("horario_editando", "00:00")

    dias_novos = st.multiselect("Dias da Semana", ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"], default=dias_orig)
    horario_novo = st.time_input("Horário da Tarefa", value=datetime.strptime(horario_orig, "%H:%M").time())

    if st.button("Salvar Agendamento Editado"):
        data["tarefas_diarias"][tarefa][idx] = {
            "dias": dias_novos,
            "horario": horario_novo.strftime("%H:%M")
        }
        salvar_dados()
        st.success("Agendamento atualizado com sucesso!")
        mudar_pagina("lista_tarefas_diarias")

    if st.button("Cancelar"):
        mudar_pagina("lista_tarefas_diarias")

         

elif pagina_atual == "estrutura_projeto":
    nome_projeto = st.session_state.get("projeto_selecionado")
    st.title(f"📐 Estrutura do Projeto: {nome_projeto}")

    projeto = data["projetos"].get(nome_projeto, {})
    etapas = projeto.get("etapas", {})

    # Botão para editar o projeto
    if st.button(f"📁 Projeto: {nome_projeto}"):
        mudar_pagina("inserir_projeto", projeto=nome_projeto)

    for etapa_nome, etapa_info in etapas.items():
        if st.button(f"📂 Etapa: {etapa_nome}", key=f"etapa_{etapa_nome}"):
            mudar_pagina("inserir_etapa", projeto=nome_projeto)

        for tarefa_nome, tarefa_detalhes in etapa_info.get("tarefas", {}).items():
            if isinstance(tarefa_detalhes, dict):
                data_limite = tarefa_detalhes.get("data_limite", "Sem data")
                status = tarefa_detalhes.get("status", "Não iniciado")
            else:
                data_limite = "Sem data"
                status = tarefa_detalhes

            if st.button(f"📌 {tarefa_nome} — 🕓 {data_limite} — *{status}*", key=f"tarefa_{etapa_nome}_{tarefa_nome}"):
                st.session_state["etapa_selecionada"] = etapa_nome
                mudar_pagina("inserir_tarefa", projeto=nome_projeto)

    st.markdown("---")
    if st.button("🏠 Voltar ao Início"):
        mudar_pagina("inicio") #botãoestrutura 



elif pagina_atual == "lista_projetos":
    st.title("Projetos Criados")

    projetos_ordenados = sorted(data["projetos"].keys())

    for projeto in projetos_ordenados:
        col1, col2, col3 = st.columns([0.7, 0.15, 0.15])

        with col1:
            if st.button(f"📁 {projeto}", key=f"abrir_{projeto}"):
                st.session_state["projeto_selecionado"] = projeto
                mudar_pagina("detalhes_projeto")

        with col2:
            if st.button("✏️ Editar", key=f"editar_{projeto}"):
                mudar_pagina("inserir_projeto", projeto=projeto)

        with col3:
            if st.button("❌ Excluir", key=f"excluir_{projeto}"):
                del data["projetos"][projeto]
                salvar_dados()
                st.rerun()

    st.markdown("---")
    if st.button("Início", key="inicio_lista_projetos"):
     mudar_pagina("inicio")#botãoprojetoscriados
     
     
elif pagina_atual == "dashboard_projetos":
    st.title("📊 Dashboard dos Projetos")

    # Simula extração dos dados do JSON real
    linhas = []
    for projeto, info in data.get("projetos", {}).items():
        for etapa, detalhes in info.get("etapas", {}).items():
            for tarefa, t_info in detalhes.get("tarefas", {}).items():
                linhas.append({
                    "Projeto": projeto,
                    "Etapa": etapa,
                    "Tarefa": tarefa,
                    "Data Limite": t_info.get("data_limite", "Sem data"),
                    "Status": t_info.get("status", "Não iniciado")
                })

    if not linhas:
        st.info("Nenhum dado de projeto para exibir ainda.")
        st.stop()

    df = pd.DataFrame(linhas)
    df["Data Limite"] = pd.to_datetime(df["Data Limite"], errors="coerce")

    tipo_visao = st.selectbox("Escolha o tipo de visualização", ["Planilha", "Gráfico de Pizza", "Linha do Tempo (Gantt)"])

    if tipo_visao == "Planilha":
        df_visao = df.copy()
        df_visao["Urgente"] = df_visao["Data Limite"].apply(
            lambda x: "✅" if pd.isna(x) or x.date() >= datetime.today().date() else "⚠️ Vencida"
        )
        st.dataframe(df_visao)

    elif tipo_visao == "Gráfico de Pizza":
        status_count = df["Status"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(status_count, labels=status_count.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

    elif tipo_visao == "Linha do Tempo (Gantt)":
        df_gantt = df[["Tarefa", "Data Limite", "Status"]].copy()
        df_gantt = df_gantt.dropna(subset=["Data Limite"])
        df_gantt["Início"] = df_gantt["Data Limite"] - pd.Timedelta(days=2)
        fig = px.timeline(
            df_gantt,
            x_start="Início",
            x_end="Data Limite",
            y="Tarefa",
            color="Status",
            title="Tarefas por Prazo"
        )
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    if st.button("Início"):
        mudar_pagina("inicio")
     
 


        
        
