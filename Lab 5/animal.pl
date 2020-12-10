/* Prolog version of the animal identification game (simple expert system) */
/* presented in a Lisp program in Chapter 6 of Winston and Horn (1985).    */

/* hypotheses to be tested */
hypothesize(ostrich)   :- ostrich, !.
hypothesize(tiger)     :- tiger, !.
hypothesize(cheetah)   :- cheetah, !.
hypothesize(giraffe)   :- giraffe, !.
hypothesize(zebra)     :- zebra, !.
hypothesize(penguin)   :- penguin, !.
hypothesize(albatross) :- albatross, !.
hypothesize(unknown).             /* no diagnosis */

/* animal identification rules */
tiger :- mammal,  
         carnivore,
         verify(has_tawny_color), 
         verify(has_black_stripes).
cheetah :- mammal, 
           carnivore, 
           verify(has_tawny_color),
           verify(has_dark_spots).
giraffe :- ungulate, 
           verify(has_long_neck), 
           verify(has_long_legs).
zebra :- ungulate,  
         verify(has_black_stripes).

ostrich :- bird,  
           verify(does_not_fly), 
           verify(has_long_neck).
penguin :- bird, 
           verify(does_not_fly), 
           verify(swims),
           verify(is_black_and_white).
albatross :- bird,
             verify(appears_in_story_Ancient_Mariner),
             verify(flys_well).

/* classification rules */
mammal    :- verify(has_hair), !.
mammal    :- verify(gives_milk).
bird      :- verify(has_feathers), !.
bird      :- verify(flys), 
             verify(lays_eggs).
carnivore :- verify(eats_meat), !.
carnivore :- verify(has_pointed_teeth), 
             verify(has_claws),
             verify(has_forward_eyes).
ungulate :- mammal, 
            verify(has_hooves), !.
ungulate :- mammal, 
            verify(chews_cud).

