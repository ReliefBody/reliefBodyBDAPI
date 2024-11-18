server = 'reliefbody.database.windows.net'
database = 'ReliefBodySport-API'
username = 'reliefbodyadmin'
password = 'punqe5-zyrzoV-zuxrit'

connection_string = (
    'DRIVER={ODBC Driver 18 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
    'Connection Timeout=30;'
)