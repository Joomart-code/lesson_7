import flet as ft
from db import main_db 

def main(page: ft.Page):
    page.title = "TODO"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 700
    page.window_height = 500
    page.padding = 20

    task_list = ft.Column(spacing=10)
    filter_type = 'all'

    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks(filter_type=filter_type):
            task_list.controls.append(view_tasks(
                task_id=task_id,
                task_text=task_text,
                completed=completed
            ))
        page.update()

    def clear_completed(e):
        main_db.delete_completed_tasks() 
        load_tasks() 

    def view_tasks(task_id, task_text, completed=None):
        checkbox = ft.Checkbox(
            value=bool(completed),
            fill_color=ft.Colors.GREEN_900,
            on_change=lambda e: toggle_task(task_id=task_id, is_completed=e.control.value)
        )

        task_field = ft.TextField(
            read_only=True, 
            value=task_text, 
            expand=True
            )
        

        def enable_edit(e):
            task_field.read_only = not task_field.read_only
            page.update()

        def save_task(e):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            page.update()

        def delete_task(e):
            main_db.delete_task(task_id)
            load_tasks()

        return ft.Row([
            checkbox, 
            task_field, 
            ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit),
            ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task),
            ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_task, icon_color=ft.Colors.RED_400)
        ])
    
    def toggle_task(task_id, is_completed):
        conn = main_db.sqlite3.connect(main_db.path_db)
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (1 if is_completed else 0, task_id))
        conn.commit()
        conn.close()
        load_tasks()

    def add_task(e):
        if task_input.value:
            main_db.add_task(task=task_input.value)
            task_input.value = ""
            load_tasks()

    task_input = ft.TextField(label="Введите задачу", expand=True, border_color=ft.Colors.BLACK, on_submit=add_task)
    task_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_task)

    filter_buttons = ft.Row([
        ft.ElevatedButton('Все', on_click=lambda e: set_filter('all'), bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK),
        ft.ElevatedButton('В работе', on_click=lambda e: set_filter('uncompleted'), bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK),
        ft.ElevatedButton('Готово', on_click=lambda e: set_filter('completed'), bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK),
        
        
        ft.OutlinedButton(
            'Очистить выполненные', 
            on_click=clear_completed, 
            icon=ft.Icons.DELETE_SWEEP, 
            style=ft.ButtonStyle(color=ft.Colors.BLUE_900)
        ),
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()

    page.add(
        ft.Column([
            ft.Row([task_input, task_button]),
            filter_buttons,
            ft.Divider(height=20),
            task_list
        ])
    )
    load_tasks()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)