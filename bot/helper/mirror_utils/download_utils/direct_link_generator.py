from math import pow, floor
from requests import get as rget, head as rhead, post as rpost, Session as rsession
from re import findall as re_findall, sub as re_sub, match as re_match, search as re_search, compile as re_compile, DOTALL
from time import sleep, time
from urllib.parse import urlparse, unquote, parse_qs
from json import loads as jsonloads
from lk21 import Bypass
from lxml import etree
from cfscrape import create_scraper
import cloudscraper
from bs4 import BeautifulSoup
from base64 import standard_b64encode, b64decode
from http.cookiejar import MozillaCookieJar
from os import path as ospath
from playwright.sync_api import Playwright, sync_playwright, expect

from bot import LOGGER, config_dict
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.bot_utils import *
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException

fmed_list = ['fembed.net', 'fembed.com', 'femax20.com', 'fcdn.stream', 'feurl.com', 'layarkacaxxi.icu',
             'naniplay.nanime.in', 'naniplay.nanime.biz', 'naniplay.com', 'mm9842.com']


def direct_link_generator(link: str):
    """ direct links generator """
    if 'youtube.com' in link or 'youtu.be' in link:
        raise DirectDownloadLinkException(f"ERROR: Gunakan /{BotCommands.WatchCommand} untuk mirror YouTube link\nGunakan /{BotCommands.ZipWatchCommand} untuk membuat zip dari YouTube Playlist link")
    elif 'zippyshare.com' in link:
        return zippy_share(link)
    elif 'yadi.sk' in link or 'disk.yandex.com' in link:
        return yandex_disk(link)
    elif 'mediafire.com' in link:
        return mediafire(link)
    elif 'uptobox.com' in link:
        return uptobox(link)
    elif 'osdn.net' in link:
        return osdn(link)
    elif 'github.com' in link:
        return github(link)
    elif 'hxfile.co' in link:
        return hxfile(link)
    elif 'anonfiles.com' in link:
        return anonfiles(link)
    elif 'letsupload.io' in link:
        return letsupload(link)
    elif '1drv.ms' in link:
        return onedrive(link)
    elif 'pixeldrain.com' in link:
        return pixeldrain(link)
    elif 'antfiles.com' in link:
        return antfiles(link)
    elif 'streamtape.com' in link:
        return streamtape(link)
    elif 'bayfiles.com' in link:
        return anonfiles(link)
    elif 'racaty.net' in link:
        return racaty(link)
    elif '1fichier.com' in link:
        return fichier(link)
    elif 'solidfiles.com' in link:
        return solidfiles(link)
    elif 'krakenfiles.com' in link:
        return krakenfiles(link)
    elif 'uploadhaven.com' in link:
        return uploadhaven(link)
    elif 'upload.ee' in link:
        return uploadee(link)
    elif 'romsget.io' in link:
        return link if link == 'static.romsget.io' else romsget(link)
    elif 'romsgames.net' in link:
        return link if link == 'static.downloadroms.io' else downloadroms(link)
    elif 'rocklinks.net' in link:
        return rock(link)
    elif 'try2link.com' in link:
        return try2link(link)
    elif 'ez4short.com' in link:
        return ez4(link)
    elif 'ouo.io' in link or 'ouo.press' in link:
        return ouo(link)
    elif 'terabox' in link:
        return terabox(link)
    elif 'wetransfer.com' in link:
        return wetransfer(link)
    elif 'gofile.io' in link:
        return gofile(link)
    elif is_filepress_link(link):
        return filepress(link)
    elif is_gdtot_link(link):
        return gdtot(link)
    elif is_unified_link(link):
        return unified(link)
    elif is_udrive_link(link):
        return udrive(link)
    elif is_sharer_link(link):
        return sharer_pw_dl(link)
    elif is_sharedrive_link(link):
        return shareDrive(link)
    elif any(x in link for x in fmed_list):
        return fembed(link)
    elif any(x in link for x in ['sbembed.com', 'watchsb.com', 'streamsb.net', 'sbplay.org']):
        return sbembed(link)
    else:
        raise DirectDownloadLinkException(f'No Direct link function found for {link}')

        
