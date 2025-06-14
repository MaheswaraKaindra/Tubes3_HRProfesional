import flet as ft
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.frontend.home import Home
from src.frontend.about import About
from src.frontend.summary import Summary

app_state = {
    "search_results": [],
    "last_info_text": "",
    "selected_cv": None,
}

def main(page: ft.Page):
    page.title = "CV Analyzer App by HRProfesional"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.bgcolor = '#395B9D'
    final_results = {
                    'name': '10554236', 
                    'path': 'data\Accountant\10554236.pdf',
                    'keyword_counts': 2,
                    'relevance_score': 2
                }
    search_output = {
        'results': final_results,
        'scan_count': 5,
        'exact_time': 100,
        'fuzzy_time': 100
    }

    pages = {
        "/home": Home(page, app_state),
        "/about": About(page),
        "/summary": Summary(page, app_state)
    }

    def route_change(route):
        page.views.clear()
        current_view = pages.get(page.route, pages["/home"]).build_ui()
        current_view.bgcolor = page.bgcolor
        page.views.append(current_view)
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route or "/home")

if __name__ == "__main__":
    ft.app(target=main)
