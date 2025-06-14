import os
import flet as ft
from flet import WebView

class CV:
    def __init__(self, page: ft.Page, state: dict):
        self.page = page
        self.state = state
        self.page.title = "CV Analyzer App by HRProfesional"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.bgcolor = "#395B9D"

    def build_ui(self) -> ft.View:
        selected_cv = self.state.get("selected_cv")
        cv_path = selected_cv.get("path")
        if not cv_path:
            return ft.View(
                route="/cv",
                bgcolor=self.page.bgcolor,
                controls=[
                    ft.Text(
                        "No CV selected. Please go back and choose a CV first.",
                        color="#FAF7F0",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    )
                ],
            )

        # Header Section
        def on_home_click(e):
            self.page.go("/home")
            
        self.home_button = ft.ElevatedButton( # home button
            "Home",
            bgcolor="#FAF7F0",
            color="#000000",
            width=100,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=on_home_click,
        )

        self.header_content = ft.Container(
            content=ft.Row(
                [
                    ft.Text("CV Analyzer App by HRProfesional", color="#FAF7F0", size=36, weight=ft.FontWeight.BOLD),
                    ft.Row([self.home_button], alignment=ft.MainAxisAlignment.END, expand=True)
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=self.page.window.width,
            bgcolor='#395B9D',
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            alignment=ft.alignment.center_left
        )

        abs_path = os.path.abspath(cv_path)
        file_url = f"file:///{abs_path.replace(os.sep, '/')}"  

        body = ft.Container(
            content=WebView(url=file_url, expand=True),
            expand=True,
        )

        return ft.View(
            route="/cv",
            bgcolor=self.page.bgcolor,
            controls=[
                ft.Column(
                    [
                        self.header_content,
                        ft.Container(body, expand=True),
                    ],
                    expand=True,
                )
            ]
        )

  
