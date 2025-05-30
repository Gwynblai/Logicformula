from Hash_table import *

# === Пример использования ===
if __name__ == '__main__':
    ht = HashTable(size=20)

    # Вставим записи с биологической тематикой и фамилиями ученых (пример)
    ht.insert("Абаев", "Студент Сергей")
    ht.insert("Бобков", "Студент Тимур")
    ht.insert("Видерт", "Студент Евгений")
    ht.insert("Гракова", "Студент Иван")
    ht.insert("Кожевников", "Студент Максим")
    ht.insert("Ковалев", "Профессор")
    ht.insert("Крикунов", "Исследователь")
    ht.insert("Кот", "Аспирант")
    ht.insert("Давыденко", "Студент Александр")
    ht.insert("Горбань", "Научный сотрудник")
    ht.insert("Данилов", "Лаборант")
    ht.insert("Козлов", "Магистрант")
    ht.insert("Азимов", "Ассистент")
    ht.insert("Бобков", "Студент Тимур")



    ht.display_detailed()

    ht.insert("Бобков", "Красавчик")
    ht.display_detailed()

    # Поиск примера
    print("Поиск 'Кожевников':")
    res = ht.search("Кожевников")
    if res:
        print(vars(res))
    else:
        print("Не найден")

    # Удаление примера
    print("\nУдаляем 'Кот':")
    ht.delete("Кот")
    ht.display_detailed()
