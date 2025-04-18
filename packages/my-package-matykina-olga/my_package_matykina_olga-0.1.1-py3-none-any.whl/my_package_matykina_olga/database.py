def connect():
    print("Connected to database")

def _internal_function():
    print("This is a private internal function")

def main():
    connect()
    print('Этот код выполняется только при запуске database.py напрямую')

if __name__ == '__main__':
    main()