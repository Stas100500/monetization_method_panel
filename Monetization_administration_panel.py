import tkinter as tk
from tkinter import ttk

class Content:
    def __init__(self, name, creator, base_price):
        self.name = name
        self.creator = creator
        self.base_price = base_price
        self.rented = False
        self.rental_price = base_price  # Изначальная цена аренды

    def rent_content(self):
        self.rented = True

    def extend_rental(self):
        if self.rented:
            print(f"Продление аренды для {self.name} успешно.")
        else:
            print(f"{self.name} в данный момент не арендуется.")

    def offer_discount(self, discount):
        if self.rented:
            self.rental_price -= self.rental_price * discount
            print(f"Скидка {discount} предложена для {self.name}. Новая цена аренды: {self.rental_price}")
        else:
            print(f"{self.name} в данный момент не арендуется.")
            
    def final_offer(self, discount):
        if self.rented:
            final_price = self.base_price * (1 - discount)
            print(f"Финальное предложение для {self.name}: {final_price}.")
        else:
            print(f"{self.name} в данный момент не арендуется.")      
class User:
   def __init__(self, name, balance=0):
        self.name = name
        self.partnerships = []  # Здесь хранятся партнёрские программы, к которым принадлежит пользователь
        self.balance = balance  # Атрибут для отслеживания баланса счета пользователя

   def add_funds(self, amount):
        self.balance += amount
        print(f"Баланс счета пользователя {self.name} увеличен на {amount}. Новый баланс: {self.balance}")
   def deduct_funds(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Списано {amount} с баланса счета пользователя {self.name}. Новый баланс: {self.balance}")
            return True
        else:
            print(f"Недостаточно средств на балансе счета пользователя {self.name}.")
            return False

class Game:
    def __init__(self):
        self.contents = []
        self.content_partnerships = {}  # Словарь для хранения связей между контентом и партнёрскими программами


    def add_content(self, content):
        self.contents.append(content) # Список партнёрских программ, к которым принадлежит автор контента
        author_partnerships = content.creator.partnerships # Связь между контентом и партнёрскими программами автора
        self.content_partnerships[content] = author_partnerships

    def rent_content(self, content):
        if content in self.contents:
            content.rent_content()
            print(f"{content.name} успешно арендован.")
        else:
            print("Контент не найден в игре.")

    def rent_on_credit(self, content, user):
        if user.deduct_funds(content.base_price):
            content.rent_content()
            print(f"{content.name} успешно арендован на кредит пользователем {user.name}.")
        else:
            print(f"Невозможно арендовать {content.name} на кредит из-за недостаточного баланса счета пользователя {user.name}.")

    def extend_rental(self, content):
        if content in self.contents and content.rented:
            content.extend_rental()
        else:
            print("Контент не арендуется или не найден в игре.")

    def offer_discount(self, content, discount):
        if content in self.contents and content.rented:
            content.offer_discount(discount)
        else:
            print("Контент не арендуется или не найден в игре.")

    def final_offer(self, discount):
        if self.rented:
            final_price = self.base_price * (1 - discount)
            print(f"Финальное предложение для {self.name}: {final_price}.")
        else:
            print(f"{self.name} в данный момент не арендуется.")
    

class PartnerProgram:
    def __init__(self, name, commission_rate):
        self.name = name
        self.commission_rate = commission_rate
        self.partners = {}

    def register_partner(self, user):
        if user not in self.partners:
            self.partners[user] = 0
            print(f"User {user} registered for the {self.name} partner program.")
        else:
            print(f"User {user} is already registered for the {self.name} partner program.")

    def link_content(self, content, partner):
        if partner in self.partners:
            print(f"Content '{content.name}' linked with partner {partner}.")
        else:
            print(f"User {partner} is not registered for the {self.name} partner program.")

def update_partner_programs_info(game, content_partnerships, listbox_content, text_partner_programs):
    content_index = listbox_content.curselection()
    if content_index:
        content = game.contents[content_index[0]]
        text_partner_programs.delete('1.0', tk.END)  # Очистка текстовое поле
        linked_programs = [program.name for program in content_partnerships.get(content, [])]  # Список партнёрских программ, к которым привязан контент
        if linked_programs:
            text_partner_programs.insert(tk.END, "\n".join(linked_programs))
        else:
            text_partner_programs.insert(tk.END, "Контент не привязан ни к одной партнёрской программе.")
    else:
        text_partner_programs.insert(tk.END, "Выберите контент для просмотра связей.")

def register_partner(partner_program, user, initial_balance=0):
    user.add_funds(initial_balance)  #  Начальный баланс при регистрации партнера
    partner_program.register_partner(user)



def add_content():
    name = entry_content_name.get().strip()
    creator_name = entry_content_creator.get().strip()
    price_entry = entry_content_price.get().strip()

    if not name or not creator_name or not price_entry:
        text_output.insert(tk.END, "Введите все данные для добавления контента.\n")
        return

    try:
        base_price = float(price_entry)
    except ValueError:
        text_output.insert(tk.END, "Некорректная цена контента.\n")
        return

    creator = None
    for user in [user1, user2]:
        if user.name == creator_name:
            creator = user
            break

    if creator is None:
        text_output.insert(tk.END, f"Пользователь с именем '{creator_name}' не найден.\n")
        return

    content = Content(name, creator, base_price)
    game.add_content(content)
    listbox_content.insert(tk.END, content.name)
    text_output.insert(tk.END, f"Добавлен контент: {name}\n")

def rent_content():
    content_index = listbox_content.curselection()
    if content_index:
        content = game.contents[content_index[0]]
        game.rent_content(content)
    else:
        text_output.insert(tk.END, "Выберите контент для аренды.\n")
        
def update_user_balance():
    user_index = combobox_user.current() # Функция для обновления баланса пользователя в текстовом поле
    if user_index >= 0:
        user = [user1, user2][user_index]
        text_balance.delete('1.0', tk.END)
        text_balance.insert(tk.END, str(user.balance))
        
def extend_rental():
    content_index = listbox_content.curselection()
    if content_index:
        content = game.contents[content_index[0]]
        game.extend_rental(content)
    else:
        text_output.insert(tk.END, "Выберите контент для продления аренды.\n")

def offer_discount():
    content_index = listbox_content.curselection()
    if content_index:
        content = game.contents[content_index[0]]
        discount_entry = entry_discount.get()
        if discount_entry:  # Проверка, что поле ввода не пустое
            try:
                discount = float(discount_entry)
                game.offer_discount(content, discount) 
            except ValueError:
                text_output.insert(tk.END, "Введите корректное числовое значение скидки.\n")
        else:
            text_output.insert(tk.END, "Введите значение скидки.\n")
    else:
        text_output.insert(tk.END, "Выберите контент для предложения скидки.\n")

def final_offer():
    content_index = listbox_content.curselection()
    if content_index:
        content = game.contents[content_index[0]]
        discount_entry = entry_discount.get()
        if discount_entry:  # Проверка, что поле ввода не пустое
            discount = float(discount_entry)
            content.final_offer(discount)
        else:
            text_output.insert(tk.END, "Введите значение скидки.\n")
    else:
        text_output.insert(tk.END, "Выберите контент для финального предложения.\n")


def rent_on_credit():
    content_index = listbox_content.curselection() # Функция для аренды контента на кредит
    user_index = combobox_user.current()
    if content_index and user_index >= 0:
        content = game.contents[content_index[0]]
        user = [user1, user2][user_index]
        credit_amount_entry = entry_credit_rent.get()
        try:
            credit_amount = float(credit_amount_entry)
            if user.balance >= credit_amount:
                user.balance -= credit_amount
                content.rent_content()
                text_output.insert(tk.END, f"{content.name} успешно арендован на кредит пользователем {user.name}.\n")
                update_user_balance()  # Обновление баланса пользователя в интерфейсе
                listbox_content.delete(0, tk.END)  # Очистка списока контента
                for content in game.contents:  # Обновление списока контента после аренды на кредит
                    listbox_content.insert(tk.END, content.name)
            else:
                text_output.insert(tk.END, "Недостаточно средств для аренды на кредит.\n")
        except ValueError:
            text_output.insert(tk.END, "Некорректная сумма долговой аренды.\n")


# Создание экземпляра класса Game для управления контентом
game = Game()

# Создание экземпляров пользователей
user1 = User("Пользователь1")
user2 = User("Пользователь2")

# Создание экземпляра контента с указанием пользователя в качестве создателя
content1 = Content("Контент1", user1, 1000)
content2 = Content("Контент2", user2, 2000)

# Добавление контента в игру
game.add_content(content1)
game.add_content(content2)

# Создание экземпляров партнёрских программ
gold_partners = PartnerProgram("Gold Partners", 0.15)
silver_partners = PartnerProgram("Silver Partners", 0.2)


# Создание главного окна
root = tk.Tk()
root.title("Панель администратора системы монетизации")

# Создание вкладок
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Вкладка для работы с контентом
content_tab = ttk.Frame(notebook)
notebook.add(content_tab, text='Контент')

# Вкладка для работы с партнёрскими программами
partners_tab = ttk.Frame(notebook)
notebook.add(partners_tab, text='Партнёрские программы')

# Создание переменной для ввода скидки
entry_discount = None

# Создание метки и поля ввода для имени пользователя
label_user_name = tk.Label(partners_tab, text="Имя пользователя:")
label_user_name.grid(row=0, column=0, padx=10, pady=5)

entry_user_name = tk.Entry(partners_tab)
entry_user_name.grid(row=0, column=1, padx=10, pady=5)

# Создание кнопок для регистрации партнёров
button_register_gold = tk.Button(partners_tab, text="Зарегистрировать в Gold Partners", command=lambda: register_partner(gold_partners, entry_user_name.get()))
button_register_gold.grid(row=1, column=0, padx=10, pady=5)

button_register_silver = tk.Button(partners_tab, text="Зарегистрировать в Silver Partners", command=lambda: register_partner(silver_partners, entry_user_name.get()))
button_register_silver.grid(row=1, column=1, padx=10, pady=5)

# Создание меток и полей для добавления контента
label_content_name = tk.Label(content_tab, text="Название контента:")
label_content_name.grid(row=0, column=0, padx=10, pady=5)

entry_content_name = tk.Entry(content_tab)
entry_content_name.grid(row=0, column=1, padx=10, pady=5)

label_content_creator = tk.Label(content_tab, text="Создатель контента:")
label_content_creator.grid(row=1, column=0, padx=10, pady=5)

entry_content_creator = tk.Entry(content_tab)
entry_content_creator.grid(row=1, column=1, padx=10, pady=5)

label_content_price = tk.Label(content_tab, text="Базовая цена контента:")
label_content_price.grid(row=2, column=0, padx=10, pady=5)

entry_content_price = tk.Entry(content_tab)
entry_content_price.grid(row=2, column=1, padx=10, pady=5)

# Создание кнопок для добавления контента
button_add_content = tk.Button(content_tab, text="Добавить контент", command=add_content)
button_add_content.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Создание метки для выбора пользователя
label_user_selection = tk.Label(content_tab, text="Выберите пользователя:")
label_user_selection.grid(row=4, column=0, padx=10, pady=5)

# Создание выпадающего списка для выбора пользователя
user_options = [user.name for user in [user1, user2]]
combobox_user = ttk.Combobox(content_tab, values=user_options)
combobox_user.grid(row=4, column=1, padx=10, pady=5)

# Создание метки и поля для отображения баланса пользователя
label_balance = tk.Label(content_tab, text="Баланс счета:")
label_balance.grid(row=5, column=0, padx=10, pady=5)

text_balance = tk.Text(content_tab, height=1, width=20)
text_balance.grid(row=5, column=1, padx=10, pady=5)

# Создание метки и поля для ввода суммы долговой аренды
label_credit_rent = tk.Label(content_tab, text="Сумма долговой аренды:")
label_credit_rent.grid(row=6, column=0, padx=10, pady=5)

entry_credit_rent = tk.Entry(content_tab)
entry_credit_rent.grid(row=6, column=1, padx=10, pady=5)

# Создание кнопки для аренды контента на кредит
button_rent_on_credit = tk.Button(content_tab, text="Арендовать на кредит", command=rent_on_credit)
button_rent_on_credit.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

# Создание кнопок для аренды контента, предложения скидки и финального предложения
button_rent_content = tk.Button(content_tab, text="Арендовать контент", command=rent_content)
button_rent_content.grid(row=8, column=0, padx=10, pady=5)

button_offer_discount = tk.Button(content_tab, text="Предложить скидку", command=offer_discount)
button_offer_discount.grid(row=8, column=1, padx=10, pady=5)

button_final_offer = tk.Button(content_tab, text="Финальное предложение", command=final_offer)
button_final_offer.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

# Создание списка для выбора контента
listbox_content = tk.Listbox(content_tab)
listbox_content.grid(row=10, column=0, columnspan=2, padx=10, pady=5)
for content in game.contents:
    listbox_content.insert(tk.END, content.name)

# Создание текстового поля для вывода сообщений
text_output = tk.Text(content_tab, height=10, width=50)
text_output.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

# Обновление баланса при выборе пользователя из комбобокса
combobox_user.bind("<<ComboboxSelected>>", lambda event: update_user_balance())

root.mainloop()