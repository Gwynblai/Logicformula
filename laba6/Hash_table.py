from prettytable import PrettyTable

class HashTableEntry:
    def __init__(self, key=None, data=None):
        self.key = key            # ключ (фамилия)
        self.value = self._calc_key_value(key) if key else None  # V - вычисленное значение по первым двум буквам
        self.hash_address = None  # h(V)
        self.chain_start = 0      # C - начало цепочки (для простоты 1 если начало, иначе 0)
        self.in_use = 0           # U - флаг занятости (1/0)
        self.terminal = 0         # T - конец цепочки (1/0)
        self.link = 0             # L - связь (в данном примере не используем, оставим 0)
        self.deleted = 0          # D - удалено (флаг)
        self.p0 = None            # P0 - индекс предыдущей ячейки в цепочке
        self.pi = data            # Pi - данные (информация о студенте)

    def _calc_key_value(self, key):
        # Вычисляем V по первым двум буквам согласно русскому алфавиту А=0,Б=1,...Я=32
        # key ожидается строкой, берем первые 2 буквы
        if not key or len(key) < 2:
            return None
        alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        base = len(alphabet)  # 33
        key = key.upper()
        # Приводим первую и вторую букву к индексу в алфавите
        try:
            first = alphabet.index(key[0])
            second = alphabet.index(key[1])
        except ValueError:
            # если буква не из алфавита, возвращаем None
            return None
        # Формула: V = first*base^1 + second*base^0
        return first * base + second

class HashTable:
    def __init__(self, size=20):
        self.size = size
        self.table = [HashTableEntry() for _ in range(size)]
        self.count = 0

    def _hash(self, value):
        return value % self.size if value is not None else 0

    def insert(self, key, data):
        # Проверка на уже существующий ключ
        existing_entry = self.search(key)
        if existing_entry is not None:
            print(f"[Вставка] Ключ '{key}' уже существует, обновляем данные.")
            existing_entry.pi = data
            return False

        entry_value = HashTableEntry(key).value
        if entry_value is None:
            print(f"[Ошибка] Невозможно вычислить значение V для ключа '{key}'")
            return False
        hash_index = self._hash(entry_value)

        # Поиск начала цепочки для этого хеш-адреса
        start_index = None
        for i, entry in enumerate(self.table):
            if entry.in_use == 1 and entry.chain_start == 1 and entry.hash_address == hash_index and entry.deleted == 0:
                start_index = i
                break

        new_entry = HashTableEntry(key, data)
        new_entry.value = entry_value
        new_entry.hash_address = hash_index
        new_entry.in_use = 1
        new_entry.deleted = 0
        new_entry.link = 0  # не используется, оставим 0

        if start_index is None:
            # Нет цепочки с таким хешем — вставляем как начало цепочки
            new_entry.chain_start = 1
            new_entry.p0 = None
            new_entry.terminal = 1

            # Вставляем в первую свободную ячейку
            for i in range(self.size):
                if self.table[i].in_use == 0 or self.table[i].deleted == 1:
                    self.table[i] = new_entry
                    self.count += 1
                    return True

            print("[Ошибка] Нет свободных ячеек для вставки")
            return False
        else:
            # Есть цепочка, нужно добавить в конец цепочки
            # Найдём последний элемент цепочки
            last_index = None
            for i, entry in enumerate(self.table):
                if (entry.in_use == 1 and entry.hash_address == hash_index and
                        entry.deleted == 0 and entry.terminal == 1):
                    last_index = i
                    break

            if last_index is None:
                print("[Ошибка] Цепочка найдена, но последний элемент не найден")
                return False

            # Новый элемент — продолжение цепочки
            new_entry.chain_start = 0
            new_entry.p0 = last_index + 1  # индексы для пользователя с 1, как в таблице
            new_entry.terminal = 1

            # Обновляем последний элемент: он уже не терминальный
            self.table[last_index].terminal = 0

            # Вставляем новый элемент в первую свободную ячейку
            for i in range(self.size):
                if self.table[i].in_use == 0 or self.table[i].deleted == 1:
                    self.table[i] = new_entry
                    self.count += 1
                    return True

            print("[Ошибка] Нет свободных ячеек для вставки")
            return False

    def search(self, key):
        # Ищем запись с ключом key (учитывая удалённые)
        for entry in self.table:
            if entry.key == key and entry.deleted == 0 and entry.in_use == 1:
                return entry
        return None

    def delete(self, key):
        for i, entry in enumerate(self.table):
            if entry.key == key and entry.in_use == 1 and entry.deleted == 0:
                self.table[i].deleted = 1
                self.table[i].in_use = 0
                self.count -= 1
                print(f"Ключ '{key}' удалён.")
                return True
        print(f"Ключ '{key}' не найден для удаления.")
        return False

    def load_factor(self):
        return self.count / self.size

    def display_detailed(self):
        table = PrettyTable()
        table.field_names = [
            "#", "Фамилия (ключ)", "V", "h", "№ строки ТХ", "ID",
            "C", "U", "T", "L", "D", "P0", "Pi (данные)"
        ]
        for i, entry in enumerate(self.table, 1):
            ID = f"ID{i}" if entry.key else ""
            table.add_row([
                i,
                entry.key if entry.key else "",
                entry.value if entry.value is not None else "",
                entry.hash_address if entry.hash_address is not None else "",
                i,
                ID,
                entry.chain_start,
                entry.in_use,
                entry.terminal,
                entry.link,
                entry.deleted,
                entry.p0 if entry.p0 is not None else "",
                entry.pi if entry.pi is not None else ""
            ])
        print(table)
        print(f"Коэффициент заполнения: {self.load_factor():.2f}\n")