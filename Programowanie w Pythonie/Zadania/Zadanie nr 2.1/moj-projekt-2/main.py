#Ćwiczenia praktyczne 1 – eksperymenty z kontekstem

class Logger:
    def __enter__(self):
        print("Start sekcji logowania")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Koniec sekcji logowania")

with Logger():
    print("Wykonuję operację w sekcji logowania")

class FileWriter:
    def __init__(self, path):
        self.path = path
        self.file = None

    def __enter__(self):
        self.file = open(self.path, "w", encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file is not None:
            self.file.close()

        if exc_type is not None:
            print(f"Błąd podczas zapisu: {exc_value}")

        return False

with FileWriter("test.txt") as f:
    f.write("Cześć!\n")
    raise ValueError("<treść wyjątku>")
    f.write("Test.\n")

print("Plik został zapisany i zamknięty.")
