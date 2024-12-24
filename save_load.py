import pickle

def save_game(data, filename="savefile.pkl"):
    """Сохранение данных игры в файл."""
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_game(filename="savefile.pkl"):
    """Загрузка данных игры из файла."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None  # Если файл не найден, возвращаем None
