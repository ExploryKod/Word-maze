# 01/12/2021
# Code plus propre avec une fonction de tri pour remplacer .sort 
# une seule fonction bien identifié par action et pas dans la fonction noyau (order ordonne, letter_blend mélange les lettres ...)

# LISTE DES FONCTIONS : 
# - F1 liste_de_mots() - fonction qui va choisir au hasard 3 mots dans une liste (Amélioration possible : un tiers peut complexifier en choississant le nombre de mots)
# - F2 tri_rapide(parametre) - Comme son nom l'indique, cette fonction est utilisé pour trier des données si une liste entre en paramètre (en l'occurence la "liste_de_mots()")
# - F3 order(parametre) - Cette fonction va ordonner les mots et supprimer les doublons, il en ressort une liste ordonnée de lettres. 
# - F4 lettre_blend(parametre) - Cette fonction prend en paramètre la liste de F3 pour la désordonner aléatoirement et styliser le résultat pour générer un affichage utilisateur.
# - F5 play() - Fonction principale qui appelle les autres : elle se compose de 4 blocs de codes (dont 3 sous-blocs) qui sont les étapes du jeu. 
# F5 - BLOC 01 - On souhaite la bienvenue et on mobilise F1 pour générer une liste de mots secrets (variable secret_words). 
# F5 - BLOC 02 - On affiche la liste des lettres (mobilisation de F4 avec la variable secret-words du BLOC 01 en paramètre).
# F5 - BLOC 03 - On entre dans le tour à tour (3 tours) via une boucle while 
# ------ Bloc 3.1 : demander de deviner un mot B
# -------Bloc 3bis : Eliminer les tricheurs
# -------Bloc 3ter : vérifier les conditions de victoires par tour et comptabiliser le score par mot trouvé
# -------Bloc 3quater : nous récapitulons les mots trouvés 
# F5 - BLOC 04 - On donne les résultats de fin de manche avec des phrases d'encouragement si besoin est. 
# F5 - BLOC 05 - Les résultats finaux aprés les 3 manches sont affichés - Possibilité de rejouer. 

from random import sample
from random import randint
from random import randrange

def chose_list(num):
  
  if num == 1:
    words_list_1 = ["vide","doux","visuel","vent","faux","goal","armada","radis","magie"]
    return words_list_1
  elif num == 2:
    words_list_2 = ["pluie","beffroy","chicons","chtimi","endives","chicoree","coron"]
    return words_list_2
  elif num == 3:
    words_list_3 = ["grand","petit","arme","grue","furet","vendre","crème","amour"]
    return words_list_3

# F1 la fonction liste_des_mots nous permet de choisir aléatoirement 3 mots dans ma liste (On aurait aussi pu utiliser la version de Abdoulaye mais attention à garder les mêmes noms de variable ou tout actualiser)
def list_of_words(words_list):
  
  i = 0
  while i < len(words_list):
    chosen_words = sample(words_list,3)
    i = i + 1
    return chosen_words

# F2 fonction pour trier alphabétiquement en vue de la suppression des doublons (doivent se trouver à index+1 et non index+2)
def fast_sort(List_to_order):

    if len(List_to_order) <= 1:
        return List_to_order

    mediane = [List_to_order[0]]
    L1 = []
    L2 = []
    i = 1

    while i < len(List_to_order):
        if List_to_order[i]>mediane[0]:
            L2.append(List_to_order[i])
        elif List_to_order[i] < mediane[0]:
            L1.append(List_to_order[i])
        else :
            mediane.append(List_to_order[i])
        i = i + 1
    order_result = fast_sort(L1) + mediane + fast_sort(L2)

    return order_result

# F3 fonction qui permet de melanger les 3 mots cachés 
def order(liste):
  # Usage du paramètre via une variabe qui sert d'intermédiare pour coller les mots distinct en une suite de lettre.
  temporary_list = ['','',''] # ici il faut une variable différente pour la liste à trier : une liste intermédiaire qui collera les 3 mots ensemble en 1 chaîne de caractère.
  temporary_list[0] = liste[0] + liste[1] + liste[2] # Peut t-on raccourcir ici  en mettant directement en list(liste[0] + liste[1] + liste[2]) ?
  liste = list(temporary_list[0])
  # F3 - BLOC 01 - Triage avec appel de la fonction de tri rapide
  liste = fast_sort(liste) # liste devient liste_intermediaire mais triée
  j = 0
  # F3 - BLOC 02 - Suppression des doublons en boucle (afin d'agir aussi si + de 2 lettres identiques se suivent) 
  # (car une fois triées les lettres identiques se suivent) 
  while j <= len(liste):
    i = 0
    while i < len(liste)-1:
      if liste[i] == liste[i+1]:
        del liste[i+1]
      i = i + 1
    j = j + 1

  return liste