def rock(url: str) -> str:
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'rocklinks.net' in url:
        DOMAIN = "https://blog.disheye.com"
    else:
        DOMAIN = "https://go.techyjeeshan.xyz"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    if 'rocklinks.net' in url:
        final_url = f"{DOMAIN}/{code}?quelle=" 
    else:
        final_url = f"{DOMAIN}/{code}?quelle="

    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"    
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" } 
    sleep(10)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("

def try2link(url):
    client = create_scraper()    
    url = url[:-1] if url[-1] == '/' else url    
    params = (('d', int(time()) + (60 * 4)),)
    r = client.get(url, params=params, headers= {'Referer': 'https://newforex.online/'})   
    soup = BeautifulSoup(r.text, 'html.parser')
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    sleep(7)    
    headers = {'Host': 'try2link.com', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://try2link.com', 'Referer': url}    
    bypassed_url = client.post('https://try2link.com/links/go', headers=headers,data=data)
    return bypassed_url.json()["url"]

def ez4(url):    
    client = cloudscraper.create_scraper(allow_brotli=False)      
    DOMAIN = "https://ez4short.com"     
    ref = "https://techmody.io/"   
    h = {"referer": ref}  
    resp = client.get(url,headers=h)   
    soup = BeautifulSoup(resp.content, "html.parser")    
    inputs = soup.find_all("input")   
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }   
    sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("

ANCHOR_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8uaW86NDQz&hl=en&v=1B_yv3CBEV10KtI2HJ6eEXhJ&size=invisible&cb=4xnsug1vufyr'

def RecaptchaV3(ANCHOR_URL):
    url_base = 'https://www.google.com/recaptcha/'
    post_data = "v={}&reason=q&c={}&k={}&co={}"
    client = rsession()
    client.headers.update({
    'content-type': 'application/x-www-form-urlencoded'
    })
    matches = re_findall('([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
    url_base += matches[0]+'/'
    params = matches[1]
    res = client.get(url_base+'anchor', params=params)
    token = re_findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split('=') for pair in params.split('&'))
    post_data = post_data.format(params["v"], token, params["k"], params["co"])
    res = client.post(url_base+'reload', params=f'k={params["k"]}', data=post_data)
    answer = re_findall(r'"rresp","(.*?)"', res.text)[0]    
    return answer

def ouo(url: str) -> str:
    client = rsession()
    tempurl = url.replace("ouo.press", "ouo.io")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    res = client.get(tempurl)
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"
    for _ in range(2):
        if res.headers.get('Location'):
            break
        bs4 = BeautifulSoup(res.content, 'html.parser')
        inputs = bs4.form.findAll("input", {"name": re_compile(r"token$")})
        data = { input.get('name'): input.get('value') for input in inputs }        
        ans = RecaptchaV3(ANCHOR_URL)
        data['x-token'] = ans
        h = {'content-type': 'application/x-www-form-urlencoded'}        
        res = client.post(next_url, data=data, headers=h, allow_redirects=False)
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"
    return res.headers.get('Location')
        
def zippy_share(url: str) -> str:
    base_url = re_search('http.+.zippyshare.com', url).group()
    response = rget(url)
    pages = BeautifulSoup(response.text, "html.parser")
    js_script = pages.find("div", style="margin-left: 24px; margin-top: 20px; text-align: center; width: 303px; height: 105px;")
    if js_script is None:
        js_script = pages.find("div", style="margin-left: -22px; margin-top: -5px; text-align: center;width: 303px;")
    js_script = str(js_script)

    try:
        var_a = re_findall(r"var.a.=.(\d+)", js_script)[0]
        mtk = int(pow(int(var_a),3) + 3)
        uri1 = re_findall(r"\.href.=.\"/(.*?)/\"", js_script)[0]
        uri2 = re_findall(r"\+\"/(.*?)\"", js_script)[0]
    except:
        try:
            a, b = re_findall(r"var.[ab].=.(\d+)", js_script)
            mtk = eval(f"{floor(int(a)/3) + int(a) % int(b)}")
            uri1 = re_findall(r"\.href.=.\"/(.*?)/\"", js_script)[0]
            uri2 = re_findall(r"\)\+\"/(.*?)\"", js_script)[0]
        except:
            try:
                mtk = eval(re_findall(r"\+\((.*?).\+", js_script)[0] + "+ 11")
                uri1 = re_findall(r"\.href.=.\"/(.*?)/\"", js_script)[0]
                uri2 = re_findall(r"\)\+\"/(.*?)\"", js_script)[0]
            except:
                try:
                    mtk = eval(re_findall(r"\+.\((.*?)\).\+", js_script)[0])
                    uri1 = re_findall(r"\.href.=.\"/(.*?)/\"", js_script)[0]
                    uri2 = re_findall(r"\+.\"/(.*?)\"", js_script)[0]
                except Exception as err:
                    LOGGER.error(err)
                    raise DirectDownloadLinkException("ERROR: Failed to Get Direct Link")
    dl_url = f"{base_url}/{uri1}/{int(mtk)}/{uri2}"
    return dl_url

def yandex_disk(url: str) -> str:
    """ Yandex.Disk direct link generator
    Based on https://github.com/wldhx/yadisk-direct """
    try:
        link = re_findall(r'\b(https?://(yadi.sk|disk.yandex.com|disk.yandex.ru|disk.yandex.com.tr|disk.yandex.com.ru)\S+)', url)[0][0]
    except IndexError:
        return "No Yandex.Disk links found\n"
    api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
    try:
        return rget(api.format(link)).json()['href']
    except KeyError:
        raise DirectDownloadLinkException("ERROR: File not found/Download limit reached\n")

def uptobox(url: str) -> str:
    """ Uptobox direct link generator
    based on https://github.com/jovanzers/WinTenCermin and https://github.com/sinoobie/noobie-mirror """
    try:
        link = re_findall(r'\bhttps?://.*uptobox\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No Uptobox links found\n")
    UPTOBOX_TOKEN = config_dict['UPTOBOX_TOKEN']
    if not UPTOBOX_TOKEN:
        LOGGER.error('UPTOBOX_TOKEN not provided!')
        dl_url = link
    else:
        try:
            link = re_findall(r'\bhttp?://.*uptobox\.com/dl\S+', url)[0]
            dl_url = link
        except:
            file_id = re_findall(r'\bhttps?://.*uptobox\.com/(\w+)', url)[0]
            file_link = 'https://uptobox.com/api/link?token=%s&file_code=%s' % (UPTOBOX_TOKEN, file_id)
            req = rget(file_link)
            result = req.json()
            if result['message'].lower() == 'success':
                dl_url = result['data']['dlLink']
            elif result['message'].lower() == 'waiting needed':
                waiting_time = result["data"]["waiting"] + 1
                waiting_token = result["data"]["waitingToken"]
                sleep(waiting_time)
                req2 = rget(f"{file_link}&waitingToken={waiting_token}")
                result2 = req2.json()
                dl_url = result2['data']['dlLink']
            elif result['message'].lower() == 'you need to wait before requesting a new download link':
                cooldown = divmod(result['data']['waiting'], 60)
                raise DirectDownloadLinkException(f"ERROR: Uptobox is being limited please wait {cooldown[0]} min {cooldown[1]} sec.")
            else:
                LOGGER.info(f"UPTOBOX_ERROR: {result}")
                raise DirectDownloadLinkException(f"ERROR: {result['message']}")
    return dl_url

def mediafire(url: str) -> str:
    try:
        link = re_findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
        link = link.split('?dkey=')[0]
    except IndexError:
        raise DirectDownloadLinkException("No MediaFire links found\n")
    try:
        page = BeautifulSoup(rget(link).content, 'lxml')
        info = page.find('a', {'aria-label': 'Download file'})
        dl_url = info.get('href')
        return dl_url
    except Exception as e:
        LOGGER.error(e)
        raise DirectDownloadLinkException("ERROR: Generate link Mediafire gagal!")

def osdn(url: str) -> str:
    """ OSDN direct link generator """
    osdn_link = 'https://osdn.net'
    try:
        link = re_findall(r'\bhttps?://.*osdn\.net\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No OSDN links found\n")
    page = BeautifulSoup(
        rget(link, allow_redirects=True).content, 'lxml')
    info = page.find('a', {'class': 'mirror_link'})
    link = unquote(osdn_link + info['href'])
    mirrors = page.find('form', {'id': 'mirror-select-form'}).findAll('tr')
    urls = []
    for data in mirrors[1:]:
        mirror = data.find('input')['value']
        urls.append(re_sub(r'm=(.*)&f', f'm={mirror}&f', link))
    return urls[0]

def github(url: str) -> str:
    """ GitHub direct links generator """
    try:
        re_findall(r'\bhttps?://.*github\.com.*releases\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No GitHub Releases links found\n")
    download = rget(url, stream=True, allow_redirects=False)
    try:
        return download.headers["location"]
    except KeyError:
        raise DirectDownloadLinkException("ERROR: Can't extract the link\n")

def hxfile(url: str) -> str:
    """ Hxfile direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    return Bypass().bypass_filesIm(url)

def anonfiles(url: str) -> str:
    """ Anonfiles direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    return Bypass().bypass_anonfiles(url)

def letsupload(url: str) -> str:
    """ Letsupload direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    try:
        link = re_findall(r'\bhttps?://.*letsupload\.io\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No Letsupload links found\n")
    return Bypass().bypass_url(link)

def fembed(link: str) -> str:
    """ Fembed direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    dl_url= Bypass().bypass_fembed(link)
    count = len(dl_url)
    lst_link = [dl_url[i] for i in dl_url]
    return lst_link[count-1]

def sbembed(link: str) -> str:
    """ Sbembed direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    dl_url= Bypass().bypass_sbembed(link)
    count = len(dl_url)
    lst_link = [dl_url[i] for i in dl_url]
    return lst_link[count-1]

def onedrive(link: str) -> str:
    """ Onedrive direct link generator
    Based on https://github.com/UsergeTeam/Userge """
    link_without_query = urlparse(link)._replace(query=None).geturl()
    direct_link_encoded = str(standard_b64encode(bytes(link_without_query, "utf-8")), "utf-8")
    direct_link1 = f"https://api.onedrive.com/v1.0/shares/u!{direct_link_encoded}/root/content"
    resp = rhead(direct_link1)
    if resp.status_code != 302:
        raise DirectDownloadLinkException("ERROR: Unauthorized link, the link may be private")
    return resp.next.url

def pixeldrain(url: str) -> str:
    """ Based on https://github.com/yash-dk/TorToolkit-Telegram """
    url = url.strip("/ ")
    file_id = url.split("/")[-1]
    if url.split("/")[-2] == "l":
        info_link = f"https://pixeldrain.com/api/list/{file_id}"
        dl_link = f"https://pixeldrain.com/api/list/{file_id}/zip"
    else:
        info_link = f"https://pixeldrain.com/api/file/{file_id}/info"
        dl_link = f"https://pixeldrain.com/api/file/{file_id}"
    resp = rget(info_link).json()
    if resp["success"]:
        return dl_link
    else:
        raise DirectDownloadLinkException(f"ERROR: Cant't download due {resp['message']}.")

def antfiles(url: str) -> str:
    """ Antfiles direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    return Bypass().bypass_antfiles(url)

def streamtape(url: str) -> str:
    """ Streamtape direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    return Bypass().bypass_streamtape(url)

def racaty(url: str) -> str:
    """ Racaty direct link generator
    based on https://github.com/SlamDevs/slam-mirrorbot"""
    dl_url = ''
    try:
        re_findall(r'\bhttps?://.*racaty\.net\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No Racaty links found\n")
    scraper = create_scraper()
    r = scraper.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    op = soup.find("input", {"name": "op"})["value"]
    ids = soup.find("input", {"name": "id"})["value"]
    rpost = scraper.post(url, data = {"op": op, "id": ids})
    rsoup = BeautifulSoup(rpost.text, "lxml")
    dl_url = rsoup.find("a", {"id": "uniqueExpirylink"})["href"].replace(" ", "%20")
    return dl_url

def fichier(link: str) -> str:
    link = link.split('&af=')[0]
    regex = r"^([http:\/\/|https:\/\/]+)?.*1fichier\.com\/\?.+"
    gan = re_match(regex, link)
    if not gan:
      raise DirectDownloadLinkException("ERROR: Link yang kamu masukkan salah!")
    if "::" in link:
      pswd = link.split("::")[-1]
      url = link.split("::")[-2]
    else:
      pswd = None
      url = link
    try:
      if pswd is None:
        req = rpost(url)
      else:
        pw = {"pass": pswd}
        req = rpost(url, data=pw)
    except:
      raise DirectDownloadLinkException("ERROR: Tidak dapat menjangkau server 1fichier!")
    if req.status_code == 404:
      raise DirectDownloadLinkException("ERROR: File tidak ditemukan atau link yang Anda masukkan salah!")
    soup = BeautifulSoup(req.content, 'lxml')
    if soup.find("a", {"class": "ok btn-general btn-orange"}) is not None:
        dl_url = soup.find("a", {"class": "ok btn-general btn-orange"})["href"]
        if dl_url is None:
          raise DirectDownloadLinkException("ERROR: Generate link 1fichier gagal!")
        else:
          return dl_url
    elif len(soup.find_all("div", {"class": "ct_warn"})) == 3:
        str_2 = soup.find_all("div", {"class": "ct_warn"})[-1]
        if "you must wait" in str(str_2).lower():
            numbers = [int(word) for word in str(str_2).split() if word.isdigit()]
            if not numbers:
                raise DirectDownloadLinkException("ERROR: 1fichier limit. Silahkan tunggu beberapa jam/menit.")
            else:
                raise DirectDownloadLinkException(f"ERROR: 1fichier limit. Silahkan tunggu {numbers[0]} menit lagi!")
        elif "protect access" in str(str_2).lower():
          raise DirectDownloadLinkException(f"ERROR: Link diproteksi!\n\n<b>Link ini membutuhkan password!</b>\n- Ketik <b>::</b> setelah link dan masukan password nya.\n\n<b>Contoh:</b>\n<code>/{BotCommands.MirrorCommand} https://1fichier.com/?blablabla::mirror-gan</code>\n\n* Tidak ada spasi diantara simbol <b>::</b>\n* Untuk password nya, kamu bisa menambahkan spasi!")
        else:
            print(str_2)
            raise DirectDownloadLinkException("ERROR: Generate link 1fichier Gagal!")
    elif len(soup.find_all("div", {"class": "ct_warn"})) == 4:
        str_1 = soup.find_all("div", {"class": "ct_warn"})[-2]
        str_3 = soup.find_all("div", {"class": "ct_warn"})[-1]
        if "you must wait" in str(str_1).lower():
            numbers = [int(word) for word in str(str_1).split() if word.isdigit()]
            if not numbers:
                raise DirectDownloadLinkException("ERROR: 1fichier limit. Silahkan tunggu beberapa jam/menit.")
            else:
                raise DirectDownloadLinkException(f"ERROR: 1fichier limit. Silahkan tunggu {numbers[0]} menit lagi!")
        elif "bad password" in str(str_3).lower():
          raise DirectDownloadLinkException("ERROR: Password yang kamu masukkan salah!")
        else:
            raise DirectDownloadLinkException("ERROR: Generate link 1fichier Gagal!")
    else:
        raise DirectDownloadLinkException("ERROR: Generate link 1fichier Gagal!")

def solidfiles(url: str) -> str:
    """ Solidfiles direct link generator
    Based on https://github.com/Xonshiz/SolidFiles-Downloader
    By https://github.com/Jusidama18 """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
    }
    pageSource = rget(url, headers = headers).text
    mainOptions = str(re_search(r'viewerOptions\'\,\ (.*?)\)\;', pageSource).group(1))
    return jsonloads(mainOptions)["downloadUrl"]

def krakenfiles(page_link: str) -> str:
    """ krakenfiles direct link generator
    Based on https://github.com/tha23rd/py-kraken
    By https://github.com/junedkh """
    page_resp = rsession().get(page_link)
    soup = BeautifulSoup(page_resp.text, "lxml")
    try:
        token = soup.find("input", id="dl-token")["value"]
    except:
        raise DirectDownloadLinkException(f"Page link is wrong: {page_link}")

    hashes = [
        item["data-file-hash"]
        for item in soup.find_all("div", attrs={"data-file-hash": True})
    ]
    if not hashes:
        raise DirectDownloadLinkException(f"ERROR: Hash not found for : {page_link}")


    dl_hash = hashes[0]

    payload = f'------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="token"\r\n\r\n{token}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'
    headers = {
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        "cache-control": "no-cache",
        "hash": dl_hash,
    }

    dl_link_resp = rsession().post(
        f"https://krakenfiles.com/download/{hash}", data=payload, headers=headers)

    dl_link_json = dl_link_resp.json()

    if "url" in dl_link_json:
        return dl_link_json["url"]
    else:
        raise DirectDownloadLinkException(f"ERROR: Failed to acquire download URL from kraken for : {page_link}")


def uploadhaven(url: str) -> str:
    ses = rsession()
    ses.headers = {'Referer':'https://uploadhaven.com/'}
    req = ses.get(url)
    bs = BeautifulSoup(req.text, 'lxml')
    try:
        form = bs.find("form", {'id':'form-download'})
        postdata = {
            "_token": form.find("input", attrs={"name": "_token"}).get("value"),
            "key": form.find("input", attrs={"name": "key"}).get("value"),
            "time": form.find("input", attrs={"name": "time"}).get("value"),
            "hash": form.find("input", attrs={"name": "hash"}).get("value")
        }
        #wait = form.find("span", {'class':'download-timer-seconds d-inline'}).text
        sleep(15)
        post = ses.post(url, data=postdata)
        dl_url = re_findall('"src", "(.*?)"', post.text)
        return dl_url[0]
    except Exception as e:
        LOGGER.error(e)
        raise DirectDownloadLinkException("ERROR: Generate UploadHaven gagal!")


def romsget(url: str) -> str:
    try:
        req = rget(url)
        bs1 = BeautifulSoup(req.text, 'html.parser')
#        LOGGER.info(req.text)

        upos = bs1.find('form', {'id':'download-form'}).get('action')
        meid = bs1.find('input', {'id':'mediaId'}).get('name')
        try:
            dlid = bs1.find('button', {'data-callback':'onDLSubmit'}).get('dlid')
        except:
            dlid = bs1.find('div', {'data-callback':'onDLSubmit'}).get('dlid')

        pos = rpost("https://www.romsget.io"+upos, data={meid:dlid})
        bs2 = BeautifulSoup(pos.text, 'html.parser')
        udl = bs2.find('form', {'name':'redirected'}).get('action')
        prm = bs2.find('input', {'name':'attach'}).get('value')
        return f"{udl}?attach={prm}"
    except Exception as e:
        LOGGER.error(e)
        raise DirectDownloadLinkException("ERROR: Generate link gagal")


def uploadee(url: str) -> str:
    try:
        soup = BeautifulSoup(rget(url).content, 'lxml')
        s_a=soup.find('a', attrs={'id':'d_l'})
        dl_link=s_a['href']
        return dl_link
    except:
        raise DirectDownloadLinkException(
            f"Failed to acquire download URL from upload.ee for : {url}")


def gdtot(url: str) -> str:
    """ Gdtot google drive link generator
    By https://github.com/xcscxr """

    if not config_dict['GDTOT_CRYPT']:
        raise DirectDownloadLinkException("ERROR: CRYPT cookie not provided")

    match = re_findall(r'https?://(.+)\.gdtot\.(.+)\/\S+\/\S+', url)[0]

    with rsession() as client:
        client.cookies.update({'crypt': config_dict['GDTOT_CRYPT']})
        client.get(url)
        res = client.get(f"https://{match[0]}.gdtot.{match[1]}/dld?id={url.split('/')[-1]}")
    matches = re_findall('gd=(.*?)&', res.text)
    try:
        decoded_id = b64decode(str(matches[0])).decode('utf-8')
    except:
        raise DirectDownloadLinkException("ERROR: Try in your broswer, mostly file not found or user limit exceeded!")
    return f'https://drive.google.com/open?id={decoded_id}'


account = {"email": config_dict['UNIFIED_EMAIL'], "passwd": config_dict['UNIFIED_PASS']}


def account_login(client, url, email, password):
    data = {"email": email, "password": password}
    client.post(f"https://{urlparse(url).netloc}/login", data=data)


def gen_payload(data, boundary=f'{"-"*6}_'):
    data_string = ""
    for item in data:
        data_string += f"{boundary}\r\n"
        data_string += (
            f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
        )
    data_string += f"{boundary}--\r\n"
    return data_string


def parse_infou(data):
    info = re_findall(">(.*?)<\/li>", data)
    info_parsed = {}
    for item in info:
        kv = [s.strip() for s in item.split(":", maxsplit=1)]
        info_parsed[kv[0].lower()] = kv[1]
    return info_parsed


def unified(url: str) -> str:
    if (config_dict['UNIFIED_EMAIL'] or config_dict['UNIFIED_PASS']) is None:
        raise DirectDownloadLinkException(
            "UNIFIED_EMAIL and UNIFIED_PASS env vars not provided"
        )
    client = cloudscraper.create_scraper(delay=10, browser='chrome')
    client.headers.update(
        {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        }
    )

    account_login(client, url, account["email"], account["passwd"])

    res = client.get(url)
    key = re_findall('"key",\s+"(.*?)"', res.text)[0]

    ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")

    info_parsed = parse_infou(res.text)
    info_parsed["error"] = False
    info_parsed["link_type"] = "login"  # direct/login

    headers = {
        "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
    }

    data = {"type": 1, "key": key, "action": "original"}

    if len(ddl_btn):
        info_parsed["link_type"] = "direct"
        data["action"] = "direct"

    while data["type"] <= 3:
        try:
            response = client.post(url, data=gen_payload(data), headers=headers).json()
            break
        except:
            data["type"] += 1

    if "url" in response:
        info_parsed["gdrive_link"] = response["url"]
    elif "error" in response and response["error"]:
        info_parsed["error"] = True
        info_parsed["error_message"] = response["message"]
    else:
        info_parsed["error"] = True
        info_parsed["error_message"] = "Something went wrong :("

    if info_parsed["error"]:
        raise DirectDownloadLinkException(f"ERROR! {info_parsed['error_message']}")

    if urlparse(url).netloc == "appdrive.info":
        flink = info_parsed["gdrive_link"]
        return flink

    elif urlparse(url).netloc == "driveapp.in":
        res = client.get(info_parsed["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath("//a[contains(@class,'btn')]/@href")[
            0
        ]
        flink = drive_link
        return flink

    else:
        res = client.get(info_parsed["gdrive_link"])
        drive_link = etree.HTML(res.content).xpath(
            "//a[contains(@class,'btn btn-primary')]/@href"
        )[0]
        flink = drive_link
        return flink
    

def parse_info(res, url):
    info_parsed = {}
    if 'drivebuzz' in url:
        info_chunks = re_findall('<td\salign="right">(.*?)<\/td>', res.text)
    else:
        info_chunks = re_findall(">(.*?)<\/td>", res.text)
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i + 1]
    return info_parsed


def udrive(url: str) -> str:
    if 'katdrive' or 'hubdrive' in url:
        client = rsession()
    else:
        client = cloudscraper.create_scraper(delay=10, browser='chrome')
        
    if "hubdrive" in url:
        if "hubdrive.in" in url:
            url = url.replace(".in",".pro")
        client.cookies.update({"crypt": config_dict['HUBDRIVE_CRYPT']})
    if "drivehub" in url:
        client.cookies.update({"crypt": config_dict['KATDRIVE_CRYPT']})
    if "katdrive" in url:
        client.cookies.update({"crypt": config_dict['KATDRIVE_CRYPT']})
    if "kolop" in url:
        if "kolop.icu" in url:
            url = url.replace(".icu",".cyou")
        client.cookies.update({"crypt": config_dict['KATDRIVE_CRYPT']})
    if "drivefire" in url:
        client.cookies.update({"crypt": config_dict['DRIVEFIRE_CRYPT']})
    if "drivebuzz" in url:
        client.cookies.update({"crypt": config_dict['DRIVEFIRE_CRYPT']})
    res = client.get(url)
    info_parsed = parse_info(res, url)
    info_parsed["error"] = False

    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"

    file_id = url.split("/")[-1]

    data = {"id": file_id}

    headers = {"x-requested-with": "XMLHttpRequest"}

    try:
        res = client.post(req_url, headers=headers, data=data).json()["file"]
    except:
        raise DirectDownloadLinkException(
            "ERROR! File Not Found or User rate exceeded !!"
        )

    if 'drivefire' in url:
        decoded_id = res.rsplit('/', 1)[-1]
        flink = f"https://drive.google.com/file/d/{decoded_id}"
        return flink
    elif 'drivehub' in url:
        gd_id = res.rsplit("=", 1)[-1]
        flink = f"https://drive.google.com/open?id={gd_id}"
        return flink
    elif 'drivebuzz' in url:
        gd_id = res.rsplit("=", 1)[-1]
        flink = f"https://drive.google.com/open?id={gd_id}"
        return flink
    else:
        gd_id = re_findall('gd=(.*)', res, DOTALL)[0]

    info_parsed["gdrive_url"] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed["src_url"] = url
    flink = info_parsed['gdrive_url']

    return flink
    

def sharer_pw_dl(url: str)-> str:
    
    client = cloudscraper.create_scraper(delay=10, browser='chrome')
    client.cookies["XSRF-TOKEN"] = config_dict['XSRF_TOKEN']
    client.cookies["laravel_session"] = config_dict['laravel_session']
    
    res = client.get(url)
    token = re_findall("_token\s=\s'(.*?)'", res.text, DOTALL)[0]
    data = { '_token': token, 'nl' :1}
    headers={ 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'x-requested-with': 'XMLHttpRequest'}

    try:
        response = client.post(url+'/dl', headers=headers, data=data).json()
        drive_link = response
        return drive_link['url']
    
    except:
        if drive_link["message"] == "OK":
            raise DirectDownloadLinkException("Something went wrong. Could not generate GDrive URL for your Sharer Link")
        else:
            finalMsg = BeautifulSoup(drive_link["message"], "lxml").text
            raise DirectDownloadLinkException(finalMsg)
        
def shareDrive(url,directLogin=True):
    """ shareDrive google drive link generator
    by https://github.com/majnurangeela/sharedrive-dl """

    successMsgs = ['success', 'Success', 'SUCCESS']

    scrapper = rsession()

    #retrieving session PHPSESSID
    cook = scrapper.get(url)
    cookies = cook.cookies.get_dict()
    config_dict['PHPSESSID'] = cookies['PHPSESSID']

    headers = {
        'authority' : urlparse(url).netloc,
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin' : f'https://{urlparse(url).netloc}/',
        'referer' : url,
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35',
        'X-Requested-With' : 'XMLHttpRequest'
    }

    if directLogin==True:
        cookies = {
            'PHPSESSID' : config_dict['PHPSESSID']
        }

        data = {
            'id' : url.rsplit('/',1)[1],
            'key' : 'direct'
        }
    else:
        cookies = {
            'PHPSESSID' : config_dict['PHPSESSID'],
            'PHPCKS' : config_dict['SHAREDRIVE_PHPCKS']
        }

        data = {
            'id' : url.rsplit('/',1)[1],
            'key' : 'original'
        }
    
    resp = scrapper.post(f'https://{urlparse(url).netloc}/post', headers=headers, data=data, cookies=cookies)
    toJson = resp.json()

    if directLogin==True:
        if toJson['message'] in successMsgs:
            driveUrl = toJson['redirect']
            return driveUrl
        else:
            shareDrive(url,directLogin=False)
    else:
        if toJson['message'] in successMsgs:
            driveUrl = toJson['redirect']
            return driveUrl
        else:
            raise DirectDownloadLinkException("ERROR! File Not Found or User rate exceeded !!")

def prun(playwright: Playwright, link:str) -> str:
    """ filepress google drive link generator
    By https://t.me/maverick9099
    GitHub: https://github.com/majnurangeela"""

    browser = playwright.chromium.launch()
    context = browser.new_context()

    page = context.new_page()
    page.goto(link)

    firstbtn = page.locator("xpath=//div[text()='Direct Download']/parent::button")
    expect(firstbtn).to_be_visible()
    firstbtn.click()
    sleep(10)

    secondBtn = page.get_by_role("button", name="Download Now")
    expect(secondBtn).to_be_visible()
    with page.expect_navigation():
        secondBtn.click()

    Flink = page.url

    context.close()
    browser.close()

    if 'drive.google.com' in Flink:
        return Flink
    else:
        raise DirectDownloadLinkException("Unable To Get Google Drive Link!")


def filepress(link:str) -> str:
    with sync_playwright() as playwright:
        flink = prun(playwright, link)
        return flink

def terabox(url) -> str:
    if not ospath.isfile('terabox.txt'):
        raise DirectDownloadLinkException("ERROR: terabox.txt not found")
    try:
        session = rsession()
        res = rsession('GET', url)
        key = res.url.split('?surl=')[-1]
        jar = MozillaCookieJar('terabox.txt')
        jar.load()
        rsession.cookies.update(jar)
        res = rsession('GET', f'https://www.terabox.com/share/list?app_id=250528&shorturl={key}&root=1')
        result = res.json()['list']
    except Exception as e:
        raise DirectDownloadLinkException(f"ERROR: {e.__class__.__name__}")
    if len(result) > 1:
        raise DirectDownloadLinkException("ERROR: Can't download mutiple files")
    result = result[0]
    if result['isdir'] != '0':
        raise DirectDownloadLinkException("ERROR: Can't download folder")
    return result['dlink']

def gofile(url: str) -> str:
    api_uri = 'https://api.gofile.io'
    client = rsession()
    args = {'fileNum':0, 'password':''}

    try:
        if '--' in url:
            _link = url.split('--')
            url = _link[0]
            for l in _link[1:]:
                if 'pw:' in l:
                    args['password'] = l.strip('pw:')
                if 'fn:' in l:
                    args['fileNum'] = int(l.strip('fn:'))

        crtAcc = client.get(api_uri+'/createAccount').json()
        data = {
            'contentId': url.split('/')[-1],
            'token': crtAcc['data']['token'],
            'websiteToken': '12345',
            'cache': 'true',
            'password': sha256(args['password'].encode('utf-8')).hexdigest()
        }
        getCon = client.get(api_uri+'/getContent', params=data).json()
    except:
        raise DirectDownloadLinkException("ERROR: Tidak dapat mengambil direct link")

    fileNum = args.get('fileNum')
    if getCon['status'] == 'ok':
        rstr = jsondumps(getCon)
        link = re_findall(r'"link": "(.*?)"', rstr)
        if fileNum > len(link):
            fileNum = 0 #Force to first link
    elif getCon['status'] == 'error-passwordWrong':
        raise DirectDownloadLinkException(f"ERROR: Link ini memerlukan password!\n\n- Tambahkan <b>--pw:</b> setelah link dan ketik password filenya.\n\n<b>Contoh:</b>\n<code>/{BotCommands.MirrorCommand[0]} https://gofile.io/d/xyz--pw:love you</code>")
    else:
        raise DirectDownloadLinkException("ERROR: Generate link Gofile gagal!")

    dl_url = link[fileNum] if fileNum == 0 else link[fileNum-1]
    headers=f"""Host: {urlparse(dl_url).netloc}
                Cookie: accountToken={data['token']}
            """
    return dl_url, headers

def wetransfer(url):
    """ WeTransfer direct link generator
    By https://github.com/TheCaduceus/Link-Bypasser/ """
    api = "https://api.emilyx.in/api"
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        raise DirectDownloadLinkException("ERROR: File tidak ditemukan atau link yang kamu masukan salah!")
    try:
        resp = client.post(api, json={"type": "wetransfer", "url": url})
        res = resp.json()
    except BaseException:
        raise DirectDownloadLinkException("ERROR: Server API sedang down atau link yang kamu masukan salah!")
    if res["success"] is True:
        return res["url"]
    else:
        raise DirectDownloadLinkException(f"ERROR: {res['msg']}")