#%%

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re


file = open("lista.html", "r", encoding="utf8")
data = file.read()
file.close()


soup = BeautifulSoup (data, "html.parser" )
beers = soup.find_all( "a", "css-1x5s8wf")

# print(len(beers))


data = []
for beer in beers:
    link = beer.get("href")
    link = "https://www.systembolaget.se" + link
    
    style = beer.find("p", "css-i37je3").text

    name1 = beer.find("p", "css-1n0krvs").text
    try:
        name2 = beer.find("p", "css-123rcq0").text
    except:
        name2 = ""

    info = beer.find_all("p", "css-bbhn7t")

    country = info[0].text

    size = info[1].text[:-3]

    vol = info[2].text[:-7]
    v = vol.split(",")
    if len(v) != 1:
        n, d = v
        abv = int(n)+0.1*int(d)
    else:
        abv = int(vol)

    price = beer.find("p", "css-17znts1").text
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
        store_info = beer.find("div", "css-1w6cke0").text
        num_in_store = re.search("Antal i butik(.*) st", store_info).group(1)
        section = re.search("stSektion(.*)Hylla(.*)", store_info).group(1)
        shelf = re.search("stSektion(.*)Hylla(.*)", store_info).group(2)
    except:
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
    else:
        övrigt.append(b)

print(övrigt)


ordered = lager + [[],[]] + vete + [[],[]] + ale + [[],[]] + porter + [[],[]] + suröl + [[],[]] + cider + [[],[]] + alkoholfritt + [[],[]] + övrigt

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
