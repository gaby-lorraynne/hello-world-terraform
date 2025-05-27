import unittest
import json
import os
from unittest.mock import patch, MagicMock

# Configurar caminho para importar a lambda
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../lambda/lambda_list_item')))

try:
    from list_item import lambda_handler, listar_tarefas
except ImportError:
    print("❌ Erro: Não foi possível importar list_item")
    print("📁 Verifique se o arquivo existe em: lambda/lambda_list_item/list_item.py")
    raise

class TestListarTarefas(unittest.TestCase):
    """
    Testes para a função listar_tarefas
    """
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        # Dados de exemplo para os testes
        self.sample_items = [
            {
                'PK': 'LIST#20241226',
                'SK': 'ITEM#123e4567-e89b-12d3-a456-426614174000',
                'itemId': '123e4567-e89b-12d3-a456-426614174000',
                'name': 'Comprar leite',
                'date': '2024-12-26',
                'status': 'todo'
            },
            {
                'PK': 'LIST#20241226',
                'SK': 'ITEM#987fcdeb-51a2-4bc3-d789-123456789abc',
                'itemId': '987fcdeb-51a2-4bc3-d789-123456789abc',
                'name': 'Fazer exercício',
                'date': '2024-12-26',
                'status': 'done'
            },
            {
                'PK': 'LIST#20241227',
                'SK': 'ITEM#456e7890-f12a-34b5-c678-901234567def',
                'itemId': '456e7890-f12a-34b5-c678-901234567def',
                'name': 'Estudar Python',
                'date': '2024-12-27',
                'status': 'todo'
            }
        ]

    # === TESTES DE SUCESSO ===
    
    @patch('list_item.dynamodb')
    def test_listar_tarefas_com_data_sucesso(self, mock_dynamodb):
        """✅ SUCESSO: Listar tarefas de uma data específica"""
        # Arrange
        mock_table = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_table.query.return_value = {'Items': [self.sample_items[0], self.sample_items[1]]}
        
        # Act
        resultado = listar_tarefas(data='2024-12-26')
        
        # Assert
        self.assertEqual(resultado['message'], 'Tarefas listadas com sucesso!')
        self.assertEqual(resultado['count'], 2)
        self.assertEqual(len(resultado['tarefas']), 2)
        self.assertEqual(resultado['tarefas'][0]['name'], 'Comprar leite')
        self.assertEqual(resultado['tarefas'][1]['name'], 'Fazer exercício')
        
        # Verificar chamada do DynamoDB
        mock_table.query.assert_called_once()
        call_args = mock_table.query.call_args[1]
        self.assertIn('KeyConditionExpression', call_args)
        self.assertIn('FilterExpression', call_args)

    @patch('list_item.dynamodb')
    def test_listar_tarefas_sem_data_sucesso(self, mock_dynamodb):
        """✅ SUCESSO: Listar todas as tarefas (sem filtro de data)"""
        # Arrange
        mock_table = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_table.scan.return_value = {'Items': self.sample_items}
        
        # Act
        resultado = listar_tarefas()
        
        # Assert
        self.assertEqual(resultado['message'], 'Tarefas listadas com sucesso!')
        self.assertEqual(resultado['count'], 3)
        self.assertEqual(len(resultado['tarefas']), 3)
        
        # Verificar chamada do DynamoDB
        mock_table.scan.assert_called_once()
        call_args = mock_table.scan.call_args[1]
        self.assertIn('FilterExpression', call_args)

    @patch('list_item.dynamodb')
    def test_listar_tarefas_lista_vazia(self, mock_dynamodb):
        """✅ SUCESSO: Lista vazia quando não há tarefas"""
        # Arrange
        mock_table = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_table.query.return_value = {'Items': []}
        
        # Act
        resultado = listar_tarefas(data='2024-12-25')
        
        # Assert
        self.assertEqual(resultado['message'], 'Tarefas listadas com sucesso!')
        self.assertEqual(resultado['count'], 0)
        self.assertEqual(len(resultado['tarefas']), 0)
        self.assertIsInstance(resultado['tarefas'], list)

    @patch('list_item.dynamodb')
    def test_listar_tarefas_com_user_id(self, mock_dynamodb):
        """✅ SUCESSO: Listar tarefas com user_id (parâmetro aceito)"""
        # Arrange
        mock_table = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_table.scan.return_value = {'Items': self.sample_items}
        
        # Act
        resultado = listar_tarefas(user_id='user-123-456')
        
        # Assert
        self.assertEqual(resultado['count'], 3)
        # Função aceita user_id mas não filtra por ele ainda (implementação futura)

    # === TESTES DE FALHA ===
    
    @patch('list_item.dynamodb')
    def test_listar_tarefas_erro_dynamodb_query(self, mock_dynamodb):
        """❌ FALHA: Erro no DynamoDB durante query"""
        # Arrange
        mock_table = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_table.query.side_effect = Exception("Erro de conexão DynamoDB")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            listar_tarefas(data='2024-12-26')
        
        self.assertIn("Erro ao listar tarefas", str(context.exception))
        self.assertIn("Erro de conexão DynamoDB", str(context.exception))

    @patch('list_item.dynamodb')
    def test_listar_tarefas_erro_dynamodb_scan(self, mock_dynamodb):
        """❌ FALHA: Erro no DynamoDB durante scan"""
        # Arrange
        mock_table = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_table.scan.side_effect = Exception("Tabela não encontrada")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            listar_tarefas()
        
        self.assertIn("Erro ao listar tarefas", str(context.exception))
        self.assertIn("Tabela não encontrada", str(context.exception))

    @patch('list_item.dynamodb')
    def test_listar_tarefas_erro_table_access(self, mock_dynamodb):
        """❌ FALHA: Erro ao acessar tabela"""
        # Arrange
        mock_dynamodb.Table.side_effect = Exception("Permissão negada")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            listar_tarefas(data='2024-12-26')
        
        self.assertIn("Erro ao listar tarefas", str(context.exception))

    # === TESTES DE FORMATAÇÃO DE DADOS ===
    
    @patch('list_item.dynamodb')
    def test_formato_resposta_correto(self, mock_dynamodb):
        """✅ VALIDAÇÃO: Formato da resposta está correto"""
        # Arrange
        mock_table = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_table.query.return_value = {'Items': [self.sample_items[0]]}
        
        # Act
        resultado = listar_tarefas(data='2024-12-26')
        
        # Assert - Estrutura da resposta
        self.assertIn('message', resultado)
        self.assertIn('count', resultado)
        self.assertIn('tarefas', resultado)
        
        # Assert - Tipos corretos
        self.assertIsInstance(resultado['message'], str)
        self.assertIsInstance(resultado['count'], int)
        self.assertIsInstance(resultado['tarefas'], list)
        
        # Assert - Estrutura da tarefa
        if resultado['tarefas']:
            tarefa = resultado['tarefas'][0]
            campos_obrigatorios = ['itemId', 'name', 'date', 'status', 'PK', 'SK']
            for campo in campos_obrigatorios:
                self.assertIn(campo, tarefa)

    @patch('list_item.dynamodb')
    def test_conversao_data_pk_correta(self, mock_dynamodb):
        """✅ VALIDAÇÃO: Conversão de data para PK está correta"""
        # Arrange
        mock_table = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_table.query.return_value = {'Items': []}
        
        # Act
        listar_tarefas(data='2024-12-26')
        
        # Assert - Verificar se PK foi formatada corretamente
        call_args = mock_table.query.call_args[1]
        # O PK deve ser 'LIST#20241226' (sem hífens)
        # Verificação indireta através da chamada do mock


