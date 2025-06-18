# 🔗 Integrador Sankhya ↔️ Olist

## 🎟️ Visão Geral

Este projeto realiza a integração entre o sistema de gestão **Sankhya** e a plataforma **Olist**, automatizando os processos de:

- Cadastro de produtos
- Atualização de estoque
- Importação de pedidos
- Sincronização de status

O objetivo é centralizar a operação, evitar lançamentos manuais e manter os dados de ambos os sistemas atualizados, proporcionando mais eficiência e menor risco de erros.

## ⚙️ Funcionamento

- 🔑 **Autenticação:** Conexão segura com a API do Olist e base de dados do Sankhya.
- 🗓️ **Execução:** Funciona de forma agendada, por serviço em background ou execução manual.
- 🔄 **Processamento:** Busca, transforma e envia os dados entre os sistemas, conforme regras definidas.
- 📌 **Logs:** Todas as interações são salvas em arquivos de log e/ou banco de dados.

## 🚀 Escopos da aplicação

- 🏷️ **Produtos:** _Criação e atualização de produtos do Sankhya no Olist._
  - Os produtos são enviados do Sankhya para o Olist mediante identificação no cadastro de produtos
  ![Aba Marketplace do cadastro de produtos](docs/img/cadastro_produto_mkp.png)
  - A sincronização de cadastro dos produtos ocorre 2 vezes ao dia
  - O vínculo entre os registros é feito pelo código do produto no Sankhya, que é armazenado o campo SKU no Olist
  - Uma vez que a integração do produto está habilitada (campo Integrar Marketplace), todas as alterações do seu cadastro no Sankhya são monitoradas e enviadas para o Olist.
  - Produtos que foram cadastrados como componentes de uma Variação no Olist recebem o código do Produto Pai no Sankhya
  - Não é possível alterar o ID do produto no Sankhya
  - As informações do cadastro de produto sincronizadas entre os sistemas são:
    - SKU (código do produto no Sankhya)
    - ID (código do produto no Olist)
    - ID produto pai (se o produto for item de variação no Olist)
    - Nome
    - Descrição
    - Unidade
    - Origem
    - NCM
    - GTIN
    - CEST
    - Marca
    - Categoria
    - Medidas (altura/largura/comprimento)
    - Peso (líquido/bruto)
    - Estoque (mínimo/máximo)

- 📦 **Gestão de estoque:** _Atualização automática dos saldos de estoque no Olist conforme o Sankhya._
  - Os produtos que estão com a integração habilitada tem sua movimentação de estoque monitorada para sincronização com o estoque disponível no Olist
  - A sincronização de estoque dos produtos ocorre a cada 15 minutos
  - A quantidade do estoque a ser sincronizada para o Olist é definida pela _Política de estoque_
    - **Todo o estoque:** considera todo o estoque disponível _(Estoque físico - Estoque reservado)_ nas empresas 1 e 31 e aplica a fórmula
      > **Estoque do produto = Estoque disponível**
    - **Apenas validade curta:** considera apenas os lotes com validade <= 365 dias (1 ano) e aplica a fórmula
      > Se Lote com validade curta, então **Estoque do produto = Estoque disponível**. Se não, Estoque do produto = 0
    - **Regra de barreira:** considera uma porcentagem sobre o valor do estoque mínimo do produto, ou um valor absoluto
      - **Usar valor padrão:** considera 10% sobre o estoque mínimo e aplica a fórmula
        > Se Estoque disponível > Estoque mínimo + 10%, então **Estoque do produto = Estoque disponível - (Estoque mínimo + 10%)**. Se não, Estoque do produto = 0
      - **Usar valor personalizado:**
        - **Tipo de barreira:**
          - **Porcentagem:** considera o valor informado no campo _Valor barreira de estoque_ sobre o estoque mínimo e aplica a fórmula
            > Se Estoque disponível > Estoque mínimo + Valor%, então **Estoque do produto = Estoque disponível - (Estoque mínimo + Valor%)**. Se não, Estoque do produto = 0
          - **Quantidade:** considera o valor informado no campo _Valor barreira de estoque_ como ponto de corte e aplica a fórmula
            > Se Estoque disponível > Valor, então **Estoque do produto = Estoque disponível - Valor**. Se não, Estoque do produto = 0
  - O valor padrão para Política de estoque é _Todo o estoque_
  - Ao ser sincronizado pela primeira vez, é realizado um movimento de _Balanço_ que envia o estoque atual do produto, de acordo com a Política de estoque definida, para o Olist
  - A sincronização consiste em:
    1. Buscar na tabela temporária os produtos que tiveram alteração de estoque desde a última sincronização
    2. Consultar o estoque atual na Olist via API
    3. Comparar o saldo das aplicaçãoes
    4. Gera movimento de entrada ou saída no Olist de acordo com a diferença encontrada
    - Obs.: a sincronização Olist > Sankhya ocorre na importação dos pedidos, onde o próprio Sankhya já tem implementada a atualização do saldo nos estoques

