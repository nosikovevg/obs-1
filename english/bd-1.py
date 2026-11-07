import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
import random

db = sqlite3.connect("mydict.db")
c = db.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS dict1 (
    n INTEGER PRIMARY KEY AUTOINCREMENT,
    t TEXT,
    en TEXT,
    ru TEXT,
    re BOOLEAN DEFAULT 0,
    komm TEXT
)
""")
db.commit()


def save_to_db():
    en_text = entry_en.get().strip()
    ru_text = entry_ru.get().strip()
    t_text = entry_t.get().strip()
    komm_text = entry_komm.get().strip()
    re_value = re_var.get()

    if not en_text or not ru_text:
        messagebox.showwarning("Внимание", "Пожалуйста, заполните поля EN и RU!")
        return

    try:
        c.execute(
            "INSERT INTO dict1 (t, en, ru, re, komm) VALUES (?, ?, ?, ?, ?)",
            (t_text, en_text, ru_text, re_value, komm_text)
        )
        db.commit()

        entry_t.delete(0, END)
        entry_en.delete(0, END)
        entry_ru.delete(0, END)
        entry_komm.delete(0, END)
        re_var.set(False)

        load_table_data()
        messagebox.showinfo("Успех", "Данные успешно сохранены!")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")


def load_table_data():
    for row in tree.get_children():
        tree.delete(row)

    try:
        c.execute("SELECT n, t, en, ru, re, komm FROM dict1")
        rows = c.fetchall()

        for row in rows:
            re_status = "Да" if row[4] else "Нет"
            tree.insert("", END, values=(row[0], row[1], row[2], row[3], re_status, row[5]))

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

def update_count():
    try:
        c.execute("SELECT COUNT(*) FROM dict1")
        count = c.fetchone()[0]
        label_count.config(text=f"Количество записей в таблице dict1: {count}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось получить количество записей: {e}")
# def show_random_en():
#     try:
#         c.execute(
#             "SELECT en FROM dict1 WHERE re = 0 ORDER BY RANDOM() LIMIT 1"
#         )
#         row = c.fetchone()

#         if row is None:
#             label_random.config(text="Нет слов для повторения (все re = 1)")
#         else:
#             label_random.config(text=f"Случайное слово: {row[0]}")

#     except Exception as e:
#         messagebox.showerror("Ошибка", f"Не удалось выбрать случайное слово: {e}")

current_random_id = None


def show_random_en():
    global current_random_id

    try:
        c.execute(
            "SELECT n, en FROM dict1 WHERE re = 0 ORDER BY RANDOM() LIMIT 1"
        )
        row = c.fetchone()

        if row is None:
            current_random_id = None
            label_random_en.config(text="Нет слов для повторения (все re = 1)")
            btn_show_ru.config(state=DISABLED)
        else:
            current_random_id = row[0]
            label_random_en.config(text=f"Случайное слово: {row[1]}")
            btn_show_ru.config(state=NORMAL)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось выбрать случайное слово: {e}")
#----------------------------------------------
def show_ru_for_current():
    if current_random_id is None:
        messagebox.showwarning("Внимание", "Сначала выберите случайное слово!")
        return

    try:
        c.execute(
            "SELECT ru FROM dict1 WHERE n = ?",
            (current_random_id,)
        )
        row = c.fetchone()

        if row is None:
            label_ru_random.config(text="Перевод не найден")
        else:
            label_ru_random.config(text=f"Перевод: {row[0]}")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось получить перевод: {e}")
##############################################################
def show_random_ru():
    global current_random_id

    try:
        c.execute(
            "SELECT n, ru FROM dict1 WHERE re = 0 ORDER BY RANDOM() LIMIT 1"
        )
        row = c.fetchone()

        if row is None:
            current_random_id = None
            label_random_ru.config(text="Нет слов для повторения (все re = 1)")
            btn_show_en.config(state=DISABLED)
        else:
            current_random_id = row[0]
            label_random_ru.config(text=f"Случайное слово: {row[1]}")
            btn_show_en.config(state=NORMAL)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось выбрать случайное слово: {e}")
#----------------------------------------------
#----------------------------------------------
def show_en_for_current():
    if current_random_id is None:
        messagebox.showwarning("Внимание", "Сначала выберите случайное слово!")
        return

    try:
        c.execute(
            "SELECT en FROM dict1 WHERE n = ?",
            (current_random_id,)
        )
        row = c.fetchone()

        if row is None:
            label_en_random.config(text="Перевод не найден")
        else:
            label_en_random.config(text=f"Перевод: {row[0]}")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось получить перевод: {e}")

##################################################################
root = Tk()
root.title("Урок английского языка - AUDIO")
root.geometry("900x600+150+150")

notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)

tab1 = Frame(notebook, padx=15, pady=15)
tab2 = Frame(notebook, padx=15, pady=15)
tab3 = Frame(notebook, padx=15, pady=15)
tab4 = Frame(notebook, padx=15, pady=15)
notebook.add(tab1, text="Добавить запись")
notebook.add(tab2, text="Просмотр базы (dict1)")
notebook.add(tab3, text="Тренажер 1")
notebook.add(tab4, text="Тренажер 2")
# ---------- Вкладка добавления ----------

Label(tab1, text="Тип (t):", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
entry_t = Entry(tab1, width=30, font=("Arial", 10))
entry_t.grid(row=0, column=1, pady=5, padx=5)

Label(tab1, text="Английское слово (en):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
entry_en = Entry(tab1, width=30, font=("Arial", 10))
entry_en.grid(row=1, column=1, pady=5, padx=5)

Label(tab1, text="Русский перевод (ru):", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
entry_ru = Entry(tab1, width=30, font=("Arial", 10))
entry_ru.grid(row=2, column=1, pady=5, padx=5)

Label(tab1, text="Комментарий (komm):", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
entry_komm = Entry(tab1, width=30, font=("Arial", 10))
entry_komm.grid(row=3, column=1, pady=5, padx=5)

re_var = BooleanVar(value=False)

Checkbutton(
    tab1,
    text="Повторить слово (re)",
    variable=re_var,
    font=("Arial", 10)
).grid(row=4, column=1, sticky="w", pady=5)

Button(
    tab1,
    text="Сохранить в БД",
    command=save_to_db,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold")
).grid(row=5, column=0, columnspan=2, pady=15, sticky="we")

# ---------- Вкладка просмотра ----------

columns = ("n", "t", "en", "ru", "re", "komm")

tree = ttk.Treeview(tab2, columns=columns, show="headings")

tree.heading("n", text="ID (n)")
tree.heading("t", text="Тип (t)")
tree.heading("en", text="English (en)")
tree.heading("ru", text="Русский (ru)")
tree.heading("re", text="Повт. (re)")
tree.heading("komm", text="Коммент (komm)")

tree.column("n", width=50, anchor="center")
tree.column("t", width=100)
tree.column("en", width=150)
tree.column("ru", width=150)
tree.column("re", width=80, anchor="center")
tree.column("komm", width=200)

tree.pack(fill=BOTH, expand=True, side=LEFT)

scrollbar = ttk.Scrollbar(tab2, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(fill=Y, side=RIGHT)

Button(
    tab2,
    text="Обновить таблицу",
    command=load_table_data,
    bg="#2196F3",
    fg="white",
    font=("Arial", 9)
).pack(fill=X, pady=5)

load_table_data()
# ---------- Вкладка тренажера 1----------
label_count = Label(
    tab3,
    text="Количество записей в таблице dict1: 0",
    font=("Arial", 12, "bold")
)
label_count.pack(pady=20)

Button(
    tab3,
    text="Обновить количество",
    command=update_count,
    bg="#2196F3",
    fg="white",
    font=("Arial", 10, "bold")
).pack(pady=10)

label_random_en = Label(
    tab3,
    text="Случайное слово: —",
    font=("Arial", 14, "bold"),
    wraplength=500
)
label_random_en.pack(pady=20)

Button(
    tab3,
    text="Показать случайное слово (re = 0)",
    command=show_random_en,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold")
).pack(pady=10)
#------------------------------------------------------
btn_show_ru = Button(
    tab3,
    text="Показать перевод (ru)",
    command=show_ru_for_current,
    bg="#FF9800",
    fg="white",
    font=("Arial", 10, "bold"),
    state=DISABLED
)
btn_show_ru.pack(pady=10)

label_ru_random = Label(
    tab3,
    text="Перевод: —",
    font=("Arial", 14, "bold"),
    wraplength=500
)
label_ru_random.pack(pady=10)

# ---------- Вкладка тренажера 2-----------------
label_random_ru = Label(
    tab4,
    text="Случайное слово: —",
    font=("Arial", 14, "bold"),
    wraplength=500
)
label_random_ru.pack(pady=20)

Button(
    tab4,
    text="Показать случайное слово ru (re = 0)",
    command=show_random_ru,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold")
).pack(pady=10)
#------------------------------------------------------
btn_show_en = Button(
    tab4,
    text="Показать перевод (en)",
    command=show_en_for_current,
    bg="#FF9800",
    fg="white",
    font=("Arial", 10, "bold"),
    state=DISABLED
)
btn_show_en.pack(pady=10)
label_en_random = Label(
    tab4,
    text="Перевод: —",
    font=("Arial", 14, "bold"),
    wraplength=500
)
label_en_random.pack(pady=10)


root.mainloop()

c.execute("SELECT * FROM dict1")
print(c.fetchall())

db.close()