import os
import flet as ft
import fitz
import base64
from . import summary

class CV:
    def __init__(self, page: ft.Page, state: dict):
        self.page = page
        self.state = state
        self.page.title = "CV Analyzer App by HRProfesional"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.bgcolor = "#395B9D"
        self.display_scale = 1.0  # skala tampilan awal
        self.scale_step = 0.1     # perubahan zoom

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

        def on_summary_click(cv_data):
            self.state["selected_cv"] = cv_data
            self.page.views.append(summary.Summary(self.page, self.state).build_ui())
            self.page.go("/summary")

        self.summary_button = ft.ElevatedButton( # summary button
            "Summary",
            bgcolor="#FAF7F0",
            color="#000000",
            width=100,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=lambda e: on_summary_click(selected_cv)
        )

        self.header_content = ft.Container(
            content=ft.Row(
                [
                    ft.Text("CV Analyzer App by HRProfesional", color="#FAF7F0", size=36, weight=ft.FontWeight.BOLD),
                    ft.Row([self.summary_button, self.home_button], spacing=5, alignment=ft.MainAxisAlignment.END, expand=True)
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=self.page.window.width,
            bgcolor='#395B9D',
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            alignment=ft.alignment.center_left
        )

        # PDF Viewer Section
        pdf_viewer = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            source_path = os.path.join(project_root, cv_path)

            if not os.path.exists(source_path):
                raise FileNotFoundError(f"File tidak ditemukan: {source_path}")

            doc = fitz.open(source_path)
            mat = fitz.Matrix(2.0, 2.0)
            
            for page_doc in doc:
                pix = page_doc.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                image_base64 = base64.b64encode(img_data).decode('utf-8')
                
                pdf_page_image = ft.Image(
                    src_base64=image_base64,
                    width= page_doc.rect.width * self.display_scale,
                    fit=ft.ImageFit.FILL,
                )
                
                pdf_viewer.controls.append(pdf_page_image)
            
            doc.close()

        except Exception as e:
            error_message = ft.Text(f"Gagal merender PDF: {e}", color="red", size=16)
            pdf_viewer.controls.append(error_message)

        # Kontrol Zoom
        zoom_display = ft.Text(f"{int(self.display_scale * 100)}%", weight=ft.FontWeight.BOLD, color="#000000")

        def update_image_sizes():
            for image_control in pdf_viewer.controls:
                if isinstance(image_control, ft.Image):
                    image_control.width = 800 * self.display_scale
            zoom_display.value = f"{int(self.display_scale * 100)}%"
            self.page.update()

        def zoom_in(e):
            self.display_scale += self.scale_step
            if self.display_scale > 3.0: self.display_scale = 3.0
            update_image_sizes()

        def zoom_out(e):
            self.display_scale -= self.scale_step
            if self.display_scale < 0.2: self.display_scale = 0.2
            update_image_sizes()

        zoom_controls = ft.Row(
            [
                ft.IconButton(ft.Icons.ZOOM_OUT, on_click=zoom_out, tooltip="Zoom In"),
                zoom_display,
                ft.IconButton(ft.Icons.ZOOM_IN, on_click=zoom_in, tooltip="Zooom Out"),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        panel_content= ft.Container(
            content=ft.Column(
                [
                    ft.Container(zoom_controls, bgcolor="#FFFFFF", border_radius=ft.border_radius.all(5)),
                    pdf_viewer,
                ],
                expand=True,
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            bgcolor="#DEE2E2",
            alignment=ft.alignment.top_center,
            padding=10
        )

        return ft.View(
            route="/cv",
            bgcolor=self.page.bgcolor,
            controls=[
                ft.Column(
                    [
                        self.header_content,
                        ft.Container(panel_content, expand=True),
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
