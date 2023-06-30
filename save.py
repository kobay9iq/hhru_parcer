import csv


def save_as_csv(jobs):
    file = open("vacancy_export.csv", mode="w", newline="", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["Tittle", "Company", "City",
                    "Experience", "Salary", "Link"])

    for vacancy in jobs:
        try:
            writer.writerow(list(vacancy.values()))
        except:
            print(list(vacancy.values()))

    print("Экспорт завершен успешно")

    return
