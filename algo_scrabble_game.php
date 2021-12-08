<?php 

// Ce code est pourri : passé au crible du Clean Code, que devient-il ? 
// Comment remplacer les fonction prédéfinis par des algos de qualité ? 

// PBM :
/*
- Chose_list ne choisis pas vraiment aléatoirement car de nombreux mots vont être choisis à nouveau. Comment la rendre vraiment aléatoire ? Comment utilisé MySQL pour avoir une base de donnée importante ?
- Faire quelque-chose d'interactif où un joueur choisi des mots et l'autre devine (utiliser une base de donnée, passer via HTML/CSS (formulaire) etc...) 
- Algo de tri en Php, remplacer shuffle ?? 
- UPPER / LOWER 

 */


// TABLE LOGIQUE
/* 

chose_list($) => choix d'une liste selon un paramètre, retourne ARRAY de 3 mot selon rand(0,lenarray)

PACKAGE 01 : FROM WORDS TO MELT LETTERS
string_of_words($ - returnchose_list) => retourne une liste de mots collés STRING à partir de return du chose_list($)
fast_sort($ - return string_of_words) => retourne un ARRAY de lettres ordonnées
letters_not_twice($ - return of fast_word) => retourne un ARRAY de lettres uniques
disorder_letters($ - return from no_letter_twice) => retourne un array de lettres désordonnées
style_letters($ - return from disorder_letter) => stylise les lettres 

PACKAGE 02 : FROM LETTERS TO WIN / OVER

*/

function chose_list($num_round){
# ici nous aimerions utiliser MySQL pour que la base soit trés grande et aussi ne plus pouvoir accéder à ceux déjà données.
    if($num_round == 1){
        $words_list_1 = ["vide","doux","visuel","vent","faux","goal","armada","radis","magie"];
        $words_list_2 = ["jour","mois","annee","bissextil","brassière","port","bêtise","mage","grande"];
        $words_list_3 = ["grace","angeline","croix","victoire","barrière","monstre","batisse","risque","bellatre"];
        $i = rand(0,count($words_list_1)-1);
        shuffle($words_list_1);
        shuffle($words_list_2);
        shuffle($words_list_3);
        $secret_1 = $words_list_1[$i];
        $secret_2 = $words_list_2[$i];
        $secret_3 = $words_list_3[$i];

        $array_secret = [$secret_1,$secret_2,$secret_3];
        return $array_secret;
    }
    
    elseif($num_round == 2){
// Toujours garder 8 indices (0 à 8 inclu) c'est à dire le count de la 1ère variable - pkoi mettre des shuffle(words_list_1) ne marche pas ? (NULL is given as result)
        $words_list_1 = ["pluie","montagne","violon","guitare","endives","chicoree","coron","fromage","emmental"];
        $words_list_2 = ["banshee","kraken","siderant","sirènes","bêler","vendre","batifoler","mage","grande"];
        $words_list_3 = ["vivant","juge","rêtre","dents","ruser","rendu","brise", "clause","sérieux"];
        
        shuffle($words_list_1);
        shuffle($words_list_2);
        shuffle($words_list_3);

        $i = rand(0,count($words_list_1)-1);
        $secret_1 = $words_list_1[$i];
        $secret_2 = $words_list_2[$i];
        $secret_3 = $words_list_3[$i];

        $array_secret = [$secret_1,$secret_2,$secret_3];
        return $array_secret;
    }

    elseif($num_round == 3){
        $words_list_1 = ["grand","petit","arme","grue","furet","oracle","magnétique","fourier","amateur"];
        $words_list_2 = ["rompre","danser","parier","vouvoyer","corriger","voir","paraitre","doloris","bijoux"];
        $words_list_3 = ["fouet","diablotin","crisser","maîtrise","bécasse","rageur","buste","perle","vaincre"];

        shuffle($words_list_1);
        shuffle($words_list_2);
        shuffle($words_list_3);

        $i = rand(0,count($words_list_1)-1);
        $secret_1 = $words_list_1[$i];
        $secret_2 = $words_list_2[$i];
        $secret_3 = $words_list_3[$i];

        $array_secret = [$secret_1,$secret_2,$secret_3];
        return $array_secret;
    } 

}

// ------------------ PACKAGE O1 -------------------------

// Use in param01 the secret_words array generated with another variable (don't use the function itself as we want to SETTLE it) and the number of the round/array of words from
function string_of_words($secret_arr){

    $value = $secret_arr;
    $string = $value[0].$value[1].$value[2]; // it is understated in PHP that it will be a value == string
    
    return $string;
    
    }
   
// Transforme 3 mots collés en array de lettres ordonnées
function fast_sort($string_of_three_words) // param is here equiv to strings_of_words result (A STRING) - RETURN ARRAY
{
    $array_to_order = [];
    for ($i=0; $i<strlen($string_of_three_words); $i++) 
    { 

        $array_to_order[] = $string_of_three_words[$i]; 
    }

    sort($array_to_order);
    return $array_to_order;
}

function letters_not_twice($three_words) {        // Param = result of fast_sort - RETURN ARRAY
    $unique_letters = array_unique($three_words);

return $unique_letters;
}

function disorder_letters($letters_to_disorder){   // Param is an array from not_letter_twice - RETURN ARRAY
    shuffle($letters_to_disorder);
    shuffle($letters_to_disorder);

    return $letters_to_disorder;
}

