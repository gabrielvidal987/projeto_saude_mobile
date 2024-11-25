import flet as ft
import threading
import time
import mysql.connector
import requests
import json

usuario = None
password = None
ip_request = None
page_flet = None
    
# Realiza um request para resgatar os dados de todos os usuarios
def request_get_usuarios():
    url = f"http://{ip_request}:3000/api/usuarios"  # Substitua pela URL do seu servidor
    try:
        # Faz a requisição GET para o endpoint
        response = requests.get(url)
        # Verifica se a resposta foi bem-sucedida (status code 200)
        if response.status_code == 200:
            # Retorna os dados recebidos (em formato JSON)
            return response.json()
        else:
            # Caso o status não seja 200, retorna o erro
            print(f"Erro ao fazer requisição. Status code: {response.status_code}")
            return None
    except Exception as e:
        # Captura qualquer exceção que ocorrer durante a requisição
        print(f"Ocorreu um erro ao fazer a requisição: {str(e)}")
        return None
    
# Realiza o request para poder alterar a senha de um usuario
def request_alterar_senha(id_sys, nome, nova_senha):
    url = f"http://{ip_request}:3000/api/alterarsenha"  # Substitua pela URL do seu servidor
    payload = {
        "id_sys": id_sys,
        "nome": nome,
        "nova_senha": nova_senha
    }
    try:
        # Envia a requisição PUT com os dados (payload) no corpo da requisição
        response = requests.put(url, json=payload)
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Retorna a resposta JSON
            return response.json()
        else:
            # Caso o status não seja 200, imprime o erro
            print(f"Erro ao alterar senha. Status code: {response.status_code}")
            return None
    except Exception as e:
        # Caso ocorra uma exceção (por exemplo, erro de rede)
        print(f"Ocorreu um erro ao fazer a requisição: {str(e)}")
        return None
  
# Realiza o request para poder criar um usuário
def request_criar_usuario(nome, senha, nivel_acesso):
    url = f"http://{ip_request}:3000/api/novousuario"  # Substitua pela URL do seu servidor
    payload = {
        "nome": nome,
        "senha": senha,
        "nivel_acesso": nivel_acesso,
    }
    try:
        # Envia a requisição POST com os dados (payload) no corpo da requisição
        response = requests.post(url, json=payload)
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Retorna a resposta JSON
            return response.json()
        else:
            # Caso o status não seja 200, imprime o erro
            print(f"Erro ao criar usuario. Status code: {response.status_code}")
            return None
    except Exception as e:
        # Caso ocorra uma exceção (por exemplo, erro de rede)
        print(f"Ocorreu um erro ao fazer a requisição: {str(e)}")
        return None
    
# Realiza o request para deletar um usuário
def request_deletar_usuario(id,nome):
    url = f"http://{ip_request}:3000/api/deletarusuario"  # Substitua pela URL do seu servidor
    payload = {
        "id_sys": id,
        "nome": nome,
    }
    try:
        # Envia a requisição POST com os dados (payload) no corpo da requisição
        response = requests.delete(url, json=payload)
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Retorna a resposta JSON
            return response.json()
        else:
            # Caso o status não seja 200, imprime o erro
            print(f"Erro ao apagar usuario. Status code: {response.status_code}")
            return None
    except Exception as e:
        # Caso ocorra uma exceção (por exemplo, erro de rede)
        print(f"Ocorreu um erro ao fazer a requisição: {str(e)}")
        return None
    
