import flet as ft
import about

class Home:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "CV Analyzer App by HRProfesional"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.bgcolor = '#395B9D'

        self.build_ui()

    def build_ui(self):
        # Header Section
        def on_about_us_click(e):
            self.page.clean()
            about_page = about.About(self.page)
            about_page.build_ui()

        self.about_us_button = ft.ElevatedButton( # about us button
            "About Us",
            bgcolor="#FAF7F0",
            color="#000000",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
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

        def on_search_click(e):
            keywords = self.keywords_input.value.split(',')
            num_applicants = self.num_applicants_input.value
            algorithm = self.algorithm_options.value
            # TODO: panggil fungsi pencarian
            print(f"Searching for: {keywords}, Number of applicants: {num_applicants}, Algorithm: {algorithm}")

        self.search_button = ft.ElevatedButton( # search button
            "Search",
            bgcolor="#FDF6EC",
            color="#395B9D",
            width=450,
            height=40,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
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
        def create_cv_card(name, results):
            # result adalah dictionary dengan keyword sebagai key dan jumlah kemunculan sebagai value
            total_matches = sum(results.values())
            keyword_texts = []
            for i, (keyword, count) in enumerate(results.items()):
                if (i == 3):
                    keyword_texts.append(ft.Text(f"... and {len(results) - 3} more keywords", size=12, color="#000000"))
                    break
                if (count == 1):
                    keyword_texts.append(
                        ft.Text(f"{i+1}. {keyword}: {count} occurence", size=12, color="#000000")
                    )
                elif (count > 1):
                    keyword_texts.append(
                        ft.Text(f"{i+1}. {keyword}: {count} occurences", size=12, color="#000000")
                )
                
            return ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [   
                            ft.Row(
                                [   
                                    ft.Container(
                                        content=ft.Text(name, weight=ft.FontWeight.BOLD, size=18, color="#000000"), # nama
                                        alignment=ft.alignment.top_left,
                                        expand=True
                                    ),
                                    ft.Container(
                                        content=ft.Text(f"{total_matches} matches", size=12, color="#000000"), # total matches 
                                        alignment=ft.alignment.top_right,
                                        expand=False
                                    ), 
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                spacing=5
                            ),
                            ft.Container(height=5),
                            ft.Text("Matched keywords:", size=12, weight=ft.FontWeight.W_500, color="#000000"),
                            ft.Column(keyword_texts, spacing=2, expand=True),
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.TextButton("Summary", style=ft.ButtonStyle(
                                                                bgcolor="#395B9D", 
                                                                color="#DEE2E2", 
                                                                shadow_color="#395B9D",
                                                                shape=ft.RoundedRectangleBorder(radius=8) 
                                                            )
                                                ),
                                        alignment=ft.alignment.bottom_left,
                                        expand=True,
                                    ),
                                    ft.Container(
                                        content=ft.TextButton("View CV", style=ft.ButtonStyle(
                                                                bgcolor="#395B9D", 
                                                                color="#DEE2E2", 
                                                                shadow_color="#395B9D",
                                                                shape=ft.RoundedRectangleBorder(radius=8)
                                                            )
                                                ),
                                        alignment=ft.alignment.bottom_right,
                                    ),
                                    
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.END,
                                spacing=5
                            )
                        ],
                        spacing=3
                    ),
                    width=200,
                    padding=15,
                    bgcolor="#FFFFFF",
                    border_radius=8,
                    shadow=ft.BoxShadow(blur_radius=5, color="#395B9D")
                )
            )
        

        # Hasil Pencarian CV
        cv_results_grid = ft.GridView(
            runs_count=3,
            max_extent=280,
            child_aspect_ratio=0.85, # Sesuaikan rasio aspek kartu
            spacing=10,
            run_spacing=10,
            padding=10,
            # expand=True
        )

        # Tambahkan beberapa contoh kartu ke grid
        example_cvs = [
            {"name": "Efrina",       "keyword_counts": {"Java": 2, "Python": 2}},
            {"name": "Budi Santoso", "keyword_counts": {"JavaScript": 1, "React": 1, "Node.js": 1, "SQL": 1}},
            {"name": "Citra Ayu",    "keyword_counts": {"Data Analysis": 2, "SQL": 2, "Tableau": 1}},
            {"name": "David Lee",    "keyword_counts": {"Marketing": 1, "SEO": 1}},
        ]
        for cv_data in example_cvs:
            cv_results_grid.controls.append(create_cv_card(cv_data["name"], cv_data["keyword_counts"]))

        # TODO: dari algoritma, cuma placeholder
        results_info_text = ft.Text("Exact Match: 100 CVs scanned in 100 ms", size=14, color="#863E38", weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER)

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

def main(page: ft.Page):
    app = Home(page)

if __name__ == "__main__":
    ft.app(target=main)