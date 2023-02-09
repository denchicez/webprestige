import dateparser as dp
import requests as rq
from bs4 import BeautifulSoup


def html_head(table):
    answer = '''<html>
        <head>
            <title>STOLOTO</title>
        </head>
        <body>'''
    answer += table
    answer += '''</body></html>'''
    return answer


def convert_arr_table_to_html(table):
    html = '''<table width="100%" border="1"><tbody>'''
    for row in table:
        html = html + '''<tr>'''
        for element in row:
            html = html + f'''<td>{element}</td>'''
        html = html + '''</tr>'''
    html = html + '''</tbody></table>'''
    return html_head(html)


async def stoloto_top3_table():
    resp = rq.get('https://www.stoloto.ru/top3/archive')
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('div', class_='month')
    rows = table.find_all('div', class_='elem')
    table = [["Время", "Тираж", "Номера"]]
    for _ in range(3):
        for i in range(10):
            table[0].append(i)
    table[0].append("sum")
    table[0].append("max")
    table[0].append("min")
    table[0].append("m-m")
    for i, row in enumerate(rows):
        try:
            ids = row.find('a').text
            numbers = row.find('span', class_='zone').text
            dates = row.find('div', class_='draw_date').text
            a, b, c = numbers.split()
            table.append([dates, ids, a + "-" + b + "-" + c])
            a = int(a)
            b = int(b)
            c = int(c)
            for index_number in range(3):
                for j in range(10):
                    if j == int(numbers.split()[index_number]):
                        table[len(table) - 1].append(j)
                    else:
                        table[len(table) - 1].append("")
            table[len(table) - 1].append(a + b + c)
            table[len(table) - 1].append(max(a, b, c))
            table[len(table) - 1].append(min(a, b, c))
            table[len(table) - 1].append(max(a, b, c) - min(a, b, c))
        except Exception as e:
            print(e)
            pass
    return table


async def stoloto_keno2_table():
    table = [["Время", "Тираж"]]
    for i in range(1, 81):
        if i < 10:
            table[0].append("0" + str(i))
        else:
            table[0].append(i)
    for page in range(1, 4):
        headers = {
            'authority': 'www.stoloto.ru',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'device-type': 'MOBILE',
            'referer': 'https://www.stoloto.ru/keno2/archive/',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'gosloto-partner': 'bXMjXFRXZ3coWXh6R3s1NTdUX3dnWlBMLUxmdg',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        params = {
            'count': '10',
            'game': 'keno2',
            'page': page,
        }
        url = 'https://www.stoloto.ru/p/api/mobile/api/v35/service/draws/archive'
        # print(url)
        resp = rq.get(url, headers=headers, params=params)
        # time.sleep(2)
        resp = resp.json()
        draws = resp['draws']
        for draw in draws:
            table.append([])
            table[len(table) - 1].append(dp.parse(draw['date']).strftime('%d.%m.%Y %H:%M:%S'))
            table[len(table) - 1].append(draw['number'])
            numbers = draw['combination']['serialized'][9:]
            for j in range(1, 81):
                if str(j) in numbers:
                    table[len(table) - 1].append(str(j))
                else:
                    table[len(table) - 1].append("")

    return table


async def stoloto_bigloto_table():
    table = [["Время", "Тираж"]]
    for i in range(1, 51):
        if i < 10:
            table[0].append("0" + str(i))
        else:
            table[0].append(i)
    for i in range(1, 11):
        if i < 10:
            table[0].append("0" + str(i))
        else:
            table[0].append(str(i))
    for page in range(1, 4):
        headers = {
            'authority': 'www.stoloto.ru',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'device-type': 'MOBILE',
            'referer': 'https://www.stoloto.ru/keno2/archive/',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'gosloto-partner': 'bXMjXFRXZ3coWXh6R3s1NTdUX3dnWlBMLUxmdg',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        params = {
            'count': '10',
            'game': '5x2',
            'page': page,
        }
        url = 'https://www.stoloto.ru/p/api/mobile/api/v35/service/draws/archive'
        resp = rq.get(url, headers=headers, params=params)
        resp = resp.json()
        draws = resp['draws']
        for draw in draws:
            table.append([])
            table[len(table) - 1].append(dp.parse(draw['date']).strftime('%d.%m.%Y %H:%M:%S'))
            table[len(table) - 1].append(draw['number'])
            numbers = draw['combination']['serialized'][:-2]
            for j in range(1, 51):
                if str(j) in numbers:
                    table[len(table) - 1].append(str(j))
                else:
                    table[len(table) - 1].append("")
            numbers = draw['combination']['serialized'][-2:]
            for j in range(1, 11):
                if str(j) in numbers:
                    table[len(table) - 1].append(str(j))
                else:
                    table[len(table) - 1].append("")

    return table
