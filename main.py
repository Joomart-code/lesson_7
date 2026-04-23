import flet as ft
from db import main_db 


def main(page: ft.Page):
    page.title = "Список Задач"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column()
    
    counter_text = ft.Text("", size=16, color=ft.Colors.GREY_500)

    filter_type = 'all'
    
    task_input = ft.TextField(label="Введите задачу",
    expand=True,
    border_radius=10,
    hint_text ="Что нужно сделать?",
    )
    quantity_input = ft.TextField(
    label="Кол-во",
    width=80,
    value="1",
    border_radius=10,
    )
   # Функция список задач пуст:
    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, quantity, completed in main_db.get_tasks(filter_type=filter_type):
            task_list.controls.append(view_tasks(
                task_id=task_id,
                task_text=task_text,
                quantity=quantity,
                completed=completed
                ))
        if not task_list.controls:
            task_list.controls.append(ft.Text('Список задач пуст 📭', size=18, color=ft.Colors.GREY_500,italic=True))
        
        all_tasks = main_db.get_tasks('all')
        completed_tasks = main_db.get_tasks('completed')
        counter_text.value = f"✅ {len(completed_tasks)}/{len(all_tasks)}"
        page.update()
#______________________________________________________________________

    def view_tasks(task_id, task_text, quantity=1, completed=None):
        checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id=task_id, is_completed=e.control.value)
            )

        task_field = ft.TextField(read_only=True, value=task_text, expand=True)
        quantity_text = ft.Text(f"x{quantity}", size=14, color=ft.Colors.GREY_500, width=40)

        def enable_edit(e):
            if task_field.read_only == True:
                task_field.read_only = False
            else:
                task_field.read_only = True


        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(e):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)
        
        
            #Добавляю кнопку удаления:__________________________________________________________________________
        def delete_task(e):
            main_db.delete_task(task_id=task_id)
            load_tasks()
            page.update()
        
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_700, on_click=delete_task)
        #______________________________________________________________________________________________________



        return ft.Row([checkbox, task_field, edit_button, quantity_text, save_button, delete_button])

    def toggle_task(task_id, is_completed):
        print(is_completed)
        main_db.update_task(task_id=task_id, completed=int(is_completed))
        load_tasks()
        page.update()

    def add_task(e):
        if task_input.value:
            task = task_input.value
            quantity = int(quantity_input.value) if quantity_input.value else 1
            task_id = main_db.add_task(task=task,quantity=quantity)
            print(f'Задача {task} добавлена! Его ID - {task_id}')
            task_input.value = None
            quantity_input.value = "1"
            load_tasks()
        page.update()  
          
    task_input.on_submit=add_task


    task_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_task)

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()


    filter_buttons = ft.Row([
        ft.ElevatedButton('Все задачи', on_click=lambda e: set_filter('all'), icon=ft.Icons.APPS, icon_color=ft.Colors.BLACK),
        ft.ElevatedButton('В работе', on_click=lambda e: set_filter('uncompleted'), icon=ft.Icons.AUTORENEW, icon_color=ft.Colors.YELLOW_900),
        ft.ElevatedButton('Готово', on_click=lambda e: set_filter('completed'), icon=ft.Icons.DONE_ALL, icon_color=ft.Colors.GREEN_900)
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
    

    send_task = ft.Row([task_input, task_button, quantity_input])
    #Кнопка изменения темы:___________________________
    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_btn.icon = ft.Icons.LIGHT_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_btn.icon = ft.Icons.DARK_MODE
        page.update()

    theme_btn = ft.IconButton(
    icon=ft.Icons.DARK_MODE,
    on_click=change_theme
    )
#_____________________________________________
    page.add(
        ft.Row([
         ft.Text("Список задач", size=35, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
         theme_btn
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    counter_text,
    send_task,
    filter_buttons,
    task_list
)
    load_tasks()

if __name__ == "__main__":
    main_db.init_db()
    ft.run(main, view=ft.AppView.WEB_BROWSER)