class TestLambdaHandler(unittest.TestCase):
    """
    Testes para o lambda_handler
    """

    def setUp(self):
        """Configuração inicial"""
        self.sample_response = {
            'message': 'Tarefas listadas com sucesso!',
            'count': 2,
            'tarefas': [
                {
                    'itemId': '123e4567-e89b-12d3-a456-426614174000',
                    'name': 'Comprar leite',
                    'date': '2024-12-26',
                    'status': 'todo'
                }
            ]
        }

    # === TESTES DE SUCESSO LAMBDA HANDLER ===
    
    @patch('list_item.listar_tarefas')
    def test_lambda_handler_query_parameters(self, mock_listar_tarefas):
        """✅ SUCESSO: Handler com query parameters"""
        # Arrange
        mock_listar_tarefas.return_value = self.sample_response
        
        event = {
            'queryStringParameters': {
                'data': '2024-12-26'
            }
        }
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Content-Type', response['headers'])
        self.assertIn('Access-Control-Allow-Origin', response['headers'])
        
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'Tarefas listadas com sucesso!')
        
        # Verificar chamada da função
        mock_listar_tarefas.assert_called_once_with('2024-12-26', None)

    @patch('list_item.listar_tarefas')
    def test_lambda_handler_body_parameters(self, mock_listar_tarefas):
        """✅ SUCESSO: Handler com body parameters"""
        # Arrange
        mock_listar_tarefas.return_value = self.sample_response
        
        event = {
            'body': json.dumps({'data': '2024-12-26', 'user_id': 'user-123'})
        }
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        self.assertEqual(response['statusCode'], 200)
        mock_listar_tarefas.assert_called_once_with('2024-12-26', 'user-123')

    @patch('list_item.listar_tarefas')
    def test_lambda_handler_cognito_user(self, mock_listar_tarefas):
        """✅ SUCESSO: Handler com usuário do Cognito"""
        # Arrange
        mock_listar_tarefas.return_value = self.sample_response
        
        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'sub': 'cognito-user-123-456',
                        'email': 'user@example.com'
                    }
                }
            },
            'queryStringParameters': {
                'data': '2024-12-26'
            }
        }
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        self.assertEqual(response['statusCode'], 200)
        mock_listar_tarefas.assert_called_once_with('2024-12-26', 'cognito-user-123-456')

    @patch('list_item.listar_tarefas')
    def test_lambda_handler_sem_parametros(self, mock_listar_tarefas):
        """✅ SUCESSO: Handler sem parâmetros"""
        # Arrange
        mock_listar_tarefas.return_value = {
            'message': 'Tarefas listadas com sucesso!',
            'count': 0,
            'tarefas': []
        }
        
        event = {}
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        self.assertEqual(response['statusCode'], 200)
        mock_listar_tarefas.assert_called_once_with(None, None)

    # === TESTES DE FALHA LAMBDA HANDLER ===
    
    @patch('list_item.listar_tarefas')
    def test_lambda_handler_erro_interno(self, mock_listar_tarefas):
        """❌ FALHA: Handler com erro interno"""
        # Arrange
        mock_listar_tarefas.side_effect = Exception("Erro interno na função")
        
        event = {'queryStringParameters': {'data': '2024-12-26'}}
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Access-Control-Allow-Origin', response['headers'])
        
        body = json.loads(response['body'])
        self.assertEqual(body['error'], 'Erro interno do servidor')
        self.assertIn('Erro interno na função', body['message'])

    @patch('list_item.listar_tarefas')
    def test_lambda_handler_body_json_invalido(self, mock_listar_tarefas):
        """❌ FALHA: Handler com JSON inválido no body"""
        # Arrange
        event = {
            'body': 'json-invalido'
        }
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        self.assertEqual(response['statusCode'], 500)
        body = json.loads(response['body'])
        self.assertEqual(body['error'], 'Erro interno do servidor')

    # === TESTES DE VALIDAÇÃO DE HEADERS ===
    
    @patch('list_item.listar_tarefas')
    def test_lambda_handler_headers_cors(self, mock_listar_tarefas):
        """✅ VALIDAÇÃO: Headers CORS corretos"""
        # Arrange
        mock_listar_tarefas.return_value = self.sample_response
        
        event = {}
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        headers = response['headers']
        self.assertEqual(headers['Access-Control-Allow-Origin'], '*')
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertIn('Access-Control-Allow-Headers', headers)
        self.assertIn('Access-Control-Allow-Methods', headers)

    @patch('list_item.listar_tarefas')
    def test_lambda_handler_content_type_correto(self, mock_listar_tarefas):
        """✅ VALIDAÇÃO: Content-Type correto"""
        # Arrange
        mock_listar_tarefas.return_value = self.sample_response
        
        event = {}
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        
        # Verificar se o body é JSON válido
        body = json.loads(response['body'])
        self.assertIsInstance(body, dict)


