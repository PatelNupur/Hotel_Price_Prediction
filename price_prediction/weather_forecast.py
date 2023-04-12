from bs4 import BeautifulSoup
import requests

s = requests.session()
url = "https://www.weatherbug.com/weather-forecast/10-day-weather/texas-city-tx-77539"
r = s.get(url)

soup = BeautifulSoup(r.content, 'html.parser')
div1 = soup.find_all('div', class_="day-card__mobile__section is-night")
all_div = soup.find_all('div', class_="day-card__desktop-wrap")


def weather_report():
    lst = []
    for div in all_div:
        day = div.find("span", class_="day").text.strip()
        date = div.find("span", class_="date").text.strip()
        temperatures = div.findAll("div", class_="temp")

        if len(temperatures) == 1:
            day_temperature = temperatures[0].text.strip()
            night_temperature = None
        else:
            day_temperature = temperatures[0].text.strip()
            night_temperature = temperatures[1].text.strip()

        description = div.find("div", class_="description").text.strip()
        x = {
            'day': day,
            'date': date,
            'day_temperature': day_temperature,
            'night_temperature': night_temperature,
            'description': description,
        }
        lst.append(x)
    return lst

