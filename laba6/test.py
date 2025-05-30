import unittest
from Hash_table import *

class TestHashTableEntry(unittest.TestCase):
    def test_entry_initialization(self):
        entry = HashTableEntry()
        self.assertIsNone(entry.key)
        self.assertIsNone(entry.value)
        self.assertIsNone(entry.hash_address)
        self.assertEqual(entry.chain_start, 0)
        self.assertEqual(entry.in_use, 0)
        self.assertEqual(entry.terminal, 0)
        self.assertEqual(entry.link, 0)
        self.assertEqual(entry.deleted, 0)
        self.assertIsNone(entry.p0)
        self.assertIsNone(entry.pi)

    def test_entry_with_key(self):
        entry = HashTableEntry(key="Иванов")
        self.assertEqual(entry.key, "Иванов")
        self.assertIsNotNone(entry.value)
        self.assertIsNone(entry.hash_address)
        self.assertEqual(entry.chain_start, 0)
        self.assertEqual(entry.in_use, 0)
        self.assertEqual(entry.terminal, 0)
        self.assertEqual(entry.link, 0)
        self.assertEqual(entry.deleted, 0)
        self.assertIsNone(entry.p0)
        self.assertIsNone(entry.pi)

    def test_entry_with_key_and_data(self):
        entry = HashTableEntry(key="Петров", data="Студент Петров")
        self.assertEqual(entry.key, "Петров")
        self.assertIsNotNone(entry.value)
        self.assertEqual(entry.pi, "Студент Петров")

    def test_value_calculation(self):
        # Test value calculation for Russian letters
        entry1 = HashTableEntry(key="АА")
        entry2 = HashTableEntry(key="АБ")
        entry3 = HashTableEntry(key="БА")

        # А=0, Б=1, base=33
        # V = first*33 + second
        self.assertEqual(entry1.value, 0 * 33 + 0)  # АА
        self.assertEqual(entry2.value, 0 * 33 + 1)  # АБ
        self.assertEqual(entry3.value, 1 * 33 + 0)  # БА

    def test_invalid_key_value(self):
        entry1 = HashTableEntry(key="A")  # too short
        entry2 = HashTableEntry(key="12")  # non-Russian letters
        entry3 = HashTableEntry(key="")  # empty

        self.assertIsNone(entry1.value)
        self.assertIsNone(entry2.value)
        self.assertIsNone(entry3.value)


class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(size=5)  # smaller size for testing

    def test_initialization(self):
        self.assertEqual(self.ht.size, 5)
        self.assertEqual(len(self.ht.table), 5)
        self.assertEqual(self.ht.count, 0)

        for entry in self.ht.table:
            self.assertIsInstance(entry, HashTableEntry)
            self.assertIsNone(entry.key)

    def test_hash_function(self):
        self.assertEqual(self.ht._hash(0), 0)
        self.assertEqual(self.ht._hash(4), 4)
        self.assertEqual(self.ht._hash(5), 0)  # 5 % 5 = 0
        self.assertEqual(self.ht._hash(6), 1)  # 6 % 5 = 1
        self.assertEqual(self.ht._hash(None), 0)

    def test_insert_first_item(self):
        # Insert first item - should be start of chain
        result = self.ht.insert("Иванов", "Иван Иванов, курс 1")
        self.assertTrue(result)
        self.assertEqual(self.ht.count, 1)

        # Check the inserted entry
        entry = self.ht.table[0]
        self.assertEqual(entry.key, "Иванов")
        self.assertEqual(entry.pi, "Иван Иванов, курс 1")
        self.assertEqual(entry.chain_start, 1)
        self.assertEqual(entry.in_use, 1)
        self.assertEqual(entry.terminal, 1)
        self.assertEqual(entry.deleted, 0)
        self.assertIsNone(entry.p0)

    def test_insert_with_collision(self):
        # Force a collision by using keys with same hash
        # Mock the hash function to return same value for different keys
        original_hash = self.ht._hash
        self.ht._hash = lambda x: 2  # all hashes will be 2

        # Insert first item
        self.ht.insert("АА", "Студент 1")  # V=0, h=2
        self.assertEqual(self.ht.count, 1)

        # Insert second item with same hash
        self.ht.insert("АК", "Студент 2")  # Different key but same hash
        self.assertEqual(self.ht.count, 2)

        # Check chain structure
        # Find start of chain
        start_index = None
        for i, entry in enumerate(self.ht.table):
            if entry.chain_start == 1 and entry.hash_address == 2:
                start_index = i
                break

        self.assertIsNotNone(start_index)
        start_entry = self.ht.table[start_index]
        self.assertEqual(start_entry.terminal, 0)  # No longer terminal

        # Find terminal entry
        terminal_index = None
        for i, entry in enumerate(self.ht.table):
            if entry.terminal == 1 and entry.hash_address == 2:
                terminal_index = i
                break

        self.assertIsNotNone(terminal_index)
        terminal_entry = self.ht.table[terminal_index]
        self.assertEqual(terminal_entry.p0, start_index + 1)  # 1-based index

        # Restore original hash function
        self.ht._hash = original_hash

    def test_search(self):
        # Insert test data
        self.ht.insert("Иванов", "Иван Иванов")
        self.ht.insert("Петров", "Петр Петров")

        # Search existing
        entry1 = self.ht.search("Иванов")
        self.assertIsNotNone(entry1)
        self.assertEqual(entry1.pi, "Иван Иванов")

        entry2 = self.ht.search("Петров")
        self.assertIsNotNone(entry2)
        self.assertEqual(entry2.pi, "Петр Петров")

        # Search non-existing
        entry3 = self.ht.search("Сидоров")
        self.assertIsNone(entry3)

    def test_delete(self):
        # Insert test data
        self.ht.insert("Иванов", "Иван Иванов")
        self.assertEqual(self.ht.count, 1)

        # Delete existing
        result = self.ht.delete("Иванов")
        self.assertTrue(result)
        self.assertEqual(self.ht.count, 0)

        # Verify deleted flag
        for entry in self.ht.table:
            if entry.key == "Иванов":
                self.assertEqual(entry.deleted, 1)
                self.assertEqual(entry.in_use, 0)
                break
        else:
            self.fail("Entry not found after deletion")

        # Delete non-existing
        result = self.ht.delete("Сидоров")
        self.assertFalse(result)

    def test_load_factor(self):
        # Empty table
        self.assertEqual(self.ht.load_factor(), 0)

        # Add some items
        self.ht.insert("АА", "Студент 1")
        self.assertEqual(self.ht.load_factor(), 1 / 5)

        self.ht.insert("АБ", "Студент 2")
        self.assertEqual(self.ht.load_factor(), 2 / 5)

        self.ht.insert("АВ", "Студент 3")
        self.assertEqual(self.ht.load_factor(), 3 / 5)

        # Delete one
        self.ht.delete("АБ")
        self.assertEqual(self.ht.load_factor(), 2 / 5)

    def test_update_existing(self):
        # Insert initial data
        self.ht.insert("Иванов", "Старые данные")
        self.assertEqual(self.ht.count, 1)

        # Update existing
        self.ht.insert("Иванов", "Новые данные")
        self.assertEqual(self.ht.count, 1)  # Count shouldn't change

        # Verify update
        entry = self.ht.search("Иванов")
        self.assertEqual(entry.pi, "Новые данные")

    def test_display_detailed(self):
        # Just verify it runs without errors
        self.ht.insert("Иванов", "Данные 1")
        self.ht.insert("Петров", "Данные 2")
        self.ht.display_detailed()


if __name__ == '__main__':
    unittest.main()