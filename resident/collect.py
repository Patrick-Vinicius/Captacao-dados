#%%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd 


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.6',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

   
def get_content(url):
    resp = requests.get(url, headers=headers)
    return resp


# %%

def get_basic_infos(soup):
    div_page=soup.find("div" , class_ = "td-page-content")
    paragrafo = div_page.find_all("p")[1]
    ems = paragrafo.find_all("em")
    
    data = {}

    for i in ems:
        chave , valor, *_ = i.text.split(":")
        chave = chave.strip()
        data[chave] = valor.strip()
    return data


#%%
def get_apericoes(soup):
        lis = soup.find("div" , class_ = "td-page-content").find("h4").find_next().find_all("li")
                
        aparicoes = [i.text for i in lis]
        return aparicoes
#%%


def get_personagens_infos(url):
    resp = get_content(url)
    if resp.status_code != 200:
        print("Não foi possível obter os dados")
        return {}
    else:
        soup = BeautifulSoup(resp.text)
        data = get_basic_infos(soup)
        data["Aparicoes"] = get_apericoes(soup)
        return data
# %%
def get_links():
    url = "https://www.residentevildatabase.com/personagens/"
    resp = requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(resp.text) 
    ancoras =(soup_personagens.find("div", class_="td-page-content").find_all("a"))
    links = [i['href'] for i in ancoras]
    return links

# %%
links = get_links()
data = []

for i in tqdm(links):
    d = get_personagens_infos(i)
    d["link"] = i
    data.append(d)
#%%
df = pd.DataFrame(data)
df
# %%
df.to_parquet("dados_re.parquet", index= False)
#%%
df_new = pd.read_parquet("dados_re.parquet")
df_new

# %%
