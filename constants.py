DATABASE_PATH = 'database/FundStatus.db'
DB_COLUMNS = ['Id', 'Fecha', 'Aporte', 'Participaciones', 'Valor_participacion']
FUNDS_WEB_PAGES = {
    'Kutxabank_fondo': 'https://es.investing.com/funds/kutxabank-gestion-activa-rendimient',
    'MyInvestor': 'https://es.investing.com/funds/ie00byx5mx67',
    'Kutxabank_EPSV': 'https://es.investing.com/funds/kutxabank-bolsa-global-pp',
    'BBVA_Q_Mejores_ideas': 'https://es.investing.com/funds/quality-mejores-ideas-fi',
}
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
OPTIONS_FOR_PERCENT = ['Porcentaje', 'Valor total']
OPTIONS_FOR_SPACING = ['Igualmente espaciado', 'Por fechas']