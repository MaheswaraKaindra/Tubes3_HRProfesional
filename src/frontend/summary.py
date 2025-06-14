import flet as ft
from . import utils
from ..backend.extract_summary import parse_resume, print_parse_result
from ..backend.pdf_to_string import pdf_to_string
from ..backend.fetch_from_db import get_applicant_by_cv_path

class Summary:
    def __init__(self, page: ft.Page, state: dict):
        self.page = page
        self.state = state
        self.page.title = "CV Analyzer App by HRProfesional"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.bgcolor = '#395B9D'

    def build_ui(self):
        selected_cv = self.state.get("selected_cv")
        if not selected_cv:
            return ft.View(
                route="/summary",
                bgcolor=self.page.bgcolor,
                controls=[
                    ft.Text("No CV selected. Please select a CV from the home page.", color="#FAF7F0", size=24, weight=ft.FontWeight.BOLD)
                ]
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

        # Left Panel - Other CVs
        cv_results_grid = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            # padding=10,
            expand=True
        )

        def on_summary_click(cv_data):
            self.state["selected_cv"] = cv_data
            self.page.views.append(Summary(self.page, self.state).build_ui())
            self.page.go("/summary")

        def on_view_cv_click(e):
            self.page.clean()

        for cv_data in self.state.get("search_results", []):
            if cv_data.get("path") != selected_cv.get("path"):
                summary_handler = lambda _, cv=cv_data: on_summary_click(cv)
                cv_results_grid.controls.append(
                    utils.create_cv_card(self.page, 
                        cv_data["name"], 
                        cv_data["keyword_counts"], 
                        on_summary_click=summary_handler, 
                        on_view_cv_click=on_view_cv_click
                    )
                )

        left_panel_content = ft.Container(
            content=ft.Column(
                [ 
                    ft.Text("Other CVs", size=20, weight=ft.FontWeight.BOLD, color="#DEE2E2", text_align=ft.TextAlign.CENTER),
                    # ft.Divider(height=1, color="#000000"),
                    cv_results_grid,
                ],
                spacing=5,
                expand=True
            ),
            bgcolor="#395B9D",
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

        cv_path = selected_cv.get("path")
        if not cv_path:
            return ft.View(route="/summary", controls=[ft.Text("No search results yet!")])
        text = pdf_to_string(cv_path) if cv_path else ""
        parsed_text = parse_resume(text) if text else {}
        profile = get_applicant_by_cv_path(cv_path) if cv_path else {}

        profile_card = ft.Card(
            height=200,
            content=ft.Container(
                content=ft.Column(
                    [   
                        ft.Text("PROFILE", size=20, weight=ft.FontWeight.BOLD, color="#000000", text_align=ft.TextAlign.CENTER),
                        ft.Divider(height=1, color="#000000"),
                        ft.Text(f"Name: {profile[1]} \nDate of Birth: {profile[2]} \nAddress: {profile[3]} \nPhone Number: {profile[4]} \nRole: {profile[5]} \n", 
                                size=16, color="#000000", text_align=ft.TextAlign.LEFT),
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

        cv_summary_grid.controls.append(profile_card) # profil

        summary_string = "\n".join(parsed_text.get('summary', [])) or "Not available"
        skills_string = "\n".join(parsed_text.get('skills', [])) or "Not available"
        education_string = "\n".join(parsed_text.get('education', [])) or "Not available"
        experience_items = []
        for job in parsed_text.get('experience', []):
            date_range = job.get('date_range') or '-'
            company = job.get('company') or '-'
            location = job.get('location') or '-'
            job_title = job.get('job_title') or '-'
            responsibilities_list = job.get('responsibilities', [])
            if responsibilities_list:
                responsibilities_text = '\n'.join([f"  • {resp}" for resp in responsibilities_list])
            else:
                responsibilities_text = "-"
            job_text = (
                f"Date range: {date_range}\n"
                f"Company: {company}\n"
                f"Location: {location}\n"
                f"Job Title: {job_title}\n"
                f"Responsibilities:\n{responsibilities_text}"
            )
            experience_items.append(job_text)
        experience_string = "\n\n".join(experience_items) or "Not available"

        cv_summary_grid.controls.append(create_cv_summary_card("SUMMARY", summary_string))
        cv_summary_grid.controls.append(create_cv_summary_card("SKILLS", skills_string))
        cv_summary_grid.controls.append(create_cv_summary_card("EXPERIENCE", experience_string))
        cv_summary_grid.controls.append(create_cv_summary_card("EDUCATION", education_string))
        
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
            route="/summary",
            bgcolor=self.page.bgcolor,
            controls=[
                ft.Column(
                    [
                        self.header_content,
                        ft.Container(main_layout, expand=True),
                    ],
                    expand=True,
                )
            ]
        )

def main(page: ft.Page):
    summary = Summary(page)
    page.views.append(summary.build_ui())
    # page.bgcolor = '#395B9D'
    page.update()
    # home = home(page)
    # output = home.search_output
    # cv_path = output['results']['path']
    # text = pdf_to_string(cv_path)
    # parsed_text = parse_resume(text)
    # profile = get_applicant_by_cv_path(cv_path)

    # print_parse_result(parsed_text)
    # print(profile)

if __name__ == "__main__":
    ft.app(target=main)