function style_letters($letters_to_style){      // param is result of disorder_letters - RETURN STR
    $your_letters = implode("  ",$letters_to_style);

    return "\n\n      >>>-------------\n\n".$your_letters."\n\n              ------------<<<\n";
}   

// PACKAGE 02 - One package to trigger letters for the user from the variable from secret words generator

function secret_words_letters($secret_wds_arr) {

    $secret_wds_str = string_of_words($secret_wds_arr);
    $sort_wds_arr = fast_sort($secret_wds_str);
    $not_twice_letters_arr = letters_not_twice($sort_wds_arr);
    $disorder_letters_arr = disorder_letters($not_twice_letters_arr);
    $style_letters_str = style_letters($disorder_letters_arr);
    
    return $style_letters_str;

   /* echo "3 MOTS COLLES en string:\n";
     print_r($secret_wds_str);
     echo "ORDRE CROISSANT DES LETTRES:\n";
     print_r($sort_wds_arr );
     echo "PAS DEUX FOIS MEME LETTRE\n";
     print_r($not_twice_letters_arr);
     echo "DESORDRE DES LETTRES uniques\n";
     print_r($disorder_letters_arr);
     echo "STYLE DES LETTRES\n";
     print_r($style_letters_str); */
}

// PACKAGE 03 - the play itself 

function winning_or_not($secret_w_arr,$user_word) {
# Pourquoi score ne veut pas se charger en +1 par win (valeur reste la même ou ne change qu'une fois !) - ça ne marche pas non-plus si le score est 0 !
    if (($user_word === $secret_w_arr[0]) || ($user_word === $secret_w_arr[1]) || ($user_word === $secret_w_arr[2])) {
        echo "\nyou win";
        echo "\nPerfect ! {$user_word} is among the three secret words";
        return 'win';
    }elseif (($user_word != $secret_w_arr[0]) || ($user_word != $secret_w_arr[1]) || ($user_word != $secret_w_arr[2])) {
        echo "\nSorry, you lose"; 
        return 'lose';
    }
}


function turn_to_play($three_secret_w){   # Three_secret_w === our_secret_words
    $already_found = [];
    $turn = 1;
    $score = 0;
    $penalty = 0;
    while ($turn < 4) {
        
        echo "\nSECRET WORDS FOR DEBUGG:";
        var_dump($three_secret_w);
        echo "Enter one word (words are all in lower case): ";
        $found_word = readline();
            if (in_array($found_word,$already_found) === True){     # if in_array($arr,valuetobesearched) == True so the value to be searched is inside $arr
                echo "\n{$found_word} have been chosen before so choose another word";
                echo "\n we decide to grant you a new try: ";
                $found_word = readline();
                    if (in_array($found_word,$already_found) === True){
                       echo "No new try so you win.... 2 points of penalty (deduced from final score)...";
                       $penalty += 2;         
                    }
            }   
        array_push($already_found,$found_word);
        winning_or_not($three_secret_w,$found_word);
        $victory = winning_or_not($three_secret_w,$found_word);
        if ($victory === 'win'){
            $score += 1;
        } elseif ($victory === 'lose') {
            $score += 0;
        } 
        echo "\nYour score is {$score}";
        echo "\nThe amount of your penalty : {$penalty}";
        $turn = $turn + 1;    
    }

    $score = $score - $penalty;
    return $score;
}

# Mieux compdre la compta des score de tours et round - pkoi ça marchais pas.
# lA redondance de mots... 
# attention les mots reviennent trop souvent.

function welcome_to_play() {

    echo "Welcome in the game of words: guess a word and see if you win or not. \nThere is 3 round and you can guess a word three times. \nThere is three words to be guessed at each round.";
    $round = 1;
    $total_score = [];
    while ($round < 4){
        if ($round == 1){
            echo "\nFirst ROUND";
            $our_secret_words = chose_list(1);
            $letters = secret_words_letters($our_secret_words);
            echo "\nThis is the letters from the three secret words (double letters are only stated once): ";
            echo "{$letters}";
            $vic_1 = turn_to_play($our_secret_words);
            array_push($total_score,$vic_1);
        } elseif ($round == 2){
            echo "\nSecond ROUND";
            $our_secret_words = chose_list(2);
            $letters = secret_words_letters($our_secret_words);
            echo "\nThis is the letters from the three secret words (double letters are only stated once): ";
            echo "{$letters}";
            $vic_2 = turn_to_play($our_secret_words);
            array_push($total_score,$vic_2);
        } else {
            echo "\nThird ROUND";
            $our_secret_words = chose_list(3);
            $letters = secret_words_letters($our_secret_words);
            echo "\nThis is the letters from the three secret words (double letters are only stated once): ";
            echo "{$letters}";
            $vic_3 = turn_to_play($our_secret_words); # il s'active aussi en tant que fonction (et retourne en plus le résultat qui sera stocké dans la variable)
            array_push($total_score,$vic_3);
        }
    $round = $round + 1;
    }
    $total_score_sum = array_sum($total_score);
    echo "\n\nYour final score is: ".$total_score_sum." points.";    
    # ICI RESULTAT DE VICTOIRE FINAL AVEC SNOOPY
    
}

welcome_to_play()

?>

