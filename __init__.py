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
app_estoque = App().Estoque()

st.title("Painel de Controle - Olist")

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
                    status_ol, values_send2 = asyncio.run(app_produto.ol_atualizar_produtos())
                    status_sinc.append(status_ol)
                    status_snk, values_receive2 = asyncio.run(app_produto.snk_atualizar_produtos())
                    status_sinc.append(status_snk)
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
        btn_receive_pd = st.button("🔄 Atualizar pedidos",key='btn_update_all_pd',use_container_width=True)
        with st.empty():
            if btn_receive_pd:
                with st.status("Aguarde...", expanded=True) as status:
                    status_receive, values_receive = asyncio.run(app_pedido.busca_novos())
                    if status_receive:
                        for v in values_receive:
                            st.caption(v)
                        status.update(label="✅ Atualizações recebidas com sucesso!", state="complete", expanded=False)                        
                    else:
                        status.update(label="Falha na sincronização! Verifique os logs.", state="error", expanded=False)
 
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
                    with st.expander(label="✅ Atualizações enviadas com sucesso!"):
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
                        #if int(number): produto = int(number) else: None
                        try: produto = int(number)
                        except: pass
                        finally:                        
                            status_bal, values_bal = asyncio.run(app_estoque.balanco(produto=produto))
                            if status_bal:
                                with st.expander(label="✅ Balanço de estoque executado com sucesso!"):
                                    for v in values_bal: st.caption(v)    
                            else:
                                st.error("Falha na sincronização! Verifique os logs.")                           
                    except ValueError as e: st.error(f"Número inválido ou vazio. {e}")
                    finally: pass
