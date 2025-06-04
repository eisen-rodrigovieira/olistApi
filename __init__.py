import asyncio
import streamlit as st
from src.app.app import App

st.set_page_config(
    page_title="Integração Olist",
    page_icon="🔗",
    layout="wide"
    # initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

app_produto = App().Produto()
app_pedido = App().Pedido()

st.title("Painel de Controle - Olist")

with st.container():
    st.divider()
    st.subheader("📦 Produtos")
    col1_pr, col2_pr, col3_pr = st.columns(3)

    with col1_pr:
        btn_send_pr = st.button("📤 Enviar atualizações para Olist",key='btn_send_pr',use_container_width=True)
        with st.empty():
            if btn_send_pr:
                with st.spinner("Aguarde",show_time=True):
                    status_send, values_send = asyncio.run(app_produto.ol_atualizar_produtos())
                if status_send:
                    with st.expander(label="✅ Atualizações enviadas com sucesso!"):
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
                    with st.expander(label="✅ Atualizações recebidas com sucesso!"):
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
                    status_sinc[0], values_send2 = asyncio.run(app_produto.ol_atualizar_produtos())
                    status_sinc[1], values_receive2 = asyncio.run(app_produto.snk_atualizar_produtos())
                if False in status_sinc:
                    st.error("Falha na sincronização! Verifique os logs.")
                else:
                    vl = values_send2+values_receive2
                    with st.expander(label="✅ Sincronização concluída com sucesso!"):
                        for v in vl:
                            st.write(v)
    st.divider()
    st.subheader("🛒 Pedidos")    
    
    col1_pd, col2_pd = st.columns(2)
    with col1_pd:
        btn_receive_pd = st.button("📥 Receber pedidos novos",key='btn_receive_pd',use_container_width=True)
        with st.empty():
            if btn_receive_pd:    
                with st.spinner("Aguarde",show_time=True):
                    status_receive, values_receive = asyncio.run(app_pedido.busca_novos())
                if status_receive:
                    with st.expander(label="✅ Atualizações recebidas com sucesso!"):
                        for v in values_receive:
                            st.caption(v)    
                else:
                    st.error("Falha na sincronização! Verifique os logs.")   

    with col2_pd:
        btn_update_all_pd = st.button("🔄 Atualizar pedidos",key='btn_update_all_pd',use_container_width=True,disabled=True)
        with st.empty():
            if btn_update_all_pd:
                st.warning("👷🏼⚠️ Em desenvolvimento")   
        st.warning("👷🏼⚠️ Em desenvolvimento")
