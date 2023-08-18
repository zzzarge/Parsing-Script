import requests

from bs4 import BeautifulSoup as BS

from save import write_to_txt, write_to_csv

from engine import DBManager, ENIGNE
"""
get - получение данных
delete - для удаления данных
post - для отправки данных
put, patch - для обновления данных
"""

def get_html(url):

    """
    Функция отправляет get запрос на url адрес. 
    В случае, если запрос прошёл успешно - функция возвращает html код, 
    нет - срабатывает print"""

    request = requests.get(url) # Отправка запроса
    if request.status_code == 200: #Проверка на успешный запрос
        return request.text #Возвращается html код страницы
    print("Неверный url адрес или ошибка сервера")


def get_links(html): 
    """
    Функция создаёт экземпляр класса BeautifulSoup, в котором прописаны все необходимые методы поиска
    ифнормации в html коде
    """

    soup = BS(html, "html.parser")
    wrapper = soup.find("div", {"class": "listings-wrapper"}) #через метод find() находится определённый тег, в котором содержится нужная информация
    posts: list[BS] = wrapper.find_all("div", {"class": "listing"}) #Находим список всех постов на одной странице

    # post = wrapper.find("div", {"class": "listing"}) #Находим один пост с данными

    links = []
    for post in posts:
        main_info = post.find("div", {"class": "right-info"})

        link = main_info.find("p", {"class": "title"}).find("a").get("href") #находим неполную ссылку на пост
        link = "https://www.house.kg" + link #Создаём рабочу ссылку на пост 

        links.append(link)

    return links


def parse_data(html):
    soup = BS(html, "html.parser")
    header = soup.find("div", {"class": "details-header"})
    buttom = header.find("div", {"class": "bottom-info"})

    title = header.find("div", {"class": "left"}).find("h1").text.strip()
    address = header.find("div", {"class": "left"}).find("div", {"class": "address"}).text.strip()

    price_dollar = header.find("div", {"class": "right"}).find("div", {"class": "price-dollar"}).text.strip()
    price_som = header.find("div", {"class": "right"}).find("div", {"class": "price-som"}).text.strip()

    description = soup.find("div", {"class": "details-main"}).find("div", {"class": "right"}).find("div", {"class": "description"}).find("p").text.strip()
    uploaded = buttom.find("span", {"class": "added-span"}).text.strip()
    views = buttom.find("span", {"class": "view-count"}).text.strip()
    # likes = buttom.find("span", {"class": "favourite-count"}).text.strip()

    phone = soup.find("div", {"class": "phone-fixable-block"}).find("div", {"class": "number"}).text.strip()

    details = soup.find("div", {"class": "details-main"}).find("div", {"class": "left"})
    info_rows: list[BS] = details.find_all("div", {"class": "info-row"})

    data = {
        "title": title,
        "address": address,
        "dollar": price_dollar,
        "som": price_som,
        "description": description,
        "uploaded": uploaded,
        "views": views,
        # "likes": likes,
        "phone": phone,
    }

    for row in info_rows:
        label = row.find("div", {"class": "label"}).text.strip()
        value = row.find("div", {"class": "info"}).text.strip()
        data.update({label: value})
    
    return data
        

def main():
    URL = "https://www.house.kg/snyat-kvartiru?rooms=1"
    html_code = get_html(url=URL)
    links = get_links(html=html_code)
    apartaments_data = []
    for link in links:
        link_html = get_html(link)
        link_data = parse_data(link_html)
        apartaments_data.append(link_data)


    manager = DBManager(engine=ENIGNE)
    for data in apartaments_data:
        manager.insert_post(data)
    
    # write_to_csv("one-room-2", *apartaments_data)



if __name__ == "__main__":
    main()