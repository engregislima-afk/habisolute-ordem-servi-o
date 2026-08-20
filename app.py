
import os
import io
import re
import smtplib
from email.message import EmailMessage
from datetime import date, datetime
from decimal import Decimal

import pandas as pd
import requests
import streamlit as st
from sqlalchemy import (
    create_engine, Column, Integer, String, Numeric, Date, DateTime,
    ForeignKey, Text, Boolean
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(
    page_title="Habisolute OS",
    page_icon="🧪",
    layout="wide"
)


def aplicar_tema_profissional():
    st.markdown("""
    <style>
    :root {
        --hb-bg: #f6f8fb;
        --hb-card: #ffffff;
        --hb-border: #e6eaf0;
        --hb-text: #1f2937;
        --hb-muted: #6b7280;
        --hb-primary: #f97316;
        --hb-primary-dark: #ea580c;
        --hb-sidebar: #111827;
        --hb-sidebar-muted: #9ca3af;
    }

    /* Página */
    .stApp {
        background: var(--hb-bg);
        color: var(--hb-text);
    }

    /* Remove respiros excessivos */
    .block-container {
        max-width: 1500px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: var(--hb-sidebar);
        border-right: 0;
        min-width: 250px !important;
        max-width: 250px !important;
    }

    section[data-testid="stSidebar"] * {
        color: #f9fafb;
    }

    section[data-testid="stSidebar"] .stRadio label {
        padding: .45rem .6rem;
        border-radius: 8px;
        margin-bottom: .12rem;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,.07);
    }

    section[data-testid="stSidebar"] [data-baseweb="radio"] {
        gap: .55rem;
    }

    /* Cabeçalhos */
    h1, h2, h3, h4 {
        color: var(--hb-text);
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 2rem !important;
        font-weight: 750 !important;
        margin-bottom: .2rem !important;
    }

    h2 {
        font-size: 1.4rem !important;
    }

    /* Cards métricos */
    div[data-testid="stMetric"] {
        background: var(--hb-card);
        border: 1px solid var(--hb-border);
        padding: 1rem 1.1rem;
        border-radius: 12px;
        box-shadow: 0 1px 2px rgba(16,24,40,.04);
    }

    div[data-testid="stMetric"] label {
        color: var(--hb-muted) !important;
        font-size: .82rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.65rem !important;
        color: var(--hb-text);
    }

    /* Inputs */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    textarea {
        border-radius: 8px !important;
    }

    /* Botões */
    .stButton > button,
    .stDownloadButton > button,
    button[kind="primary"] {
        border-radius: 8px !important;
        min-height: 40px;
        font-weight: 650;
        border: 1px solid var(--hb-border);
        box-shadow: none;
    }

    button[kind="primary"] {
        background: var(--hb-primary) !important;
        border-color: var(--hb-primary) !important;
    }

    button[kind="primary"]:hover {
        background: var(--hb-primary-dark) !important;
        border-color: var(--hb-primary-dark) !important;
    }

    /* Tabelas */
    div[data-testid="stDataFrame"] {
        background: var(--hb-card);
        border: 1px solid var(--hb-border);
        border-radius: 12px;
        overflow: hidden;
    }

    /* Expander */
    details {
        background: var(--hb-card);
        border: 1px solid var(--hb-border) !important;
        border-radius: 10px !important;
    }

    /* Alertas */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Separadores */
    hr {
        border-color: var(--hb-border);
    }

    /* Esconde header padrão do Streamlit e reduz ruído visual */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Componentes próprios */
    .hb-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #fff;
        border: 1px solid var(--hb-border);
        border-radius: 12px;
        padding: .85rem 1rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 2px rgba(16,24,40,.03);
    }

    .hb-brand {
        display: flex;
        align-items: center;
        gap: .75rem;
    }

    .hb-brand-badge {
        width: 38px;
        height: 38px;
        display:flex;
        align-items:center;
        justify-content:center;
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 10px;
        font-size: 1.25rem;
    }

    .hb-brand-title {
        font-size: 1rem;
        font-weight: 750;
        color: var(--hb-text);
        line-height: 1.05;
    }

    .hb-brand-sub {
        font-size: .76rem;
        color: var(--hb-muted);
        margin-top: .2rem;
    }

    .hb-chip {
        display:inline-flex;
        align-items:center;
        padding:.32rem .55rem;
        border-radius:999px;
        font-size:.75rem;
        background:#f3f4f6;
        color:#4b5563;
        border:1px solid #e5e7eb;
    }

    .hb-page-head {
        margin-bottom: 1rem;
    }

    .hb-page-title {
        font-size: 1.55rem;
        font-weight: 760;
        color: var(--hb-text);
        margin-bottom: .18rem;
    }

    .hb-page-sub {
        color: var(--hb-muted);
        font-size: .9rem;
    }

    .hb-section {
        background: var(--hb-card);
        border: 1px solid var(--hb-border);
        border-radius: 12px;
        padding: 1rem 1.1rem .5rem 1.1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px rgba(16,24,40,.03);
    }

    .hb-section-title {
        font-size: .95rem;
        font-weight: 750;
        color: var(--hb-text);
        margin-bottom: .15rem;
    }

    .hb-section-sub {
        color: var(--hb-muted);
        font-size: .78rem;
        margin-bottom: .75rem;
    }

    .hb-kpi-label {
        font-size: .75rem;
        color: var(--hb-muted);
        text-transform: uppercase;
        letter-spacing: .04em;
        font-weight: 700;
    }

    .hb-sidebar-logo {
        padding: .7rem .4rem 1rem .4rem;
        margin-bottom: .5rem;
        border-bottom: 1px solid rgba(255,255,255,.09);
    }

    .hb-sidebar-logo .name {
        color: white;
        font-weight: 800;
        font-size: 1.05rem;
    }

    .hb-sidebar-logo .sub {
        color: var(--hb-sidebar-muted);
        font-size: .72rem;
        margin-top: .15rem;
    }
    </style>
    """, unsafe_allow_html=True)

def topo_sistema():
    st.markdown("""
    <div class="hb-topbar">
        <div class="hb-brand">
            <div class="hb-brand-badge">🧪</div>
            <div>
                <div class="hb-brand-title">Habisolute OS</div>
                <div class="hb-brand-sub">Controle tecnológico e faturamento</div>
            </div>
        </div>
        <div class="hb-chip">Sistema operacional</div>
    </div>
    """, unsafe_allow_html=True)

def cabecalho_pagina(titulo, subtitulo):
    st.markdown(
        f"""
        <div class="hb-page-head">
            <div class="hb-page-title">{titulo}</div>
            <div class="hb-page-sub">{subtitulo}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def inicio_secao(titulo, subtitulo=""):
    st.markdown(
        f"""
        <div class="hb-section">
            <div class="hb-section-title">{titulo}</div>
            <div class="hb-section-sub">{subtitulo}</div>
        """,
        unsafe_allow_html=True
    )

def fim_secao():
    st.markdown("</div>", unsafe_allow_html=True)

aplicar_tema_profissional()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///habisolute_os.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# =========================
# MODELOS
# =========================
class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True)
    cnpj = Column(String(18), unique=True, nullable=False)
    razao_social = Column(String(200), nullable=False)
    nome_fantasia = Column(String(200))
    inscricao_estadual = Column(String(50))
    telefone = Column(String(50))
    email = Column(String(200))
    responsavel = Column(String(200))
    cep = Column(String(20))
    logradouro = Column(String(200))
    numero = Column(String(30))
    complemento = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(100))
    uf = Column(String(2))
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.now)

    obras = relationship("Obra", back_populates="cliente")


class Obra(Base):
    __tablename__ = "obras"
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    nome = Column(String(200), nullable=False)
    codigo = Column(String(60))
    cep = Column(String(20))
    logradouro = Column(String(200))
    numero = Column(String(30))
    complemento = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(100))
    uf = Column(String(2))
    responsavel = Column(String(200))
    telefone = Column(String(50))
    email = Column(String(200))
    data_inicio = Column(Date)
    status = Column(String(30), default="Ativa")
    observacoes = Column(Text)

    cliente = relationship("Cliente", back_populates="obras")


class Servico(Base):
    __tablename__ = "servicos"
    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), unique=True, nullable=False)
    categoria = Column(String(100), nullable=False)
    descricao = Column(String(250), nullable=False)
    unidade = Column(String(30), nullable=False)
    valor_padrao = Column(Numeric(12, 2), default=0)
    ativo = Column(Boolean, default=True)


class PrecoCliente(Base):
    __tablename__ = "precos_clientes"
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    obra_id = Column(Integer, ForeignKey("obras.id"), nullable=True)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=False)
    valor = Column(Numeric(12, 2), nullable=False)
    vigencia_inicio = Column(Date)
    vigencia_fim = Column(Date)


class OrdemServico(Base):
    __tablename__ = "ordens_servico"
    id = Column(Integer, primary_key=True)
    numero = Column(String(30), unique=True, nullable=False)
    data = Column(Date, default=date.today)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    obra_id = Column(Integer, ForeignKey("obras.id"), nullable=False)
    solicitante = Column(String(200))
    responsavel_habisolute = Column(String(200))
    solicitacao_cliente = Column(String(100))
    pedido_compra = Column(String(100))
    centro_custo = Column(String(100))
    observacoes = Column(Text)
    status = Column(String(30), default="Aberta")
    criado_em = Column(DateTime, default=datetime.now)


class ItemOS(Base):
    __tablename__ = "itens_os"
    id = Column(Integer, primary_key=True)
    os_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=False)
    quantidade = Column(Numeric(12, 2), nullable=False)
    valor_unitario = Column(Numeric(12, 2), nullable=False)
    descricao_customizada = Column(String(250))


class HistoricoEnvio(Base):
    __tablename__ = "historico_envios"
    id = Column(Integer, primary_key=True)
    os_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=False)
    enviado_em = Column(DateTime, default=datetime.now)
    destinatario = Column(String(250), nullable=False)
    assunto = Column(String(300))
    status = Column(String(50), default="Enviado")
    mensagem_erro = Column(Text)


Base.metadata.create_all(bind=engine)


# =========================
# HELPERS
# =========================
def db():
    return SessionLocal()

def moeda(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def limpar_cnpj(cnpj):
    return re.sub(r"\D", "", cnpj or "")

def formatar_cnpj(cnpj):
    n = limpar_cnpj(cnpj)
    if len(n) == 14:
        return f"{n[:2]}.{n[2:5]}.{n[5:8]}/{n[8:12]}-{n[12:]}"
    return cnpj

@st.cache_data(ttl=3600)
def consultar_cnpj(cnpj):
    n = limpar_cnpj(cnpj)
    if len(n) != 14:
        return None, "CNPJ deve ter 14 dígitos."
    url = f"https://brasilapi.com.br/api/cnpj/v1/{n}"
    try:
        r = requests.get(url, timeout=12)
        if r.status_code != 200:
            return None, f"Consulta não retornou dados ({r.status_code})."
        d = r.json()
        return {
            "cnpj": formatar_cnpj(n),
            "razao_social": d.get("razao_social", ""),
            "nome_fantasia": d.get("nome_fantasia", ""),
            "cep": str(d.get("cep", "") or ""),
            "logradouro": d.get("logradouro", ""),
            "numero": d.get("numero", ""),
            "complemento": d.get("complemento", ""),
            "bairro": d.get("bairro", ""),
            "cidade": d.get("municipio", ""),
            "uf": d.get("uf", ""),
            "telefone": d.get("ddd_telefone_1", "") or "",
            "email": d.get("email", "") or "",
        }, None
    except Exception as e:
        return None, f"Falha na consulta: {e}"

def proximo_numero_os(s):
    ano = date.today().year
    prefixo = f"{ano}-"
    ult = (
        s.query(OrdemServico)
        .filter(OrdemServico.numero.like(f"{prefixo}%"))
        .order_by(OrdemServico.id.desc())
        .first()
    )
    seq = 1
    if ult:
        try:
            seq = int(ult.numero.split("-")[-1]) + 1
        except:
            seq = ult.id + 1
    return f"{ano}-{seq:06d}"

def obter_preco(s, cliente_id, obra_id, servico_id, data_ref=None):
    data_ref = data_ref or date.today()
    q = (
        s.query(PrecoCliente)
        .filter(
            PrecoCliente.cliente_id == cliente_id,
            PrecoCliente.servico_id == servico_id,
        )
    )

    especifico = (
        q.filter(PrecoCliente.obra_id == obra_id)
        .order_by(PrecoCliente.id.desc())
        .all()
    )
    geral = (
        q.filter(PrecoCliente.obra_id.is_(None))
        .order_by(PrecoCliente.id.desc())
        .all()
    )
    for item in especifico + geral:
        ini_ok = item.vigencia_inicio is None or item.vigencia_inicio <= data_ref
        fim_ok = item.vigencia_fim is None or item.vigencia_fim >= data_ref
        if ini_ok and fim_ok:
            return float(item.valor)

    srv = s.query(Servico).get(servico_id)
    return float(srv.valor_padrao or 0) if srv else 0.0

def gerar_pdf_os(s, os_id):
    osrv = s.query(OrdemServico).get(os_id)
    cliente = s.query(Cliente).get(osrv.cliente_id)
    obra = s.query(Obra).get(osrv.obra_id)
    itens = s.query(ItemOS).filter(ItemOS.os_id == os_id).all()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=15*mm, leftMargin=15*mm,
        topMargin=15*mm, bottomMargin=15*mm
    )
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("<b>HABISOLUTE ENGENHARIA E CONTROLE TECNOLÓGICO</b>", styles["Title"]))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(f"<b>ORDEM DE SERVIÇO Nº {osrv.numero}</b>", styles["Heading2"]))
    story.append(Spacer(1, 3*mm))
    endereco = ", ".join([x for x in [obra.logradouro, obra.numero, obra.bairro, obra.cidade, obra.uf] if x])
    dados = [
        ["Data", osrv.data.strftime("%d/%m/%Y")],
        ["Cliente", cliente.razao_social],
        ["CNPJ", cliente.cnpj],
        ["Obra", obra.nome],
        ["Endereço", endereco],
        ["Solicitante", osrv.solicitante or ""],
        ["Responsável Habisolute", osrv.responsavel_habisolute or ""],
        ["Pedido de compra", osrv.pedido_compra or ""],
        ["Centro de custo", osrv.centro_custo or ""],
        ["Status", osrv.status],
    ]
    t = Table(dados, colWidths=[45*mm, 125*mm])
    t.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("BACKGROUND", (0,0), (0,-1), colors.lightgrey),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
    ]))
    story.append(t)
    story.append(Spacer(1, 5*mm))

    linhas = [["Código", "Serviço", "Qtd.", "Un.", "Unitário", "Total"]]
    total = 0
    for item in itens:
        srv = s.query(Servico).get(item.servico_id)
        subt = float(item.quantidade) * float(item.valor_unitario)
        total += subt
        linhas.append([
            srv.codigo if srv else "",
            item.descricao_customizada or (srv.descricao if srv else ""),
            f"{float(item.quantidade):.2f}".replace(".", ","),
            srv.unidade if srv else "",
            moeda(item.valor_unitario),
            moeda(subt),
        ])
    linhas.append(["", "", "", "", "TOTAL", moeda(total)])
    ti = Table(linhas, colWidths=[22*mm, 68*mm, 18*mm, 17*mm, 25*mm, 28*mm])
    ti.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (4,-1), (5,-1), "Helvetica-Bold"),
        ("ALIGN", (2,1), (-1,-1), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(ti)

    if osrv.observacoes:
        story.append(Spacer(1, 5*mm))
        story.append(Paragraph(f"<b>Observações:</b> {osrv.observacoes}", styles["BodyText"]))

    story.append(Spacer(1, 15*mm))
    ass = Table([
        ["____________________________________", "____________________________________"],
        ["Responsável Habisolute", "Cliente / Solicitante"],
    ], colWidths=[85*mm, 85*mm])
    ass.setStyle(TableStyle([("ALIGN",(0,0),(-1,-1),"CENTER")]))
    story.append(ass)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def dataframe_excel_bytes(df, sheet_name="Dados"):
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name[:31])
    out.seek(0)
    return out.getvalue()


def enviar_email_os(destinatario, assunto, corpo, pdf_bytes, numero_os):
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    smtp_from = os.getenv("SMTP_FROM", smtp_user)
    smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

    if not all([smtp_host, smtp_user, smtp_password, smtp_from]):
        raise RuntimeError(
            "Configuração SMTP incompleta. Defina SMTP_HOST, SMTP_PORT, SMTP_USER, "
            "SMTP_PASSWORD e opcionalmente SMTP_FROM."
        )

    msg = EmailMessage()
    msg["From"] = smtp_from
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.set_content(corpo)

    msg.add_attachment(
        pdf_bytes,
        maintype="application",
        subtype="pdf",
        filename=f"OS_{numero_os}.pdf"
    )

    context = ssl.create_default_context()

    if smtp_port == 465:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=20) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
            server.ehlo()
            if smtp_use_tls:
                server.starttls(context=context)
                server.ehlo()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)


def get_email_config():
    def cfg(name, default=None):
        try:
            return st.secrets.get(name, os.getenv(name, default))
        except Exception:
            return os.getenv(name, default)

    return {
        "host": cfg("SMTP_HOST", "smtp.gmail.com"),
        "port": int(cfg("SMTP_PORT", "587")),
        "user": cfg("SMTP_USER", ""),
        "password": cfg("SMTP_PASSWORD", ""),
        "from_email": cfg("SMTP_FROM", cfg("SMTP_USER", "")),
        "from_name": cfg("SMTP_FROM_NAME", "Habisolute Engenharia e Controle Tecnológico"),
    }

def enviar_os_email(destinatario, assunto, mensagem, pdf_bytes, numero_os):
    config = get_email_config()
    if not config["user"] or not config["password"]:
        raise RuntimeError("E-mail do sistema ainda não configurado. Defina SMTP_USER e SMTP_PASSWORD nos Secrets do Streamlit.")

    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = f'{config["from_name"]} <{config["from_email"]}>'
    msg["To"] = destinatario
    msg.set_content(mensagem)
    msg.add_attachment(
        pdf_bytes,
        maintype="application",
        subtype="pdf",
        filename=f"OS_{numero_os}.pdf"
    )

    with smtplib.SMTP(config["host"], config["port"], timeout=20) as server:
        server.starttls()
        server.login(config["user"], config["password"])
        server.send_message(msg)

def seed_servicos():
    s = db()
    try:
        if s.query(Servico).count() == 0:
            padrao = [
                ("CON-001", "Concreto", "Moldagem de corpo de prova", "un", 0),
                ("CON-002", "Concreto", "Ruptura de corpo de prova", "un", 0),
                ("CON-003", "Concreto", "Ensaio de abatimento (Slump Test)", "ensaio", 0),
                ("CON-004", "Concreto", "Módulo de elasticidade", "ensaio", 0),
                ("SOL-001", "Solos", "Ensaio de compactação", "ensaio", 0),
                ("SOL-002", "Solos", "CBR", "ensaio", 0),
                ("SOL-003", "Solos", "Granulometria", "ensaio", 0),
                ("SOL-004", "Solos", "Limite de liquidez", "ensaio", 0),
                ("ALV-001", "Alvenaria", "Ruptura de bloco", "un", 0),
                ("ALV-002", "Alvenaria", "Ruptura de prisma", "un", 0),
                ("ARG-001", "Argamassa", "Ensaio / ruptura de argamassa", "ensaio", 0),
                ("MOB-001", "Mobilização", "Mobilização de equipe", "viagem", 0),
                ("DIA-001", "Equipe", "Diária de laboratorista", "diária", 0),
                ("KM-001", "Deslocamento", "Quilometragem", "km", 0),
            ]
            for c, cat, desc, un, valor in padrao:
                s.add(Servico(codigo=c, categoria=cat, descricao=desc, unidade=un, valor_padrao=valor))
            s.commit()
    finally:
        s.close()

seed_servicos()


# =========================
# UI
# =========================

st.sidebar.markdown("""
<div class="hb-sidebar-logo">
    <div class="name">HABISOLUTE</div>
    <div class="sub">Engenharia • Controle Tecnológico</div>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navegação",
    [
        "Dashboard",
        "Clientes",
        "Obras",
        "Serviços",
        "Preços por cliente",
        "Nova OS",
        "Consultar OS",
        "Fechamento mensal",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption("Habisolute Engenharia")
topo_sistema()

s = db()

try:
    if menu == "Dashboard":
        cabecalho_pagina("Visão geral", "Acompanhe rapidamente clientes, obras, ordens de serviço e valores executados.")
        total_clientes = s.query(Cliente).count()
        total_obras = s.query(Obra).count()
        total_os = s.query(OrdemServico).count()

        hoje = date.today()
        oss_mes = s.query(OrdemServico).filter(
            OrdemServico.data >= hoje.replace(day=1)
        ).all()

        valor_mes = 0
        for o in oss_mes:
            itens = s.query(ItemOS).filter(ItemOS.os_id == o.id).all()
            valor_mes += sum(float(i.quantidade) * float(i.valor_unitario) for i in itens)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Clientes ativos", total_clientes)
        c2.metric("Obras cadastradas", total_obras)
        c3.metric("Ordens de serviço", total_os)
        c4.metric("Executado no mês", moeda(valor_mes))

        st.markdown("### Atalhos rápidos")
        a1, a2, a3, a4 = st.columns(4)
        a1.info("**Clientes**\n\nCadastros e dados fiscais")
        a2.info("**Nova OS**\n\nLançar serviços executados")
        a3.info("**Consultar OS**\n\nImprimir, exportar e enviar")
        a4.info("**Fechamento**\n\nConsolidar período mensal")

        st.markdown("### Últimas ordens de serviço")
        ultimas = s.query(OrdemServico).order_by(OrdemServico.id.desc()).limit(20).all()
        rows = []
        for o in ultimas:
            cli = s.query(Cliente).get(o.cliente_id)
            obra = s.query(Obra).get(o.obra_id)
            itens = s.query(ItemOS).filter(ItemOS.os_id == o.id).all()
            total = sum(float(i.quantidade) * float(i.valor_unitario) for i in itens)
            rows.append({
                "OS": o.numero, "Data": o.data, "Cliente": cli.razao_social if cli else "",
                "Obra": obra.nome if obra else "", "Status": o.status, "Total": total
            })
        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Total": st.column_config.NumberColumn("Total", format="R$ %.2f"),
                }
            )
        else:
            st.info("Ainda não há ordens de serviço cadastradas.")

    elif menu == "Clientes":
        cabecalho_pagina("Clientes", "Cadastre e mantenha os dados comerciais e fiscais dos clientes.")

        cnpj_input = st.text_input("CNPJ")
        if st.button("🔎 Buscar CNPJ"):
            dados, erro = consultar_cnpj(cnpj_input)
            if erro:
                st.error(erro)
            else:
                st.session_state["cnpj_dados"] = dados
                st.success("Dados encontrados.")

        dados = st.session_state.get("cnpj_dados", {})
        with st.form("form_cliente"):
            c1, c2 = st.columns(2)
            cnpj = c1.text_input("CNPJ *", value=dados.get("cnpj", formatar_cnpj(cnpj_input)))
            razao = c2.text_input("Razão Social *", value=dados.get("razao_social", ""))
            c3, c4 = st.columns(2)
            fantasia = c3.text_input("Nome Fantasia", value=dados.get("nome_fantasia", ""))
            ie = c4.text_input("Inscrição Estadual")
            c5, c6, c7 = st.columns([1,2,1])
            cep = c5.text_input("CEP", value=dados.get("cep", ""))
            logradouro = c6.text_input("Logradouro", value=dados.get("logradouro", ""))
            numero = c7.text_input("Número", value=dados.get("numero", ""))
            c8, c9, c10 = st.columns([2,2,1])
            bairro = c8.text_input("Bairro", value=dados.get("bairro", ""))
            cidade = c9.text_input("Cidade", value=dados.get("cidade", ""))
            uf = c10.text_input("UF", value=dados.get("uf", ""))
            complemento = st.text_input("Complemento", value=dados.get("complemento", ""))
            c11, c12, c13 = st.columns(3)
            telefone = c11.text_input("Telefone", value=dados.get("telefone", ""))
            email = c12.text_input("E-mail", value=dados.get("email", ""))
            responsavel = c13.text_input("Responsável")
            salvar = st.form_submit_button("💾 Salvar cliente")

            if salvar:
                if not limpar_cnpj(cnpj) or not razao.strip():
                    st.error("CNPJ e Razão Social são obrigatórios.")
                elif s.query(Cliente).filter(Cliente.cnpj == formatar_cnpj(cnpj)).first():
                    st.error("Esse CNPJ já está cadastrado.")
                else:
                    s.add(Cliente(
                        cnpj=formatar_cnpj(cnpj), razao_social=razao.strip(),
                        nome_fantasia=fantasia, inscricao_estadual=ie,
                        telefone=telefone, email=email, responsavel=responsavel,
                        cep=cep, logradouro=logradouro, numero=numero,
                        complemento=complemento, bairro=bairro, cidade=cidade, uf=uf
                    ))
                    s.commit()
                    st.session_state.pop("cnpj_dados", None)
                    st.success("Cliente cadastrado com sucesso.")
                    st.rerun()

        st.divider()
        st.subheader("Clientes cadastrados")
        clientes = s.query(Cliente).order_by(Cliente.razao_social).all()
        if clientes:
            st.dataframe(pd.DataFrame([{
                "ID": c.id, "CNPJ": c.cnpj, "Razão Social": c.razao_social,
                "Fantasia": c.nome_fantasia, "Cidade": c.cidade, "UF": c.uf,
                "Telefone": c.telefone, "E-mail": c.email
            } for c in clientes]), use_container_width=True, hide_index=True)

            st.markdown("#### ✏️ Editar cliente")
            mapa_ed_cli = {f"{c.razao_social} • {c.cnpj}": c.id for c in clientes}
            ed_cli_label = st.selectbox("Selecione o cliente para editar", list(mapa_ed_cli.keys()), key="editar_cliente_select")
            ed_cli = s.query(Cliente).get(mapa_ed_cli[ed_cli_label])

            with st.form("form_editar_cliente"):
                e1, e2 = st.columns(2)
                ed_cnpj = e1.text_input("CNPJ", value=ed_cli.cnpj or "")
                ed_razao = e2.text_input("Razão Social", value=ed_cli.razao_social or "")
                e3, e4 = st.columns(2)
                ed_fantasia = e3.text_input("Nome Fantasia", value=ed_cli.nome_fantasia or "")
                ed_ie = e4.text_input("Inscrição Estadual", value=ed_cli.inscricao_estadual or "")
                e5, e6, e7 = st.columns([1,2,1])
                ed_cep = e5.text_input("CEP", value=ed_cli.cep or "")
                ed_logradouro = e6.text_input("Logradouro", value=ed_cli.logradouro or "")
                ed_numero = e7.text_input("Número", value=ed_cli.numero or "")
                e8, e9, e10 = st.columns([2,2,1])
                ed_bairro = e8.text_input("Bairro", value=ed_cli.bairro or "")
                ed_cidade = e9.text_input("Cidade", value=ed_cli.cidade or "")
                ed_uf = e10.text_input("UF", value=ed_cli.uf or "")
                ed_complemento = st.text_input("Complemento", value=ed_cli.complemento or "")
                e11, e12, e13 = st.columns(3)
                ed_telefone = e11.text_input("Telefone", value=ed_cli.telefone or "")
                ed_email = e12.text_input("E-mail", value=ed_cli.email or "")
                ed_responsavel = e13.text_input("Responsável", value=ed_cli.responsavel or "")
                ed_ativo = st.checkbox("Cliente ativo", value=bool(ed_cli.ativo))
                salvar_ed_cli = st.form_submit_button("💾 Salvar alterações", type="primary")

                if salvar_ed_cli:
                    novo_cnpj = formatar_cnpj(ed_cnpj)
                    duplicado = s.query(Cliente).filter(
                        Cliente.cnpj == novo_cnpj,
                        Cliente.id != ed_cli.id
                    ).first()
                    if duplicado:
                        st.error("Já existe outro cliente com esse CNPJ.")
                    elif not ed_razao.strip():
                        st.error("A Razão Social é obrigatória.")
                    else:
                        ed_cli.cnpj = novo_cnpj
                        ed_cli.razao_social = ed_razao.strip()
                        ed_cli.nome_fantasia = ed_fantasia
                        ed_cli.inscricao_estadual = ed_ie
                        ed_cli.cep = ed_cep
                        ed_cli.logradouro = ed_logradouro
                        ed_cli.numero = ed_numero
                        ed_cli.bairro = ed_bairro
                        ed_cli.cidade = ed_cidade
                        ed_cli.uf = ed_uf
                        ed_cli.complemento = ed_complemento
                        ed_cli.telefone = ed_telefone
                        ed_cli.email = ed_email
                        ed_cli.responsavel = ed_responsavel
                        ed_cli.ativo = ed_ativo
                        s.commit()
                        st.success("Cliente atualizado com sucesso.")
                        st.rerun()

    elif menu == "Obras":
        cabecalho_pagina("Obras", "Organize as obras vinculadas a cada cliente e seus responsáveis.")
        clientes = s.query(Cliente).order_by(Cliente.razao_social).all()
        if not clientes:
            st.warning("Cadastre primeiro um cliente.")
        else:
            mapa_cli = {f"{c.razao_social} • {c.cnpj}": c.id for c in clientes}
            with st.form("form_obra"):
                cliente_label = st.selectbox("Cliente *", list(mapa_cli.keys()))
                nome = st.text_input("Nome da obra *")
                codigo = st.text_input("Código da obra")
                c1, c2, c3 = st.columns([1,2,1])
                cep = c1.text_input("CEP")
                logradouro = c2.text_input("Logradouro")
                numero = c3.text_input("Número")
                c4, c5, c6 = st.columns([2,2,1])
                bairro = c4.text_input("Bairro")
                cidade = c5.text_input("Cidade")
                uf = c6.text_input("UF")
                complemento = st.text_input("Complemento")
                c7, c8, c9 = st.columns(3)
                responsavel = c7.text_input("Responsável da obra")
                telefone = c8.text_input("Telefone")
                email = c9.text_input("E-mail")
                c10, c11 = st.columns(2)
                data_inicio = c10.date_input("Data de início", value=None)
                status = c11.selectbox("Status", ["Ativa", "Suspensa", "Finalizada"])
                obs = st.text_area("Observações")
                salvar = st.form_submit_button("💾 Salvar obra")
                if salvar:
                    if not nome.strip():
                        st.error("Informe o nome da obra.")
                    else:
                        s.add(Obra(
                            cliente_id=mapa_cli[cliente_label], nome=nome.strip(), codigo=codigo,
                            cep=cep, logradouro=logradouro, numero=numero, complemento=complemento,
                            bairro=bairro, cidade=cidade, uf=uf, responsavel=responsavel,
                            telefone=telefone, email=email, data_inicio=data_inicio,
                            status=status, observacoes=obs
                        ))
                        s.commit()
                        st.success("Obra cadastrada.")
                        st.rerun()

        st.divider()
        obras = s.query(Obra).order_by(Obra.id.desc()).all()
        if obras:
            linhas = []
            for o in obras:
                cli = s.query(Cliente).get(o.cliente_id)
                linhas.append({
                    "ID": o.id, "Cliente": cli.razao_social if cli else "",
                    "Obra": o.nome, "Código": o.codigo, "Cidade": o.cidade,
                    "UF": o.uf, "Status": o.status
                })
            st.dataframe(pd.DataFrame(linhas), use_container_width=True, hide_index=True)

            st.markdown("#### ✏️ Editar obra")
            mapa_ed_obra = {}
            for o in obras:
                cli = s.query(Cliente).get(o.cliente_id)
                mapa_ed_obra[f"{o.nome} • {cli.razao_social if cli else ''}"] = o.id

            ed_obra_label = st.selectbox("Selecione a obra para editar", list(mapa_ed_obra.keys()), key="editar_obra_select")
            ed_obra = s.query(Obra).get(mapa_ed_obra[ed_obra_label])

            clientes_ed = s.query(Cliente).order_by(Cliente.razao_social).all()
            mapa_clientes_ed = {f"{c.razao_social} • {c.cnpj}": c.id for c in clientes_ed}
            labels_clientes_ed = list(mapa_clientes_ed.keys())
            atual_cli_label = next((lab for lab, cid in mapa_clientes_ed.items() if cid == ed_obra.cliente_id), labels_clientes_ed[0])

            with st.form("form_editar_obra"):
                ed_cliente_label = st.selectbox(
                    "Cliente",
                    labels_clientes_ed,
                    index=labels_clientes_ed.index(atual_cli_label)
                )
                ed_nome = st.text_input("Nome da obra", value=ed_obra.nome or "")
                ed_codigo = st.text_input("Código da obra", value=ed_obra.codigo or "")
                oe1, oe2, oe3 = st.columns([1,2,1])
                ed_cep = oe1.text_input("CEP", value=ed_obra.cep or "")
                ed_logradouro = oe2.text_input("Logradouro", value=ed_obra.logradouro or "")
                ed_numero = oe3.text_input("Número", value=ed_obra.numero or "")
                oe4, oe5, oe6 = st.columns([2,2,1])
                ed_bairro = oe4.text_input("Bairro", value=ed_obra.bairro or "")
                ed_cidade = oe5.text_input("Cidade", value=ed_obra.cidade or "")
                ed_uf = oe6.text_input("UF", value=ed_obra.uf or "")
                ed_complemento = st.text_input("Complemento", value=ed_obra.complemento or "")
                oe7, oe8, oe9 = st.columns(3)
                ed_responsavel = oe7.text_input("Responsável da obra", value=ed_obra.responsavel or "")
                ed_telefone = oe8.text_input("Telefone", value=ed_obra.telefone or "")
                ed_email = oe9.text_input("E-mail", value=ed_obra.email or "")
                oe10, oe11 = st.columns(2)
                ed_data_inicio = oe10.date_input("Data de início", value=ed_obra.data_inicio)
                status_opcoes = ["Ativa", "Suspensa", "Finalizada"]
                status_idx = status_opcoes.index(ed_obra.status) if ed_obra.status in status_opcoes else 0
                ed_status = oe11.selectbox("Status", status_opcoes, index=status_idx)
                ed_obs = st.text_area("Observações", value=ed_obra.observacoes or "")
                salvar_ed_obra = st.form_submit_button("💾 Salvar alterações", type="primary")

                if salvar_ed_obra:
                    if not ed_nome.strip():
                        st.error("Informe o nome da obra.")
                    else:
                        ed_obra.cliente_id = mapa_clientes_ed[ed_cliente_label]
                        ed_obra.nome = ed_nome.strip()
                        ed_obra.codigo = ed_codigo
                        ed_obra.cep = ed_cep
                        ed_obra.logradouro = ed_logradouro
                        ed_obra.numero = ed_numero
                        ed_obra.bairro = ed_bairro
                        ed_obra.cidade = ed_cidade
                        ed_obra.uf = ed_uf
                        ed_obra.complemento = ed_complemento
                        ed_obra.responsavel = ed_responsavel
                        ed_obra.telefone = ed_telefone
                        ed_obra.email = ed_email
                        ed_obra.data_inicio = ed_data_inicio
                        ed_obra.status = ed_status
                        ed_obra.observacoes = ed_obs
                        s.commit()
                        st.success("Obra atualizada com sucesso.")
                        st.rerun()

    elif menu == "Serviços":
        cabecalho_pagina("Serviços", "Gerencie o catálogo de ensaios, mobilizações, diárias e demais serviços.")
        with st.form("form_servico"):
            c1, c2 = st.columns(2)
            codigo = c1.text_input("Código *")
            categoria = c2.selectbox("Categoria", [
                "Concreto", "Solos", "Alvenaria", "Argamassa",
                "Mobilização", "Equipe", "Deslocamento", "Outros"
            ])
            descricao = st.text_input("Descrição do serviço *")
            c3, c4 = st.columns(2)
            unidade = c3.text_input("Unidade *", placeholder="un, ensaio, diária, km...")
            valor_padrao = c4.number_input("Valor padrão", min_value=0.0, step=1.0, format="%.2f")
            salvar = st.form_submit_button("💾 Salvar serviço")
            if salvar:
                if not codigo or not descricao or not unidade:
                    st.error("Código, descrição e unidade são obrigatórios.")
                elif s.query(Servico).filter(Servico.codigo == codigo).first():
                    st.error("Código já cadastrado.")
                else:
                    s.add(Servico(
                        codigo=codigo.strip(), categoria=categoria,
                        descricao=descricao.strip(), unidade=unidade.strip(),
                        valor_padrao=valor_padrao
                    ))
                    s.commit()
                    st.success("Serviço cadastrado.")
                    st.rerun()

        servicos = s.query(Servico).order_by(Servico.categoria, Servico.descricao).all()
        if servicos:
            st.dataframe(pd.DataFrame([{
                "ID": x.id, "Código": x.codigo, "Categoria": x.categoria,
                "Serviço": x.descricao, "Unidade": x.unidade,
                "Valor padrão": float(x.valor_padrao or 0)
            } for x in servicos]), use_container_width=True, hide_index=True)

            st.markdown("#### ✏️ Editar serviço")
            mapa_ed_srv = {f"{x.codigo} • {x.descricao}": x.id for x in servicos}
            ed_srv_label = st.selectbox("Selecione o serviço para editar", list(mapa_ed_srv.keys()), key="editar_servico_select")
            ed_srv = s.query(Servico).get(mapa_ed_srv[ed_srv_label])

            categorias = ["Concreto", "Solos", "Alvenaria", "Argamassa", "Mobilização", "Equipe", "Deslocamento", "Outros"]
            cat_idx = categorias.index(ed_srv.categoria) if ed_srv.categoria in categorias else len(categorias)-1

            with st.form("form_editar_servico"):
                se1, se2 = st.columns(2)
                ed_codigo = se1.text_input("Código", value=ed_srv.codigo or "")
                ed_categoria = se2.selectbox("Categoria", categorias, index=cat_idx)
                ed_descricao = st.text_input("Descrição do serviço", value=ed_srv.descricao or "")
                se3, se4 = st.columns(2)
                ed_unidade = se3.text_input("Unidade", value=ed_srv.unidade or "")
                ed_valor_padrao = se4.number_input(
                    "Valor padrão",
                    min_value=0.0,
                    value=float(ed_srv.valor_padrao or 0),
                    step=1.0,
                    format="%.2f"
                )
                ed_ativo = st.checkbox("Serviço ativo", value=bool(ed_srv.ativo))
                salvar_ed_srv = st.form_submit_button("💾 Salvar alterações", type="primary")

                if salvar_ed_srv:
                    duplicado = s.query(Servico).filter(
                        Servico.codigo == ed_codigo.strip(),
                        Servico.id != ed_srv.id
                    ).first()
                    if duplicado:
                        st.error("Já existe outro serviço com esse código.")
                    elif not ed_codigo.strip() or not ed_descricao.strip() or not ed_unidade.strip():
                        st.error("Código, descrição e unidade são obrigatórios.")
                    else:
                        ed_srv.codigo = ed_codigo.strip()
                        ed_srv.categoria = ed_categoria
                        ed_srv.descricao = ed_descricao.strip()
                        ed_srv.unidade = ed_unidade.strip()
                        ed_srv.valor_padrao = ed_valor_padrao
                        ed_srv.ativo = ed_ativo
                        s.commit()
                        st.success("Serviço atualizado com sucesso.")
                        st.rerun()

    elif menu == "Preços por cliente":
        cabecalho_pagina("Preços por cliente", "Defina valores comerciais por cliente, obra e período de vigência.")
        clientes = s.query(Cliente).order_by(Cliente.razao_social).all()
        servicos = s.query(Servico).filter(Servico.ativo == True).order_by(Servico.descricao).all()
        if not clientes or not servicos:
            st.warning("Cadastre clientes e serviços antes.")
        else:
            mapa_cli = {f"{c.razao_social} • {c.cnpj}": c.id for c in clientes}
            cli_label = st.selectbox("Cliente", list(mapa_cli.keys()))
            cliente_id = mapa_cli[cli_label]
            obras = s.query(Obra).filter(Obra.cliente_id == cliente_id).order_by(Obra.nome).all()
            mapa_obra = {"Todas as obras (preço geral)": None}
            mapa_obra.update({o.nome: o.id for o in obras})
            obra_label = st.selectbox("Obra", list(mapa_obra.keys()))
            obra_id = mapa_obra[obra_label]

            with st.form("form_preco"):
                mapa_srv = {f"{x.codigo} • {x.descricao} ({x.unidade})": x.id for x in servicos}
                srv_label = st.selectbox("Serviço", list(mapa_srv.keys()))
                valor = st.number_input("Valor", min_value=0.0, step=1.0, format="%.2f")
                c1, c2 = st.columns(2)
                inicio = c1.date_input("Vigência inicial", value=date.today())
                usar_fim = c2.checkbox("Definir data final")
                fim = st.date_input("Vigência final", value=date.today()) if usar_fim else None
                salvar = st.form_submit_button("💾 Salvar preço")
                if salvar:
                    s.add(PrecoCliente(
                        cliente_id=cliente_id, obra_id=obra_id,
                        servico_id=mapa_srv[srv_label], valor=valor,
                        vigencia_inicio=inicio, vigencia_fim=fim
                    ))
                    s.commit()
                    st.success("Preço cadastrado.")
                    st.rerun()

            precos = s.query(PrecoCliente).filter(PrecoCliente.cliente_id == cliente_id).order_by(PrecoCliente.id.desc()).all()
            rows = []
            for p in precos:
                srv = s.query(Servico).get(p.servico_id)
                obra = s.query(Obra).get(p.obra_id) if p.obra_id else None
                rows.append({
                    "Obra": obra.nome if obra else "Todas",
                    "Código": srv.codigo if srv else "",
                    "Serviço": srv.descricao if srv else "",
                    "Valor": float(p.valor),
                    "Início": p.vigencia_inicio,
                    "Fim": p.vigencia_fim,
                })
            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

                st.markdown("#### ✏️ Editar preço cadastrado")
                mapa_ed_preco = {}
                for p in precos:
                    srv = s.query(Servico).get(p.servico_id)
                    obra = s.query(Obra).get(p.obra_id) if p.obra_id else None
                    label = f"{srv.codigo if srv else ''} • {srv.descricao if srv else ''} • {obra.nome if obra else 'Todas as obras'} • {moeda(p.valor)}"
                    mapa_ed_preco[label] = p.id

                ed_preco_label = st.selectbox(
                    "Selecione o preço para editar",
                    list(mapa_ed_preco.keys()),
                    key="editar_preco_select"
                )
                ed_preco = s.query(PrecoCliente).get(mapa_ed_preco[ed_preco_label])

                servicos_ed = s.query(Servico).filter(Servico.ativo == True).order_by(Servico.descricao).all()
                mapa_srv_ed = {f"{x.codigo} • {x.descricao} ({x.unidade})": x.id for x in servicos_ed}
                labels_srv_ed = list(mapa_srv_ed.keys())
                atual_srv_label = next((lab for lab, sid in mapa_srv_ed.items() if sid == ed_preco.servico_id), labels_srv_ed[0])

                obras_ed = s.query(Obra).filter(Obra.cliente_id == cliente_id).order_by(Obra.nome).all()
                mapa_obra_ed = {"Todas as obras (preço geral)": None}
                mapa_obra_ed.update({o.nome: o.id for o in obras_ed})
                labels_obra_ed = list(mapa_obra_ed.keys())
                atual_obra_label = next((lab for lab, oid in mapa_obra_ed.items() if oid == ed_preco.obra_id), labels_obra_ed[0])

                with st.form("form_editar_preco"):
                    ed_srv_label = st.selectbox(
                        "Serviço",
                        labels_srv_ed,
                        index=labels_srv_ed.index(atual_srv_label)
                    )
                    ed_obra_label = st.selectbox(
                        "Obra",
                        labels_obra_ed,
                        index=labels_obra_ed.index(atual_obra_label)
                    )
                    ed_valor = st.number_input(
                        "Valor",
                        min_value=0.0,
                        value=float(ed_preco.valor),
                        step=1.0,
                        format="%.2f"
                    )
                    pe1, pe2 = st.columns(2)
                    ed_inicio = pe1.date_input("Vigência inicial", value=ed_preco.vigencia_inicio or date.today())
                    ed_tem_fim = pe2.checkbox("Definir data final", value=ed_preco.vigencia_fim is not None)
                    ed_fim = st.date_input("Vigência final", value=ed_preco.vigencia_fim or date.today()) if ed_tem_fim else None
                    salvar_ed_preco = st.form_submit_button("💾 Salvar alterações", type="primary")

                    if salvar_ed_preco:
                        ed_preco.servico_id = mapa_srv_ed[ed_srv_label]
                        ed_preco.obra_id = mapa_obra_ed[ed_obra_label]
                        ed_preco.valor = ed_valor
                        ed_preco.vigencia_inicio = ed_inicio
                        ed_preco.vigencia_fim = ed_fim
                        s.commit()
                        st.success("Preço atualizado com sucesso.")
                        st.rerun()

    elif menu == "Nova OS":
        cabecalho_pagina("Nova Ordem de Serviço", "Registre os serviços executados e gere a OS do cliente.")
        clientes = s.query(Cliente).order_by(Cliente.razao_social).all()
        if not clientes:
            st.warning("Cadastre um cliente primeiro.")
        else:
            if "itens_os_temp" not in st.session_state:
                st.session_state.itens_os_temp = []

            numero_os = proximo_numero_os(s)
            st.info(f"Próximo número: **{numero_os}**")

            mapa_cli = {f"{c.razao_social} • {c.cnpj}": c.id for c in clientes}
            cli_label = st.selectbox("Cliente *", list(mapa_cli.keys()), key="os_cliente")
            cliente_id = mapa_cli[cli_label]

            obras = s.query(Obra).filter(Obra.cliente_id == cliente_id, Obra.status != "Finalizada").order_by(Obra.nome).all()
            if not obras:
                st.warning("Esse cliente não possui obra ativa cadastrada.")
            else:
                mapa_obra = {o.nome: o.id for o in obras}
                obra_label = st.selectbox("Obra *", list(mapa_obra.keys()))
                obra_id = mapa_obra[obra_label]

                c1, c2, c3 = st.columns(3)
                data_os = c1.date_input("Data da OS", value=date.today())
                solicitante = c2.text_input("Solicitante")
                responsavel = c3.text_input("Responsável Habisolute")
                c4, c5, c6 = st.columns(3)
                sol_cli = c4.text_input("Solicitação do cliente")
                pedido = c5.text_input("Pedido de compra")
                ccusto = c6.text_input("Centro de custo")
                observacoes = st.text_area("Observações")

                st.markdown("#### Adicionar serviços")
                servicos = s.query(Servico).filter(Servico.ativo == True).order_by(Servico.categoria, Servico.descricao).all()
                mapa_srv = {f"{x.codigo} • {x.descricao} ({x.unidade})": x.id for x in servicos}
                srv_label = st.selectbox("Serviço", list(mapa_srv.keys()), key="srv_add")
                srv_id = mapa_srv[srv_label]
                preco_sugerido = obter_preco(s, cliente_id, obra_id, srv_id, data_os)

                a1, a2, a3 = st.columns(3)
                qtd = a1.number_input("Quantidade", min_value=0.01, value=1.0, step=1.0)
                valor_unit = a2.number_input("Valor unitário", min_value=0.0, value=float(preco_sugerido), step=1.0, format="%.2f")
                desc_custom = a3.text_input("Descrição personalizada", placeholder="Opcional")

                if st.button("➕ Adicionar item"):
                    srv = s.query(Servico).get(srv_id)
                    st.session_state.itens_os_temp.append({
                        "servico_id": srv_id,
                        "codigo": srv.codigo,
                        "descricao": desc_custom or srv.descricao,
                        "unidade": srv.unidade,
                        "quantidade": float(qtd),
                        "valor_unitario": float(valor_unit),
                    })
                    st.rerun()

                if st.session_state.itens_os_temp:
                    df_itens = pd.DataFrame(st.session_state.itens_os_temp)
                    df_show = df_itens.copy()
                    df_show["total"] = df_show["quantidade"] * df_show["valor_unitario"]
                    st.dataframe(df_show[["codigo","descricao","unidade","quantidade","valor_unitario","total"]],
                                 use_container_width=True, hide_index=True)
                    total_os = float(df_show["total"].sum())
                    st.metric("Total da OS", moeda(total_os))

                    cbtn1, cbtn2 = st.columns(2)
                    if cbtn1.button("🗑️ Limpar itens"):
                        st.session_state.itens_os_temp = []
                        st.rerun()

                    if cbtn2.button("💾 Salvar OS", type="primary"):
                        nova = OrdemServico(
                            numero=numero_os, data=data_os, cliente_id=cliente_id, obra_id=obra_id,
                            solicitante=solicitante, responsavel_habisolute=responsavel,
                            solicitacao_cliente=sol_cli, pedido_compra=pedido,
                            centro_custo=ccusto, observacoes=observacoes, status="Executada"
                        )
                        s.add(nova)
                        s.flush()
                        for item in st.session_state.itens_os_temp:
                            s.add(ItemOS(
                                os_id=nova.id, servico_id=item["servico_id"],
                                quantidade=item["quantidade"],
                                valor_unitario=item["valor_unitario"],
                                descricao_customizada=item["descricao"]
                            ))
                        s.commit()
                        st.session_state.itens_os_temp = []
                        st.success(f"OS {numero_os} salva com sucesso.")
                        st.rerun()
                else:
                    st.info("Adicione pelo menos um serviço à OS.")

    elif menu == "Consultar OS":
        cabecalho_pagina("Consultar OS", "Pesquise, visualize, imprima, exporte e envie ordens de serviço.")
        f1, f2 = st.columns([3, 1])
        termo = f1.text_input("Pesquisar", placeholder="Número da OS, cliente ou obra...")
        status_filtro = f2.selectbox("Status", ["Todos", "Aberta", "Executada", "Conferida", "Fechada", "Faturada", "Recebida"])
        q = s.query(OrdemServico).order_by(OrdemServico.id.desc())
        if status_filtro != "Todos":
            q = q.filter(OrdemServico.status == status_filtro)
        ordens = q.limit(200).all()

        cards = []
        for o in ordens:
            cli = s.query(Cliente).get(o.cliente_id)
            obra = s.query(Obra).get(o.obra_id)
            texto = f"{o.numero} {cli.razao_social if cli else ''} {obra.nome if obra else ''}".lower()
            if termo and termo.lower() not in texto:
                continue
            itens = s.query(ItemOS).filter(ItemOS.os_id == o.id).all()
            total = sum(float(i.quantidade) * float(i.valor_unitario) for i in itens)
            cards.append((o, cli, obra, total))

        for o, cli, obra, total in cards:
            with st.expander(f"OS {o.numero} • {o.data.strftime('%d/%m/%Y')} • {obra.nome if obra else ''} • {moeda(total)}"):
                st.write(f"**Cliente:** {cli.razao_social if cli else ''}")
                st.write(f"**CNPJ:** {cli.cnpj if cli else ''}")
                st.write(f"**Obra:** {obra.nome if obra else ''}")
                st.write(f"**Status:** {o.status}")
                itens = s.query(ItemOS).filter(ItemOS.os_id == o.id).all()
                rows = []
                for i in itens:
                    srv = s.query(Servico).get(i.servico_id)
                    rows.append({
                        "Código": srv.codigo if srv else "",
                        "Serviço": i.descricao_customizada or (srv.descricao if srv else ""),
                        "Qtd.": float(i.quantidade),
                        "Unidade": srv.unidade if srv else "",
                        "Valor unit.": float(i.valor_unitario),
                        "Total": float(i.quantidade) * float(i.valor_unitario)
                    })
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True)

                pdf = gerar_pdf_os(s, o.id)
                excel = dataframe_excel_bytes(df, f"OS {o.numero}")
                b1, b2, b3 = st.columns(3)
                b1.download_button(
                    "📄 Baixar / Imprimir OS", pdf,
                    file_name=f"OS_{o.numero}.pdf", mime="application/pdf",
                    key=f"pdf_{o.id}"
                )
                b2.download_button(
                    "📊 Exportar OS em Excel", excel,
                    file_name=f"OS_{o.numero}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"xls_{o.id}"
                )
                if b3.button("✉️ Enviar OS por e-mail", key=f"abrir_email_{o.id}"):
                    st.session_state[f"email_os_{o.id}"] = True

                if st.session_state.get(f"email_os_{o.id}", False):
                    st.markdown("##### Enviar OS ao cliente")
                    email_padrao = (obra.email if obra and obra.email else "") or (cli.email if cli else "") or ""
                    destinatario = st.text_input(
                        "E-mail do destinatário",
                        value=email_padrao,
                        key=f"dest_{o.id}"
                    )
                    assunto = st.text_input(
                        "Assunto",
                        value=f"Ordem de Serviço {o.numero} - Habisolute",
                        key=f"assunto_{o.id}"
                    )
                    mensagem = st.text_area(
                        "Mensagem",
                        value=(
                            f"Olá,\n\nSegue em anexo a Ordem de Serviço nº {o.numero}, "
                            f"referente à obra {obra.nome if obra else ''}.\n\n"
                            "Atenciosamente,\nHabisolute Engenharia e Controle Tecnológico"
                        ),
                        height=150,
                        key=f"msg_{o.id}"
                    )
                    ec1, ec2 = st.columns(2)
                    if ec1.button("📨 Confirmar envio", type="primary", key=f"enviar_{o.id}"):
                        if not destinatario or "@" not in destinatario:
                            st.error("Informe um e-mail válido.")
                        else:
                            try:
                                enviar_os_email(destinatario, assunto, mensagem, pdf, o.numero)
                                st.success(f"OS {o.numero} enviada para {destinatario}.")
                                st.session_state[f"email_os_{o.id}"] = False
                            except Exception as e:
                                st.error(f"Não foi possível enviar: {e}")
                    if ec2.button("Cancelar", key=f"cancelar_email_{o.id}"):
                        st.session_state[f"email_os_{o.id}"] = False
                        st.rerun()

    elif menu == "Fechamento mensal":
        cabecalho_pagina("Fechamento mensal", "Consolide as OS do período por cliente e obra.")
        clientes = s.query(Cliente).order_by(Cliente.razao_social).all()
        if not clientes:
            st.warning("Nenhum cliente cadastrado.")
        else:
            mapa_cli = {"Todos os clientes": None}
            mapa_cli.update({f"{c.razao_social} • {c.cnpj}": c.id for c in clientes})
            c1, c2, c3 = st.columns(3)
            cli_label = c1.selectbox("Cliente", list(mapa_cli.keys()))
            inicio = c2.date_input("Data inicial", value=date.today().replace(day=1))
            fim = c3.date_input("Data final", value=date.today())

            cliente_id = mapa_cli[cli_label]
            obras = []
            if cliente_id:
                obras = s.query(Obra).filter(Obra.cliente_id == cliente_id).order_by(Obra.nome).all()
            mapa_obra = {"Todas as obras": None}
            mapa_obra.update({o.nome: o.id for o in obras})
            obra_label = st.selectbox("Obra", list(mapa_obra.keys()))
            obra_id = mapa_obra[obra_label]

            q = s.query(OrdemServico).filter(OrdemServico.data >= inicio, OrdemServico.data <= fim)
            if cliente_id:
                q = q.filter(OrdemServico.cliente_id == cliente_id)
            if obra_id:
                q = q.filter(OrdemServico.obra_id == obra_id)
            ordens = q.order_by(OrdemServico.data, OrdemServico.numero).all()

            rows = []
            for o in ordens:
                cli = s.query(Cliente).get(o.cliente_id)
                obra = s.query(Obra).get(o.obra_id)
                itens = s.query(ItemOS).filter(ItemOS.os_id == o.id).all()
                for i in itens:
                    srv = s.query(Servico).get(i.servico_id)
                    total = float(i.quantidade) * float(i.valor_unitario)
                    rows.append({
                        "OS": o.numero,
                        "Data": o.data,
                        "Cliente": cli.razao_social if cli else "",
                        "CNPJ": cli.cnpj if cli else "",
                        "Obra": obra.nome if obra else "",
                        "Código": srv.codigo if srv else "",
                        "Categoria": srv.categoria if srv else "",
                        "Serviço": i.descricao_customizada or (srv.descricao if srv else ""),
                        "Quantidade": float(i.quantidade),
                        "Unidade": srv.unidade if srv else "",
                        "Valor unitário": float(i.valor_unitario),
                        "Total": total,
                        "Status": o.status,
                    })

            if rows:
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.metric("TOTAL DO PERÍODO", moeda(df["Total"].sum()))
                excel = dataframe_excel_bytes(df, "Fechamento")
                st.download_button(
                    "📊 Exportar fechamento para Excel",
                    excel,
                    file_name=f"Fechamento_{inicio.strftime('%Y%m%d')}_{fim.strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            else:
                st.info("Nenhuma OS encontrada para o período selecionado.")

finally:
    s.close()
