from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.sql import text
from sqlalchemy.orm import Session

from settings import (
    DATABASE,
    USER,
    PASSWORD,
    HOST,
    PORT
)



URL = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
    USER, PASSWORD, HOST, PORT, DATABASE
)

ENIGNE = create_engine(url=URL, echo=True)


class DBManager():

    def __init__(self, engine):
        self.engine: Engine = engine
        self.create_table()

    def create_table(self):
        with Session(bind=self.engine) as session:
            request = text("""CREATE TABLE if not exists post (
                id INTEGER PRIMARY KEY auto_increment, 
                title VARCHAR(255) NOT NULL,
                address VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                dollar VARCHAR(255) NOT NULL,
                som VARCHAR(255) NOT NULL,
                phone VARCHAR(255) NOT NULL,
                uploaded VARCHAR(255) NOT NULL,
                views VARCHAR(255) NOT NULL,
                тип_предложения VARCHAR(255),
                безопасность VARCHAR(255),
                высота_потолков VARCHAR(255),
                балкон VARCHAR(255),
                входная_дверь VARCHAR(255),
                газ VARCHAR(255),
                дом VARCHAR(255),
                интернет VARCHAR(255),
                мебель VARCHAR(255),
                отопление VARCHAR(255),
                парковка VARCHAR(255),
                период_аренды VARCHAR(255),
                площадь VARCHAR(255),
                пол VARCHAR(255),
                разное TEXT,
                санузел VARCHAR(255),
                серия VARCHAR(255),
                состояние VARCHAR(255),
                телефон VARCHAR(255),        
                этаж VARCHAR(255)
                )
            """)
            session.execute(request)
            session.commit()

    def insert_post(self, data: dict):
        insert = "INSERT INTO post ("
        instance = "VALUES ("
        for key, value in data.items():
            insert += f"{self.__convert_to_column(key)}, "
            instance += f'"{self.__convert_to_row(value)}", '
        insert = insert.rstrip(", ")
        instance = instance.rstrip(", ")

        with Session(bind=self.engine) as session:
            request = text(f"{insert}) {instance});")
            session.execute(request)
            session.commit()

    
    def already_exists(self, data) -> bool:
        """
        Если объект уже находится в базе данных, то метод будет возвращать True
        Иначе - False
        """  
        with Session(bind=self.engine) as session:
            request = 'SELECT title, address, phone FROM post WHERE title="{}" and address="{}" and phone="{}" LIMIT 1;'.format(
                data["title"], data["address"], data["phone"]
            )
            post = session.execute(text(request))
            if post.rowcount == 0:
                return False
            return True

        


    def __convert_to_column(self, key: str):
        column = key.replace(" ", "_")
        column = column.lower()
        return column
    
    def __convert_to_row(self, value: str):
        row = value.replace('"', "'")
        row = row.replace("\n", " ")
        row = row.replace("\r", " ")
        return row