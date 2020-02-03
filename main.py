import requests
from bs4 import BeautifulSoup
import json
import threading
import random
import time

def getHTML(url: str, headers: dict):
    try:
        response = requests.get(url, headers = headers)
        return response.text
    except Exception as e:
        raise e


def fetch(url: str, headers: dict) -> dict:
    try:
        response = requests.get(url, headers = headers)
        return json.loads(response.text) 
    except Exception as e:
        return None


def sarchBranches(urlToBranche:str) -> list:
    headers={
            "Accept":"application/json, text/plain",
            "Accept-Charset": "utf-8",
            "Accept-Language":"ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cache-Control":"no-cache",
            "Connection":"keep-alive",
            "Cookie":"openBeta=1; _ga=GA1.2.1427680370.1580240917; _gid=GA1.2.389844167.1580240917; _ym_uid=1580240917438934614; _ym_d=1580240917; _ym_isad=2; __gads=ID=33c5cfcda78f38a0-22d804b469b30074:T=1580293435:S=ALNI_MZ-vocJR0zPwIsSt2UxDPi-qbI8LA; _2gis_webapi_user=d4dd3826-c732-446c-88cb-a55d9a05e503; lang=ru; __utma=64270060.1427680370.1580240917.1580241048.1580292832.3; __utmz=64270060.1580241048.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _2gis_webapi_session=a59cdcbe-c514-4bec-bdf9-5cc4940e80d8; __utmc=64270060; __utmb=64270060.6.10.1580292832; _ym_visorc_8071507=w; _ym_visorc_837864=b; ipp_key=v1580294220632%2Fv3394bda35d2ce766e8c9b6163aeca6afa04ab3%2FkBs9%2F%2B%2BP1aWqoLe4R7q4aA%3D%3D; ipp_uid=1580294220630%2FX8wS7nxxuLZ1J7qQ%2FbLtKnIWM27dQxpU83vObuw%3D%3D; ipp_uid1=1580294220630; ipp_uid2=X8wS7nxxuLZ1J7qQ%2FbLtKnIWM27dQxpU83vObuw%3D%3D",
            "Host":"2gis.ru",   
            "Origin":"https://2gis.ru",
            "Pragma":"no-cache",
            "Referer":"https://2gis.ru/search/%D0%A1%D1%82%D1%80%D0%B0%D1%85%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/geo/70030076118167641/39.578818%2C47.131318?m=39.691771%2C47.222099%2F11",
            "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
        }
    response = getHTML(urlToBranche,headers)
    soup = BeautifulSoup(response)
    branchesHTML = soup.find_all('div', {'class':'_46pzdl'})
    linksToBranches = []
    for item in branchesHTML:
        linksToBranches.append(item.find('a', {'class':'_13ptbeu'}).get('href'))
    return linksToBranches

def searchOrganizations(coordinates:str):
    url = "https://2gis.ru/search/страхование?{0}".format(coordinates)
    headers={
        "Host": "2gis.ru",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        'Accept-Encoding': "gzip, deflate",
        "Connection": "keep-alive",
        "Cookie": "captcha=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpcCI6IjgzLjIyMS4yMDUuMjAxIiwiYXVkIjoicGFyc2VyLWRldGVjdG9yIiwiZXhwIjoxNTgwNjQ2NTQyLCJpc3MiOiJjYXB0Y2hhIn0.toP0OcfESstpYNnhB6zCrVAXARRe0vJFM0csYWSdjSuxqW3Zc8orKegW0UsBTt0eU-hPwamfWk7quAtcBIg9fQ;",
        "Upgrade-Insecure-Requests": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "Trailers",
    }
    response = getHTML(url,headers)
    soup = BeautifulSoup(response,features="html.parser")
    countOrganizations = soup.find('span', {'class':'_1cho7kd9'})
    return countOrganizations

def parsingPriview(result:dict):
    data = {}
    try:
        data['id'] = result['id']
    except KeyError as e:
        return None
    try:
        data['name'] = result['name']
    except KeyError as e:
        return None
    try:
        data['address'] = result['address']
    except KeyError as e:
        return None
    try:
        data['address_name'] = result['address_name']
    except KeyError as e:
        return None 
    try:
        data['city'] = result['adm_div'][0]['name']
    except KeyError as e:
        return None
    try:
        data['point'] = result['point']
    except KeyError as e:
        return None
    try:
        data['text'] = result['ads']['text']
    except KeyError as e:
        data['text'] = 'non-data'
    try:
        data['article'] = result['ads']['article']
    except KeyError as e:
        data['article'] = 'non-data'
    try:
        data['rating'] = result['reviews']['general_rating']
    except KeyError as e:
        data['rating'] = 'non-data'
    try:
        data['org_id'] = result['org']['id']
    except KeyError as e:
        return None   
    try:
        data['branch_count'] = result['org']['branch_count']
    except KeyError as e:
        return None 
    return data

