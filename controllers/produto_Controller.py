import mysql.connector
from models.produto import Produto

user = "root"
senha = ""
host = "localhost"
banco = "lanchonete"

#retorna a conexâo extabelecida ou retorna None quando der errado
def conectar():
    conexao=None
    try:
        conexao =  mysql.connector.connect(
            host=host,
            user=user,
            password=senha,
            database=banco
        )
    except mysql.connector.Error as e:
        print(f"Erro ao conectar com o BD:{e}")

    return conexao

#finalizar a conexão o fim das operações
def fechar_conexao(conexao):
    if conexao.is_connected():
        conexao.close()
        print("Conexão com o BD encerrada!")
    
# C - Criar um novo registro no banc de dados
def inserir(conexao, produto):
    try:
        cursor = conexao.cursor()
        query = "INSERT INTO produto(descricao, preco, qtd) VALUES(%s ,%s ,%s)"  #usar o ''%s'' para o SQL injector
        cursor.execute(query, (produto.descricao, produto.preco, produto.qtd))
        conexao.commit()
        print(f'{produto.descricao}, registrado com sucesso!')

    except mysql.connector.Error as e:
        print(f"Erro ao inserir produto:{e}")  
    finally:
        cursor.close()

# R - Read retorna uma lista de objeto peoduto
def listar(conexao): 
    listaProdutos=[]
    try:
      cursor = conexao.cursor()
      query = "Select * from produto"
      cursor.execute(query)
      registros = cursor.fetchall()
      
      for registro in registros:
          objeto = Produto(*registro)   #Produto (registro[0], registro[1],registro[2]....)
          listaProdutos.append(objeto)
      
    except mysql.connector.Error as e:
        print(f"Erro ao listar produtos:{e}")  
    finally:
        cursor.close()
    return listaProdutos


# U - uptade - atualizar uma informação de uma linha 
def update(conexao, idProduto, valor, qtd):
    try:
        cursor = conexao.cursor()
        query = "UPDATE produto SET preco=%s, qtd=%s WHERE idProduto=%s"
        cursor.execute(query, (valor, qtd, idProduto))
        conexao.commit()
        print(f'{idProduto}, atualizado com sucesso!')

    except mysql.connector.Error as e:
        print(f"Erro ao atualizar produto:{e}")  
    finally:
        cursor.close()


# D - deleta uam linha a partir de um ID
def delete(conexao, idProduto):
    try:
        cursor = conexao.cursor()
        query = "DELETE FROM Produto WHERE idProduto= %s"
        cursor.execute(query, (idProduto,))
        conexao.commit()
        print(f'{idProduto}, excluído com sucesso!')

    except mysql.connector.Error as e:
        print(f"Erro ao excluir produto:{e}")
    finally:
        cursor.close()


#buscar informações de uma linha
def buscar(conexao, busca):
    listaProduto=[]
    try:
        cursor = conexao.cursor()
        query = "Select * from Produto WHERE descricao like %s"
        cursor.execute(query, ('%'+busca+'%',))
        registros = cursor.fetchall()
      
        for produto in registros:
          objeto = Produto(*produto)   #Produto (produto[0], produto[1],produto[2]....)
          listaProduto.append(objeto)


    except mysql.connector.Error as e:
        print(f"Erro ao buscar produto:{e}")
    finally:
        cursor.close()
    return listaProduto


##Main
conexao = conectar()

if conexao!=None:
    print("Conectado com o banco de dados")

                #  TESTES
#    inserir(conexao, 'x-salada', 16, 4)
#    update (conexao, 31, 17, 6)
#    delete (conexao, 32)  --- repetido para teste e excluido
#    buscar(conexao, 'Torta')
#    buscar(conexao, 'X')
#    print (listar(conexao))

#    produtos = listar(conexao)
#    for produto in produtos:
 #      produto.listar()
    
#    produtos = buscar(conexao, 'Chapeu')
#    if produtos!=[]:
#        for produto in produtos:
#            produto.listar()
#    else:
#        print('Nenhum produto encontrado!')

    fechar_conexao(conexao)