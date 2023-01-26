from Profil import Profil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
from time import sleep

option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_argument("--disable-notifications")
prefs = {"profile.managed_default_content_settings.images": 2}
prefs = {'profile.default_content_setting_values': {'images': 2,
                            'plugins': 2, 'popups': 2, 'geolocation': 2,
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                            'durable_storage': 2}}
option.add_experimental_option("prefs", prefs)
driver=webdriver.Chrome(executable_path="C:\\Users\\Dudu\\Programmes\\chromedriver_win32\\chromedriver.exe",chrome_options=option)

#Root profile
root=Profil(url="https://www.facebook.com/valentin.ducroux",nom="Valentin Ducroux")

#Start
driver.get(root.url)

#Cookies ok
driver.find_element(By.XPATH,"//button[@title='Autoriser les cookies essentiels et optionnels']").click()

#Connexion
driver.find_element(By.ID,"email").send_keys("valentin.ducroux@gmail.com")
driver.find_element(By.ID,"pass").send_keys("4K&RTRT3ya#dxx9F")
driver.find_element(By.ID,"loginbutton").click()

#Attendre la fin de connexion
WebDriverWait(driver, 100).until(EC.title_contains(root.nom))

#Connections


def get_Friends(profile):
    #Go aux amis
    if "profile.php" in profile.url:
        driver.get(profile.url + "&sk=friends")
    else:
        driver.get(profile.url+"/friends")
    driver.execute_script("document.body.style.zoom='25%'")

    #Nb amis
    field_nb_amis=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[1]")
    if "K" in field_nb_amis.get_attribute("innerText"):
        print(f"{profile.nom} a trop d'amis. On passe.")
        # return []

    #Recupérer tous les amis
    liens=[]
    real_profiles=[]

    #Descends tant qu'il reste des amis
    while (not profile.url+"/photos_albums" in driver.find_element(By.TAG_NAME,"body").get_attribute("innerHTML")) and (not "Photos de " in driver.find_element(By.TAG_NAME,"body").get_attribute("innerText")):
        driver.find_element(By.TAG_NAME,"body").send_keys(Keys.END)

    div_amis = driver.find_element(By.XPATH,
                                   "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]")

    soup = BeautifulSoup(div_amis.get_attribute("innerHTML"))

    for a in soup.find_all('a'):
        lien = a.get('href')
        nom = a.find('span').text


        if "friends_mutual" not in lien and lien not in liens and nom != "":
            real_profiles.append(Profil(lien, nom))
            liens.append(lien)

    return real_profiles


my_friends = get_Friends(root)
amis_a_delete=[]

import networkx as nx
G = nx.Graph()
G.add_node(root.nom)

#profondeur 1
for friend in my_friends:
    G.add_node(friend.nom)
    G.add_edge(friend.nom,root.nom)
    f1 = open("all_links.txt", 'a+', encoding="utf-8")
    f1.write(root.nom + "/" + friend.nom + "\n")
    f1.close()
    print(friend.nom,"-",friend.url)
print(f"Amis de {root.nom} extraits.")
nx.write_gexf(G, "80.gexf")
print(f"Fichier gexf généré avec les amis de {root.nom}")

#profondeur 2
c=0
for f in my_friends:
    c+=1
    #Je consulte le fichier des liens
    ff = open("all_links.txt", 'r',encoding="utf-8")
    #Si le nom est présent sur une ligne en premier, on passe
    if f.nom+"/" in ff.read():
        print("Personne deja traitee")
        continue
    ff.close()

    liste=get_Friends(f)
    if len(liste):
        for i in liste:
            G.add_node(i.nom)
            G.add_edge(f.nom,i.nom)
            f1 = open("all_links.txt", 'a+',encoding="utf-8")
            f1.write(f.nom+"/"+i.nom+"\n")
            f1.close()
            print(i.nom, "-", i.url)
    else:
        amis_a_delete.append(f)

    for a in amis_a_delete:
        if G.has_node(a.nom):
            G.remove_node(a.nom)
    print(f"Amis de {f.nom} extraits.")
    nx.write_gexf(G, "80.gexf")
    print(f"Fichier gexf généré avec les amis de {root.nom} et les amis de {c} de ses amis.")



