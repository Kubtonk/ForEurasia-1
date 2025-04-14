def get_user_info():
    print("Введите данные пользователя:")
    name = input("ФИО: ")
    company = input("Компания: ")
    phone = input("Контактный телефон: ")
    email = input("Email: ")

    return {
        "имя": name,
        "компания": company,
        "номер телефона": phone,
        "email": email
    }
