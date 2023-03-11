import sqlalchemy
from sqlalchemy.orm import sessionmaker
from modules import create_tables, Publisher, Stock, Shop, Book, Sale

def data_connect():
    database = 'postgresql'
    login = 'postgres'
    password = 'doka7744'
    port = 'localhost:5432'
    db_name = 'psql5_db'
    DSN = f'{database}://{login}:{password}@{port}/{db_name}'
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)
    return engine

def data_populating(session):
    publisher1 = Publisher(name="Пушкин")
    publisher2 = Publisher(name="Тургенев")
    publisher3 = Publisher(name="Достоевский")
    publisher4 = Publisher(name="Лермонтов")
    session.add_all([publisher1, publisher2, publisher3, publisher4])

    shop1 = Shop(name="ЧитайГород")
    shop2 = Shop(name="АСТ")
    shop3 = Shop(name="Буквоед")
    shop4 = Shop(name="Книжный")
    session.add_all([shop1, shop2, shop3, shop4])

    book1 = Book(title="Капитанская дочка", publisher=publisher1)
    book2 = Book(title="Евгений Онегин", publisher=publisher1)
    book3 = Book(title="Отцы и дети", publisher=publisher2)
    book4 = Book(title="Преступление и наказание", publisher=publisher3)
    book5 = Book(title="Идиот", publisher=publisher3)
    book6 = Book(title="Мцыри", publisher=publisher4)
    session.add_all([book1, book2, book3, book4, book5, book6])

    stock1 = Stock(count=200, book=book1, shop=shop1)
    stock2 = Stock(count=300, book=book2, shop=shop2)
    stock3 = Stock(count=500, book=book3, shop=shop3)
    stock4 = Stock(count=50, book=book4, shop=shop3)
    stock5 = Stock(count=150, book=book5, shop=shop4)
    stock6 = Stock(count=400, book=book6, shop=shop4)
    session.add_all([stock1, stock2, stock3, stock4, stock5, stock6])

    sale1 = Sale(price=2500, date_sale="2022-06-23", stock=stock1, count=10)
    sale2 = Sale(price=4000, date_sale="2022-08-12", stock=stock2, count=20)
    sale3 = Sale(price=1200, date_sale="2022-11-06", stock=stock3, count=30)
    sale4 = Sale(price=800, date_sale="2023-01-01", stock=stock4, count=40)
    sale5 = Sale(price=8000, date_sale="2021-10-17", stock=stock5, count=50)
    sale6 = Sale(price=3000, date_sale="2022-12-11", stock=stock6, count=60)
    session.add_all([sale1, sale2, sale3, sale4, sale5, sale6])


def sale_information(id_publisher=None, name_publisher=None):
    if id_publisher != None:
        book_name = session.query(Book).join(Publisher).filter(Publisher.id == id_publisher).all()
        shop_name = session.query(Stock).join(Book).filter(Book.id_publisher == id_publisher).all()
        sale_price = session.query(Sale).join(Stock).join(Book).filter(Book.id_publisher == id_publisher).all()
        for i in range(len(book_name)):
            print(f" {book_name[i].title} | {shop_name[i]} | {sale_price[i].price} | {sale_price[i].date_sale} ")
    elif name_publisher != None:
        book_name = session.query(Book).join(Publisher).filter(Publisher.name == name_publisher).all()
        shop_name = session.query(Stock).join(Book).join(Publisher).filter(Publisher.name == name_publisher).all()
        sale_price = session.query(Sale).join(Stock).join(Book).join(Publisher).filter(Publisher.name == name_publisher).all()
        for i in range(len(book_name)):
            print(f" {book_name[i].title} | {shop_name[i]} | {sale_price[i].price} | {sale_price[i].date_sale} ")

def input_info():
    str_ = int(input("Введите цифру 1 или 2 для определения поля ввода: "))
    if str_ == 1:
        id = int(input("Введите айди писателя: "))
        return id
    elif str_ == 2:
        name = input("Введите имя писателя: ")
        return name

if __name__ == "__main__":
    engine = data_connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    data_populating(session)
    # sale_information(1)
    tmp = input_info()
    if type(tmp) is int:
        id = tmp
        name = None
    else:
        name = tmp
        id = None
    sale_information(id, name)
    session.commit()
    session.close()