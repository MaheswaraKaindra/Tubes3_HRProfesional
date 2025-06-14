import flet as ft

def create_cv_card(page:ft.Page, name, results, on_summary_click=None, on_view_cv_click=None, height=250):
    def details_dialog(e):
        full_keyword_texts = []
        for i, (keyword, count) in enumerate(results.items()):
            if (count == 1):
                full_keyword_texts.append(
                ft.Text(f"{i+1}. {keyword}: {count} occurence", size=12, color="#000000")
            )
            elif (count > 1):
                full_keyword_texts.append(
                ft.Text(f"{i+1}. {keyword}: {count} occurences", size=12, color="#000000")
            ) 
        dialog_content = ft.Column(
            controls=full_keyword_texts,
            tight=True,
            scroll=ft.ScrollMode.AUTO,
            height=200,
        )
        details_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Matched keywords: "),
            content=dialog_content,
            scrollable=True,
            actions=[
                ft.TextButton("Close", on_click=lambda e: close_dialog(e), style=ft.ButtonStyle(
                        color="#395B9D",
                        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500)
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        def close_dialog(e):
            details_dialog.open = False
            page.update()

        page.dialog = details_dialog
        details_dialog.open = True
        page.update()

    # result adalah dictionary dengan keyword sebagai key dan jumlah kemunculan sebagai value
    total_matches = sum(count for count in results.values() if isinstance(count, int))
    matched_keywords_text = ft.Container(
        content=ft.Text(f"Matched keywords:", size=12, weight=ft.FontWeight.W_500, color="#000000"),
        on_click=details_dialog,
        tooltip="See all matched keywords",
    )
    keyword_texts = []
    for i, (keyword, count) in enumerate(results.items()):
        if (i == 3):
            keyword_texts.append(ft.Text(f"... and {len(results) - 3} more keywords", size=12, color="#000000"))
            break
        if isinstance(count, int) and count == 1:
            keyword_texts.append(
                ft.Text(f"{i+1}. {keyword}: {count} occurence", size=12, color="#000000")
            )
        elif isinstance(count, int) and count > 1:
            keyword_texts.append(
                ft.Text(f"{i+1}. {keyword}: {count} occurences", size=12, color="#000000")
            )
        else:
            # For fuzzy matches (string), show the string as is
            keyword_texts.append(
                ft.Text(f"{i+1}. {keyword}: {count}", size=12, color="#000000")
            )
        
    return ft.Card(
        height = height,
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
                    matched_keywords_text,
                    ft.Column(keyword_texts, spacing=2, expand=True),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.ElevatedButton("Summary", style=ft.ButtonStyle(
                                                        bgcolor="#395B9D", 
                                                        color="#DEE2E2", 
                                                        shadow_color="#395B9D",
                                                        shape=ft.RoundedRectangleBorder(radius=8) 
                                                    ),
                                                    on_click=on_summary_click
                                        ),
                                alignment=ft.alignment.bottom_left,
                                expand=True,
                            ),
                            ft.Container(
                                content=ft.ElevatedButton("View CV", style=ft.ButtonStyle(
                                                        bgcolor="#395B9D", 
                                                        color="#DEE2E2", 
                                                        shadow_color="#395B9D",
                                                        shape=ft.RoundedRectangleBorder(radius=8)
                                                    ),
                                                    on_click=on_view_cv_click
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