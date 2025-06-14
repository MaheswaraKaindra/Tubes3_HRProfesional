import flet as ft
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.frontend.home import Home
from src.frontend.about import About
from src.frontend.summary import Summary
from src.frontend.cv import CV

app_state = {
    "search_results": [],
    "last_info_text": "",
    "selected_cv": None,
}

def main(page: ft.Page):
    page.title = "CV Analyzer App by HRProfesional"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.bgcolor = '#395B9D'

    loading_sign = ft.Container(
        content=ft.Column(
            [
                ft.Text("Loading...", color="#FAF7F0", size=36, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                ft.ProgressRing(width=30, height=30, stroke_width=3, color="#FAF7F0")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        expand=True
    )
    page.add(loading_sign)


    pages = {
        "/home": Home(page, app_state),
        "/about": About(page),
        "/summary": Summary(page, app_state),
        "/cv": CV(page, app_state)
    }

    def route_change(route):
        page.views.clear()
        current_view = pages.get(page.route, pages["/home"]).build_ui()
        current_view.bgcolor = page.bgcolor
        page.views.append(current_view)
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route or "/home")

if __name__ == "__main__":
    assets_folder_path = "assets"

    ft.app(target=main, assets_dir=assets_folder_path,)
