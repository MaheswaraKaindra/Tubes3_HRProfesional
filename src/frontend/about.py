import flet as ft

class About:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "CV Analyzer App by HRProfesional"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.bgcolor = '#395B9D'

    def build_ui(self):
        # Header Section
        def on_home_click(e):
            self.page.go("/home")

        self.home_button = ft.ElevatedButton(
            "Home",
            bgcolor="#FAF7F0",
            color="#000000",
            width=100,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
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

        panel_content = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text("About Us", size=28,  weight=ft.FontWeight.BOLD, color="#256988", text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,
                        padding=ft.padding.all(5),
                    ),
                    ft.Divider(height=1, color="#000000"),
                    ft.Container(
                        content=ft.Text("HRProfesional", size=24, weight=ft.FontWeight.BOLD, color="#000000", text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=10, bottom=5),
                    ),
                    ft.Image(
                        src="HRProfesional.jpg",
                        width=200,
                        height=200,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Undergraduate Informatics Engineering Students \nfrom Institut Teknologi Bandung \nwho love Algorithm Strategy",
                            size=16,
                            color="#000000",
                            text_align=ft.TextAlign.CENTER,
                            width=500,
                            # wrap=True,
                        ),
                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                        alignment=ft.alignment.center,
                    ),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#DEE2E2",
            padding=ft.padding.all(25),
            border_radius=ft.border_radius.all(10),
            margin=ft.margin.all(10),
            expand=4,
            alignment=ft.alignment.center
        )

        # self.page.clean()
        # self.page.add(
        #     ft.Column(
        #         [
        #             self.header_content,
        #             ft.Container(
        #                 content=panel_content,
        #                 alignment=ft.alignment.center,
        #                 expand=True
        #             )
        #         ],
        #         expand=True,
        #     )
        # )
        # self.page.update()

        return ft.View(
            route="/about",
            controls=[
                ft.Column(
                    [
                        self.header_content,
                        ft.Container(
                            content=panel_content,
                            alignment=ft.alignment.center,
                            expand=True
                        )
                    ],
                    expand=True,
                )
            ]
        )

    
