import asyncio
from src.app.app import App

app_estoque = App().Estoque()

if __name__=='__main__':
    # asyncio.run(app_estoque.balanco())
    asyncio.run(app_estoque.atualizar())