- 🛒 **Importação de pedidos:** _Importa os pedidos realizados no Olist para o Sankhya, gerando automaticamente os registros internos._
  - O Olist recebe os pedidos dos marketplaces, que por sua vez são sincronizados para o Sankhya a fim de manter os dados de venda atualizados no ERP
  - Cada status do pedido no Olist gera uma ação de sincronização para o Sankhya conforme abaixo:
    1. **<span style="color:limegreen">Pedido aprovado</span>:** o pedido recebe o status _Aprovado_ no Olist mediante confirmação da disponibilidade de estoque do item e do pagamento do pedido no marketplace. _Nesta etapa, o pedido é importado no Sankhya gerando um Pedido de Venda na empresa 31 para o cliente Shopee Storya_
    2. **<span style="color:cyan">Pedido preparando envio</span>:** o pedido recebe o status _Preparando Envio_ no Olist quando é feita a ação de _Gerar nota fiscal_. Este gatilho cria a NF e envia o pedido para o módulo de Separação/Embalagem no Olist. _Nesta etapa, o Pedido de Venda é confirmado no Sankhya_
    3. **<span style="color:royalblue">Pedido faturado</span>:** o pedido recebe o status _Faturado_ no Olist após a conclusão da Separação/Embalagem, que dispara a autorização da NFe na Sefaz. _Nesta etapa o respectivo Pedido de Venda no Sankhya tem a informação de Lote/Validade dos produtos sincronizada_.
    4. A partir disso, os itens com seus lotes e quantidades são adicionados a uma Nota de Transferência da empresa 1 para 31 no Sankhya, a qual será confirmada no final de cada turno. Após a confirmação, os Pedidos de Venda são faturados e suas respectivas Notas são geradas, os dados da NFe são importados do Olist e as Notas são confirmadas no Sankhya.

- 🧠 **Logs e relatórios:** _Registro de todas as operações, com detalhes para auditoria e rastreabilidade._
  - O histórico de ações realizadas pelo integrador fica disponível no _Painel de Controle > aba lateral > seção Logs._
  ![Log de eventos do integrador](docs/img/logs.png)

## 👨‍💻 Como Usar

### Execução agendada:
- A integração é executada via agendador de tarefas conforme abaixo:
  - **Produtos:** diariamente, às 08h30 e 13h30
  - **Estoque:** diariamente, a cada 15 minutos
  - **Pedidos:** diariamente, a cada 30 minutos

### Execução manual:
  - Acesse o Painel de Controle e selecione o tipo de sincronização para executar
  ![Painel de Controle do integrador](docs/img/painel.png)

## 💡 Dúvidas Frequentes (FAQ)

- **😕 O que acontece se a conexão com um dos sistemas falhar?**\
  👉 O sistema registra o erro no log e tenta novamente na próxima execução agendada.

- **😕 Há risco de pedidos duplicados?**\
  👉 Não. O sistema verifica os IDs únicos dos pedidos no Olist e no Sankhya antes de importar.

- **😕 O que fazer caso o integrador trave?**\
  👉 Sim. Comunique o setor de Informática via Agidesk solicitando a reinicialização do serviço.

- **😕 É possível pausar a integração?**\
  👉 Sim. Comunique o setor de Informática via Agidesk solicitando interrupção do serviço.

## ℹ️ Manutenção e Suporte

- **Suporte:** Entre em contato pelo e-mail [**ti@grupoeisen.com.br**](mailto\:ti@grupoeisen.com.br) ou pelo Agidesk _Tecnologia da Informação > Sistemas > Erro do sistema_.

---
---

## 📄 Licença e Termos

Uso interno restrito. Proibida a distribuição sem autorização da empresa.

