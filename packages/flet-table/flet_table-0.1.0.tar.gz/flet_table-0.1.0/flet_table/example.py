import flet as ft 
from dataclasses import dataclass
from typing import Optional
from flet_table.table import create_flet_table, create_image_table
import pymysql 
from flet_table.hash_pass_window import check_password_hash, create_password_hash

connection = pymysql.connect(
    **{
    'host': 'yourlocalhost',
    'database': 'yourdb',
    'user': 'youruser',
    'password': 'yourpassword',
    'charset': 'utf8mb4'
}
)

@dataclass
class User: 
    user_id : Optional[int] = None 
    role_id : Optional[int] = None 

user = User() 

def main_page(page : ft.Page):
    page.title = 'Shop'

def login_page(page : ft.Page):
    page.title = 'login_page'
    page.add(ft.Text('Зайти в приложение'))
    username = ft.TextField(hint_text='username')
    password = ft.TextField(hint_text='password', password=True, can_reveal_password=True, autofocus=True)

    def log_user(e):
        with connection.cursor() as cursor: 
            cursor.execute(f'select * from user where username = {username}')
            user = cursor.fetchone() 
            if user is None: 
                page.add(ft.AlertDialog(
                title=ft.Text("Hi, this is a non-modal dialog!"),
                on_dismiss=lambda e: page.add(ft.Text("Non-modal dialog dismissed")),
                ))
                page.update() 
            else:


    button = ft.Button('Войти', on_click=)
    page.add(ft.Container(username))
    page.add(ft.Container(password))
    
    

def create_page(page : ft.Page):
    page.title = 'create_page'
    page.add(ft.Text('Зайти в приложение'))
    username = ft.TextField(hint_text='username')
    password = ft.TextField(hint_text='password', password=True, can_reveal_password=True, autofocus=True)
    page.add(ft.Container(username))
    button = ft.Button('Зарегестрироваться', on_click=)
    page.add(ft.Container(password))





if __name__ == '__main__':
    ft.app(login_page)