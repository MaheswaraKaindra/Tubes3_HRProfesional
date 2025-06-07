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

        about_us_button = ft.ElevatedButton(
            "About Us",
            bgcolor="#FAF7F0",
            color="#000000",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=on_about_us_click,
        )

        header_content = ft.Container(
            content=ft.Row(
                [
                    ft.Text("CV Analyzer App by HRProfesional", color="#FAF7F0", size=36, weight=ft.FontWeight.BOLD),
                    ft.Row([about_us_button], alignment=ft.MainAxisAlignment.END, expand=True)
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=self.page.window.width,
            bgcolor='#395B9D',
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            alignment=ft.alignment.center_left
        )

        # Left Panel - Search Controls
        keywords_input = ft.TextField(
            label="Enter keywords separated by comma",
            border_color="#395B9D",
            border_radius=5,
            bgcolor="#FFFFFF",
            text_style=ft.TextStyle(color="#000000")
        )

        algorithm_switch = ft.Switch(value=True, active_color="#395B9D")

        num_applicants_input = ft.TextField(
            label="Enter amount",
            border_color="#395B9D",
            border_radius=5,
            bgcolor="#FFFFFF",
            # width=150, # Lebar spesifik untuk input jumlah
            text_style=ft.TextStyle(color="#000000")
        )

        def on_search_click(e):
            # Logika untuk menangani klik tombol pencarian
            keywords = keywords_input.value.split(',')
            num_applicants = num_applicants_input.value
            algorithm = "BM" if algorithm_switch.value else "KMP"
            print(f"Searching for: {keywords}, Number of applicants: {num_applicants}, Algorithm: {algorithm}")

        search_button = ft.ElevatedButton(
            "Search",
            bgcolor="#FDF6EC", # Warna krem muda
            color="#395B9D", # Warna teks biru tua
            width=450,
            height=40,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=on_search_click, # Event handler untuk klik tombol
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
                    ft.Container(height=10), # Spasi
                    ft.Text("What are you looking for?", size=16, weight=ft.FontWeight.W_500, color="#863E38"),
                    keywords_input,
                    ft.Container(height=10), # Spasi
                    ft.Text("Choose the searching algorithm", size=16, weight=ft.FontWeight.W_500, color="#863E38"),
                    ft.Row(
                        [   
                            ft.Container(width=120), # Spasi
                            ft.Text("KMP", size=16, color="#000000", weight=ft.FontWeight.W_500),
                            algorithm_switch,
                            ft.Text("BM", size=16, color="#000000", weight=ft.FontWeight.W_500),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    ),
                    ft.Container(height=10), # Spasi
                    ft.Text("How many applicants do you want?", size=16, weight=ft.FontWeight.W_500, color="#863E38"),
                    num_applicants_input,
                    ft.Container(height=15), # Spasi lebih besar sebelum tombol
                    search_button,
                ],
                spacing=10, # Jarak antar kontrol di kolom kiri
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
                            ft.Text(name, weight=ft.FontWeight.BOLD, size=18, color="#000000"),
                            # Tampilkan total matches
                            ft.Text(f"{total_matches} matches", size=12, color="#000000"),
                            ft.Container(height=5),
                            ft.Text("Matched keywords:", size=12, weight=ft.FontWeight.W_500, color="#000000"),
                            # Tampilkan daftar keyword beserta jumlah kemunculannya
                            ft.Column(keyword_texts, spacing=2),
                            ft.Container(height=10), # TODO
                            ft.Row(
                                [
                                    ft.TextButton("Summary", style=ft.ButtonStyle(color="#395B9D")),
                                    ft.TextButton("View CV", style=ft.ButtonStyle(color="#395B9D")),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                                spacing=5
                            )
                        ],
                        spacing=3
                    ),
                    width=250,
                    padding=15,
                    bgcolor="#FFFFFF",
                    border_radius=8,
                    shadow=ft.BoxShadow(blur_radius=5, color="#395B9D")
                )
            )
        

        # Hasil Pencarian CV
        cv_results_grid = ft.GridView(
            runs_count=3, # Jumlah kolom, sesuaikan dengan keinginan
            max_extent=280, # Lebar maksimal setiap item, ini akan membantu responsivitas
            child_aspect_ratio=0.85, # Sesuaikan rasio aspek kartu
            spacing=10,
            run_spacing=10,
            padding=10,
            # expand=True # Biarkan GridView mengambil ruang yang tersedia
        )

        # Tambahkan beberapa contoh kartu ke grid
        example_cvs = [
            {"name": "Efrina",       "keyword_counts": {"Java": 2, "Python": 2}},
            {"name": "Budi Santoso", "keyword_counts": {"JavaScript": 1, "React": 1, "Node.js": 1}},
            {"name": "Citra Ayu",    "keyword_counts": {"Data Analysis": 2, "SQL": 2, "Tableau": 1}},
            {"name": "David Lee",    "keyword_counts": {"Marketing": 1, "SEO": 1}},
        ]
        for cv_data in example_cvs:
            cv_results_grid.controls.append(create_cv_card(cv_data["name"], cv_data["keyword_counts"]))

        # TODO: dari algoritma
        results_info_text = ft.Text("100 CVs scanned in 100 ms", size=14, color="#863E38", weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER)

        right_panel_content = ft.Container(
            content=ft.Column(
                [   
                    ft.Container(
                        content=ft.Text("Results", size=28, weight=ft.FontWeight.BOLD, color="#256988", text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(bottom=5),
                        # expand=True
                    ),
                    ft.Container(
                        content=results_info_text,
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(bottom=5),
                    ),
                    ft.Divider(height=1, color="#000000"),
                    ft.Container(cv_results_grid, expand=True) # Biarkan GridView mengisi sisa ruang
                ],
                spacing=10,
                # expand=True # Biarkan Column mengambil ruang yang tersedia
            ),
            bgcolor="#DEE2E2",
            padding=ft.padding.all(25),
            border_radius=ft.border_radius.all(10),
            margin=ft.margin.all(10),
        )

        # Main layout - Row with two panels
        main_layout = ft.Row(
            [
                ft.Container(left_panel_content, expand=2, padding=5), # Panel kiri mengambil 2 bagian
                ft.Container(right_panel_content, expand=3, padding=5), # Panel kanan mengambil 3 bagian
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            # expand=True # Biarkan Row utama mengambil sisa tinggi
        )

        # Bersihkan halaman dan tambahkan semua elemen
        self.page.clean()
        self.page.add(
            ft.Column(
                [
                    header_content,
                    ft.Container(main_layout, expand=True) # Biarkan main_layout mengisi sisa ruang vertikal
                ],
                expand=True # Biarkan Column utama mengambil seluruh tinggi halaman
            )
        )
        self.page.update()

def main(page: ft.Page):
    app = Home(page)

if __name__ == "__main__":
    ft.app(target=main)