AUTH_URL           = 'https://accounts.tiny.com.br/realms/tiny/protocol/openid-connect'
API_URL            = 'https://api.tiny.com.br/public-api/v3'
REDIRECT_URI       = 'https://eisen-rodrigovieira.github.io/authApi/'
ENDPOINT_TOKEN     = '/token'
ENDPOINT_PRODUTOS  = '/produtos'
ENDPOINT_ESTOQUES  = '/estoque'
ENDPOINT_PEDIDOS   = '/pedidos'
ENDPOINT_SEPARACAO = '/separacao'
ENDPOINT_NOTAS     = '/notas'
ENDPOINT_CLIENTES  = '/contatos'
PATH_TOKENS        = 'json/tokens_history.json'
PATH_LOGS          = 'src/logs/olistApi.log'
PATH_DOCS          = 'docs/documentacao.md'
LOGGER_FORMAT      = '%(asctime)s | %(levelname)s | %(name)s line:%(lineno)d >> %(message)s'
REQ_TIME_SLEEP     = 1.5
TASKS              = ['Olist - Aplicação','Olist - Integra estoque','Olist - Integra pedidos','Olist - Integra produtos']
TASK_TIME          = ["5M","10M","15M","30M","1H","1D"]

