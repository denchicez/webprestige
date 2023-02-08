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
    table = [["Тираж", "Номера"]]
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
            a, b, c = numbers.split()
            table.append([ids, a + "-" + b + "-" + c])
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
