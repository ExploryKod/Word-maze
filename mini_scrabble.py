# Projet mini scrable python

# Fini le 02/12/2021
# WEB1 groupe de : Amaury FRANSSEN , Farmata SIDIBE , Abdoulaye DIOP


#------------------------------------- Code -------------------------------------------

# TABLE DES MATIERES DU PROGRAMME (F1 = fonction 1, FP = fonction principale de jeu, BLOC : bloc de code cohérent interne aux fonctions)
# - F1 list_of_words() - fonction qui va choisir au hasard 3 mots dans une liste (Amélioration possible : un tiers peut complexifier en choississant le nombre de mots)
# - F2 tri_rapide(parametre) - Comme son nom l'indique, cette fonction est utilisé pour trier des données si une liste entre en paramètre (en l'occurence la "liste_de_mots()")
# - F3 order(parametre) - Cette fonction va ordonner les mots et supprimer les doublons, il en ressort une liste ordonnée de lettres. 
# - F4 letter_blend(parametre) - Cette fonction prend en paramètre la liste de F3 pour la désordonner aléatoirement et styliser le résultat pour générer un affichage utilisateur.
# - F5 play_scrabble(parametre par defaut) - Fonction principale qui appelle les autres : elle se compose de 5 blocs de codes (dont 4 sous-blocs) qui sont les étapes du jeu. 
# FP - BLOC 01 - On souhaite la bienvenue et on mobilise F1 pour générer une liste de mots secrets (variable secret_words). 
# FP - BLOC 02 - On affiche la liste des lettres (mobilisation de F4 avec la variable secret-words du BLOC 01 en paramètre).
# FP - BLOC 03 - On entre dans le tour à tour (3 tours) via une boucle while 
# ------ Bloc 3.1 : demander de deviner un mot B
# -------Bloc 3.2 : Eliminer les tricheurs
# -------Bloc 3.3 : vérifier les conditions de victoires par tour et comptabiliser le score par mot trouvé
# -------Bloc 3.4 : nous récapitulons les mots trouvés 
# FP - BLOC 04 - On donne les résultats de fin de manche avec des phrases d'encouragement si besoin est. 
# FP - BLOC 05 - Les résultats finaux aprés les 3 manches sont affichés - Possibilité de rejouer. 

from random import sample
from random import randint
from random import randrange
# elle génére le dessin snoopy en ASCII ( source: https://www.asciiart.eu/animals/bears)
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


# fonction qui génére les listes
def chose_list(num):
  
  if num == 1:
    words_list_1 = ["vide","doux","visuel","vent","faux","goal","armada"]
    return words_list_1
  elif num == 2:
    words_list_2 = ["pluie","montagne","violon","endives","chicoree","coron"]
    return words_list_2
  elif num == 3:
    words_list_3 = ["grand","petit","arme","grue","furet","vendre","crème","amour"]
    return words_list_3

# F1 la fonction list_of_words() nous permet de choisir aléatoirement 3 mots du choix de la liste dans la fonction chose_list()
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

    mediane = [List_to_order[0]] # pivot
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
  temporary_list = ['','',''] 
  temporary_list[0] = liste[0] + liste[1] + liste[2] 
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
    # Usage de randrange : cela permet de répartir aléatoirement les index de la liste contenu dans my_word. 

    my_word = order(liste_2) # TAMIS 01 la variable stocke les mots mélangés dans le désordre (TYPE : LISTE)
    blend_letters = ''
    for i in range(0, len(my_word)):
        index = randrange(0, len(my_word))
        blend_letters += my_word[index] # TAMIS 02 blend_letters va stocker des lettres dans le string blend_letters dans le désordre (TYPE = string)
        del my_word[index]    

    # BLOC DE STYLISATION et de résultat (espacer les lettres puis les encadrer)
    list(blend_letters) 
    your_letters = '' 
    for g in blend_letters:
            your_letters += g+str('    ')
     
    return str('                    \n>>>-----------------------------------------------\n\n                    ')+your_letters+str('                    \n\n                    -----------------------------------------------<<<')   # 50


