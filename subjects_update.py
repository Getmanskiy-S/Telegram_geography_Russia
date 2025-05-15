import requests
from bs4 import BeautifulSoup
import sqlite3


def update_subjects():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute('DELETE from subjects')
    con.commit()
    url = "https://ru.wikipedia.org/wiki/Субъекты_Российской_Федерации"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем основную таблицу с классами wikitable и sortable
    table = soup.find('table', {'class': 'wikitable', 'class': 'sortable'})

    # Пропускаем заголовок таблицы
    for row in table.find_all('tr')[2:-1]:
        cols = row.find_all(['th', 'td'])

        # Извлекаем данные из ячеек
        if 'Республика' in cols[1].get_text(strip=True) or 'край' in cols[1].get_text(strip=True) \
                or 'область' in cols[1].get_text(strip=True) or 'АО' in cols[1].get_text(strip=True):
            name = cols[1].get_text(strip=True)
        else:
            continue
        if name.endswith(']'):
            name = name[:name.index('[')]
        if cols[2].find('img'):
            flag = 'https:' + cols[2].find('img')['src']
        else:
            continue
        if cols[3].find('img'):
            emblem = 'https:' + cols[3].find('img')['src']
        else:
            continue
        if len(cols[4].get_text(strip=True)) > 1:
            area = ''
            for s in cols[4].get_text(strip=True):
                if s.isdigit():
                    area += s
                elif s != ' ':
                    break
        else:
            continue
        if len(cols[5].get_text(strip=True)) > 1:
            population = ''
            for s in cols[5].get_text(strip=True)[1:]:
                if s.isdigit():
                    population += s
                elif s != ' ':
                    break
        else:
            continue
        if len(cols[6].get_text(strip=True)) > 1:
            capital = cols[6].get_text(strip=True)
        else:
            continue
        cur.execute(f"INSERT INTO subjects(name,flag,emblem,square,population,center) VALUES(?, ?, ?, ?, ?, ?)",
                    (name, flag, emblem, area, population, capital))
    con.commit()
    con.close()
