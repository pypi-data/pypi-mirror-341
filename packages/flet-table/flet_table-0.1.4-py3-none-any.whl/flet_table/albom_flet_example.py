import flet as ft
from flet_table.diagrams import Database
from datetime import datetime


def main(page: ft.Page):
    page.title = 'Фабрика окон'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    db = Database()

    greet_text = ft.Text(value='Добрый день, пройдите авторизацию', color='white', size=20)
    result_text = ft.Text(value='', color='red', size=16)
    login_input = ft.TextField(label='Введите логин', width=400)
    password_input = ft.TextField(label='Введите пароль', width=400, password=True, can_reveal_password=True)

    def show_main_page(e=None):
        page.clean()
        result_text.value = ''
        result_text.color = 'red'
        login_input.value = ''
        password_input.value = ''
        auth_button = ft.ElevatedButton('Авторизация', on_click=check_auth)

        page.add(
            ft.Column(
                [
                    greet_text,
                    login_input,
                    password_input,
                    ft.Row([
                        auth_button,
                        reg_button
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    result_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    def check_auth(e):
        login = login_input.value.strip()
        password = password_input.value.strip()

        if not login or not password:
            result_text.value = 'Введите данные для авторизации'
            page.update()
            return

        conn = None
        try:
            conn = db.connect()
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT id, fio, login, password, source_table FROM (
                        SELECT id, fio, login, password, 'user_client' as source_table FROM client
                        UNION ALL
                        SELECT id, fio, login, password, 'user_manager' as source_table FROM manager
                    ) AS ALL_USERS
                    WHERE login = %s AND password = %s;
                ''', (login, password))
                user = cursor.fetchone()
                if user:
                    if user[4] == 'user_client':
                        show_window_for_client(user[1])
                    elif user[4] == 'user_manager':
                        show_window_for_manager(user[1])
                else:
                    result_text.value = 'Неверный логин или пароль'
                    page.update()
        except Exception as e:
            result_text.value = f'Ошибка: {e}'
            page.update()
        finally:
            if conn:
                conn.close()

    def reg_window(e):
        page.clean()
        page.title = 'Окно регистрации'
        reg_password_input = ft.TextField(label='Введите пароль', width=400, can_reveal_password=True, password=True)
        reg_login_input = ft.TextField(label='Введите логин', width=400)
        reg_fio_input = ft.TextField(label='Введите ФИО', width=400)
        message_reg = ft.Text('Заполните поля для регистрации', size=20)

        def reg_client(e):
            login_reg = reg_login_input.value.strip()
            password_reg = reg_password_input.value.strip()
            fio_reg = reg_fio_input.value.strip()

            if not login_reg or not password_reg or not fio_reg:
                result_text.value = 'Введите данные'
                page.update()
                return

            conn = None
            try:
                conn = db.connect()
                with conn.cursor() as cursor:
                    cursor.execute('INSERT INTO client (fio, login, password) VALUES (%s, %s, %s)',
                                   (fio_reg, login_reg, password_reg))
                    conn.commit()
                    result_text.value = 'Регистрация прошла успешно'
                    result_text.color = 'green'
                    page.update()
            except Exception as e:
                result_text.value = f'Ошибка: {e}'
                page.update()
            finally:
                if conn:
                    conn.close()

        registration_button = ft.ElevatedButton('Зарегистрироваться', on_click=reg_client)
        back_button = ft.ElevatedButton('Назад', on_click=show_main_page)

        page.add(
            ft.Column(
                [
                    message_reg,
                    reg_fio_input,
                    reg_login_input,
                    reg_password_input,
                    ft.Row([registration_button, back_button], alignment=ft.MainAxisAlignment.CENTER),
                    result_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    def show_window_for_client(username):
        page.clean()
        page.title = 'Окно клиента'

        hello_text = ft.Text(f'Привет, {username}!', size=20)
        result_text = ft.Text('', size=16)

        image = ft.Image(
            src='photo\\Бухгалтер.jpeg',
            width=150,
            height=200,
            fit=ft.ImageFit.CONTAIN
        )

        type_dropdown = ft.Dropdown(
            label='Выберите тип окна',
            width=400,
            options=[],
        )

        width_input = ft.TextField(label='Введите ширину рамы', width=400)
        height_input = ft.TextField(label='Введите длину рамы', width=400)

        # Словарь для хранения стоимости по id окна
        window_costs = {}

        # Загрузка типов окон в dropdown
        conn = None
        try:
            conn = db.connect()
            with conn.cursor() as cursor:
                cursor.execute('SELECT id, name_type, cost_for_mm FROM type_window;')
                types = cursor.fetchall()

                # Заполняем dropdown и словарь стоимости
                for id, name, cost_for_mm in types:
                    if name:
                        type_dropdown.options.append(ft.dropdown.Option(text=name, key=str(id)))
                        window_costs[str(id)] = cost_for_mm
        except Exception as ex:
            result_text.value = f'Ошибка загрузки типов: {ex}'
            result_text.color = 'red'
        finally:
            if conn:
                conn.close()
            page.update()

        # Функция создания заказа
        def new_order(e):
            type_value = type_dropdown.value
            width = width_input.value.strip()
            height = height_input.value.strip()

            if not all([type_value, width, height]):
                result_text.value = 'Пожалуйста, заполните все поля.'
                result_text.color = 'red'
                page.update()
                return

            try:
                width = float(width)
                height = float(height)
            except ValueError:
                result_text.value = 'Неверный формат для ширины или длины.'
                result_text.color = 'red'
                page.update()
                return

            # Получаем стоимость по id из словаря
            cost_for_mm = window_costs.get(type_value, 0)
            cost = width * height * float(cost_for_mm)

            # Вставка данных в базу данных
            conn = None
            try:
                conn = db.connect()
                with conn.cursor() as cursor:
                    cursor.execute(''' 
                        INSERT INTO order_plate (id_type_window, date, width, height, cost, status) 
                        VALUES (%s, NOW(), %s, %s, %s, 'новый');
                    ''', (type_value, width, height, cost))
                    conn.commit()

                result_text.value = f'Заказ успешно добавлен! Сумма заказа: {cost}'
                result_text.color = 'green'

                # Очистка полей
                type_dropdown.value = None
                width_input.value = ''
                height_input.value = ''

            except Exception as ex:
                result_text.value = f'Ошибка при добавлении заказа: {ex}'
                result_text.color = 'red'
            finally:
                if conn:
                    conn.close()
                page.update()

        insert_button = ft.ElevatedButton('Создать заказ', on_click=new_order)
        back_button = ft.ElevatedButton('Назад', on_click=show_main_page)

        page.add(
            ft.Column(
                [
                    hello_text,
                    image,
                    type_dropdown,
                    width_input,
                    height_input,
                    result_text,
                    insert_button,
                    back_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        page.update()



    def show_window_for_manager(username):
        page.clean()
        page.title = 'Окно менеджера'

        hello_text = ft.Text(f'Привет, {username}!', size=20)
        input_filter_overplate = ft.TextField(label='Введите название покрытия', width=400)
        message_text = ft.Text('', color='red', size=16)
        selected_date = ft.Text('Дата не выбрана')
        image = ft.Image(src='photo\\Администратор.png', width=150, height=200, fit=ft.ImageFit.CONTAIN)

        def on_date_change(e):
            try:
                raw_date = str(e.data).split("T")[0]
                parsed_date = datetime.fromisoformat(raw_date).date()
                selected_date.value = parsed_date.strftime("%Y-%m-%d")
            except Exception as ex:
                selected_date.value = "Дата не выбрана"
                message_text.value = f"Ошибка выбора даты: {ex}"
                message_text.color = 'red'
            page.update()

        date_picker = ft.DatePicker(on_change=on_date_change)
        page.overlay.append(date_picker)

        def open_date_picker():
            date_picker.open = True
            page.update()

        pick_date_button = ft.ElevatedButton("Выбрать дату", on_click=lambda e: open_date_picker())

        orders_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text('ID')),
                ft.DataColumn(label=ft.Text('Покрытие')),
                ft.DataColumn(label=ft.Text('Дата')),
                ft.DataColumn(label=ft.Text('Ширина')),
                ft.DataColumn(label=ft.Text('Высота')),
                ft.DataColumn(label=ft.Text('Статус')),
            ],
            rows=[]
        )

        def filter_orders(e):
            cover = input_filter_overplate.value.strip()
            date_str = selected_date.value.strip()

            if not cover or date_str == "Дата не выбрана":
                message_text.value = "Введите покрытие и выберите дату!"
                message_text.color = 'red'
                page.update()
                return

            try:
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                message_text.value = "Неверный формат даты"
                message_text.color = 'red'
                page.update()
                return

            conn = None
            try:
                conn = db.connect()
                with conn.cursor() as cursor:
                    cursor.execute('''
                        SELECT * FROM order_plate
                        WHERE overplate LIKE %s AND date = %s
                        ORDER BY id;
                    ''', (f'%{cover}%', parsed_date))
                    data = cursor.fetchall()

                if not data:
                    message_text.value = 'Нет заказов по заданным параметрам.'
                    message_text.color = 'orange'
                    orders_table.rows = []
                else:
                    orders_table.rows = [
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(str(row[0]))),
                            ft.DataCell(ft.Text(row[1])),
                            ft.DataCell(ft.Text(str(row[2]))),
                            ft.DataCell(ft.Text(str(row[3]))),
                            ft.DataCell(ft.Text(str(row[4]))),
                            ft.DataCell(ft.Text(row[5])),
                        ]) for row in data
                    ]
                    message_text.value = f'Найдено заказов: {len(data)}'
                    message_text.color = 'green'

            except Exception as ex:
                message_text.value = f"Ошибка БД: {ex}"
                message_text.color = 'red'
            finally:
                if conn:
                    conn.close()
                page.update()

        show_button = ft.ElevatedButton('Показать заказы', on_click=filter_orders)
        back_button = ft.ElevatedButton('Назад', on_click=show_main_page)

        page.add(
            ft.Column(
                [
                    hello_text,
                    image,
                    input_filter_overplate,
                    ft.Row([pick_date_button, selected_date], alignment=ft.MainAxisAlignment.CENTER),
                    show_button,
                    orders_table,
                    message_text,
                    back_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        page.update()

    auth_button = ft.ElevatedButton('Авторизация', on_click=check_auth)
    reg_button = ft.ElevatedButton('Регистрация', on_click=reg_window)

    show_main_page()

ft.app(target=main)
