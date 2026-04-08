# Théorie-des-langages

Affectatiopn print : 'x=2;x=x*5;print(x);'

Affectation élargie, affectation : 'x=9; x+=4; x++; print(x);'

If : 'if(1<2){print(5+5);};'

Else : 'if(1<2){print(5+5);}else{print(50);};'

While : 'while(3<2){print(1+1);};'

For : 'x=4;while(x<30){x=x+3;print(x);};for(i=0;i<4;i=i+1){print(i*i);};'

Fonction avec param et return explicite : 'fonctionValue toto(a, b){c=a+b ;return c ;} ; x = toto(3, 5) ; print(x) ;'

Fonction avec param et return implicite : 'fonctionValue toto(a, b){c=a+b ; toto=c ;} ; toto(3, 5) ;' 
=> Une syntaxe error se déclenche 

Nous pouvons faire des commentaires avec un #.

Gestion des types de chaînes de caratères : 'x = "Bonjour"; print(x);'

Gestion des tableaux :  - Création d'un tableau : scores[] = [3 ; 0] ;
                        - Affichage d'un tableau : print(scores[1]) ;
