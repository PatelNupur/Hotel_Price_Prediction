from bs4 import BeautifulSoup
import requests


def events():
    s = requests.session()
    url = "https://www.officeholidays.com/countries/usa/2023"
    r = s.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')
    All_tr = soup.find_all('tr')
    events_lst = []
    for tr in All_tr:
        All_td = tr.find_all('td')
        try:
            holidays = All_td[2].text
            date = All_td[1].text
            a = {
                "date": date,
                "holidays": holidays
            }
            events_lst.append(a)
        except:
            pass
    return events_lst
