#%%

# Search and replace in spreacsheet
# ([0-9])\.
# $1,

import html2text


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re



pubrunda = False # pris * 1.25 
dyr = False # + 10 kr


file = open("lista.html", "r", encoding="utf8")
data = file.read()
file.close()





soup = BeautifulSoup (data, "html.parser" )
text = soup.get_text("|")


# Slice and dice text
a = text.split("Byt vy")
b = a[1].split("pant tillkommer")
c = re.split('(Hylla\|(?>–|[0-9]+)\|)', b[0])
d = c[0:-1]


beers = []
i = 0
while i < len(d):
    print(i)
    b = d[i] + d[i+1]
    beers.append(b)
    i += 2



# beers = soup.find_all( "a", "css-145u7id")

data = []
for beer in beers:
    beer = re.split('\|', beer)
    banned = ["", "Nyhet", 'Odling & Produktion', 'Eko', 'Miljöcertifierad', 'Socialt ansvar', 'Ekologiskt']

    # print(beer)
    beer = list(filter(lambda x: x not in banned, beer))
    print(len(beer))
    print(beer)
    print("\n")



    # link = beer.get("href")
    # link = "https://www.systembolaget.se" + link
    link =""
    
    # style = beer.find("p", "css-apwxtg").text
    style = beer[0]

    # name1 = beer.find("p", "css-1i86311").text
    name1 = beer[1]
    # try:
    #     name2 = beer.find("p", "css-i3atuq").text
    # except:
    #     name2 = ""
    name2 = beer[2]

    # info = beer.find("div", "css-1dtnjt5").text

    # country = re.search("([^0-9]*)", info).group(1)
    country = beer[-10]

    # size = re.search("([0-9]*) ml", info).group(1)
    size = beer[-9]

    # vol = re.search("ml(.*) % vol", info).group(1)
    # v = vol.split(",")
    # if len(v) != 1:
    #     n, d = v
    #     abv = int(n)+0.1*int(d)
    # else:
    #     abv = int(vol)
    abv = beer[-8]

    # price = beer.find("p", "css-1k0oafj").text
    price = beer[-7]

    # print(price)
    n, d = price.split(":")
    n = int(n)
    if "*" in d:
        n += 1
        d = d[:-1]
    if d == "-":
        price = n
    else:
        price = n+0.01*int(d)

    # try:
    #     store_info = beer.find("div", "css-1x8g9wn").text
    #     #store_info = beer.find("div", "css-1x8g9wn")
    #     print(store_info)
    #     num_in_store = re.search("Antal i butik(.*) st", store_info).group(1)
    #     section = re.search("stSektion(.*)Hylla(.*)", store_info).group(1)
    #     shelf = re.search("stSektion(.*)Hylla(.*)", store_info).group(2)
    # except:
    #     print("fail\n\n\n")
    #     num_in_store = ""
    #     section = ""
    #     shelf = ""

    num_in_store = beer[-5]
    section = beer[-3]
    shelf = beer[-1]

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
belgisk = []
ipa = []
övrigÖl = []
ale = []
suröl = []
porter = []
cider = []
vin = []
alkoholfritt = []

övrigt = []

sorted_data = sorted(data, key=lambda x: x[2], reverse=False)

for i, b in enumerate(sorted_data):
    if "alkoholfri" in b[6].lower():
        alkoholfritt.append(b)
    # elif "ale" in b[6].lower():
    #     ale.append(b)
    elif "belgisk" in b[6].lower():
        belgisk.append(b)
    elif "ipa" in b[6].lower() or "pale" in b[6].lower():
        ipa.append(b)
    elif "ale" in b[6].lower():
        övrigÖl.append(b)
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


ordered = [[],["Lager"]] + lager + [[],["Vete"]] + vete + [[],["Belgare"]] + belgisk + [[],["IPA/Pale ale"]] + ipa + [[],["Övrig öl"]] + övrigÖl + övrigt + [[],["Porter"]] + porter + [[],["Suröl"]] + suröl + [[],["cider"]] + cider + [[],["vin"]] + vin + [[],["alkoholfritt"]] + alkoholfritt + [[],[]]

# print(len(ordered))

# %%
columns = ["namn1", "namn2", "pris", "köp antal", "tot pris", "länk", "stil", "land", "storlek", "alkohol", "antal i butik", "sektion", "hylla"]
df = pd.DataFrame(ordered, columns=columns)

df.to_csv("öl.csv", index=False)

# %%
def myround(x):
    if pubrunda:
        x *= 1.25
    if dyr:
        x += 10

    x = float(x)+2.5
    return 5 * round(x/5)


latex = ""

s = ""
for be in lager:
    s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"
latex += s

latex += "\n\\vspace{1cm}\n \\textbf{Belgisk}\\\\\n"
s = ""
for be in belgisk:
    s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"
latex += s

latex += "\n\\vspace{1cm}\n \\textbf{IPA / Pale Ale}\\\\\n"
s = ""
for be in ipa:
    s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"
latex += s

latex += "\n\\vspace{1cm}\n \\textbf{Övrig Öl}\\\\\n"
s = ""
for be in övrigÖl:
    s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"
latex += s
for be in övrigt:
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

latex += "\n\\vspace{1cm}\n \\textbf{Vin}\\\\\n"
s = ""
for be in vin:
    s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"
latex += s

# latex += "\n\\vspace{1cm}\n \\textbf{Övrigt}\\\\\n"
# s = ""
# for be in övrigt:
#     s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"
# latex += s

latex += "\n\\vspace{1cm}\n \\textbf{Alkoholfritt}\\\\\n"
s = ""
for be in alkoholfritt:
    s += be[0] + " " + be[1] + " \dotfill " + str(myround(be[2])) + " \\\\ \n"
latex += s





print(latex)
# %%

# %%
