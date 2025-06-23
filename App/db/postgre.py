import psycopg2
import psycopg2.extras #Esse modulo permite a gente obter um dicionario quando fazemos um select,
#dai ao inves de precisarmos saber qual a posicao da coluna na lista, podemos so fazer
#"nome_variavel"["name"], embaixo, dentro do try, tem um exemplo.

hostname = 'localhost'
database = 'BDExtensao'
username = 'postgres'
pwd = 'adminext'
port_id = 5432
conn = None
cur = None

try:
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    #exemplo
    cur.execute("SELECT * FROM tb_aluno")
    for record in cur.fetchall():
        print(record["name"])


except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()