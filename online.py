from bs4 import BeautifulSoup as BS
import requests


URL = "https://www.house.kg/snyat-kvartiru?region=1&town=2&sort_by=upped_at+desc"

def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def get_posts_links(html):
    #достает 10 ссылок с страницы
    links = []
    soup = BS(html, "html.parser")
    container = soup.find("div",{"class":"container body-container"})
    main = container.find("div",{"class":"main-content"})
    listings = main.find("div",{"class":"listings-wrapper"})
    posts = listings.find_all("div",{"class":"listing"})
    for post in posts:
        header = post.find("div",{"class":"left-side"})
        link = header.find("a").get("href")
        full_link = "https://www.house.kg" + link
        links.append(full_link)
    return links

def get_post_data(html):
    soup = BS(html, "html.parser")
    main = soup.find("div",{"class":"main-content"})
    header = main.find("div",{"class":"details-header"})
    title = header.find("div",{"class":"left"}).find("h1").text.strip() #название 10 постов
    address = header.find("div",{"class":"address"}).text.strip()
    dollar = header.find("div",{"class":"price-dollar"}).text
    som = header.find("div",{"class":"price-som"}).text
    mobile = main.find("div",{"class":"phone-fixable-block"}).find("div",{"class":"number"}).text
    desc = main.find("div",{"class":"description"}).text.strip()
    lon = main.find("div",{"id":"map2gis"}).get("data-lon") #лангитюд долгота
    lat = main.find("div",{"id":"map2gis"}).get("data-lat") #Латюд ширина
    infos = main.find("div",{"class":"details-main"}).find_all("div",{"class":"info-row"})
    add_info = {} #создадим пустой словарь 
    for info in infos:
        key = info.find("div",{"class":"label"}).text.strip()
        value = info.find("div",{"class":"info"}).text.strip()
        add_info.update({key:value})
    print(add_info)


def main(): #запуск всей программы
    html = get_html(URL)
    links = get_posts_links(html)
    for link in links:
        detail_html = get_html(link) #смысл get_htlm доставать (парсить) страницу по ссылке
        get_post_data(detail_html)


if __name__ == "__main__":
    main()