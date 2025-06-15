import os
import flet as ft
import shutil

class CV:
    def __init__(self, page: ft.Page, state: dict):
        self.page = page
        self.state = state
        self.page.title = "CV Analyzer App by HRProfesional"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.bgcolor = "#395B9D"

    def build_ui(self):
        selected_cv = self.state.get("selected_cv")
        cv_path = selected_cv.get("path") if selected_cv else None

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

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        source_path = os.path.join(project_root, cv_path)
        file_name = os.path.basename(source_path)

        def open_cv_file(e):
            try:
                if not os.path.exists(source_path):
                    raise FileNotFoundError(f"File not found: {source_path}")
                if os.name == 'nt':
                    os.startfile(source_path)
                elif os.name == 'posix':
                    import subprocess
                    result = subprocess.Popen(['open', source_path])
                else:
                    raise OSError("Unsupported OS for opening files.")
            except Exception as e:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Error opening file: {str(e)}", color="#FF0000"),
                    action="OK",
                    action_color="#FFFFFF",
                )
                self.page.snack_bar.open = True
                self.page.update()

        body = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(name=ft.Icons.PICTURE_AS_PDF_ROUNDED, size=120, color="#DEE2E2"),
                    ft.Text(
                        f"CV Ready:\n{file_name}",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color="#DEE2E2"
                    ),                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Open PDF File",
                        icon=ft.Icons.OPEN_IN_NEW,
                        on_click=open_cv_file,
                        bgcolor="#FAF7F0",
                        color="#000000",
                        height=50,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=20,
                        )
                    ),
                    ft.Text(
                        "Your PDF will be opened in the default PDF viewer.",
                        italic=True,
                        size=14,
                        color="#B0C4DE" 
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
                expand=True,
            ),
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

def main(page: ft.Page):
    # testing
    mock_cv_path = os.path.join('data', 'Agriculture', '10953078.pdf')
    
    cv = CV(page, {"selected_cv": {"path": mock_cv_path}})
    page.views.append(cv.build_ui())
    page.update()

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    assets_folder_path = os.path.join(project_root, "assets")

    ft.app(target=main)