def main():
    subjectsFile = open('data.json')
    subjects = json.loads(subjectsFile.read())
    a = []
    i = 0
    for item in subjects['data']:
        if 'units' in item:
            for unit in item['units']:
                req = {}
                req['subjects'] = item['name']
                req['cout'] = searchOrganizations(unit['coordinates'])
                print(req)
                a.append(req)
                time.sleep(random.randint(2,4))
        else:
            req = {}
            req['subjects'] = item['name']
            req['cout'] = searchOrganizations(item['coordinates'])
            print(req)
            a.append(req)
            time.sleep(random.randint(2,4))
        i+=1
        print(i,'/85')
        
    data={}
    data['data'] = a
    f = open('data.json')
    f.write(json.dumps(data))

    #coordinates = "m=56.579676%2C54.126391%2F6.5"
    #searchOrganizations(coordinates)

    #url="https://catalog.api.2gis.ru/3.0/items?key=rurbbn3446&q=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0+%D0%A1%D1%82%D1%80%D0%B0%D1%85%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5&fields=items.locale,search_attributes,items.adm_div,items.region_id,items.segment_id,items.reviews,items.point,request_type,context_rubrics,items.links,items.name_ex,items.org,items.group,items.external_content,items.comment,items.ads.options,items.stat,items.description,items.geometry.centroid,items.geometry.selection,items.geometry.style,items.timezone_offset,items.context,items.address,items.is_paid,items.access,items.access_comment,items.capacity,items.schedule,items.floors,dym,ad,items.rubrics,items.routes,items.purpose,items.see_also,items.route_logo,items.has_goods,items.is_promoted,search_type,filters,widgets&type=adm_div.city,adm_div.district,adm_div.district_area,adm_div.division,adm_div.living_area,adm_div.place,adm_div.region,adm_div.settlement,attraction,branch,building,crossroad,foreign_city,gate,parking,road,route,station,street,coordinates&page_size=12&page=1&locale=ru_RU&allow_deleted=true&viewpoint1=37.03316623854902,55.987919508790824&viewpoint2=38.24272673439386,55.46847358631834&stat[sid]=9be54a41-2a07-4c4e-94a2-7fa20ed63409&stat[user]=464da36e-a8b8-46e8-9a7c-8375e2789edf&shv=2020-01-29-07&r=1796737521"
    # headers={
    #         "Accept":"application/json, text/plain",
    #         "Accept-Charset": "utf-8",
    #         "Accept-Language":"ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    #         "Cache-Control":"no-cache",
    #         "Connection":"keep-alive",
    #         "Cookie":"openBeta=1; _ga=GA1.2.1427680370.1580240917; _gid=GA1.2.389844167.1580240917; _ym_uid=1580240917438934614; _ym_d=1580240917; _ym_isad=2; __gads=ID=33c5cfcda78f38a0-22d804b469b30074:T=1580293435:S=ALNI_MZ-vocJR0zPwIsSt2UxDPi-qbI8LA; _2gis_webapi_user=d4dd3826-c732-446c-88cb-a55d9a05e503; lang=ru; __utma=64270060.1427680370.1580240917.1580241048.1580292832.3; __utmz=64270060.1580241048.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _2gis_webapi_session=a59cdcbe-c514-4bec-bdf9-5cc4940e80d8; __utmc=64270060; __utmb=64270060.6.10.1580292832; _ym_visorc_8071507=w; _ym_visorc_837864=b; ipp_key=v1580294220632%2Fv3394bda35d2ce766e8c9b6163aeca6afa04ab3%2FkBs9%2F%2B%2BP1aWqoLe4R7q4aA%3D%3D; ipp_uid=1580294220630%2FX8wS7nxxuLZ1J7qQ%2FbLtKnIWM27dQxpU83vObuw%3D%3D; ipp_uid1=1580294220630; ipp_uid2=X8wS7nxxuLZ1J7qQ%2FbLtKnIWM27dQxpU83vObuw%3D%3D",
    #         "Host":"catalog.api.2gis.ru",
    #         "Origin":"https://2gis.ru",
    #         "Pragma":"no-cache",
    #         "Referer":"https://2gis.ru/search/%D0%A1%D1%82%D1%80%D0%B0%D1%85%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/geo/70030076118167641/39.578818%2C47.131318?m=39.691771%2C47.222099%2F11",
    #         #"Referer": "https://2gis.ru/moscow/search/%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%20%D0%A1%D1%82%D1%80%D0%B0%D1%85%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/firm/70000001034536569/37.418764%2C55.718352?m=38.22983%2C55.434088%2F8.5"
    #         "TE":"Trailers",
    #         "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
    #     }
    # url = "https://2gis.ru/moscow/branches/4504136498857307"
    # print(sarchBranches(url))
    # result = response['result']
    # listOrganozations = []
    # for item in result['items']:
    #     data = parsingPriview(item)
    #     data['branch'] = sarchBranch(data)
    #     listOrganozations.append(data)
    #     print(data['name'],len(data['branch']))
    #print(len(listOrganozations))

if __name__ == '__main__':
    main()