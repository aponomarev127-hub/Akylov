import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

FILE_NAME = "movies.json"

class MovieLibrary:
    def __init__(self, window):
        self.window = window
        self.window.title("Movie Library")
        self.window.geometry("1000x650")

        self.movies = []

        self.build_ui()
        self.load_data()

    # ================= UI =================
    def build_ui(self):
        top = tk.Frame(self.window)
        top.pack(pady=10)

        tk.Label(top, text="Название").grid(row=0, column=0)
        self.title_entry = tk.Entry(top, width=20)
        self.title_entry.grid(row=0, column=1, padx=5)

        tk.Label(top, text="Жанр").grid(row=0, column=2)
        self.genre_box = ttk.Combobox(top, values=["Action","Drama","Comedy","Horror","Sci-Fi","Other"], state="readonly", width=15)
        self.genre_box.grid(row=0, column=3, padx=5)
        self.genre_box.current(0)

        tk.Label(top, text="Год").grid(row=0, column=4)
        self.year_entry = tk.Entry(top, width=10)
        self.year_entry.grid(row=0, column=5, padx=5)

        tk.Label(top, text="Рейтинг (0-10)").grid(row=0, column=6)
        self.rating_entry = tk.Entry(top, width=10)
        self.rating_entry.grid(row=0, column=7, padx=5)

        tk.Button(top, text="Добавить", command=self.add_movie).grid(row=0, column=8, padx=10)
        tk.Button(top, text="Удалить", command=self.delete_movie).grid(row=0, column=9)

        # SEARCH
        search = tk.Frame(self.window)
        search.pack(pady=5)

        tk.Label(search, text="Поиск").grid(row=0, column=0)
        self.search_entry = tk.Entry(search, width=30)
        self.search_entry.grid(row=0, column=1)
        tk.Button(search, text="Найти", command=self.search_movie).grid(row=0, column=2, padx=5)
        tk.Button(search, text="Сброс", command=self.refresh_table).grid(row=0, column=3)

        # FILTER
        filt = tk.Frame(self.window)
        filt.pack(pady=5)

        tk.Label(filt, text="Жанр").grid(row=0, column=0)
        self.filter_genre = ttk.Combobox(filt, values=["All","Action","Drama","Comedy","Horror","Sci-Fi","Other"], state="readonly", width=15)
        self.filter_genre.grid(row=0, column=1)
        self.filter_genre.set("All")

        tk.Label(filt, text="Год").grid(row=0, column=2)
        self.filter_year = tk.Entry(filt, width=10)
        self.filter_year.grid(row=0, column=3)

        tk.Button(filt, text="Фильтр", command=self.refresh_table).grid(row=0, column=4, padx=5)

        # TABLE
        self.tree = ttk.Treeview(self.window, columns=("title","genre","year","rating"), show="headings")

        for col, name in zip(self.tree["columns"], ["Название","Жанр","Год","Рейтинг"]):
            self.tree.heading(col, text=name)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(self.window, text="Сохранить JSON", command=self.save_data).pack(pady=5)

    # ================= LOGIC =================
    def validate(self, year, rating):
        try:
            year = int(year)
        except:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return None

        try:
            rating = float(rating)
            if rating < 0 or rating > 10:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
            return None

        return year, rating

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_box.get()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        if not title:
            messagebox.showerror("Ошибка", "Введите название")
            return

        result = self.validate(year, rating)
        if not result:
            return

        year, rating = result

        self.movies.append({
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        })

        self.refresh_table()
        self.save_data()

    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            return

        for item in selected:
            values = self.tree.item(item)["values"]
            self.movies = [m for m in self.movies if not (
                m["title"] == values[0] and
                m["year"] == values[2]
            )]

        self.refresh_table()
        self.save_data()

    def search_movie(self):
        query = self.search_entry.get().lower()
        self.refresh_table(search=query)

    def refresh_table(self, search=None):
        for i in self.tree.get_children():
            self.tree.delete(i)

        genre = self.filter_genre.get()
        year = self.filter_year.get().strip()

        for m in self.movies:
            if genre != "All" and m["genre"] != genre:
                continue

            if year and str(m["year"]) != year:
                continue

            if search and search not in m["title"].lower():
                continue

            self.tree.insert("", "end", values=(m["title"],m["genre"],m["year"],m["rating"]))

    # ================= JSON =================
    def save_data(self):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                self.movies = json.load(f)
        self.refresh_table()

# RUN
window = tk.Tk()
app = MovieLibrary(window)
window.mainloop()
