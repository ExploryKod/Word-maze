from random import sample

def chose_list(num):
  
  if num == 1:
    words_list_1 = [["écoute","doux","visuel","goût","toucher","odeurs","rèche"],["Sens"]]
    return words_list_1
  elif num == 2:
    words_list_2 = [
      ["pluie","welsh","Cassel","endives","chicoree","coron"],
      ["Chti"]]
    return words_list_2
  elif num == 3:
    words_list_3 = [
      ["grand","petit","large","long","plan","km","mesures","mètres"],
      ["mesure"]
    ]
    return words_list_3

# In order to choose among lists of words we use:

def list_of_words(words_list):
  indice = words_list[1]
  i = 0
  while i < len(words_list[0]):
    chosen_words = sample(words_list[0],3)
    i = i + 1
    return [chosen_words, indice]




