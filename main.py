import flet as ft
import pymongo
import os
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.environ.get("MONGODB_URI")
DATABASE_NAME = "bdoci"
COLLECTION_NAME = "docs"


class DocCard(ft.Container):
    def __init__(self, doc, on_tap):
        super().__init__(
            content=ft.Card(
                elevation=4,
                color="#2a2a2a",
                content=ft.Container(
                    padding=15,
                    content=ft.Column(
                        [
                            ft.Text(
                                doc.get("title", "No Title"),
                                style=ft.TextThemeStyle.HEADLINE_SMALL,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                f"Category: {doc.get('category', 'Uncategorized')}",
                                italic=True,
                                color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE),
                            ),
                        ],
                        spacing=5,
                    ),
                ),
            ),
            on_click=lambda e: on_tap(doc),
            ink=True,
            border_radius=ft.border_radius.all(10),
        )


def main(page: ft.Page):
    page.title = "bimbok-docs"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1a1a1a"
    page.padding = 20
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"
    }
    page.theme = ft.Theme(font_family="Roboto")

    all_docs = []

    # Show loading indicator
    loading_indicator = ft.Column(
        [ft.ProgressRing(), ft.Text("Connecting to the database...")],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )
    page.add(loading_indicator)
    page.update()

    client = None
    try:
        print("Connecting to MongoDB...")
        client = pymongo.MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.server_info()
        print("Connection successful!")
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        print(f"Fetching data from '{COLLECTION_NAME}' collection...")
        all_docs = list(collection.find({}))
        print(f"Found {len(all_docs)} documents.")

    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        page.controls.clear()
        page.add(
            ft.Column(
                [
                    ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED, size=48),
                    ft.Text(f"MongoDB connection error: {e}", color=ft.Colors.RED),
                    ft.Text(
                        "Please check your connection string and network settings."
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            )
        )
        page.update()
        return
    except Exception as e:
        page.controls.clear()
        page.add(ft.Text(f"An unexpected error occurred: {e}", color=ft.Colors.RED))
        page.update()
        return
    finally:
        if client:
            client.close()
            print("MongoDB connection closed.")

    def open_doc_view(doc):
        def close_bs(e):
            bs.open = False
            page.update()

        doc_content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            doc.get("title", "No Title"),
                            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                            weight=ft.FontWeight.BOLD,
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            on_click=close_bs,
                            icon_color=ft.Colors.WHITE,
                        ),
                    ]
                ),
                ft.Text(
                    f"Category: {doc.get('category', 'Uncategorized')}",
                    italic=True,
                    color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE),
                ),
                ft.Divider(color="#00ff00"),
                ft.Markdown(
                    doc.get("document", "*No document content*"),
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.COMMON_MARK,
                ),
                ft.Text("Code:", style=ft.TextThemeStyle.TITLE_MEDIUM),
                ft.Container(
                    content=ft.Markdown(
                        f"```python\n{doc.get('code', '# No code found')}\n```",
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        code_theme="atom-one-dark",
                    ),
                    bgcolor="#282c34",
                    padding=10,
                    border_radius=10,
                ),
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        )

        bs = ft.BottomSheet(
            ft.Container(
                doc_content,
                padding=20,
                bgcolor="#1a1a1a",
            ),
            open=True,
            on_dismiss=lambda e: None,
        )
        page.overlay.append(bs)
        page.update()

    docs_grid = ft.ResponsiveRow(spacing=20, run_spacing=20)

    def create_cards(docs):
        cards = []
        for doc in docs:
            cards.append(
                ft.Column(
                    [DocCard(doc, open_doc_view)],
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                )
            )
        return cards

    docs_grid.controls = create_cards(all_docs)

    def search_docs(e):
        search_term = e.control.value.lower()
        if not search_term:
            docs_grid.controls = create_cards(all_docs)
        else:
            filtered_docs = [
                doc
                for doc in all_docs
                if search_term in doc.get("title", "").lower()
                or search_term in doc.get("category", "").lower()
                or search_term in doc.get("document", "").lower()
            ]
            docs_grid.controls = create_cards(filtered_docs)
        docs_grid.update()

    search_bar = ft.TextField(
        label="Search documents...",
        on_change=search_docs,
        border_color="#00ff00",
        focused_border_color=ft.Colors.with_opacity(0.7, "#00ff00"),
        border_radius=10,
    )

    # Clear loading and add content
    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Documentation Hub",
                            style=ft.TextThemeStyle.DISPLAY_SMALL,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Container(width=10),
                        ft.Icon(ft.Icons.CODE, color="#00ff00", size=36),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                search_bar,
                ft.Divider(color="#00ff00", height=20),
                ft.Column([docs_grid], scroll=ft.ScrollMode.AUTO, expand=True),
            ],
            expand=True,
        )
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
