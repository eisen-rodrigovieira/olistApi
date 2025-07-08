import re
import asyncio
import streamlit as st
from datetime                 import datetime
from params                   import config
from src.app.app              import App
from src.utils.validaPath     import validaPath
from src.utils.imagemMarkdown import embed_local_images_in_markdown
from src.utils.taskManager    import taskManager

st.set_page_config(
    page_title="Integrador Olist",
    page_icon="🔗",
    layout="wide"
)

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stAppDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

font_css = """
<style>
button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
font-size: 18px;

button[data-baseweb="tab"] {
    class="flex-container"
}
}
</style>
"""
app_produto    = App().Produto()
app_estoque    = App().Estoque()
app_pedido     = App().Pedido()

valida_path    = validaPath()
task_prod      = taskManager()
task_ped       = taskManager()
task_est       = taskManager()
task_options   = config.TASK_TIME
tsk_produtos   = task_prod.get(task='Olist - Integra produtos')
tsk_estoque    = task_est.get(task='Olist - Integra estoque')
tsk_pedidos    = task_ped.get(task='Olist - Integra pedidos')
md_raw         = asyncio.run(valida_path.validar(path=config.PATH_DOCS,mode='r',method='full'))
docs           = embed_local_images_in_markdown(md_raw)
regex_dates    = r'^\d{4}-\d{2}-\d{2}'
regex_log      = r'\#\w+#.+'
regex_contexto = r'\w+'
regex_texto    = r'#\w+#\s'
regex_data     = r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}'

st.write(font_css, unsafe_allow_html=True)
st.title("Painel de Controle - Olist")
with st.container(border=True):
    tab_produtos, tab_pedidos, tab_estoque, tab_logs, tab_config, tab_ajuda = st.tabs(["**🏷️ Produtos**","**🛒 Pedidos**","**📦 Estoque**","**📰 Logs**","**⚙️ Configurações**","**💬 Ajuda**"])

    with tab_produtos:
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
    
    with tab_pedidos:
        col1_pd, col2_pd = st.columns(2)
        btn_receive_pd = st.button("🔄 Atualizar pedidos",key='btn_update_all_pd',use_container_width=True)
        with st.empty():
            if btn_receive_pd:
                with st.spinner("Aguarde",show_time=True):
                    status_aprovados, values_aprovados = asyncio.run(app_pedido.importa_aprovados())
                    status_prep_envio, values_prep_envio = asyncio.run(app_pedido.importa_prep_envio())
                    status_faturados, values_faturados = asyncio.run(app_pedido.importa_faturados())
                if status_aprovados and status_prep_envio and status_faturados:
                    with st.expander(label="Pedidos atualizados com sucesso!",icon="✅"):
                        for v in values_aprovados+values_prep_envio+values_faturados:
                            st.write(v)
                else:
                    with st.expander(label="Ocorreram erros durante a sincronização! Verifique os logs.",icon="❌"):
                        for v in values_aprovados+values_prep_envio+values_faturados:
                            st.write(v)
                            
    with tab_estoque:
        btn_send_est = st.button("🔄 Atualizar estoques",key='btn_send_est',use_container_width=True)
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

    with tab_logs:
        logs = asyncio.run(valida_path.validar(path=config.PATH_LOGS,mode='r',method='lines'))
        logs.reverse()
        date_ini = datetime.strptime(re.match(regex_dates,logs[-1]).group(),'%Y-%m-%d')
        date_fim = datetime.strptime(re.match(regex_dates,logs[0]).group(),'%Y-%m-%d')
        data = st.date_input(label="Período",value=(datetime.today().date(),datetime.today().date()),min_value=date_ini,max_value=date_fim,format='DD/MM/YYYY')
        contexto = st.pills("Contexto",options=["Todos","Produtos","Pedidos","Estoque","Notas"],default="Todos",label_visibility="collapsed")
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
 
    with tab_config:
        st.warning("👩🏻‍💻 Em desenvolvimento. Por hora, alterações nestes campos não interferem na execução do integrador")
        st.subheader("🏷️ Produtos")        
        with st.container(border=True):
            cols_tsk_produtos1 = st.columns([0.2,0.6,0.2],vertical_alignment='bottom')
            tempo_tsk_produtos1 = cols_tsk_produtos1[0].time_input(label="Horário inicial",
                                                                   key="tempo_prod1",
                                                                   value=tsk_produtos[0].get('Inicio'))
            freq_tsk_produtos1 = cols_tsk_produtos1[1].radio(label="Frequência",
                                                             key="freq_prod1",
                                                             index=task_options.index(tsk_produtos[0].get('Frequencia')),
                                                             options=task_options,
                                                             horizontal=True)
            hab_tsk_produtos1 = cols_tsk_produtos1[2].toggle(label="Habilitado",
                                                             value=tsk_produtos[0].get('Habilitado'),
                                                             key="hab_prod1")
        with st.container(border=True):
            cols_tsk_produtos2 = st.columns([0.2,0.6,0.2],vertical_alignment='bottom')
            tempo_tsk_produtos2 = cols_tsk_produtos2[0].time_input(label="Horário inicial",
                                                                   key="tempo_prod2",
                                                                   value=tsk_produtos[1].get('Inicio'))
            freq_tsk_produtos2 = cols_tsk_produtos2[1].radio(label="Frequência",
                                                             key="freq_prod2",
                                                             index=task_options.index(tsk_produtos[1].get('Frequencia')),
                                                             options=task_options,
                                                             horizontal=True)
            hab_tsk_produtos2 = cols_tsk_produtos2[2].toggle(label="Habilitado",
                                                             value=tsk_produtos[1].get('Habilitado'),
                                                             key="hab_prod2")

        st.subheader("🛒 Pedidos")
        with st.container(border=True):
            cols_tsk_pedidos = st.columns([0.2,0.6,0.2],vertical_alignment='bottom')
            tempo_tsk_pedidos = cols_tsk_pedidos[0].time_input(label="Horário inicial",
                                                key="tempo_ped",
                                                value=tsk_pedidos[0].get('Inicio'))
            freq_tsk_pedidos = cols_tsk_pedidos[1].radio(label="Frequência",
                                        key="freq_ped",
                                        index=task_options.index(tsk_pedidos[0].get('Frequencia')),
                                        options=task_options,
                                        horizontal=True)
            hab_tsk_pedidos = cols_tsk_pedidos[2].toggle(label="Habilitado",
                                        value=tsk_pedidos[0].get('Habilitado'),
                                        key="hab_ped")

        st.subheader("📦 Estoque")
        with st.container(border=True):
            cols_tsk_estoque = st.columns([0.2,0.6,0.2],vertical_alignment='bottom')
            tempo_tsk_estoque = cols_tsk_estoque[0].time_input(label="Horário inicial",
                                                               key="tempo_est",
                                                               value=tsk_estoque[0].get('Inicio'))
            freq_tsk_estoque = cols_tsk_estoque[1].radio(label="Frequência",
                                                         key="freq_est",
                                                         index=task_options.index(tsk_estoque[0].get('Frequencia')),
                                                         options=task_options,
                                                         horizontal=True)
            hab_tsk_estoque = cols_tsk_estoque[2].toggle(label="Habilitado",
                                                         value=tsk_estoque[0].get('Habilitado'),
                                                         key="hab_est")

        st.button("Salvar",use_container_width=True,type="primary")   

    with tab_ajuda:
        st.markdown(docs,unsafe_allow_html=True)