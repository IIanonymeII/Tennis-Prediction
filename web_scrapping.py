import requests
from bs4 import BeautifulSoup
from tqdm import tqdm 
from alive_progress import alive_bar
import pandas as pd 
import unidecode 
import time

def liste_url_match():
    url_match = 'https://www.lequipe.fr/Tennis/Directs'
    r = requests.get(url_match)


    soup = BeautifulSoup(r.content, 'html.parser')
    liste_url = []
    liste_tournoi= []
    total_barre = len(soup.find_all("a"))
    with alive_bar(total_barre,title='Match\'s URL : ') as bar:
        for i in soup.find_all("a"):
            if "Link liveScore__link" in str(i):
                if 'messieurs' in str(i):
                    liste_url.append(i['href'])

                    transi_str = (i['href'].replace("https://www.lequipe.fr/Tennis/",""))
                    sub_str = '/'
                    transi_str = (transi_str[:transi_str.index(sub_str) + len(sub_str)] ).replace("/","")
                    

                    if transi_str[0] == '-':
                        l = list(transi_str)
                        l[0] = '\''
                        transi_str = "".join(l)
                    liste_tournoi.append(transi_str)
            bar()
           
    return liste_url,liste_tournoi
def liste_url_player(liste_url):
    
    liste_url_player = []
    k = 0
    total_barre = len(liste_url)
    with alive_bar(total_barre,title='Player\'s URL  : ') as bar:
        for i in liste_url:
            bool_atp = False
            r = requests.get(i)
            soup = BeautifulSoup(r.content, 'html.parser')

            atp = soup.find_all('h2')
            if 'ATP' in atp[0].getText():
                bool_atp = True
                # print(i,"====>",atp[0].getText())
                liste_url_player.append([])

            
            if bool_atp:
                for j in soup.find_all("a"):
                    if "Link TennisBoard__player" in str(j):
                            liste_url_player[k].append(j['href'])
                k+=1
            bar()
    return liste_url_player


def info_joueur(liste_url_player,liste_tournoi):
    liste_player =[]
    k1 = 0
    classement = ""
    age = ""
    taille = ""
    poids =""

    total_barre = 2*len(liste_url_player)
    with alive_bar(total_barre,title='Search player\'s info : ') as bar:
        for i in liste_url_player:
            liste_player.append([])
            liste_player[k1].append(liste_tournoi[k1])
            for j in i:
                
                r = requests.get(j)
                soup = BeautifulSoup(r.content, 'html.parser')
                for k in soup.find("tbody"):
                    if "Classement" in str(k):
                        classement = ""
                        classement_bool = False
                        for l in str(k):
                            if l == 'è':
                                break
                            if classement_bool :
                                classement += l 
                            elif l ==':':
                                classement_bool = True
                                
                        classement = classement.replace(" ","")
                        try :
                            test_classement = int(classement)
                        except:
                            print("\n\n\n\n ================= ERREUR ============= \n\n\n\n")
                            print("classement erreur not int :",classement)
                    elif "Taille" in str(k):
                        taille = k.getText().replace("Taille : ","").replace(" ","").replace("m","")
                        try :
                            test_taille = int(taille)
                        except:
                            print("\n\n\n\n ================= ERREUR ============= \n\n\n\n")
                            print("taille erreur not int :",taille)
                    
                    elif "Age" in str(k):
                        age = k.getText().replace("Age : ","").replace(" ans","").replace(" ","")
                        try :
                            test_age = int(age)
                        except:
                            print("\n\n\n\n ================= ERREUR ============= \n\n\n\n")
                            print("age erreur not int :",age)

                    elif "Poids" in str(k):
                        poids = k.getText().replace("Poids :","").replace("kg","").replace(" ","")
                        try :
                            test_poids = int(poids)
                        except:
                            print("\n\n\n\n ================= ERREUR ============= \n\n\n\n")
                            print("poids erreur not int :",poids)
                name = soup.find('h1').getText()



                if name == "Brandon Nakashima":
                    url = "https://www.tennisendirect.net/atp/brandon-nakashime/"  # errue du site fini par un e au lieu d'un a

                elif name == "Taylor Fritz":
                    url = "https://www.tennisendirect.net/atp/taylor-harry-fritz/"
                    
                else:

                    name_url = unidecode.unidecode(name.lower().replace(" ","-").replace("'",""))
                    url = "https://www.tennisendirect.net/atp/"+name_url

                try : 
                    r1 = requests.get(url)
                except:
                    print("\n\n\n\n ================= ERREUR ============= \n\n\n\n")
                    print("url not working          url :",url,"            name : ",name)
                # print(r1)
                bar()
                soup1 = BeautifulSoup(r1.content, 'html.parser')
                test = soup1.find("div",{'class':"player_stats"}).getText().replace(' ','').replace('\n','')
                proba = test[ len(test)-7: len(test)].replace('%','').replace("\n","").replace(":","").replace("e","").replace("i","").replace("t","")
                bool_ = False
                bon = False
                transi = ""
                # print("test : ",test)
                for m in test:
                    # print(m,end="")
                    if m == "P" and transi != "":
                        # print("m == \"P\" and transi != \"\"")
                        break

                    if bool_:
                        # print("bool_")
                        if (bon and m != "P"):
                            bool_ = False
                            bon = False
                            # print("if")
                        else:
                            # print("else")
                            transi +=m
                            bon = False
                    if m == ')':
                        # print(" m == ')'")
                        bool_ = True
                        bon = True
                point = transi.replace("Points:","")
                # print(point)

                try :
                    test_point = int(point)
                except:
                    print("\n\n\n\n ================= ERREUR ============= \n\n\n\n")
                    print("point erreur not int :",point)
                
                for g in soup1.find_all("table", class_="table_pmatches"):
                    pass

                entier = 0
                victoire = 0
                for u in g:
                    if u != "\n":
                        if entier == 5:
                            break
                        
                        elif "alt=\"victoire\"" in str(u):
                            victoire += 1
                        entier +=1

                try :
                    test_victoire = int(victoire)

                except :
                    print("\n\n\n\n ================= ERREUR ============= \n\n\n\n")
                    print("victoire erreur not int :",victoire)

                df_players = pd.read_csv('Players_Statistics_.csv')

                try :
                    entier = 0
                    id_ = "?"
                    for h in df_players["name"]:
                        if name in h:
                            # print('\n\nname :',name,"\nh    :",h)
                            id_ = str(df_players["id"][entier])
                            break
                        entier+=1
                except :
                    print("\n\n\n\n ================= ERREUR ============= \n\n\n\n")
                    print("erreur avec le .csv")
                # print(name)
                # print("\n\n\n\n===============================================================================\n\n\n\n")
                liste_player[k1].append({"name":name,"id":id_,"classement": classement,"age": age,"Taille":taille,"Poids":poids,"proba":proba,"points":point,"last_5_matches_win":victoire})
            k1+=1
    return liste_player

def match_dans_base_de_donnee(liste_player):

    k = 0
    liste_sup = []
    for i in liste_player:
        for j in i:
            try:
                if j["id"] == "?":
                    liste_sup.append(k)
            except:
                pass
        k += 1

    liste_sup.sort(reverse = True)
    for i in liste_sup:
        del liste_player[i]

    return liste_player


def main():
    liste, liste_tournoi = liste_url_match()
    return match_dans_base_de_donnee(info_joueur(liste_url_player(liste),liste_tournoi))


if __name__ == "__main__":
    # test = main()
    # for i in test:
    #     print(i)
    for i in liste_url_match():
        print(i)