# Cria os containers
def dados_connect():
    global page_flet
    alert = ft.AlertDialog(
        title=ft.Text("Preencha todos os campos!")
    )
    def atualiza_tabela_usuarios():
        dados_usuarios = request_get_usuarios()
        if dados_usuarios:
            lista_usuarios = []
            for dados in dados_usuarios:
                lista_usuarios.append(ft.DataRow(
                    cells=[
                            ft.DataCell(ft.Text(value=dados["id_sys"],color="#ffffff")),
                            ft.DataCell(ft.Text(value=dados["nome"],color="#ffffff")),
                            ft.DataCell(ft.Text(value=dados["nivel_acesso"],color="#ffffff")),
                            ft.DataCell(ft.ElevatedButton('ALTERAR SENHA',icon=ft.icons.CREATE,on_click=lambda e, dados_usuario=dados: area_alterar_senha(e, dados_usuario))),
                            ft.DataCell(ft.ElevatedButton('DELETAR',icon=ft.icons.DELETE,on_click=lambda e, dados_usuario=dados: area_deletar_usuario(e, dados_usuario)))
                    ]
                ))
            tabela_usuarios.rows = lista_usuarios
        
    def acessa(e):
        global usuario,password,ip_request
        if usuario_input.value and senha_input.value:
            container_connect.padding = 25
            container_connect.margin = ft.margin.only(left=15,top=15,right=15,bottom=40)
            ip_request = ip_input.value
            container_connect.content.controls.pop()
            container_connect.content.controls.append(ft.ProgressRing())
            page_flet.update()
            time.sleep(3)
            atualiza_tabela_usuarios()
            container_connect.content = usuarios_content
        else:
            page_flet.open(alert)
        page_flet.update()

    def area_criar_usuario(e):
        cadastra_usuario_content.controls[0].value = ''
        cadastra_usuario_content.controls[1].value = ''
        container_connect.content = cadastra_usuario_content
        page_flet.update()
        
    def area_alterar_senha(e,dados_usuario):
        alterar_senha_content.controls[0].value = dados_usuario["id_sys"]
        alterar_senha_content.controls[1].value = dados_usuario["nome"]
        alterar_senha_content.controls[2].value = ""
        container_connect.content = alterar_senha_content
        page_flet.update()
        
    def area_deletar_usuario(e,dados_usuario):
        deletar_usuario_content.controls[0].value = dados_usuario["id_sys"]
        deletar_usuario_content.controls[1].value = dados_usuario["nome"]
        container_connect.content = deletar_usuario_content
        page_flet.update()
        
    def cadastra_usuario(e):
        nome = cadastra_usuario_content.controls[0].value
        senha = cadastra_usuario_content.controls[1].value
        nivel_acesso = cadastra_usuario_content.controls[2].value
        if request_criar_usuario(nome,senha,nivel_acesso):
            atualiza_tabela_usuarios()
            alert.title = ft.Text("Usuário cadastrado com sucesso! ")
            page_flet.open(alert)
            container_connect.content = usuarios_content
            page_flet.update()
        else:
            alert.title = ft.Text("Erro ao criar usuario. Tente novamente! ")
            page_flet.open(alert)
        
    def alterar_senha(e):
        id = alterar_senha_content.controls[0].value
        nome = alterar_senha_content.controls[1].value
        senha = alterar_senha_content.controls[2].value
        if request_alterar_senha(id,nome,senha):
            alert.title = ft.Text("Senha de usuário alterada com sucesso! ")
            page_flet.open(alert)
            container_connect.content = usuarios_content
            page_flet.update()
        else:
            alert.title = ft.Text("Erro ao alterar senha. Tente novamente! ")
            page_flet.open(alert)
            
    def deletar_usuario(e):
        id = deletar_usuario_content.controls[0].value
        nome = deletar_usuario_content.controls[1].value
        if request_deletar_usuario(id,nome):
            alert.title = ft.Text("Usuário deletado com sucesso! ")
            page_flet.open(alert)
            atualiza_tabela_usuarios()
            container_connect.content = usuarios_content
            page_flet.update()
        else:
            alert.title = ft.Text("Erro ao deletar usuario. Tente novamente! ")
            page_flet.open(alert)
            
    usuario_input = ft.TextField(label="Usuário",text_align=ft.TextAlign.CENTER,color="#ffffff",label_style=ft.TextStyle(size=20,color="#7a7b7c"),text_size=20,on_submit=acessa)
    ip_input = ft.TextField(label="IP",text_align=ft.TextAlign.CENTER,color="#ffffff",label_style=ft.TextStyle(size=20,color="#7a7b7c"),text_size=20,on_submit=acessa)
    senha_input = ft.TextField(label="Senha",text_align=ft.TextAlign.CENTER,color="#ffffff",label_style=ft.TextStyle(size=20,color="#7a7b7c"),text_size=20,on_submit=acessa,password=True)
    tabela_usuarios = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("NOME")),
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("ACESSO")),
            ft.DataColumn(ft.Text("ALTERAR SENHA")),
            ft.DataColumn(ft.Text("DELETAR"))
    ])

    usuarios_content = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("USUARIOS",text_align=ft.TextAlign.CENTER,color=ft.colors.AMBER,size=25),
                    ft.ElevatedButton('CRIAR USUARIO',icon=ft.icons.EXPOSURE_PLUS_1,on_click=area_criar_usuario)            
                    ],scroll=ft.ScrollMode.ALWAYS),
            ft.Row(
                controls=[tabela_usuarios],
                scroll=ft.ScrollMode.ALWAYS
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        height=500,
        width=10,
        scroll=ft.ScrollMode.ALWAYS,
    )
    
    cadastra_usuario_content = ft.Column(
        controls=[
            ft.TextField(label="Nome do usuário",text_align=ft.TextAlign.CENTER,color="#ffffff",label_style=ft.TextStyle(size=20,color="#7a7b7c"),text_size=20),
            ft.TextField(label="Senha de usuário",text_align=ft.TextAlign.CENTER,color="#ffffff",label_style=ft.TextStyle(size=20,color="#7a7b7c"),text_size=20,password=True),
            ft.Dropdown(
                label="Tipo de acesso",
                bgcolor="#2f2f2f",
                color=ft.colors.AMBER,
                text_size=15,
                border_color="#00b2ff",
                options=[ft.dropdown.Option('usuario'),ft.dropdown.Option('adm')]
            ),
            ft.ElevatedButton('CADASTRAR',icon=ft.icons.EXPOSURE_PLUS_1,on_click=cadastra_usuario)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER 
    )
    
    alterar_senha_content = ft.Column(
        controls=[
            ft.TextField(label="ID do usuário",text_align=ft.TextAlign.CENTER,color="#ffffff",label_style=ft.TextStyle(size=20,color="#7a7b7c"),text_size=20,read_only=True),
            ft.TextField(label="Nome do usuário",text_align=ft.TextAlign.CENTER,color="#ffffff",label_style=ft.TextStyle(size=20,color="#7a7b7c"),text_size=20,read_only=True),
            ft.TextField(label="Senha de usuário",text_align=ft.TextAlign.CENTER,color="#ffffff",label_style=ft.TextStyle(size=20,color="#7a7b7c"),text_size=20,password=True),
            ft.ElevatedButton('ALTERAR',icon=ft.icons.CREATE,on_click=alterar_senha)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER 
    )
    
    deletar_usuario_content = ft.Column(
        controls=[
            ft.TextField(label="ID do usuário",text_align=ft.TextAlign.CENTER,color="#ffffff",label_style=ft.TextStyle(size=20,color="#7a7b7c"),text_size=20,read_only=True),
            ft.TextField(label="Nome do usuário",text_align=ft.TextAlign.CENTER,color="#ffffff",label_style=ft.TextStyle(size=20,color="#7a7b7c"),text_size=20,read_only=True),
            ft.ElevatedButton('DELETAR',icon=ft.icons.DELETE,on_click=deletar_usuario)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER 
    ) 
    
    login_content = ft.Column(
        controls=[
            ft.Text("INSIRA OS DADOS DE LOGIN",text_align=ft.TextAlign.CENTER,color=ft.colors.AMBER,size=25),
            usuario_input,
            senha_input,
            ip_input,
            ft.ElevatedButton("ACESSAR!",bgcolor=ft.colors.AMBER,color=ft.colors.BLACK,on_click=acessa,width=150,height=50)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER 
    )
        
    container_connect = ft.Container(
        bgcolor="#2f2f2f",
        margin=30,
        padding=50,
        width=2000,
        border_radius=50,
        content=login_content,
    )
    
    return container_connect

# Principal modulo, cria a pagina do flet com os dados gerais
def main(page: ft.Page) -> None:
    global page_flet
    page_flet = page
    page.title="SAÚDE MOBILE"
    page.bgcolor="#212121"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    container_connect = dados_connect()
    page.add(container_connect)  
    
if __name__ == '__main__':
    ft.app(target=main,view=ft.AppView.WEB_BROWSER,port=5000, assets_dir="assets")
    # ft.app(target=main)