import csv
import timeit
from BTrees.OOBTree import OOBTree
from colorama import Fore, Style, init

init(autoreset=True)


# Функція для завантаження даних з CSV файлу
def load_items_data(filename):
    items = []
    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = {
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"]),
            }
            items.append(item)
    return items


# Функція для додавання елемента в OOBTree
def add_item_to_tree(tree, item):
    tree.insert(item["ID"], item)


# Функція для додавання елемента в dict
def add_item_to_dict(items_dict, item):
    items_dict[item["ID"]] = item


# Функція для діапазонного запиту для OOBTree
def range_query_tree(tree, min_price, max_price):
    result = []
    for key, value in tree.items(min_price, max_price):
        if min_price <= value["Price"] <= max_price:
            result.append(value)
    return result


# Функція для діапазонного запиту для dict
def range_query_dict(items_dict, min_price, max_price):
    result = []
    for item in items_dict.values():
        if min_price <= item["Price"] <= max_price:
            result.append(item)
    return result


# Основна функція для порівняння
def compare_structures(filename):
    # Завантаження даних
    items = load_items_data(filename)

    # Створення OOBTree і dict
    tree = OOBTree()
    items_dict = {}

    # Додавання елементів у OOBTree та dict
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(items_dict, item)

    # Функція для вимірювання часу діапазонного запиту для OOBTree
    def time_range_query_tree():
        return range_query_tree(tree, 10, 100)  # Приклад діапазону: ціни від 10 до 100

    # Функція для вимірювання часу діапазонного запиту для dict
    def time_range_query_dict():
        return range_query_dict(
            items_dict, 10, 100
        )  # Приклад діапазону: ціни від 10 до 100

    # Вимірювання часу для 100 діапазонних запитів на OOBTree
    oobtree_time = timeit.timeit(time_range_query_tree, number=100)

    # Вимірювання часу для 100 діапазонних запитів на dict
    dict_time = timeit.timeit(time_range_query_dict, number=100)

    # Виведення результатів
    print(
        Fore.GREEN + f"Total range_query time for OOBTree: {oobtree_time:.6f} seconds"
    )
    print(Fore.RED + f"Total range_query time for Dict: {dict_time:.6f} seconds")
    if oobtree_time < dict_time:
        print(Fore.YELLOW + "OOBTree is faster than Dict for range queries!")
    else:
        print(Fore.YELLOW + "Dict is faster than OOBTree for range queries!")


if __name__ == "__main__":
    # Шлях до файлу з даними
    filename = "generated_items_data.csv"

    # Порівняння структур
    compare_structures(filename)
