import flet as ft
import threading

from . import about, summary, utils

from src.backend import search_controller


class Home:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "CV Analyzer App by HRProfesional"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.bgcolor = '#395B9D'
        self.build_ui()
        search_controller.load_cv_data("data")

        # Global variables for search
        self.keywords = []
        self.algorithm = "BM"

        thread = threading.Thread(target=self.load_data_from_backend, daemon=True)
        thread.start()

    def load_data_from_backend(self):
        print("Loading CV data from backend...")
        search_controller.load_cv_data("data")
        print("CV data loaded successfully.")

        self.search_button.disabled = False
        self.loading_indicator.visible = False
        self.search_button_text.value = "Search"

        self.page.update()

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
        self.keywords_input = ft.TextField( # keywords input
            label="Enter keywords separated by comma",
            border_color="#395B9D",
            border_radius=5,
            bgcolor="#FFFFFF",
            text_style=ft.TextStyle(color="#000000")
        )

        self.algorithm_options = ft.RadioGroup( # algorithm input
            content=ft.Row(
                [
                    ft.Radio(value="KMP", label="KMP", label_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD), active_color="#395B9D"),
                    ft.Container(width=20),
                    ft.Radio(value="BM", label="BM", label_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD), active_color="#395B9D")
                    # might add more
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        ) 

        self.num_applicants_input = ft.TextField( # number of applicants input
            label="Enter amount",
            border_color="#395B9D",
            border_radius=5,
            bgcolor="#FFFFFF",
            text_style=ft.TextStyle(color="#000000")
        )

        self.loading_indicator = ft.ProgressRing(width=20, height=20, stroke_width=2, visible=True)
        self.search_button_text = ft.Text("Search")

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
            search_output = search_controller.search_cv_data(keywords, algorithm)

            # 3. Update UI dengan hasil pencarian
            cv_results_grid.controls.clear() # Bersihkan hasil sebelumnya

            # Update teks info
            results_info_text.value = f"{search_output['scan_count']} CVs scanned in {search_output['execution_time']:.2f} ms"

            top_results = search_output['results'][:top_n]

            if not top_results:
                cv_results_grid.controls.append(ft.Text("No matching CVs found.", text_align=ft.TextAlign.CENTER))
            else:
                for cv_data in top_results:
                    cv_results_grid.controls.append(
                        utils.create_cv_card(self.page, 
                                             cv_data["name"], 
                                             cv_data["keyword_counts"], 
                                             on_summary_click=on_summary_click, 
                                             on_view_cv_click=on_view_cv_click)
                    )
            
            self.page.update()


        self.search_button = ft.ElevatedButton( # search button
            content=ft.Row(
                [
                    self.search_button_text,
                    self.loading_indicator
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            bgcolor="#FDF6EC",
            color="#395B9D",
            width=450,
            height=40,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=on_search_click,
            disabled=True
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
        def on_summary_click(e):
            self.page.go("/summary")

        def on_view_cv_click(e):
            self.page.clean()

        results_info_text = ft.Text()

        cv_results_grid = ft.GridView(
            runs_count=3,
            max_extent=280,
            child_aspect_ratio=0.85, # Sesuaikan rasio aspek kartu
            spacing=10,
            run_spacing=10,
            padding=10,
            # expand=True
        )

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