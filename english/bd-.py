import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
db=sqlite3.connect('mydict.db')
c=db.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS dict1 (
    n INTEGER PRIMARY KEY AUTOINCREMENT,
    t TEXT,
    en TEXT,
    ru TEXT,
    re BOOLEAN DEFAULT 0,
    komm TEXT
)""")

def save_to_db():
    """Берет данные из полей ввода и сохраняет в БД."""
    en_text = entry_en.get().strip()
    ru_text = entry_ru.get().strip()

    # Проверка на пустые поля
    if not en_text or not ru_text:
        messagebox.showwarning("Внимание", "Пожалуйста, заполните оба поля!")
        return

    try:
        conn = sqlite3.connect("mydict.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO dict1 (en, ru, re) VALUES (?, ?, ?)", (en_text, ru_text, re_var)
        )
        conn.commit()
        conn.close()

        # Очищаем поля после успешного сохранения
        entry_en.delete(0, END)
        entry_ru.delete(0, END)

        messagebox.showinfo("Успех", "Данные успешно сохранены!")
    except Exception as e:
        messagebox.onerror("Ошибка", f"Не удалось сохранить данные: {e}")

###################################################
def load_table_data():
    """Выбирает все данные из БД и отрисовывает их в таблице Treeview."""
    # Сначала очищаем старые данные из виджета таблицы
    for row in tree.get_children():
        tree.delete(row)

    try:
        conn = sqlite3.connect("mydict.db")
        cursor = conn.cursor()
        cursor.execute("SELECT n, t, en, ru, re, komm FROM dict1")
        rows = cursor.fetchall()
        conn.close()

        # Заполняем таблицу строками из БД
        for row in rows:
            # Превращаем 1/0 из базы в красивый текст для отображения флажка
            re_status = "Да" if row[4] else "Нет"
            
            # Вставляем данные, заменяя True/False на понятный статус
            tree.insert("", END, values=(row[0], row[1], row[2], row[3], re_status, row[5]))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")


####################################################
from tkinter import *
root = Tk()
root.title("Урок английского языка")
root.geometry("800x200+150+150")
#######################################################
# ================= СВОЙСТВО ВКЛАДОК (NOTEBOOK) =================
notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)

# Создаем фреймы для самих вкладок
tab1 = Frame(notebook, padx=15, pady=15)
tab2 = Frame(notebook, padx=15, pady=15)

# Добавляем фреймы в панели вкладок с названиями
notebook.add(tab1, text="Добавить запись")
notebook.add(tab2, text="Просмотр базы (dict1)")

#####################################################
# Контейнер для отступов
frame = Frame(root, padx=20, pady=20)
frame.pack(fill=BOTH, expand=True)

# Поле ввода для EN
label_en = Label(tab1, text="Английское слово (en):", font=("Arial", 10))
label_en.grid(row=0, column=0, sticky="w", pady=5)

entry_en = Entry(tab1, width=25, font=("Arial", 10))
entry_en.grid(row=0, column=1, pady=5, padx=5)

# Поле ввода для RU
label_ru = Label(tab1, text="Русский перевод (ru):", font=("Arial", 10))
label_ru.grid(row=1, column=0, sticky="w", pady=5)

entry_ru = Entry(tab1, width=25, font=("Arial", 10))
entry_ru.grid(row=1, column=1, pady=5, padx=5)

# Кнопка сохранения
btn_save = Button(
    tab1,
    text="Сохранить в БД",
    command=save_to_db,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold"),
)
btn_save.grid(row=2, column=0, columnspan=2, pady=20, sticky="we")
################
# 1. Создаем булеву переменную Tkinter (по умолчанию False / 0)
re_var = BooleanVar(value=False)

# 2. Привязываем переменную к виджету Checkbutton через параметр variable
check_re = Checkbutton(
    tab1, text="Повторить слово (re)", variable=re_var, font=("Arial", 10)
)
check_re.grid(row=5, column=1, sticky="w", pady=5)
###################################################
# ================= НАПОЛНЕНИЕ ВКЛАДКИ 2 (ТАБЛИЦА) =================
# Названия колонок для отображения
columns = ("n", "t", "en", "ru", "re", "komm")

tree = ttk.Treeview(tab2, columns=columns, show="headings")
tree.pack(fill=BOTH, expand=True, side=LEFT)

# Настраиваем заголовки таблиц и ширину колонок
tree.heading("n", text="ID (n)")
tree.heading("t", text="Тип (t)")
tree.heading("en", text="English (en)")
tree.heading("ru", text="Русский (ru)")
tree.heading("re", text="Повт. (re)")
tree.heading("komm", text="Коммент (komm)")

tree.column("n", width=50, anchor="center")
tree.column("t", width=80)
tree.column("en", width=120)
tree.column("ru", width=120)
tree.column("re", width=70, anchor="center")
tree.column("komm", width=150)

# Скроллбар для таблицы (если записей будет много)
scrollbar = ttk.Scrollbar(tab2, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(fill=Y, side=RIGHT)

# Кнопка ручного обновления таблицы (хотя она обновляется сама при сохранении)
btn_refresh = Button(tab2, text="Обновить таблицу", command=load_table_data, bg="#2196F3", fg="white", font=("Arial", 9))
btn_refresh.pack(fill=X, pady=5)

# Первичная загрузка существующих данных при старте приложения
load_table_data()



####################################################
root.mainloop()
####################################################
c.execute("SELECT * FROM dict1")
print(c.fetchall())
db.commit()
db.close()