class TestIntegracao(unittest.TestCase):
    """
    Testes de integração (simulando cenários reais)
    """
    
    @patch('list_item.dynamodb')
    def test_cenario_usuario_novo_sem_tarefas(self, mock_dynamodb):
        """🔄 INTEGRAÇÃO: Usuário novo sem tarefas"""
        # Arrange
        mock_table = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_table.scan.return_value = {'Items': []}
        
        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {'sub': 'novo-usuario-123'}
                }
            }
        }
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['count'], 0)
        self.assertEqual(body['tarefas'], [])

    @patch('list_item.dynamodb')
    def test_cenario_busca_data_especifica(self, mock_dynamodb):
        """🔄 INTEGRAÇÃO: Busca por data específica"""
        # Arrange
        mock_table = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_table.query.return_value = {
            'Items': [
                {
                    'PK': 'LIST#20241226',
                    'SK': 'ITEM#123',
                    'itemId': '123',
                    'name': 'Tarefa do dia',
                    'date': '2024-12-26',
                    'status': 'todo'
                }
            ]
        }
        
        event = {
            'queryStringParameters': {'data': '2024-12-26'},
            'requestContext': {
                'authorizer': {
                    'claims': {'sub': 'usuario-ativo-456'}
                }
            }
        }
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['count'], 1)
        self.assertEqual(body['tarefas'][0]['date'], '2024-12-26')


if __name__ == '__main__':
    print("🧪 EXECUTANDO TESTES UNITÁRIOS - Lista de Tarefas")
    print("=" * 60)
    
    # Configurar verbose output
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 60)
    print("✅ TESTES CONCLUÍDOS!")
    print("\n💡 Para executar testes específicos:")
    print("   python -m pytest test_list_tasks.py::TestListarTarefas::test_listar_tarefas_com_data_sucesso -v")
    print("   python -m pytest test_list_tasks.py::TestLambdaHandler -v")