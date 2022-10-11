from random import sample

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



