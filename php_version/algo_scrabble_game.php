<?php 

chose_list($) => choix d'une liste selon un paramètre, retourne ARRAY de 3 mot selon rand(0,lenarray)


string_of_words($ - returnchose_list) => retourne une liste de mots collés STRING à partir de return du chose_list($)
fast_sort($ - return string_of_words) => retourne un ARRAY de lettres ordonnées
letters_not_twice($ - return of fast_word) => retourne un ARRAY de lettres uniques
disorder_letters($ - return from no_letter_twice) => retourne un array de lettres désordonnées
style_letters($ - return from disorder_letter) => stylise les lettres 


function chose_list($num_round){
# ici nous aimerions utiliser MySQL pour que la base soit trés grande et aussi ne plus pouvoir accéder à ceux déjà données.
    if($num_round == 1){
        $words_list_1 = ["cooperation","love","like","friendly","ennemy","mother","aunt","sibling","lovely"];
        $words_list_2 = ["day","month","year","thanksgiving","date","deadline","time","planning","gregorien"];
        $words_list_3 = ["grace","angeline","croix","croisade","catholique","diable","sacrilège","totem","prêtre"];
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


        $words_list_1 = ["pluie","montagne","violon","guitare","endives","chicoree","coron","fromage","emmental"];
        $words_list_2 = ["banshee","kraken","ulyss","sirènes","gevaudan","sparte","mythes","mage","gandalf"];
        $words_list_3 = ["contrat","juge","rêtre","penal","ainesse","statuer","surseoir", "clause","rétroactif"];
        
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
        $words_list_1 = ["grand","petit","large","minus","taille","cm","km","dm","mm"];
        $words_list_2 = ["boulanger","pain","bio","mais","farine","levure","moulin","four","croissant"];
        $words_list_3 = ["fouet","sorcières","pilori","torture","pendre","huguenots","question","inquisition","écartèlement"];

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

// ------------------ PACKAGE O1 : words organization -------------------------


function string_of_words($secret_arr){

    $value = $secret_arr;
    $string = $value[0].$value[1].$value[2]; 
    
    return $string;
    
    }
   

function fast_sort($string_of_three_words)
{
    $array_to_order = [];
    for ($i=0; $i<strlen($string_of_three_words); $i++) 
    { 

        $array_to_order[] = $string_of_three_words[$i]; 
    }

    sort($array_to_order);
    return $array_to_order;
}

function letters_not_twice($three_words) {        
    $unique_letters = array_unique($three_words);

return $unique_letters;
}

function disorder_letters($letters_to_disorder){   
    shuffle($letters_to_disorder);
    shuffle($letters_to_disorder);

    return $letters_to_disorder;
}

function style_letters($letters_to_style){    
    $your_letters = implode("  ",$letters_to_style);

    return "\n\n      >>>-------------\n\n".$your_letters."\n\n              ------------<<<\n";
}   

// --------------------PACKAGE 02 - Letters organization-------------------------

function secret_words_letters($secret_wds_arr) {

    $secret_wds_str = string_of_words($secret_wds_arr);
    $sort_wds_arr = fast_sort($secret_wds_str);
    $not_twice_letters_arr = letters_not_twice($sort_wds_arr);
    $disorder_letters_arr = disorder_letters($not_twice_letters_arr);
    $style_letters_str = style_letters($disorder_letters_arr);
    
    return $style_letters_str; }

// -------------------------------PACKAGE 03 : the game play itself ---------------------------------------

function winning_or_not($secret_w_arr,$user_word) {

    if (($user_word === $secret_w_arr[0]) || ($user_word === $secret_w_arr[1]) || ($user_word === $secret_w_arr[2])) {
        echo "\nyou win";
        echo "\nPerfect ! {$user_word} is among the three secret words";
        return 'win';
    }elseif (($user_word != $secret_w_arr[0]) || ($user_word != $secret_w_arr[1]) || ($user_word != $secret_w_arr[2])) {
        echo "\nSorry, you lose"; 
        return 'lose';
    }
}


function turn_to_play($three_secret_w){  
    $already_found = [];
    $turn = 1;
    $score = 0;
    $penalty = 0;
    while ($turn < 4) {
        
        // echo "\nSECRET WORDS FOR DEBUGG:";
        // var_dump($three_secret_w);
        echo "Enter one word (words are all in lower case): ";
        $found_word = readline();
            if (in_array($found_word,$already_found) === True){     
                echo "\n{$found_word} have been chosen before so choose another word";
                echo "\n we decide to grant you a new try: ";
                $found_word = readline();
                    if (in_array($found_word,$already_found) === True){
                       echo "No new try so you win.... 2 points of penalty (deduced from final score)...";
                       $penalty += 2;         
                    }
            }   
        array_push($already_found,$found_word);
        // winning_or_not($three_secret_w,$found_word);
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

function welcome_to_play() {

    echo "Welcome in the game of words: guess a word and see if you win or not. \nThere is 3 round and you can guess a word three times. \nThere is three words to be guessed at each round.";
    
    echo "\n\nTo help you, we pick our words in these lexical domains :";
    echo "\nSearch for english words in love and loving beings.";
    echo "\nSearch for french words in these domains : time and calendar \n- religion \n- weather \n- mythologies \n- law \n- words to measure \n- middle age persecutions";
    $round = 1;
    $total_score = [];
    while ($round < 4){
        if ($round == 1){
            echo "\n\nFirst ROUND";
            $our_secret_words = chose_list(1);
            $letters = secret_words_letters($our_secret_words);
            echo "\nThis is the letters from the three secret words (double letters are only stated once): ";
            echo "{$letters}";
            $vic_1 = turn_to_play($our_secret_words);
            array_push($total_score,$vic_1);
        } elseif ($round == 2){
            echo "\n\nSecond ROUND";
            $our_secret_words = chose_list(2);
            $letters = secret_words_letters($our_secret_words);
            echo "\nThis is the letters from the three secret words (double letters are only stated once): ";
            echo "{$letters}";
            $vic_2 = turn_to_play($our_secret_words);
            array_push($total_score,$vic_2);
        } else {
            echo "\n\nThird ROUND";
            $our_secret_words = chose_list(3);
            $letters = secret_words_letters($our_secret_words);
            echo "\nThis is the letters from the three secret words (double letters are only stated once): ";
            echo "{$letters}";
            $vic_3 = turn_to_play($our_secret_words); 
            array_push($total_score,$vic_3);
        }
    $round = $round + 1;
    }
    $total_score_sum = array_sum($total_score);
    echo "\n Now you finished the game, see below what are your final score!!";
    echo "\n\nYour final score is: ".$total_score_sum." points.";        
}

welcome_to_play()

?>

