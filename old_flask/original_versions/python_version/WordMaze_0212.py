# Finished on 02/12/2021
# Formation bachelor WEB 1ère année - groupe de : Amaury FRANSSEN , Farmata SIDIBE , Abdoulaye DIOP

from random import sample
from random import randint
from random import randrange

# ACSII art' source (named "Snoopy" in our game): https://www.asciiart.eu/animals/bears)

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


# IA can choose among these lists of words:

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

# In order to choose among lists of words we use:

def list_of_words(words_list):
  
  i = 0
  while i < len(words_list):
    chosen_words = sample(words_list,3)
    i = i + 1
    return chosen_words

# Our method to sort:

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


def order(liste):

  temporary_list = ['','',''] 
  temporary_list[0] = liste[0] + liste[1] + liste[2] 
  liste = list(temporary_list[0])
  
  liste = fast_sort(liste) 
  j = 0

  while j <= len(liste):
    i = 0
    while i < len(liste)-1:
      if liste[i] == liste[i+1]:
        del liste[i+1]
      i = i + 1
    j = j + 1

  return liste


def letter_blend(liste_2):

    my_word = order(liste_2) 
    blend_letters = ''
    for i in range(0, len(my_word)):
        index = randrange(0, len(my_word))
        blend_letters += my_word[index] 
        del my_word[index]    

    list(blend_letters) 
    your_letters = '' 
    for g in blend_letters:
            your_letters += g+str('    ')
     
    return str('                    \n>>>-----------------------------------------------\n\n                    ')+your_letters+str('                    \n\n                    -----------------------------------------------<<<')   # 50


# Game function:

def play_scrabble(user_name=input("Veillez rentrer votre nom : ")): 

    print("\n >>>>> BIENVENUE",user_name,"dans le jeu mini-scrabble !\n\n Tentez de gagner l'inestimable peluche \'Snoopy\'.")
    print("Pour un mot trouvé, vous remportez 5 points.\n")
    round_num = 4
    user_round = 0
    total_score = 0 
    
    # Round part 

    while round_num > 1:
        round_num = round_num - 1 
        user_round = user_round + 1
        base_list = chose_list(round_num)
        secret_words = list_of_words(base_list)  

        print(f"\n    | --- MANCHE N° {user_round}: ")
        letters = letter_blend(secret_words)
        indice_1 = len(secret_words[0])
        indice_2 = len(secret_words[1])
        indice_3 = len(secret_words[2])

        print(f"\nTrouvez les 3 mots cachés à partir de ces lettres: \n             {letters}         ")
        print(f"\nVoici des indices : il y a un mot de {indice_1} lettres, un autre de {indice_2} lettres et un dernier de {indice_3} lettres")

        
        number_of_guess = 0 
        user_info = 3 
        score = 0
        find_word = 0
        already_guess = [''] 

        # Turn part

        while number_of_guess < 3:
            
            # Asking user to guess words:
            
            if user_info == 1: 
                print("\n    Tentez de donner un mot une toute dernière fois:\n")
            elif user_info == 3:
                print("\n    Devinez un mot. Vous avez ",user_info,"tours pour cette manche:\n")
            else:
                print("\n    Devinez un nouveau mot. Il vous reste",user_info," tours restant:\n")
            
            found_word = input('      >>> ')  
         
            try:
                int(found_word)
                value = "\nErreur, veuillez entrer seulement des lettres."
                print(value)

            except:
                value = True
                
                # Exclude cheaters

                if found_word in already_guess:
                    text = "\nVous avez essayé de tricher en entrant un mot déjà gagné: vous êtes exclu du jeu. \n"
                    print(text)
                    return text

                already_guess.append(found_word)
                
                # Treating victory or failure :

                i = 0 
                if found_word in secret_words: 
                    print("\nBONNE REPONSE")
                    find_word +=1
                    score += 5
                    print("Vous avez gagné",score,"points lors de ce tour")
                    
                else:
                    print("\nMAUVAISE REPONSE, vous ne gagnez pas de points à ce tour")
            
                number_of_guess = number_of_guess + 1
                user_info = user_info - 1

            # User information about his performance
               
            print("\n Voici les mots que vous avez entrés jusque-là:")
            for p in already_guess:
                if p != '':
                    print("\n",p)

        # User information about his score (end of a turn)

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
 
    # User information about final results 

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