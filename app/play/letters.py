from app.play.words import *
from random import randrange
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
     
    return str(your_letters)   