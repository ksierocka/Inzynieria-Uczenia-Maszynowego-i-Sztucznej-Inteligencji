
class SafeDivision:
    def __enter__(self):
        return self

    def divide(self, a, b):
        return a / b

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is ZeroDivisionError:
            print("Nie można dzielić przez zero")
            return True

        return False

with SafeDivision() as sd:
    print(sd.divide(20, 5))

with SafeDivision() as sd:
    print(sd.divide(10, 0))

print("Program działa dalej!")