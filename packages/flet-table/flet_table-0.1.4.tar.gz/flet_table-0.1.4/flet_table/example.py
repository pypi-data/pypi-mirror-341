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

def main_page(page: ft.Page, role_id: int):
    page.title = 'Shop'
    page.clean()
    
    if role_id == 1:  # Менеджер
        page.add(ft.Text("Добро пожаловать, Менеджер!", size=24, weight="bold"))
        # Здесь можно добавить функционал для менеджера
        page.add(ft.ElevatedButton("Управление товарами", on_click=lambda e: print("Управление товарами")))
        page.add(ft.ElevatedButton("Просмотр статистики", on_click=lambda e: print("Просмотр статистики")))
        
    elif role_id == 2:  # Обычный пользователь
        page.add(ft.Text("Добро пожаловать, Пользователь!", size=24, weight="bold"))
        # Здесь можно добавить функционал для пользователя
        page.add(ft.ElevatedButton("Просмотр товаров", on_click=lambda e: print("Просмотр товаров")))
        page.add(ft.ElevatedButton("Моя корзина", on_click=lambda e: print("Моя корзина")))
    
    page.add(ft.ElevatedButton("Выйти", on_click=lambda e: login_page(page)))

def login_page(page: ft.Page):
    page.title = 'login_page'
    page.clean()
    page.add(ft.Text('Вход в приложение', size=24, weight="bold"))
    
    username = ft.TextField(label='Логин', width=300)
    password = ft.TextField(
        label='Пароль', 
        password=True, 
        can_reveal_password=True,
        width=300
    )

    def log_user(e):
        with connection.cursor() as cursor: 
            cursor.execute("SELECT * FROM user WHERE username = %s", (username.value,))
            user_data = cursor.fetchone() 
            
            if user_data is None: 
                page.snack_bar = ft.SnackBar(ft.Text("Пользователь не найден!"))
                page.snack_bar.open = True
                page.update()
            else:
                # Проверка пароля (заглушка, нужно реализовать проверку хеша)
                if password.value == "":  # Здесь должна быть проверка хеша пароля
                    user.user_id = user_data[0]  # предполагаем, что id в первом столбце
                    user.role_id = user_data[4]  # предполагаем, что role_id в пятом столбце
                    main_page(page, user.role_id)
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Неверный пароль!"))
                    page.snack_bar.open = True
                    page.update()

    login_button = ft.ElevatedButton('Войти', on_click=log_user, width=300)
    
    page.add(
        ft.Column([
            username,
            password,
            login_button,
            ft.TextButton("Зарегистрироваться", on_click=lambda e: create_page(page))
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
        )
    )

def create_page(page: ft.Page):
    page.title = 'create_page'
    page.clean()
    page.add(ft.Text('Регистрация', size=24, weight="bold"))
    
    username = ft.TextField(label='Логин', width=300)
    password = ft.TextField(
        label='Пароль', 
        password=True, 
        can_reveal_password=True,
        width=300
    )
    confirm_password = ft.TextField(
        label='Подтвердите пароль', 
        password=True, 
        can_reveal_password=True,
        width=300
    )

    def register_user(e):
        if password.value != confirm_password.value:
            page.snack_bar = ft.SnackBar(ft.Text("Пароли не совпадают!"))
            page.snack_bar.open = True
            page.update()
            return
            
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO user (username, password, role_id) VALUES (%s, %s, 2)",
                    (username.value, create_password_hash(password.value))  # Хеширование пароля
                )
                connection.commit()
                page.snack_bar = ft.SnackBar(ft.Text("Регистрация успешна!"))
                page.snack_bar.open = True
                login_page(page)
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка: {str(ex)}"))
                page.snack_bar.open = True
                page.update()

    register_button = ft.ElevatedButton('Зарегистрироваться', on_click=register_user, width=300)
    back_button = ft.TextButton("Назад к входу", on_click=lambda e: login_page(page))
    
    page.add(
        ft.Column([
            username,
            password,
            confirm_password,
            register_button,
            back_button
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
        )
    )

if __name__ == '__main__':
    ft.app(login_page)