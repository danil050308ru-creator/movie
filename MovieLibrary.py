import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []

        self.create_widgets()
        self.load_from_json()

    def create_widgets(self):
        # Ввод данных
        form_frame = ttk.Frame(self.root)
        form_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(form_frame, text="Название:").grid(row=0, column=0, sticky='w')
        self.title_entry = ttk.Entry(form_frame)
        self.title_entry.grid(row=0, column=1, sticky='ew')

        ttk.Label(form_frame, text="Жанр:").grid(row=0, column=2, sticky='w')
        self.genre_entry = ttk.Entry(form_frame)
        self.genre_entry.grid(row=0, column=3, sticky='ew')

        ttk.Label(form_frame, text="Год выпуска:").grid(row=1, column=0, sticky='w')
        self.year_entry = ttk.Entry(form_frame)
        self.year_entry.grid(row=1, column=1, sticky='ew')

        ttk.Label(form_frame, text="Рейтинг:").grid(row=1, column=2, sticky='w')
        self.rating_entry = ttk.Entry(form_frame)
        self.rating_entry.grid(row=1, column=3, sticky='ew')

        form_frame.columnconfigure((1,3), weight=1)

        # Кнопка добавления
        add_button = ttk.Button(self.root, text="Добавить фильм", command=self.add_movie)
        add_button.pack(pady=5)

        # Таблица для фильмов
        self.tree = ttk.Treeview(self.root, columns=("Название", "Жанр", "Год", "Рейтинг"), show='headings')
        for col in ("Название", "Жанр", "Год", "Рейтинг"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        # Фильтры
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(padx=10, pady=5, fill='x')

        ttk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0)
        self.genre_filter = ttk.Entry(filter_frame)
        self.genre_filter.grid(row=0, column=1)

        ttk.Label(filter_frame, text="Фильтр по году:").grid(row=0, column=2)
        self.year_filter = ttk.Entry(filter_frame)
        self.year_filter.grid(row=0, column=3)

        filter_button = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_button.grid(row=0, column=4, padx=5)

        reset_button = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)
        reset_button.grid(row=0, column=5, padx=5)

        # Сохранение/Загрузка
        save_button = ttk.Button(self.root, text="Сохранить в JSON", command=self.save_to_json)
        save_button.pack(side='left', padx=10, pady=5)

        load_button = ttk.Button(self.root, text="Загрузить из JSON", command=self.load_from_json)
        load_button.pack(side='left', padx=10, pady=5)

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        # Валидация
        if not title or not genre or not year_str or not rating_str:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        try:
            year = int(year_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return

        try:
            rating = float(rating_str)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10")
            return

        movie = {
            "название": title,
            "жанр": genre,
            "год": year,
            "рейтинг": rating
        }
        self.movies.append(movie)
        self.update_table()
        self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def update_table(self, filtered_movies=None):
        # Очистить таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        movies_to_show = filtered_movies if filtered_movies is not None else self.movies

        for movie in movies_to_show:
            self.tree.insert('', 'end', values=(
                movie["название"], movie["жанр"], movie["год"], movie["рейтинг"]
            ))

    def apply_filter(self):
        genre_filter = self.genre_filter.get().strip().lower()
        year_filter = self.year_filter.get().strip()

        filtered = self.movies
        if genre_filter:
            filtered = [m for m in filtered if genre_filter in m["жанр"].lower()]

        if year_filter:
            try:
                year = int(year_filter)
                filtered = [m for m in filtered if m["год"] == year]
            except ValueError:
                messagebox.showerror("Ошибка", "Год фильтра должен быть числом")
                return

        self.update_table(filtered)

    def reset_filter(self):
        self.genre_filter.delete(0, tk.END)
        self.year_filter.delete(0, tk.END)
        self.update_table()

    def save_to_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.movies, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Успех", "Данные сохранены успешно")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def load_from_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.movies = json.load(f)
                self.update_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