# F4 La fonction qui va mettre du désordre dans les lettres et ensuite afficher un joli résultat pour l'utilisateur 
def letter_blend(liste_2):
    # BLOC 01 - Appel de la fonction order(param) avec en paramètre une liste. Cette liste sera celle débarassée des doublons. 
    # Il nous reste alors à aléatoirement répartir les lettres en utilisant blend_letter comme accumulateur et la longueur de la liste comme base du compteur "i".
    # Usage de randrange : cela permet de répartir aléatoirement les index de la liste contenu dans my_word. 
    my_word = order(liste_2)  # TAMIS 01 la variable stocke les mots mélangés dans le désordre (TYPE : LISTE)
    blend_letters = ''
    for i in range(0, len(my_word)):
        index = randrange(0, len(my_word))
        blend_letters += my_word[index]     # TAMIS 02 blend_letters va stocker des lettres dans le désordre (TYPE = string)
        del my_word[index]    

    # BLOC DE STYLISATION et de résultat (espacer les lettres puis les encadrer)
    list(blend_letters) # On transforme la chaîne de lettres en liste de lettres désordonnées
    your_letters = '' # your_letters sera la variable qui stocke les lettres désordonnées pour affichage utilisateur 
    for g in blend_letters:
            your_letters += g+str('    ')
     
    return str('                    \n>>>-----------------------------------------------\n\n                    ')+your_letters+str('                    \n\n                    -----------------------------------------------<<<\n')   # 50


