from .database import connect
from .user_management import create_user

def main():
    print("Запуск основного приложения")
    connect()
    create_user()

if __name__ == '__main__':
    main()