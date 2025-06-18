import re
import asyncio
import streamlit as st
from datetime             import datetime, time
from params               import config
from src.app.app          import App
from src.utils.validaPath import validaPath
from src.utils.imagemMarkdown import embed_local_images_in_markdown

st.set_page_config(
    page_title="Integrador Olist",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

app_produto = App().Produto()
app_estoque = App().Estoque()
valida_path = validaPath()
md_raw = asyncio.run(valida_path.validar(path=config.PATH_DOCS,mode='r',method='full'))
docs = embed_local_images_in_markdown(md_raw)

@st.dialog('Ajuda do integrador',width='large')
def show_docs():
    st.markdown(docs,unsafe_allow_html=True)

col_title, col_help = st.columns([0.9,0.1],vertical_alignment='bottom',gap='large')
with col_title:
    st.title("Painel de Controle - Olist")
with col_help:
    if st.button("Ajuda",type='tertiary'):
        show_docs()

with st.sidebar:
    with st.expander(label="Logs do sistema",icon="📰"):

        logs = asyncio.run(valida_path.validar(path=config.PATH_LOGS,mode='r',method='lines'))
        logs.reverse()

        regex_dates    = r'^\d{4}-\d{2}-\d{2}'
        regex_log      = r'\#\w+#.+'
        regex_contexto = r'\w+'
        regex_texto    = r'#\w+#\s'
        regex_data     = r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}'

        date_ini = datetime.strptime(re.match(regex_dates,logs[-1]).group(),'%Y-%m-%d')
        date_fim = datetime.strptime(re.match(regex_dates,logs[0]).group(),'%Y-%m-%d')

        data = st.date_input(label="Período",value=(datetime.today().date(),datetime.today().date()),min_value=date_ini,max_value=date_fim,format='DD/MM/YYYY')
        contexto = st.pills("Contexto",options=["Todos","Produtos","Pedidos","Estoque"],default="Todos",label_visibility="collapsed")
        
        with st.spinner():
            with st.container(height=500):            
                    valLog = 0                
                    for l in logs:                    
                        try:
                            dt        = datetime.strptime(re.match(regex_dates,l).group(),'%Y-%m-%d').date()
                            log       = re.search(regex_log,l).group()
                            contexto_ = re.search(regex_contexto,log).group()
                            texto     = re.sub(regex_texto,'',log)
                            data_     = datetime.strptime(re.match(regex_data,l).group(),'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
                            if contexto in ['Todos',contexto_] and dt >= data[0] and dt <= data[1]:
                                valLog+=1
                                st.caption(f"{data_} - {texto}")
                        except:
                            pass
                    if not valLog:
                        st.caption("Nenhum registro pra exibir")  

    with st.expander(label="Configurações do integrador",icon="⚙️"):
        st.warning("👩🏻‍💻 Em desenvolvimento. Por hora, alterações nestes campos não interferem na execução do integrador")
        prod_config_cols = st.columns([0.7,0.3])
        prod_config_cols[0].subheader("🏷️ Produtos")
        prod_config_cols[1].toggle("Habilitado",value=True,key="prod_habilitado")
        prod_frequencia = st.radio(label="Frequência",key="prod_freq",index=5,options=["15min","30min","1h","12hs","24hs","Outro"],horizontal=True)
        if prod_frequencia == "Outro":
            prod_config_cols2 = st.columns(2)
            prod_config_cols2[0].number_input(label="Valor",value=6,min_value=1,max_value=60)
            prod_config_cols2[1].selectbox(label="Unidade",options=["min","hr"],index=1)
        prod_tempo = st.time_input("Horário inicial",key="prod_tempo",value=time(8,30))
        st.divider()

        ped_config_cols = st.columns([0.7,0.3])
        ped_config_cols[0].subheader("🛒 Pedidos")
        ped_config_cols[1].toggle("Habilitado",value=False,key="ped_habilitado")
        ped_frequencia = st.radio(label="Frequência",key="ped_freq",index=1,options=["15min","30min","1h","12hs","24hs","Outro"],horizontal=True)
        if ped_frequencia == "Outro":
            ped_config_cols2 = st.columns(2)
            ped_config_cols2[0].number_input(label="Valor",value=1,min_value=1,max_value=60)
            ped_config_cols2[1].selectbox(label="Unidade",options=["min","hr"])
        ped_tempo = st.time_input("Horário inicial",key="ped_tempo",value=time(8,0))
        st.divider()

        est_config_cols = st.columns([0.7,0.3])
        est_config_cols[0].subheader("📦 Estoque")
        est_config_cols[1].toggle("Habilitado",value=True,key="est_habilitado")
        est_frequencia = st.radio(label="Frequência",key="est_freq",index=1,options=["15min","30min","1h","12hs","24hs","Outro"],horizontal=True)
        if est_frequencia == "Outro":
            est_config_cols2 = st.columns(2)
            est_config_cols2[0].number_input(label="Valor",value=1,min_value=1,max_value=60)
            est_config_cols2[1].selectbox(label="Unidade",options=["min","hr"])
        est_tempo = st.time_input("Horário inicial",key="est_tempo",value=time(8,0))
        st.divider()

        st.button("Salvar",use_container_width=True,type="primary")        

with st.container():
    st.divider()
    st.subheader("🏷️ Produtos")
    col1_pr, col2_pr, col3_pr = st.columns(3)

    with col1_pr:
        btn_send_pr = st.button("📤 Enviar atualizações para Olist",key='btn_send_pr',use_container_width=True)
        with st.empty():
            if btn_send_pr:
                with st.spinner("Aguarde",show_time=True):
                    status_send, values_send = asyncio.run(app_produto.ol_atualizar_produtos())
                if status_send:
                    with st.expander(label="Atualizações enviadas com sucesso!",icon="✅"):
                        for v in values_send:
                            st.write(v)    
                else:
                    st.error("Falha na sincronização! Verifique os logs.")                    

    with col2_pr:
        btn_receive_pr = st.button("📥 Receber atualizações do Olist",key='btn_receive_pr',use_container_width=True)
        with st.empty():
            if btn_receive_pr:
                with st.spinner("Aguarde",show_time=True):
                    status_receive, values_receive = asyncio.run(app_produto.snk_atualizar_produtos())
                if status_receive:
                    with st.expander(label="Atualizações recebidas com sucesso!",icon="✅"):
                        for v in values_receive:
                            st.write(v)                        
                else:
                    st.error("Falha na sincronização! Verifique os logs.")

    with col3_pr:
        btn_update_all_pr = st.button("🔄 Atualizar tudo",key='btn_update_all_pr',use_container_width=True)
        with st.empty():
            if btn_update_all_pr:
                status_sinc = []
                with st.spinner("Sincronizando",show_time=True):
                    status_ol, values_send2 = asyncio.run(app_produto.ol_atualizar_produtos())
                    status_sinc.append(status_ol)
                    status_snk, values_receive2 = asyncio.run(app_produto.snk_atualizar_produtos())
                    status_sinc.append(status_snk)
                if False in status_sinc:
                    st.error("Falha na sincronização! Verifique os logs.")
                else:
                    vl = values_send2+values_receive2
                    with st.expander(label="Sincronização concluída com sucesso!",icon="✅"):
                        for v in vl:
                            st.write(v)
    st.divider()
    auxcols = st.columns([0.2,0.8])
    auxcols[0].subheader("🛒 Pedidos")    
    auxcols[1].warning("🚧 Manutenção 🚧")   
    
    col1_pd, col2_pd = st.columns(2)

    btn_receive_pd = st.button("🔄 Atualizar pedidos",key='btn_update_all_pd',use_container_width=True)
    with st.empty():
        if btn_receive_pd:
            st.warning("Em desenvolvimento e testes.",icon="👩🏻‍💻")
 
    st.divider()
    st.subheader("📦 Estoque")    
    
    col1_es, col2_es = st.columns([0.3, 0.7],vertical_alignment="top")
    with col1_es:
        btn_send_est = st.button("📤 Enviar atualizações para Olist",key='btn_send_est',use_container_width=True)
        with st.empty():
            if btn_send_est:    
                with st.spinner("Aguarde",show_time=True):
                    status_send, values_send = asyncio.run(app_estoque.atualizar())
                if status_send:
                    with st.expander(label="Atualizações enviadas com sucesso!",icon="✅"):
                        for v in values_send:
                            st.caption(v)    
                else:
                    st.error("Falha na sincronização! Verifique os logs.")

    with col2_es:
        btn_update_bal = None        
        with st.container(border=True):
            col_produto, col_botao = st.columns(2,vertical_alignment="bottom")
            with col_produto:
                number = st.text_input("Informe o código do produto")
            with col_botao:
                btn_update_bal = st.button("🔄 Executar balanço de estoque",key='btn_update_bal',use_container_width=True)
            st.caption("⚠️:red[**Executar o balanço sem especificar o produto atualiza o estoque de TODOS OS PRODUTOS**]")

            if btn_update_bal:
                produto = None
                with st.spinner("Aguarde",show_time=True):
                    try:
                        try: produto = int(number)
                        except: pass
                        finally:                        
                            status_bal, values_bal = asyncio.run(app_estoque.balanco(produto=produto))
                            if status_bal:
                                with st.expander(label="Balanço de estoque executado com sucesso!",icon="✅"):
                                    for v in values_bal: st.caption(v)    
                            else:
                                st.error("Falha na sincronização! Verifique os logs.")                           
                    except ValueError as e: st.error(f"Número inválido ou vazio. {e}")
                    finally: pass
