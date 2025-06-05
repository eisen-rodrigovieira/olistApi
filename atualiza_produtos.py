import asyncio
from src.app.app import App

app_produto = App().Produto()

if __name__=='__main__':
    asyncio.run(app_produto.ol_atualizar_produtos())
    asyncio.run(app_produto.snk_atualizar_produtos())