# FP fonction principale de jeu à travers laquelle toute les autres fonctions doivent passer pour être appelées
def play_scrabble(user_name):

  # BLOC 01 - MESSAGE DE BIENVENUE ET TRAITEMENT DE LA MANCHE 

    print("\n >>>>> Bienvenue",user_name,"dans le jeu mini-scrabble !\n\n Tentez de gagner l'inestimable peluche \'Snoopy\'.\n")
    round_num = 4
    user_round = 0
    total_score = 0 # Il faut le mettre ici pour qu'il soit comptabilisé. 
    already_guess = [''] # Doit être mis en dehors et puis servira à stocker les mots déjà trouvés  
    while round_num > 1:
        round_num = round_num - 1 
        user_round = user_round + 1
        base_list = chose_list(round_num)
        secret_words = list_of_words(base_list)   # STOCKAGE DE LA LISTE DE REFERENCE (A TROUVER POUR GAGNER) - SE FAIT UNE SEULE FOIS (Verifier que c'est pas aussi ailleurs!!)
        print("\n Mots secrets choisis:",secret_words,"\n\n") # ICI A SUPPRIMER ENSUITE 

        # BLOC 02 - AFFICHER LES LETTRES
        print(f"    | --- MANCHE N° {user_round}: ")
        letters = letter_blend(secret_words)
        print(f"\nTrouvez 3 mots à partir de ces lettres: \n\n            {letters}         ")

        # BLOC 03 (TOUR A TOUR) - LE CADRE DE LA BOUCLE WHILE EXTERNE POUR DEVINER LES MOTS
        number_of_guess = 0 
        user_info = 3 # le chiffre doit être le même que la condition de fin de boucle while + 1 (car le compteur du while démarre à 0)
        score = 0
        while number_of_guess < 3:
            
            # BLOC 03.1 DEMANDER DE DEVINER LES MOTS 
            # Nous personnalisons l'expérience en fonction du nombre d'essais restant (d'où le if ... else) - user_info stocke le résultat d'essais restant.
            if user_info == 1: 
                print("\n    Tentez de donner un mot une toute dernière fois:\n")
            elif user_info == 3:
                print("\n    Devinez un mot.\n    Vous avez ",user_info,"tours pour cette manche:\n")
            else:
                print("\n    Devinez un nouveau mot.\n    Il vous reste",user_info," tours restant:\n")
            
            print("     Ecrivez sous les traits     ")
            print("---------------------------------")
            found_word = input('>>> ')  # VARIABLE UTILISATEUR found_word : mot entré par l'utilisateur.  (TYPE : STRING)
        

            try:
                int(found_word)
                value = "\nErreur, veuillez entrer seulement des lettres."
                print(value)
            except:
                value = True
                
                # BLOC 03bis - ELIMINER LES TRICHEURS
                if found_word in already_guess:
                    text = "\nVous avez essayé de tricher en entrant un mot déjà gagné: vous êtes exclu du jeu. \n"
                    print(text)
                    return text

                already_guess.append(found_word)

                # print(already_guess)
                
                # BLOC 03ter - CONDITION DE VICTOIRE ET SCORE A CHAQUE TOUR
                i = 0 
                if found_word in secret_words: # CONDITION DE VICTOIRE - le mot trouvé par l'utilisateur est-il dans la liste de référence ? 
                    print("\nBonne réponse")
                    score += 1
                    print("Vous avez gagné",score,"points lors de ce tour")
                    
                else:
                    print("\nmauvaise réponse, vous ne gagnez pas de points à ce tour")
            
                number_of_guess = number_of_guess + 1
                user_info = user_info - 1

            # BLOC03quater - nous récapitulons les mots déjà entrés pour valoriser l'expérience utilisateur    
            print("\n Voici les mots entrés jusque-là:")
            for p in already_guess:
                if p != '':
                    print("\n",p)

        # BLOC 04 - En sortie de la 2ème boucle while on donne le score finale
        print("\n*********   SCORE DE FIN DE MANCHE   **********")
        if score > 0:
            print(f"Voici votre score finale de la manche n° {user_round}: vous avez trouvé ",score," mots.") 
        else:
            print(f"Voici votre score finale de la manche n° {user_round}: vous n'avez pas trouvé de mots") 
        total_score = total_score + score
        print(f"Votre score total à ce stade du jeu est de {total_score} points")

        if score == 3: 
            print('\nBravo !!! Vous avez tout trouvé du premier coup en 1 manche. Vous êtes bientôt digne de gagner notre peluche \'Snoopy\'!!')
            print('Snoopy est timide mais il est aussi curieux: il sort un peu de sa tanière...')
            print(snoopy(0))
        elif score > 0 and score != 3 : 
            print('\nBravo! Vous avez trouvés certains des mots cachés, voici les mots cachés:')
            print('-',secret_words[0],'\n-',secret_words[1],'\n-',secret_words[2])
            print('\nVoici vos mots:') 
            for i in already_guess[1:]: 
                print('-',i)
            print('\nCertes vous n\'êtes pas au sommet mais retenez cette leçon de confucius:\n\n             \"Le bonheur ne se trouve pas au sommet de la montagne, mais dans la façon de la gravir\"')
        elif score == 0:
            print('\n Vous avez perdu une bataille, vous n\'avez pas encore perdu la guerre')
 
    # BLOC 05 - RESULTATS FINAUX (en fonction du score totale)  - sortie de la 1ère boucle while 
    if total_score == 9:
        print("\n_________________RESULTATS FINAUX_________________")
        print("\nBravo !!! C'est incroyable, vous n'avez pas fait une seule erreur.")
        print("Comme vous en réviez, nous l'avons fait : vous gagnez la peluche \'Snoopy\'!!!")
        choice = 1
        print(snoopy(choice))
    elif total_score < 9 and total_score > 1:
        print("\n_________________RESULTATS FINAUX_________________")
        print(f"\nVoici votre résultat finale: {total_score} mots trouvés")
        print("\nBravo, vous avez trouvé certains mots mais vous pouvez persévérer et gagner plus la prochaine fois")
    elif total_score == 1:
        print("\n_________________RESULTATS FINAUX_________________")
        print(f"\nVoici votre résultat finale: {total_score} mot trouvé")
        print("\nBravo, vous avez trouvé un mot. C'est déjà un petit quelque-chose.")
    else:
        print("_________________RESULTATS FINAUX_________________")
        print(f"\nVoici votre résultat finale: {total_score} mots trouvés")
        print("\nVous n'avez rien trouvé mais gardez l'espoir, nous croyons en vous!")
    
    print("\n",user_name,",voulez-vous rejouer ? Entrez \"oui\" ou \"non\"")
    replay = input()
    if replay == "oui":
        play_scrabble(user_name)
    elif replay == "non":
        print("Au revoir et merci d'avoir joué")
        return total_score
    else:
        print("Vous n'avez ni tapé oui ni tapé non: nous considérons que vous nous quittez")
        return total_score

def snoopy(choice):

    a="   _      _"
    b="  / \.--./ \\"
    c="  \ -   - / "
    d="  | o   o |"
    e="  \.-'''-./"
    f=" '-\__Y__/-'"
    g="   \"`---`\" "

    if choice == 1:
        return a+str('\n')+b+str('\n')+c+str('\n')+d+str('\n')+e+str('\n')+f+str('\n')+g+str('\n')
    else:
        return a+str('\n')+b+str('\n')+c+str('\n')+d+str('\n')

user = 'Amaury'
play_scrabble(user)