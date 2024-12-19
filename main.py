import flet as ft
from views.login import login_view
from views.menu import menu_view
from views.inventory import inventory_view
from views.prodManage import prodManage_view
from views.addProd import addProd_view
from views.lotRegister import lotRegister_view
from views.saleRegister import saleRegister_view
from views.addUser import createUser_view
from db_connection import initialize_firebase
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Detected filter using positional arguments")


def main(page: ft.Page):
    page.window.center()
    page.window.width = 1000
    page.window.height = 700
    #page.window.maximizable = False
    page.window.resizable = False
    page.go("/login")
    page.theme_mode = ft.ThemeMode.DARK

    page.on_route_change = lambda e: navigate_to_page(page, e.route)

    initialize_firebase()

    page.window.visible = True

def navigate_to_page(page, route):
    page.clean()

    if route == "/login":
        login_view(page)
    elif route == "/menu":
        menu_view(page)
    elif route == "/inventory":
        inventory_view(page)
    elif route == "/prodManage":
        prodManage_view(page)
    elif route == "/addProd":
        addProd_view(page)
    elif route == "/lotRegister":
        lotRegister_view(page)
    elif route == "/saleRegister":
        saleRegister_view(page)
    elif route == "/createUser":
        createUser_view(page)
    else:
        login_view(page)

# Iniciar la aplicación
ft.app(main, view=ft.AppView.FLET_APP_HIDDEN)