# run_export.py

from src import export

def main():
    print("📦 Экспорт данных пользователей в CSV...")
    export.export_to_csv("exported_users.csv", mark_as_exported=True)

if __name__ == "__main__":
    main()
