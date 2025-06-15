import flet as ft
import threading
import os
from flet import WebView

from . import utils
from .summary import Summary
from .cv import CV

from src.backend import search_controller
from src.data.setup_database import setup_database


class Home:
    def __init__(self, page: ft.Page, state: dict):
        self.page = page
        self.state = state
        self.page.title = "CV Analyzer App by HRProfesional"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.bgcolor = '#395B9D'
        self.build_ui()
        setup_database()
        search_controller.load_cv_data("data")

        # Global variables for search
        self.keywords = []
        self.algorithm = "BM"

    def build_ui(self):
        # Header Section
        def on_about_us_click(e):
            self.page.go("/about")

        self.about_us_button = ft.ElevatedButton( # about us button
            "About Us",
            bgcolor="#FAF7F0",
            color="#000000",
            width=100,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=on_about_us_click,
        )

        self.header_content = ft.Container( # header
            content=ft.Row(
                [
                    ft.Text("CV Analyzer App by HRProfesional", color="#FAF7F0", size=36, weight=ft.FontWeight.BOLD),
                    ft.Row([self.about_us_button], alignment=ft.MainAxisAlignment.END, expand=True)
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=self.page.window.width,
            bgcolor='#395B9D',
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            alignment=ft.alignment.center_left
        )

        # Left Panel - Search Controls
        def validate_input(e: None):
            if self.num_applicants_input.value and self.num_applicants_input.value.strip():
                try:
                    # Coba konversi ke integer untuk memeriksa apakah itu angka
                    int(self.num_applicants_input.value)
                    self.num_applicants_input.error_text = None # Hapus error jika valid
                except ValueError:
                    # Jika gagal (bukan angka), tampilkan error dan set tidak valid
                    self.num_applicants_input.error_text = "Input must be a number"
            self.page.update()
            
        self.keywords_input = ft.TextField( # keywords input
            label="Enter keywords separated by comma",
            border_color="#395B9D",
            border_radius=5,
            bgcolor="#FFFFFF",
            text_style=ft.TextStyle(color="#000000"),
        )

        self.algorithm_options = ft.RadioGroup( # algorithm input
            value="KMP", # default
            content=ft.Row(
                [
                    ft.Radio(value="KMP", label="KMP", label_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD, color="#000000"), active_color="#395B9D"),
                    ft.Container(width=20),
                    ft.Radio(value="BM", label="BM", label_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD, color="#000000"), active_color="#395B9D"),
                    ft.Container(width=20),
                    ft.Radio(value="AC", label="Aho-Corasick", label_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD, color="#000000"), active_color="#395B9D")
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        ) 

        self.num_applicants_input = ft.TextField( # number of applicants input
            label="Enter amount",
            border_color="#395B9D",
            border_radius=5,
            bgcolor="#FFFFFF",
            text_style=ft.TextStyle(color="#000000"),
            on_change=validate_input,
        )

        def on_summary_click(cv_data):
            self.state["selected_cv"] = cv_data
            # self.page.views.append(Summary(self.page, self.state).build_ui())
            self.page.go("/summary")

        def on_view_cv_click(cv_data):
            self.state["selected_cv"] = cv_data
            # self.page.views.append(CV(self.page, self.state["selected_cv"]).build_ui())

            self.page.go("/cv")

        def update_ui_from_state():
            results_info_text.value = self.state["last_info_text"]
            cv_results_grid.controls.clear()

            if not self.state["search_results"]:
                print("No search results found.")
                cv_results_grid.controls.append(ft.Text("No matching CVs found.", text_align=ft.TextAlign.CENTER))
            else:
                sorted_cv_data = sorted(
                    self.state["search_results"],
                    key=lambda cv: sum(cv["keyword_counts"].values()),
                    reverse=True
                )
                for cv_data in sorted_cv_data:
                    summary_handler = lambda _, cv=cv_data: on_summary_click(cv)
                    view_cv_handler = lambda _, cv=cv_data: on_view_cv_click(cv)

                    cv_results_grid.controls.append(
                        utils.create_cv_card(self.page, 
                            cv_data["name"], 
                            cv_data["keyword_counts"], 
                            on_summary_click=summary_handler, 
                            on_view_cv_click=view_cv_handler,
                        )
                    )
            self.page.update()

        self.search_output = None
        def on_search_click(e):
            # 1. Ambil input dari UI
            keywords_str = self.keywords_input.value
            if not keywords_str:
                return # Jangan lakukan apa-apa jika keyword kosong

            keywords = [k.strip() for k in keywords_str.split(',')]
            algorithm = self.algorithm_options.value
            try:
                top_n = int(self.num_applicants_input.value)
            except (ValueError, TypeError):
                top_n = 10 # Default 10 jika input kosong atau tidak valid

            # 2. Panggil controller backend
            self.search_output = search_controller.search_cv_data(keywords, algorithm, top_n, fuzzy_threshold=80.0)
            self.state["search_results"] = self.search_output['results'][:top_n]
            self.state["last_info_text"] = f"{self.search_output['scan_count']} CVs scanned in {self.search_output['exact_time'] + self.search_output['fuzzy_time']:.2f} ms"

            # 3. Update UI dengan hasil pencarian
            update_ui_from_state()

        self.search_button = ft.ElevatedButton( # search button
            "Search",
            bgcolor="#FDF6EC",
            color="#395B9D",
            width=450,
            height=40,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            # expand=True,
            on_click=on_search_click,
        )


        # Left Panel - Search Controls
        left_panel_content = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Finding your desired employee\nis just one-click away!",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#256988"
                    ),
                    ft.Container(height=10),
                    ft.Text("What are you looking for?", size=16, weight=ft.FontWeight.W_500, color="#000000"),
                    self.keywords_input,
                    ft.Container(height=10),
                    ft.Text("Choose the searching algorithm", size=16, weight=ft.FontWeight.W_500, color="#000000"),
                    self.algorithm_options,
                    ft.Container(height=10),
                    ft.Text("How many applicants do you want?", size=16, weight=ft.FontWeight.W_500, color="#000000"),
                    self.num_applicants_input,
                    ft.Container(height=15),
                    self.search_button,
                ],
                spacing=10,
            ),
            bgcolor="#DEE2E2",
            padding=ft.padding.all(25),
            border_radius=ft.border_radius.all(10),
            margin=ft.margin.all(10),
        )

        # Right Panel - Results
        results_info_text = ft.Text(color="#000000")

        cv_results_grid = ft.GridView(
            runs_count=3,
            max_extent=280,
            child_aspect_ratio=0.85, # Sesuaikan rasio aspek kartu
            spacing=10,
            run_spacing=10,
            padding=10,
            # expand=True
        )

        update_ui_from_state()

        right_panel_content = ft.Container(
            content=ft.Column(
                [   
                    ft.Container(
                        content=ft.Text("Results", size=28, weight=ft.FontWeight.BOLD, color="#256988", text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,
                        # padding=ft.padding.only(bottom=5),
                    ),
                    ft.Container(
                        content=results_info_text,
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(bottom=5),
                    ),
                    ft.Divider(height=1, color="#000000"),
                    ft.Container(cv_results_grid, expand=True)
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
                ft.Container(left_panel_content, expand=2, padding=5), # Panel kiri mengambil 2 bagian
                ft.Container(right_panel_content, expand=3, padding=5), # Panel kanan mengambil 3 bagian
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            # expand=True
        )

        # self.page.clean()
        # self.page.add(
        #     ft.Column(
        #         [
        #             self.header_content,
        #             ft.Container(main_layout, expand=True)
        #         ],
        #         expand=True
        #     )
        # )
        # self.page.update()

        return ft.View(
            route="/home",
            controls=[
                ft.Column(
                    [
                        self.header_content,
                        ft.Container(main_layout, expand=True),
                    ],
                    expand=True,
                ),
            ],
        )

def main(page: ft.Page):
    app = Home(page)

if __name__ == "__main__":
    ft.app(target=main)