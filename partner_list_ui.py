import tkinter as tk
from pathlib import Path
from tkinter import ttk

from partner_discount_service import get_all_partners_with_discounts


BACKGROUND_COLOR = "#ffffff"
CARD_COLOR = "#ffffff"
BORDER_COLOR = "#909090"
TEXT_COLOR = "#1f1f1f"
BUTTON_COLOR = "#f5f5f5"


class PartnerListApplication(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("CRM: Список партнеров и скидок")
        self.geometry("860x620")
        self.minsize(700, 480)
        self.configure(background=BACKGROUND_COLOR)
        self.logo_image = tk.PhotoImage(file=self.get_resource_path("partner_logo.png"))
        self.logo_small = self.logo_image.subsample(14, 14)
        self.logo_icon = self.logo_image.subsample(32, 32)
        self.iconphoto(True, self.logo_icon)
        self.create_header()
        self.create_partner_area()
        self.load_partners()

    @staticmethod
    def get_resource_path(filename: str) -> str:
        return str(Path(__file__).parent / "resources" / filename)

    def create_header(self) -> None:
        header = tk.Frame(self, background=CARD_COLOR, padx=24, pady=16)
        header.pack(fill="x")
        logo_label = tk.Label(header, image=self.logo_small, background=CARD_COLOR)
        logo_label.pack(side="left")
        title_frame = tk.Frame(header, background=CARD_COLOR)
        title_frame.pack(side="left", padx=14)
        title_label = tk.Label(
            title_frame,
            text="CRM: Список партнеров и скидок",
            font=("Arial", 18, "bold"),
            foreground=TEXT_COLOR,
            background=CARD_COLOR,
        )
        title_label.pack(anchor="w")
        subtitle_label = tk.Label(
            title_frame,
            text="Актуальные данные из базы данных",
            font=("Arial", 10),
            foreground="#5f5f5f",
            background=CARD_COLOR,
        )
        subtitle_label.pack(anchor="w")
        refresh_button = tk.Button(
            header,
            text="Обновить",
            command=self.load_partners,
            font=("Arial", 10),
            foreground=TEXT_COLOR,
            background=BUTTON_COLOR,
            activebackground="#e8e8e8",
            activeforeground=TEXT_COLOR,
            borderwidth=1,
            relief="solid",
            padx=14,
            pady=6,
        )
        refresh_button.pack(side="right")

    def create_partner_area(self) -> None:
        container = tk.Frame(self, background=BACKGROUND_COLOR, padx=20, pady=20)
        container.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(container, background=BACKGROUND_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.cards_frame = tk.Frame(self.canvas, background=BACKGROUND_COLOR)
        self.cards_frame.bind("<Configure>", self.update_scroll_region)
        self.cards_window = self.canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", self.resize_cards_frame)
        self.cards_frame.grid_columnconfigure(0, weight=1)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_scroll_region(self, event: tk.Event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def resize_cards_frame(self, event: tk.Event) -> None:
        self.canvas.itemconfigure(self.cards_window, width=event.width)

    def load_partners(self) -> None:
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        try:
            partners = get_all_partners_with_discounts()
        except Exception as error:
            self.show_message(f"Не удалось загрузить данные: {error}")
            return
        if not partners:
            self.show_message("Партнёры не найдены.")
            return
        for index, partner in enumerate(partners):
            self.create_partner_card(partner, index)

    def show_message(self, message: str) -> None:
        message_label = tk.Label(
            self.cards_frame,
            text=message,
            font=("Arial", 12),
            foreground=TEXT_COLOR,
            background=BACKGROUND_COLOR,
        )
        message_label.grid(row=0, column=0, pady=30)

    def create_partner_card(self, partner: dict[str, object], row: int) -> None:
        card = tk.Frame(
            self.cards_frame,
            background=CARD_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            padx=24,
            pady=16,
        )
        card.grid(row=row, column=0, sticky="ew", padx=20, pady=8)
        information = tk.Frame(card, background=CARD_COLOR)
        information.pack(side="left", fill="x", expand=True)
        partner_title = self.format_partner_title(str(partner["partner_name"]))
        name_label = tk.Label(
            information,
            text=partner_title,
            font=("Arial", 12),
            foreground=TEXT_COLOR,
            background=CARD_COLOR,
        )
        name_label.pack(anchor="w")
        director_label = tk.Label(
            information,
            text="Директор",
            font=("Arial", 10),
            foreground=TEXT_COLOR,
            background=CARD_COLOR,
        )
        director_label.pack(anchor="w", pady=(4, 0))
        phone_label = tk.Label(
            information,
            text=f"Телефон: {partner['phone']}",
            font=("Arial", 10),
            foreground=TEXT_COLOR,
            background=CARD_COLOR,
        )
        phone_label.pack(anchor="w")
        rating_value = "не указан" if partner["rating"] is None else f"{partner['rating']:g}"
        rating_label = tk.Label(
            information,
            text=f"Рейтинг: {rating_value}",
            font=("Arial", 10),
            foreground=TEXT_COLOR,
            background=CARD_COLOR,
        )
        rating_label.pack(anchor="w")
        discount_label = tk.Label(
            card,
            text=f"{partner['discount_percent']}%",
            font=("Arial", 12),
            foreground=TEXT_COLOR,
            background=CARD_COLOR,
        )
        discount_label.pack(side="right", padx=10)

    @staticmethod
    def format_partner_title(partner_name: str) -> str:
        name_parts = partner_name.split(" ", 1)
        if len(name_parts) == 1:
            return f"Партнёр | {partner_name}"
        return f"{name_parts[0]} | {name_parts[1]}"


if __name__ == "__main__":
    application = PartnerListApplication()
    application.mainloop()
