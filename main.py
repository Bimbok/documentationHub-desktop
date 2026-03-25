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
            padding=5,
            content=ft.Card(
                elevation=8,
                color="#1E1E1E",
                surface_tint_color="#00FF88",
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.DESCRIPTION_OUTLINED,
                                        color="#00FF88",
                                        size=24,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            doc.get("category", "Uncategorized").upper(),
                                            size=10,
                                            weight=ft.FontWeight.W_600,
                                            color="#00FF88",
                                        ),
                                        padding=ft.padding.symmetric(6, 10),
                                        border=ft.border.all(1, "#00FF88"),
                                        border_radius=15,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Container(height=10),
                            ft.Text(
                                doc.get("title", "No Title"),
                                style=ft.TextThemeStyle.TITLE_LARGE,
                                weight=ft.FontWeight.BOLD,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                doc.get("document", "")[:80] + "...",
                                size=14,
                                color=ft.Colors.WHITE70,
                                max_lines=3,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                        spacing=10,
                    ),
                ),
            ),
            on_click=lambda e: on_tap(doc),
            ink=True,
            border_radius=ft.border_radius.all(16),
            on_hover=self._on_hover,
            animate=ft.Animation(300, ft.AnimationCurve.DECELERATE),
        )

    def _on_hover(self, e):
        self.scale = 1.05 if e.data == "true" else 1.0
        self.update()


