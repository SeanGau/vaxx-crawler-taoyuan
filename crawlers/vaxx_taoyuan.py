from bs4 import BeautifulSoup as bs
import requests, re, json, datetime, pytz

def parse_phone(_data_string):
    _match = re.search('[0-9-]+', _data_string)
    _cb = None
    if _match:
        _cb = _match.group(0) 
    else:
        _cb = _data_string
    return _cb

def parse_link(_data_string):
    _link_soup = bs(_data_string, 'html.parser')
    _link = _link_soup.select(".td-content a")
    if len(_link) > 0:
        return _link[0]['href']
    else:
        return None

def parse_brief(_data_string):
    _cb = {
        "可預約": False,
        "疫苗種類": []
    }
    if "未額滿" in _data_string:
        _cb["可預約"] = True
    if "AZ" in _data_string:
        _cb["疫苗種類"].append("AZ")
    if "Moderna" in _data_string:
        _cb["疫苗種類"].append("Moderna")
    return _cb

def crawler(_url):
    session = requests.Session()
    resp = session.get(_url)
    soup = bs(resp.content, 'html.parser')
    content_list = soup.select("#content_list .list_list")
    export_data = []
    for content in content_list:
        _data_soup = bs(str(content), 'html.parser')
        _data = {
            "行政區": _data_soup.select("[data-header='行政區']")[0].get_text().replace("\r","").replace("\n",""),
            "名稱": _data_soup.select("[data-header='名稱']")[0].get_text().replace("\r","").replace("\n",""),
            "接種時間": _data_soup.select("[data-header='接種時間']")[0].get_text().replace("\r","").replace("\n",""),
            "位址": _data_soup.select("[data-header='位址']")[0].get_text().replace("\r","").replace("\n",""),
            "聯絡電話": parse_phone(_data_soup.select("[data-header='聯絡電話']")[0].get_text()),
            "預約連結": parse_link(str(_data_soup.select("[data-header='預約網址']")[0])),
            "備註": parse_brief(_data_soup.select("[data-header='備註']")[0].get_text())
        }
        export_data.append(_data)
    return export_data

url = "https://covid-19.tycg.gov.tw/home.jsp?id=82&parentpath=0,54&websiteid=202105260001"
datas = {
    "data_source": url,
    "last_update": str(datetime.datetime.now(pytz.timezone("Asia/Taipei"))),
    "data": crawler(url)
}

with open("/home/sean/bit/static/datas/vaxx_taoyuan.json", "w", encoding="utf-8") as json_file:
    json.dump(datas, json_file, ensure_ascii=False)