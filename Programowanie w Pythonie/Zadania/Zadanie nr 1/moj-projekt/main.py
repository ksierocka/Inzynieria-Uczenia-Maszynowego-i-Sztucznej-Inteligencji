# Ćwiczenie I – instalacja Poetry, stworzenie nowej aplikacji i definicja funkcji
# Ćwiczenie II – dodanie obsługi wyjątków
# Ćwiczenie III – transformacja plików
# Ćwiczenie IV – dodanie dekoratorów

import requests, csv
from datetime import datetime
from functools import wraps

def log_time(func):
    def wrapper(*args, **kwargs):
        print(f"Start: {datetime.now()}")
        result = func(*args, **kwargs)
        print(f"Koniec: {datetime.now()}")
        return result
    return wrapper


class DownloadError(Exception):
    """Błąd ogólny podczas pobierania pliku."""
    pass

class NotFoundError(DownloadError):
    """Nie znaleziono pliku."""
    pass

class AccessDeniedError(DownloadError):
    """Brak dostępu do pliku."""
    pass

def download_file(url: str, file_name: str = "latest.txt") -> None: 

    response = requests.get(url, timeout=30)

    if response.status_code == 404:
        raise NotFoundError("Błąd 404: Nie znaleziono pliku!")

    elif response.status_code == 403:
        raise AccessDeniedError("Błąd 403: Brak dostępu do pliku!")

    response.raise_for_status()

    with open(file_name, "wb") as file:
        file.write(response.content)

if __name__ == "__main__":
    urls = [
            "https://oleksandr-fedoruk.com/sggw/podyplomowe/file",
            "http://oleksandr-fedoruk.com/sggw/podyplomowe/404",
            "http://oleksandr-fedoruk.com/sggw/podyplomowe/403",
    ]

    for i, url in enumerate(urls, start=1):
        file_name = f"test_file_{i}.csv"
        try:
            download_file(url, f"test_file_{i}.csv")

        except NotFoundError as error:
            print(error)

        except AccessDeniedError as error:
            print(error)

        else:
            print(f"Plik {file_name} został pobrany!")

        # finally:
        #     print("Zakończono próbę pobierania pliku.")


class ETL:
    def __init__(self, file_name: str):
        self.file_name = file_name
    def computing_statistics(self):
        # Wczytywanie pobranego pliku linijka po linijce
        with open(self.file_name, newline='',  encoding="utf-8") as f:
            reader = csv.reader(f)

            for row in reader:
                # Numer porządkowy
                index = int(row[0])

                # Indeksy brakujących wartości 
                missing = [
                    i for i, value in enumerate(row)
                    if value == "-"
                ]

                # Suma i średnia
                numbers = [
                    float(value) for value in row[1:]
                    if value != "-"
                ]
                total_sum = sum(numbers)
                average = total_sum / len(numbers) if numbers else None

                yield {
                    "numer porządkowy": index,
                    "suma": total_sum,
                    "średnia": average,
                    "indeksy brakujących kolumn": missing
                }
    @log_time
    def save_files(self):

            with (
                open("values.csv", "w", newline="", encoding="utf-8") as values_file,
                open("missing_values.csv", "w", newline="", encoding="utf-8") as missing_file
            ):
                values_writer = csv.writer(values_file)
                missing_writer = csv.writer(missing_file)

                # Nagłówki
                values_writer.writerow(["numer porządkowy", "suma", "średnia"])
                missing_writer.writerow(["numer porządkowy", "indeksy brakujących kolumn"])

                for result in self.computing_statistics():
                    values_writer.writerow([
                        result["numer porządkowy"],
                        result["suma"],
                        result["średnia"]
                    ])

                    missing_writer.writerow([
                        result["numer porządkowy"],
                        ";".join(map(str, result["indeksy brakujących kolumn"]))
                    ])


if __name__ == "__main__":
    etl = ETL("test_file_1.csv")
    etl.save_files()