def main(page: ft.Page):
    page.title = "bimbok-docs"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121212"  # Deeper dark background
    page.padding = 0  # We'll use custom padding for main content
    page.fonts = {
        "Inter": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        "JetBrains Mono": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap"
    }
    page.theme = ft.Theme(
        font_family="Inter",
        color_scheme=ft.ColorScheme(
            primary="#00FF88",  # Vibrant neon green accent
            secondary="#00FF88",
            surface="#1E1E1E",
            on_surface=ft.Colors.WHITE,
            outline="#333333",
        ),
        visual_density=ft.VisualDensity.COMFORTABLE,
    )

    all_docs = []
    current_category = "All"

    # Show loading indicator
    loading_indicator = ft.Container(
        content=ft.Column(
            [
                ft.ProgressRing(color="#00FF88", stroke_width=4, width=40, height=40),
                ft.Container(height=20),
                ft.Text("Initializing Documentation Hub...", size=18, weight=ft.FontWeight.W_500),
                ft.Text("Connecting to MongoDB Atlas", size=14, color=ft.Colors.WHITE70),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
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
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.WIFI_OFF_ROUNDED, color="#FF4444", size=64),
                        ft.Container(height=20),
                        ft.Text("Connection Failed", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Could not reach MongoDB: {e}", color=ft.Colors.WHITE70, text_align=ft.TextAlign.CENTER),
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "Retry Connection",
                            on_click=lambda _: page.go("/"),
                            style=ft.ButtonStyle(color="#00FF88"),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
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
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        doc.get("title", "No Title"),
                                        style=ft.TextThemeStyle.HEADLINE_LARGE,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            doc.get("category", "Uncategorized").upper(),
                                            size=12,
                                            weight=ft.FontWeight.W_600,
                                            color="#00FF88",
                                        ),
                                        padding=ft.padding.symmetric(8, 12),
                                        border=ft.border.all(1, "#00FF88"),
                                        border_radius=20,
                                    ),
                                ],
                                spacing=10,
                            ),
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE_ROUNDED,
                            on_click=close_bs,
                            icon_color=ft.Colors.WHITE70,
                            hover_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Divider(color="#333333", height=40),
                ft.Markdown(
                    doc.get("document", "*No document content*"),
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    code_theme="atom-one-dark",
                    on_tap_link=lambda e: page.launch_url(e.data),
                ),
                ft.Container(height=20),
                ft.Text("Code Example", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD, color="#00FF88"),
                ft.Container(
                    content=ft.Markdown(
                        f"```python\n{doc.get('code', '# No code found')}\n```",
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        code_theme="atom-one-dark",
                    ),
                    bgcolor="#1E1E1E",
                    padding=20,
                    border_radius=12,
                    border=ft.border.all(1, "#333333"),
                ),
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        )

        bs = ft.BottomSheet(
            ft.Container(
                doc_content,
                padding=40,
                bgcolor="#121212",
                border_radius=ft.border_radius.only(top_left=30, top_right=30),
            ),
            open=True,
            is_scroll_controlled=True,
        )
        page.overlay.append(bs)
        page.update()

    docs_grid = ft.ResponsiveRow(spacing=25, run_spacing=25)

    def create_cards(docs):
        cards = []
        for doc in docs:
            cards.append(
                ft.Column(
                    [DocCard(doc, open_doc_view)],
                    col={"xs": 12, "sm": 6, "md": 6, "lg": 4, "xl": 3},
                )
            )
        return cards

    def update_grid(filtered_docs=None):
        if filtered_docs is None:
            if current_category == "All":
                filtered_docs = all_docs
            else:
                filtered_docs = [d for d in all_docs if d.get("category") == current_category]
        
        docs_grid.controls = create_cards(filtered_docs)
        docs_grid.update()

    def search_docs(e):
        search_term = e.control.value.lower()
        if not search_term:
            update_grid()
        else:
            base_docs = all_docs if current_category == "All" else [d for d in all_docs if d.get("category") == current_category]
            filtered_docs = [
                doc
                for doc in base_docs
                if search_term in doc.get("title", "").lower()
                or search_term in doc.get("category", "").lower()
                or search_term in doc.get("document", "").lower()
            ]
            update_grid(filtered_docs)

    def category_changed(e):
        nonlocal current_category
        index = e.control.selected_index
        if index == 0:
            current_category = "All"
        else:
            current_category = categories[index - 1]
        update_grid()

    search_bar = ft.TextField(
        hint_text="Search documentation...",
        on_change=search_docs,
        prefix_icon=ft.Icons.SEARCH_ROUNDED,
        border_color="#333333",
        focused_border_color="#00FF88",
        border_radius=15,
        bgcolor="#1E1E1E",
        content_padding=20,
        expand=True,
    )

    # Get unique categories
    categories = sorted(list(set(doc.get("category", "Uncategorized") for doc in all_docs)))
    
    rail_destinations = [
        ft.NavigationRailDestination(
            icon=ft.Icons.ALL_INBOX_OUTLINED,
            selected_icon=ft.Icons.ALL_INBOX,
            label="All Documents",
        )
    ]
    for cat in categories:
        rail_destinations.append(
            ft.NavigationRailDestination(
                icon=ft.Icons.FOLDER_OUTLINED,
                selected_icon=ft.Icons.FOLDER,
                label=cat,
            )
        )

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.SELECTED,
        min_width=100,
        min_extended_width=200,
        leading=ft.Image(src="/logo.ico", width=40, height=40),
        group_alignment=-0.9,
        destinations=rail_destinations,
        on_change=category_changed,
        bgcolor="#1E1E1E",
    )

    # Main Content Area
    content_area = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Documentation Hub",
                            style=ft.TextThemeStyle.DISPLAY_SMALL,
                            weight=ft.FontWeight.W_800,
                        ),
                        ft.Container(expand=True),
                        ft.Icon(ft.Icons.TERMINAL_ROUNDED, color="#00FF88", size=32),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=20),
                ft.Row([search_bar]),
                ft.Divider(color="#333333", height=40),
                ft.Column([docs_grid], scroll=ft.ScrollMode.HIDDEN, expand=True),
            ],
            expand=True,
        ),
        padding=40,
        expand=True,
    )

    # Clear loading and add final layout
    page.controls.clear()
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1, color="#333333"),
                content_area,
            ],
            expand=True,
            spacing=0,
        )
    )
    update_grid()
    page.update()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