# FP fonction principale de jeu 
def play_scrabble(user_name=input("Veillez rentrer votre nom : ")): # paramétre par défaut pour demander le nom du joueur

  # BLOC 01 - MESSAGE DE BIENVENUE ET TRAITEMENT DE LA MANCHE 

    print("\n >>>>> BIENVENUE",user_name,"dans le jeu mini-scrabble !\n\n Tentez de gagner l'inestimable peluche \'Snoopy\'.")
    print("Pour un mot trouvé, vous remportez 5 points.\n")
    round_num = 4
    user_round = 0
    total_score = 0 
    # traitement de chaque manche 
    while round_num > 1:
        round_num = round_num - 1 
        user_round = user_round + 1
        base_list = chose_list(round_num)
        secret_words = list_of_words(base_list)  

        #

        # BLOC 02 - AFFICHER LES LETTRES
        print(f"\n    | --- MANCHE N° {user_round}: ")
        letters = letter_blend(secret_words)
        indice_1 = len(secret_words[0])
        indice_2 = len(secret_words[1])
        indice_3 = len(secret_words[2])
        print(f"\nTrouvez les 3 mots cachés à partir de ces lettres: \n             {letters}         ")
       # print("\n Mots secrets choisis:",secret_words,"\n\n") # Cela sert pour le débugging
        print(f"\nVoici des indices : il y a un mot de {indice_1} lettres, un autre de {indice_2} lettres et un dernier de {indice_3} lettres")

        # BLOC 03 (TOUR A TOUR) - LE CADRE DE LA BOUCLE WHILE EXTERNE POUR DEVINER LES MOTS
        number_of_guess = 0 
        user_info = 3 
        score = 0
        find_word = 0
        already_guess = ['']  
        while number_of_guess < 3:
            
            # BLOC 03.1 DEMANDER DE DEVINER LES MOTS 
            # Nous personnalisons l'expérience en fonction du nombre d'essais restant (d'où le if ... else) - user_info stocke le résultat d'essais restant.
            if user_info == 1: 
                print("\n    Tentez de donner un mot une toute dernière fois:\n")
            elif user_info == 3:
                print("\n    Devinez un mot. Vous avez ",user_info,"tours pour cette manche:\n")
            else:
                print("\n    Devinez un nouveau mot. Il vous reste",user_info," tours restant:\n")
            
            found_word = input('      >>> ')  # VARIABLE UTILISATEUR found_word : mot entré par l'utilisateur.  (TYPE : STRING)
        
            # Grace à try...except, nous pouvons avertir le programmeur tiers avec plus d'élégance si il y a une erreur d'entrée 
            try:
                int(found_word)
                value = "\nErreur, veuillez entrer seulement des lettres."
                print(value)
            except:
                value = True
                
                # BLOC 3.2 - ELIMINER LES TRICHEURS le jau s'arréte
                if found_word in already_guess:
                    text = "\nVous avez essayé de tricher en entrant un mot déjà gagné: vous êtes exclu du jeu. \n"
                    print(text)
                    return text

                already_guess.append(found_word)
                
                # BLOC 3.3 - CONDITION DE VICTOIRE ET SCORE A CHAQUE TOUR
                i = 0 
                if found_word in secret_words: # CONDITION DE VICTOIRE - le mot trouvé par l'utilisateur est-il dans la liste de référence ? 
                    print("\nBONNE REPONSE")
                    find_word +=1
                    score += 5
                    print("Vous avez gagné",score,"points lors de ce tour")
                    
                else:
                    print("\nMAUVAISE REPONSE, vous ne gagnez pas de points à ce tour")
            
                number_of_guess = number_of_guess + 1
                user_info = user_info - 1

            # BLOC 3.4 - nous récapitulons les mots déjà entrés pour valoriser l'expérience utilisateur    
            print("\n Voici les mots que vous avez entrés jusque-là:")
            for p in already_guess:
                if p != '':
                    print("\n",p)

        # BLOC 04 - En sortie de la 2ème boucle while on donne le score de fin de manche
        print("\n*********   SCORE DE FIN DE MANCHE   **********")
        if score > 0:
            print(f"Voici le nombre de mots trouvé lors de la manche n° {user_round}: vous avez trouvé ",find_word," mots.") 
        else:
            print(f"Voici votre score finale de la manche n° {user_round}: vous n'avez pas trouvé de mots") 
        total_score = total_score + score
        print(f"Votre score total à ce stade du jeu est de {total_score} points")

        if score == 15: 
            print('\nBravo !!! Vous avez tout trouvé du premier coup en 1 manche. Vous êtes bientôt digne de gagner notre peluche \'Snoopy\'!!')
            print('Snoopy est timide mais il est aussi curieux: il sort un peu de sa tanière...')
            print(snoopy(0))
        elif score > 0 and score != 15 : 
            print('\nOups! Vous avez trouvés certains des mots, voici les mots cachés:')
            print('- ',secret_words[0],'- ',secret_words[1],'- ',secret_words[2])
            print('\nVoici les mots que vous avez trouvés:') 
            for i in already_guess[1:]: 
                print('-',i)
            print('\nCertes vous n\'êtes pas au sommet mais retenez cette leçon de confucius:\n\n             \"Le bonheur ne se trouve pas au sommet de la montagne, mais dans la façon de la gravir\"')
        elif score == 0:
            print("Voici les mots que vous deviez trouver")
            print(' ',secret_words[0],'- ',secret_words[1],'- ',secret_words[2])
            print('\n Vous avez perdu une bataille, vous n\'avez pas encore perdu la guerre')
 
    # BLOC 05 - RESULTATS FINAUX (en fonction du score totale)  - sortie de la 1ère boucle while 
    if total_score == 45:
        print("\n_________________RESULTATS FINAUX_________________")
        print("\nBRAVO !!! C'est incroyable, vous n'avez pas fait une seule erreur.")
        print("Comme vous en réviez, nous l'avons fait : vous gagnez la peluche \'Snoopy\'!!!")
        choice = 1
        print(snoopy(choice))
    elif total_score < 45 and total_score > 5:
        print("\n_________________RESULTATS FINAUX_________________")
        print(f"\nVoici votre résultat finale: {total_score} mots trouvés")
        print("\nOUPS, vous avez trouvé certains mots mais vous pouvez persévérer et gagner plus la prochaine fois")
    elif total_score == 5:
        print("\n_________________RESULTATS FINAUX_________________")
        print(f"\nVoici votre résultat finale: {total_score} mot trouvé")
        print("\nOUPS OUPS, vous avez trouvé un mot. C'est déjà un petit quelque-chose.")
    else:
        print("_________________RESULTATS FINAUX_________________")
        print(f"\nVoici votre résultat finale: {total_score} mots trouvés")
        print("\nPERDU! Vous n'avez rien trouvé mais gardez l'espoir, nous croyons en vous!")
    
    # Bloc 06 si le joueur veut rejouer
    print("\n",user_name,",voulez-vous rejouer ? Entrez \"oui\" ou \"non\"")
    replay = input()
    if replay == "oui":
        play_scrabble(user_name)
    elif replay == "non":
        print("Fin du jeu ! merci pour votre participation, au plaisir de vous revoir")
        return
    else:
        print("Vous n'avez ni tapé oui ni tapé non: nous considérons que vous nous quittez")
        print("Fin du jeu ! merci pour votre participation, au plaisir de vous revoir")
        return


play_scrabble()