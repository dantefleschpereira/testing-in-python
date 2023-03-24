import unittest
import mysql.connector
import pysolr


class TestMySQLToSolr(unittest.TestCase):

    def setUp(self):
        # Conectar ao banco de dados de teste
        self.cnx = mysql.connector.connect(user=user, password=password,
                                           host=host,
                                           database=database)
        self.cursor = self.cnx.cursor()

        # Configurar o servidor Solr local
        self.solr = pysolr.Solr(
            'http://localhost:8983/solr/core_test', always_commit=True)

    def tearDown(self):
        # Excluir os dados de teste do Solr
        self.solr.delete(q='*:*')

    def test_mysql_to_solr(self):
        # Extrair dados do banco MySQL
        self.cursor.execute("SELECT * FROM table_test")
        data = [{'sistema': row[0], 'numero': row[1]} for row in self.cursor]

        # Transformar dados para o formato do Solr
        solr_data = [{'sistema_s': str(item['sistema']), 'numero_s': item['numero']}
                     for item in data]

        # Carregar dados no Solr
        self.solr.add(solr_data)

        # Verificar se os dados foram carregados corretamente no Solr
        results = self.solr.search(q='*:*', fl='sistema_s,numero_s')

        # Testar quantidade de registros
        self.assertEqual(len(results), len(data))

        # Testar conteúdo dos registros
        for i, result in enumerate(results):
            self.assertEqual(str(result['sistema_s']), str(data[i]['sistema']))
            self.assertEqual(str(result['numero_s']), str(data[i]['numero']))


if __name__ == '__main__':
    unittest.main()
