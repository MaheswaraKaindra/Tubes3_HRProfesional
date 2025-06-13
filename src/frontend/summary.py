import flet as ft
import home, utils

class Summary:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "CV Analyzer App by HRProfesional"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.bgcolor = '#395B9D'

    def build_ui(self):
        # Header Section
        def on_home_click(e):
            self.page.clean()
            home_page = home.Home(self.page)
            home_page.build_ui()

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
            width=self.page.window_width,
            bgcolor='#395B9D',
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            alignment=ft.alignment.center_left
        )

        # Left Panel - Other CVs
        cv_results_grid = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            # padding=10,
            expand=True
        )
        # Tambahkan beberapa contoh kartu ke grid
        example_cvs = [
            {"name": "Efrina",       "keyword_counts": {"Java": 2, "Python": 2}},
            {"name": "Budi Santoso", "keyword_counts": {"JavaScript": 1, "React": 1, "Node.js": 1, "SQL": 1}},
            {"name": "Citra Ayu",    "keyword_counts": {"Data Analysis": 2, "SQL": 2, "Tableau": 1}},
            {"name": "David Lee",    "keyword_counts": {"Marketing": 1, "SEO": 1}},
        ]

        for cv_data in example_cvs:
            cv_results_grid.controls.append(utils.create_cv_card(self.page, cv_data["name"], cv_data["keyword_counts"]))

        left_panel_content = ft.Container(
            content=ft.Column(
                [   
                    cv_results_grid,
                ],
                spacing=5,
                expand=True
            ),
            # bgcolor="#DEE2E2",
            # padding=ft.padding.all(25),
            # border_radius=ft.border_radius.all(10),
            # margin=ft.margin.all(10),
        )

        # Right Panel - Summary
        def create_cv_summary_card(content, text):
            # content: SUMMARY, SKILLS, EXPERIENCE, EDUCATION
            return ft.Card(
                height=200,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(content, size=20, weight=ft.FontWeight.BOLD, color="#000000", text_align=ft.TextAlign.CENTER),
                            ft.Divider(height=1, color="#000000"),
                            ft.Text(text, size=16, color="#000000", text_align=ft.TextAlign.LEFT),
                        ],
                        spacing=5,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.top_left,
                    bgcolor="#FFFFFF",
                    border_radius=8,
                ),
            )

        cv_summary_grid = ft.Column(  
            spacing=30,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            # padding=10
        )

        example_summary = [
            "A highly motivated and results-driven professional with a strong background in software development and project management. Proven ability to lead teams and deliver high-quality solutions on time and within budget.",
            "Python, Java, C++, Project Management, Agile Methodologies, Team Leadership",
            "Software Engineer at XYZ Corp (2019-Present)\nProject Manager at ABC Ltd (2016-2019)",
            "Bachelor of Science in Computer Science, University of Technology (2012-2016)"
        ]
        cv_summary_grid.controls.append(create_cv_summary_card("SUMMARY", example_summary[0]))
        cv_summary_grid.controls.append(create_cv_summary_card("SKILLS", example_summary[1]))
        cv_summary_grid.controls.append(create_cv_summary_card("EXPERIENCE", example_summary[2]))
        cv_summary_grid.controls.append(create_cv_summary_card("EDUCATION", example_summary[3]))
        
        right_panel_content = ft.Container(
            content=ft.Column(
                [   
                    ft.Container(
                        content=ft.Text("CV Summary", size=28, weight=ft.FontWeight.BOLD, color="#256988", text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,
                        # padding=ft.padding.only(bottom=5),
                    ),
                    ft.Divider(height=1, color="#000000"),
                    ft.Container(cv_summary_grid, expand=True)
                ],
                spacing=5,
                # expand=True
            ),
            bgcolor="#DEE2E2",
            padding=ft.padding.all(25),
            border_radius=ft.border_radius.all(10),
            margin=ft.margin.all(10),
        )

        # Main Layout
        main_layout = ft.Row(
            [
                ft.Container(left_panel_content, expand=1, padding=5), # Panel kiri mengambil 2 bagian
                ft.Container(right_panel_content, expand=5, padding=5), # Panel kanan mengambil 3 bagian
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True
        )

        self.page.clean()
        self.page.add(
            ft.Column(
                [
                    self.header_content,
                    ft.Container(main_layout, expand=True)
                ],
                expand=True
            )
        )
        self.page.update()