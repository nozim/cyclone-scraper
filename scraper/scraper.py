from lxml import html
import requests
import datetime

CYCLONES_PAGE = 'https://rammb-data.cira.colostate.edu/tc_realtime/'
CYCLONE_LIST_SELECTOR = '//div[@class="basin_storms"]/ul/li/a/@href'

CYCLONE_FORECAST_SELECTOR = '//div[@class="text_product_wrapper"]/table[1]/tr'
CYCLONE_HISTORY_SELECTOR = '//div[@class="text_product_wrapper"]/table[2]/tr'


def fetch_tree(url):
    page = requests.get(url)
    return html.fromstring(page.content)


def extract_cyclones_list():
    tree = fetch_tree(CYCLONES_PAGE)
    cyclone_urls = tree.xpath(CYCLONE_LIST_SELECTOR)
    return list(map(lambda c: CYCLONES_PAGE+c, cyclone_urls))


def tofloat(n):
    try:
        return float(n), None
    except ValueError:
        return 0, "error"


def normalize_forecast_row(row):
    if len(row) != 4:
        raise Exception("invalid row %s", row)
    (h, lat, lon, intensity) = row
    hnum, err = tofloat(h)
    if err != None:
        raise Exception("invalid hour")

    latn, err = tofloat(lat)
    if err != None:
        raise Exception("invalid lat")

    longn, err = tofloat(lon)
    if err != None:
        raise Exception("invalid long")

    intensityn, err = tofloat(intensity)
    if err != None:
        raise Exception("invalid intensity")
    return (hnum, latn, longn, intensityn)


def validatedatetime(datestr):
    try:
        datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M')
    except ValueError:
        raise


def normalize_history_row(row):
    (timestamp, lat, lon, intensity) = row
    try:
        validatedatetime(timestamp)
    except:
        raise Exception("invalid datetime")

    latn, err = tofloat(lat)
    if err != None:
        raise Exception("invalid lat")

    longn, err = tofloat(lon)
    if err != None:
        raise Exception("invalid long")

    intensityn, err = tofloat(intensity)
    if err != None:
        raise Exception("invalid intensity")

    return (timestamp, latn, longn, intensityn)


def extract_history_data(row):
    raw = row.text_content().split()
    if len(raw) != 5:
        return ()

    [date, time, lat, lon, intensity] = raw
    return (date+" "+time, lat, lon, intensity)


def extract_cyclone_details(url):
    def extract_text_content(row): return tuple(row.text_content().split())
    cyclone_tree = fetch_tree(url)
    forecast_rows = cyclone_tree.xpath(CYCLONE_FORECAST_SELECTOR)[1:]  # hint: skippig header line
    forecast_data_raw = list(map(extract_text_content, forecast_rows))
    forecast_data = list(map(normalize_forecast_row, forecast_data_raw))

    history_rows = cyclone_tree.xpath(CYCLONE_HISTORY_SELECTOR)[1:]
    history_data_raw = list(map(extract_history_data, history_rows))
    history_data = list(map(normalize_history_row, history_data_raw))
    return {'history': history_data, 'forecast': forecast_data}
