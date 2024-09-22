#%%

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re


file = open("lista.html", "r", encoding="utf8")
data = file.read()
file.close()


soup = BeautifulSoup (data, "html.parser" )
beers = soup.find_all( "a", "css-145u7id")

# print(len(beers))


data = []
for beer in beers:
    link = beer.get("href")
    link = "https://www.systembolaget.se" + link
    
    style = beer.find("p", "css-apwxtg").text

    name1 = beer.find("p", "css-1i86311").text
    try:
        name2 = beer.find("p", "css-i3atuq").text
    except:
        name2 = ""

    info = beer.find("div", "css-1dtnjt5").text

    country = re.search("([^0-9]*)", info).group(1)

    size = re.search("([0-9]*) ml", info).group(1)

    vol = re.search("ml(.*) % vol", info).group(1)
    v = vol.split(",")
    if len(v) != 1:
        n, d = v
        abv = int(n)+0.1*int(d)
    else:
        abv = int(vol)

    price = beer.find("p", "css-1k0oafj").text
    n, d = price.split(":")
    n = int(n)
    if "*" in d:
        n += 1
        d = d[:-1]
    if d == "-":
        price = n
    else:
        price = n+0.01*int(d)

    try:
        store_info = beer.find("div", "css-1x8g9wn").text
        #store_info = beer.find("div", "css-1x8g9wn")
        print(store_info)
        num_in_store = re.search("Antal i butik(.*) st", store_info).group(1)
        section = re.search("stSektion(.*)Hylla(.*)", store_info).group(1)
        shelf = re.search("stSektion(.*)Hylla(.*)", store_info).group(2)
    except:
        print("fail\n\n\n")
        num_in_store = ""
        section = ""
        shelf = ""

    
    # print(link)
    # print(style)
    # print(name1)
    # print(name2)
    # print(country)
    # print(size)
    # print(vol)
    # print(price)
    # print(num_in_store)
    # print(section)
    # print(shelf)
    # print()
    data.append([name1, name2, price, "", "",link, style, country, size, abv, num_in_store, section, shelf])







# %%


lager = []
vete = []
ale = []
suröl = []
porter = []
cider = []
vin = []
alkoholfritt = []

övrigt = []

for i, b in enumerate(data):
    if "alkoholfri" in b[6].lower():
        alkoholfritt.append(b)
    elif "ale" in b[6].lower():
        ale.append(b)
    elif "lager" in b[6].lower():
        lager.append(b)
    elif "porter" in b[6].lower():
        porter.append(b)
    elif "syrlig" in b[6].lower():
        suröl.append(b)
    elif "veteöl" in b[6].lower():
        vete.append(b)
    elif "cider" in b[6].lower() or "blanddryck" in b[6].lower():
        cider.append(b)
    elif "vin" in b[6].lower():
        vin.append(b)
    else:
        övrigt.append(b)

print(övrigt)


ordered = [[],["lager"]] + lager + [[],["vete"]] + vete + [[],["ale"]] + ale + [[],["porter"]] + porter + [[],["suröl"]] + suröl + [[],["cider"]] + cider + [[],["vin"]] + vin + [[],["alkoholfritt"]] + alkoholfritt + [[],[]] + övrigt

# print(len(ordered))

# %%
columns = ["namn1", "namn2", "pris", "köp antal", "tot pris", "länk", "stil", "land", "storlek", "alkohol", "antal i butik", "sektion", "hylla"]
df = pd.DataFrame(ordered, columns=columns)

df.to_csv("öl.csv", index=False)

# %%
def myround(x):
    x = float(x)+2.5
    return 5 * round(x/5)


latex = ""

s = ""
for be in lager:
    s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"

    
latex += s

latex += "\n\\vspace{1cm}\n \\textbf{Ale}\\\\\n"

s = ""
for be in ale:
    s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"
latex += s

latex += "\n\\vspace{1cm}\n \\textbf{Veteöl}\\\\\n"
s = ""
for be in vete:
    s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"
latex += s

latex += "\n\\vspace{1cm}\n \\textbf{Suröl}\\\\\n"
s = ""
for be in suröl:
    s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"
latex += s

latex += "\n\\vspace{1cm}\n \\textbf{Porter/Stout}\\\\\n"
s = ""
for be in porter:
    s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"
latex += s

latex += "\n\\vspace{1cm}\n \\textbf{Cider/Blanddryck}\\\\\n"
s = ""
for be in cider:
    s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"
latex += s

latex += "\n\\vspace{1cm}\n \\textbf{Alkoholfritt}\\\\\n"
s = ""
for be in alkoholfritt:
    s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"
latex += s





print(latex)
# %%

# %%
