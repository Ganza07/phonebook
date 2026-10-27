import csv
import re
from pprint import pprint

# Читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# ================= TODO 1: Обработка данных =================

# 1. Приводим ФИО к единому формату (Ф, И, О в отдельных ячейках)
for contact in contacts_list[1:]:
    # Объединяем первые три поля, убираем лишние пробелы и разбиваем по пробелам
    fullname = " ".join(contact[:3]).strip()
    parts = fullname.split()

    # Распределяем по колонкам, проверяя длину списка
    contact[0] = parts[0] if len(parts) > 0 else ""
    contact[1] = parts[1] if len(parts) > 1 else ""
    contact[2] = parts[2] if len(parts) > 2 else ""


# 2. Приводим телефоны к формату +7(999)999-99-99 [доб.XXXX]
def format_phone(phone_str):
    if not phone_str.strip():
        return ""

    # Ищем основной номер (игнорируем любые нецифровые символы между группами)
    main_match = re.search(r"(\+7|8)\D*(\d{3})\D*(\d{3})\D*(\d{2})\D*(\d{2})", phone_str)
    if not main_match:
        return phone_str  # Если не распознали, оставляем как есть

    # Собираем строку в нужном формате
    formatted = f"+7({main_match.group(2)}){main_match.group(3)}-{main_match.group(4)}-{main_match.group(5)}"

    # Ищем добавочный номер (поддерживает "доб.", "доб", "(доб. X)")
    ext_match = re.search(r"доб\.?\s*(\d{2,})", phone_str)
    if ext_match:
        formatted += f" доб.{ext_match.group(1)}"

    return formatted


for contact in contacts_list[1:]:
    contact[5] = format_phone(contact[5])

# 3. Объединяем дублирующиеся записи
contacts_dict = {}
for contact in contacts_list[1:]:
    # Группируем по Фамилии и Имени
    key = f"{contact[0]} {contact[1]}".strip()

    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        # Если человек уже есть, заполняем пустые ячейки из новой строки
        for i in range(2, 7):  # Индексы: Отчество, Организация, Должность, Телефон, Email
            if not contacts_dict[key][i] and contact[i]:
                contacts_dict[key][i] = contact[i]

# Собираем итоговый список: заголовок + уникальные строки
contacts_list = [contacts_list[0]] + list(contacts_dict.values())

pprint(contacts_list)

# ================= TODO 2: Сохранение в файл =================
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)