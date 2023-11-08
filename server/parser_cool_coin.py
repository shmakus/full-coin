import requests
from bs4 import BeautifulSoup
from database.base import SessionLocal
from database.models import CurrencyRate, Exchanges
import re
from multiprocessing import Process


def extract_coolcoin_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give": "",
            "pair_name": "",
            "receive": "",
            "payment_method": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["payment_method"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(row_data)
    return data_list


def extract_bitcoin24_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        row_data["trading_pair"] = match.group(1).replace("-to-", "-")

        data_list.append(row_data)
    return data_list


def extract_apexchange_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        row_data["trading_pair"] = match.group(1).replace("-to-", "-")

        data_list.append(row_data)
    return data_list


def extract_cashadmin_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        row_data["trading_pair"] = match.group(1).replace("-to-", "-")

        data_list.append(row_data)
    return data_list


def extract_grambit_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give": "",
            "pair_name": "",
            "receive": "",
            "payment_method": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["payment_method"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(row_data)
    return data_list


def extract_finex24_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        link = tarif_line['href'].rstrip('/')
        match = re.search(r'exchange-(.*?)$', link)

        if match:
            base_currency, quote_currency = match.group(1).split('-to-')
            trading_pair = f"{base_currency.upper()}-{quote_currency.upper()}"

            row_data = {
                "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
                "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
                "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
                "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
                "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
                "link": link,
                "exchange_id": 0,
                "trading_pair": trading_pair
            }

            data_list.append(row_data)
    return data_list


def extract_obama_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_pandpay_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_cryptomax_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give": "",
            "pair_name": "",
            "receive": "",
            "payment_method": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["payment_method"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(row_data)
    return data_list


def extract_obmen_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_excoin_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give": "",
            "pair_name": "",
            "receive": "",
            "payment_method": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["payment_method"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(row_data)
    return data_list


def extract_allmoney_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_robmen_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_cointok_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_realexchange_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_na_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_favoriteexchanger_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_to_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_realbit_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_na_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_altinbit_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_epichange_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_receivemoney_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_to_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_hot24_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_to_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_exchangeyourmoney_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_to_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_sberbit_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_niceobmen_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)
    return data_list


def extract_wmsell_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list

def extract_getexch_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give": "",
            "pair_name": "",
            "receive": "",
            "payment_method": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["payment_method"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(row_data)
    return data_list


def extract_crystaltrade_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list


def extract_100bitcoins_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list


def extract_cryptobar_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list


def extract_goldobmen_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list


def extract_adb_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give": "",
            "pair_name": "",
            "receive": "",
            "payment_method": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["payment_method"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(row_data)
    return data_list


def extract_natebit_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give": "",
            "pair_name": "",
            "receive": "",
            "payment_method": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["payment_method"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(row_data)
    return data_list


def extract_globalbits_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give": "",
            "pair_name": "",
            "receive": "",
            "payment_method": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["payment_method"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(row_data)
    return data_list


def extract_coinguru_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_to_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list


def extract_atpayz_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_to_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list


def extract_obmenlite24_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list


def extract_expochange_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give": "",
            "pair_name": "",
            "receive": "",
            "payment_method": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["payment_method"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(row_data)
    return data_list


def extract_ejpmarket_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_to_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list


def extract_24expay_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list


def extract_moneymix_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list


def extract_1654_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list


def extract_swiftchange_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)



    return data_list



def extract_intercontinental_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list


def extract_btchange_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list


def extract_bitobmenka_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_na_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list



def extract_bitbong_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "payment_method": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(row_data)

    return data_list



def scrape_and_save_data(url, exchange_name, data_extraction_callback):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        data_list = data_extraction_callback(soup)

        if data_list:
            with SessionLocal() as db:
                exchange = db.query(Exchanges).filter_by(exchange_name=exchange_name).first()
                exchange_id = exchange.id

                for row_data in data_list:
                    row_data["exchange_id"] = exchange_id
                    existing_record = db.query(CurrencyRate).filter_by(link=row_data["link"]).first()

                    if existing_record:
                        for key, value in row_data.items():
                            setattr(existing_record, key, value)
                    else:
                        new_record = CurrencyRate(**row_data)
                        db.add(new_record)

                db.commit()
                db.flush()

            print(f"Данные успешно сохранены в базе данных для {exchange_name}")
        else:
            print(f"Элементы не найдены на бирже {exchange_name}")
    else:
        print(f"Ошибка при запросе страницы {url}. Код статуса: {response.status_code}")

if __name__ == "__main__":
    # Определите URL и название бирж для каждой функции
    exchange_data_list = [
        ("https://coolcoin.best/tarifs/", "coolcoin", extract_coolcoin_data),
        ("https://bitcoin24.su/tarifs/", "bitcoin24", extract_bitcoin24_data),
        ("https://apexchange.cc/tarifs/", "apexchange", extract_apexchange_data),
        ("https://cashadmin.ru/tarifs/", "cashadmin", extract_cashadmin_data),
        ("https://grambit.biz/tarifyi/", "grambit", extract_grambit_data),
        ("https://finex24.io/tarifs/", "finex24", extract_finex24_data),
        ("https://obama.ru/tarifs/", "obama", extract_obama_data),
        ("https://pandpay.net/tarifs/", "pandpay", extract_pandpay_data),
        ("https://cryptomax.ru/tarifs/", "cryptomax", extract_cryptomax_data),
        ("https://ob-men.com/tarifs/", "ob-men", extract_obmen_data),
        ("https://excoin.in/tarifs/", "excoin", extract_excoin_data),
        ("https://allmoney.market/tarifs/", "allmoney", extract_allmoney_data),
        ("https://r-obmen.ru/tarifs/", "r-obmen", extract_robmen_data),
        ("https://cointok.net/tarifs/", "cointok", extract_cointok_data),
        ("https://real-exchange.ru/tarifs/", "real-exchange", extract_realexchange_data),
        ("https://favorite-exchanger.net/tarifs/", "favorite-exchanger", extract_favoriteexchanger_data),
        ("https://real-bit.net/tarifs/", "real-bit", extract_realbit_data),
        ("https://altinbit.com/tarifs/", "altinbit", extract_altinbit_data),
        ("https://epichange.online/tarifs/", "epichange", extract_epichange_data),
        ("https://receive-money.biz/tarifs/", "receive-money", extract_receivemoney_data),
        ("https://hot24.exchange/tarifs/", "hot24", extract_hot24_data),
        ("https://exchangeyourmoney.com/tarifs/", "exchangeyourmoney", extract_exchangeyourmoney_data),
        ("https://sberbit.vip/tarifs/", "sberbit", extract_sberbit_data),
        ("https://niceobmen.com/tarifs/", "niceobmen", extract_niceobmen_data),
        ("https://wmsell.biz/tarifs/", "wmsell", extract_wmsell_data),
        ("https://getexch.com/tarifs/", "getexch", extract_getexch_data),
        ("https://crystal-trade.org/tarifs/", "crystal-trade", extract_crystaltrade_data),
        ("https://100bitcoins.com/tarifs/", "100bitcoins", extract_100bitcoins_data),
        ##("https://sellver.com/tariffs", "sellver", extract_sellver_data), адаптировать поиск
        ("https://cryptobar.men/tarifs/", "cryptobar", extract_cryptobar_data),
        ("https://goldobmen.com/tarifs/", "goldobmen", extract_goldobmen_data),
        ("https://adb.bz/tarifs/", "adb", extract_adb_data),
        ("https://globalbits.org/tarifs/", "globalbits", extract_globalbits_data),
        ("https://natebit.pro/tarifs/", "natebit", extract_natebit_data),
        ("https://coinguru.pw/tarifs", "coinguru", extract_coinguru_data),
        ("https://atpayz.com/tarifs/", "atpayz", extract_atpayz_data),
        ("https://obmenlite24.ru/tarifs/", "obmenlite24", extract_obmenlite24_data),
        ("https://expochange.org/tarifs/", "expochange", extract_expochange_data),
        ("https://jpmarket.cc/tarifs/", "jpmarket", extract_ejpmarket_data),
        ("https://24expay.com/tarifs/", "24expay", extract_24expay_data),
        ("https://intercontinental.trade/tarifs/", "intercontinental", extract_intercontinental_data),
        ("https://moneymix.org/tarifs/", "moneymix", extract_moneymix_data),
        ("https://1654.exchange/tarifs/", "1654", extract_1654_data),
        ("https://swiftchange.net/tarifs/", "swiftchange", extract_swiftchange_data),
        ("https://btchange.ru/tarifs/", "btchange", extract_btchange_data),
        ("https://bit-obmenka.vip/tarifs/", "bit-obmenka", extract_bitobmenka_data),
        #https://obmenoff.cc/tariffs krutit nado
        ("https://bitbong.pro/tarifs/", "bitbong", extract_bitbong_data),

        # Добавьте остальные биржи и функции здесь
    ]

    processes = []

    for exchange_url, exchange_name, data_extraction_callback in exchange_data_list:
        process = Process(target=scrape_and_save_data, args=(exchange_url, exchange_name, data_extraction_callback))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

