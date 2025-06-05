import asyncio
from src.app.app import App

app_pedido = App().Pedido()

if __name__=='__main__':
    asyncio.run(app_pedido.busca_novos())

