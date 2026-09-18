import tkinter as tk
from pathlib import Path
from tkinter import ttk

from partner_discount_service import get_all_partners_with_discounts


BACKGROUND_COLOR = "#f4f4f4"
CARD_COLOR = "#ffffff"
BORDER_COLOR = "#8a8a8a"
TEXT_COLOR = "#1f1f1f"
ACCENT_COLOR = "#2d6ca2"


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
            foreground=CARD_COLOR,
            background=ACCENT_COLOR,
            activebackground="#24567f",
            activeforeground=CARD_COLOR,
            borderwidth=0,
            padx=16,
            pady=8,
        )
        refresh_button.pack(side="right")

    def create_partner_area(self) -> None:
        container = tk.Frame(self, background=BACKGROUND_COLOR, padx=20, pady=20)
        container.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(container, background=BACKGROUND_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.cards_frame = tk.Frame(self.canvas, background=BACKGROUND_COLOR)
        self.cards_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_scroll_region(self, event: tk.Event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

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
        for partner in partners:
            self.create_partner_card(partner)

    def show_message(self, message: str) -> None:
        message_label = tk.Label(
            self.cards_frame,
            text=message,
            font=("Arial", 12),
            foreground=TEXT_COLOR,
            background=BACKGROUND_COLOR,
        )
        message_label.pack(pady=30)

    def create_partner_card(self, partner: dict[str, object]) -> None:
        card = tk.Frame(
            self.cards_frame,
            background=CARD_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            padx=24,
            pady=16,
        )
        card.pack(fill="x", padx=1, pady=8)
        information = tk.Frame(card, background=CARD_COLOR)
        information.pack(side="left", fill="x", expand=True)
        name_label = tk.Label(
            information,
            text=f"Партнёр | {partner['partner_name']}",
            font=("Arial", 13),
            foreground=TEXT_COLOR,
            background=CARD_COLOR,
        )
        name_label.pack(anchor="w")
        email_label = tk.Label(
            information,
            text=f"Email: {partner['email']}",
            font=("Arial", 10),
            foreground=TEXT_COLOR,
            background=CARD_COLOR,
        )
        email_label.pack(anchor="w", pady=(4, 0))
        phone_label = tk.Label(
            information,
            text=f"Телефон: {partner['phone']}",
            font=("Arial", 10),
            foreground=TEXT_COLOR,
            background=CARD_COLOR,
        )
        phone_label.pack(anchor="w")
        quantity_label = tk.Label(
            information,
            text=f"Объём: {partner['total_quantity']} шт.",
            font=("Arial", 10),
            foreground=TEXT_COLOR,
            background=CARD_COLOR,
        )
        quantity_label.pack(anchor="w")
        discount_label = tk.Label(
            card,
            text=f"{partner['discount_percent']}%",
            font=("Arial", 16),
            foreground=TEXT_COLOR,
            background=CARD_COLOR,
        )
        discount_label.pack(side="right", padx=10)


if __name__ == "__main__":
    application = PartnerListApplication()
    application.mainloop()
