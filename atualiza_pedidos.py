import asyncio
from src.app.app import App

app_pedido = App().Pedido()

if __name__=='__main__':
    asyncio.run(app_pedido.importa_aprovados())
    asyncio.run(app_pedido.importa_prep_envio())
    asyncio.run(app_pedido.importa_faturados())

