from EllipticNoneFiniteCurve import EllipticNoneFiniteCurve
from Crypto import EllipticFiniteCurve
from Point import Point
import unittest
import sys
import os

# Ajoute le chemin du dossier contenant le fichier à importer
sys.path.append(os.path.abspath("Crypto/"))

# Maintenant, tu peux importer ton fichier
from EllipticFiniteCurve import EllipticFiniteCurve

def point_is_abélien(Curve):
        '''
        Permet d'afficher le résultat de toute les règle des groupes 
        abéliens
        '''
        print("------Début test------")
        #vérifie si dans la liste il y a bien au moins 1 point 
        if(len(Curve.points) >= 1):
            print("Liste de points:",Curve.points)

            print("--Commutativité--")
            print(commutativity(Curve))

            print("--Associativité--")
            print(associativity(Curve))

            print("--Fermeture--")
            print(closing(Curve))

            print("--Neutre Element--")
            print(neutral_element(Curve))

            print("--reverse--")
            print(reverse(Curve))
        else: return ValueError("Liste de points vide")

def commutativity(Curve):
        '''
        Vérifie si les éléments son commutatif.C'est à dire, 
        qu'on peux échanger les places de deux facteurs sans impacter 
        le résultat.
        '''
        i = 0
        commutativité_check = True
        #On parcoure toute la liste de point
        while(i<len(Curve.points)-1 and commutativité_check == True):
            a = Curve.points[i]
            j = i
            #Pour tout les point de la liste on additionne les autres point en évitant de refaire les même calcules
            while(j < len(Curve.points) and commutativité_check == True):
                b = Curve.points[j]
                #On fait la différence avec le résultat None
                if(Curve.addition(a,b) != None and Curve.addition(b,a) != None):
                    try:
                        #On vérifie les valeurs respective de x et y
                        unittest.TestCase().assertAlmostEqual(Curve.addition(a,b)[0], Curve.addition(b,a)[0], delta=1e-5)
                        unittest.TestCase().assertAlmostEqual(Curve.addition(a,b)[1], Curve.addition(b,a)[1], delta=1e-5)
                    except AssertionError:
                        commutativité_check = False
                        
                else: commutativité_check = Curve.addition(a,b) == Curve.addition(b,a)
                j += 1
            i += 1
        return commutativité_check

def associativity(Curve):
        '''
        Vérifie si, peux importe l'odre dans lequel on calcule, le 
        résulta n'est pas impacté
        '''
        #vérifie si dans la liste il y a bien au moins 1 point 
        i = 0
        associativité_check = True
        #On parcour tout les éléments de la liste de point intelligemment pour pas faire plusieur foit le même calcule
        #tant que aucun problème n'a été identifié
        while(i<len(Curve.points) and associativité_check == True):
            a = Curve.points[i]
            j = i 
            while(j<len(Curve.points) and associativité_check == True):
                b = Curve.points[j]
                k = j
                while(k<len(Curve.points) and associativité_check == True):
                    c = Curve.points[k]
                    bc = Curve.addition(b,c)
                    ab = Curve.addition(a,b)
                    #On vérifie si le point calculé n'est pas None pour créer un pour avec les résultat trouvé
                    if bc != None:
                        bc = Point(bc[0], bc[1], "bc")
                    if ab != None:
                        ab = Point(ab[0], ab[1], "ab")    
                    #On fait la différence avec le résultat None
                    if(Curve.addition(a,bc) != None and Curve.addition(ab,c) != None):
                        try:
                            #On vérifie les valeurs respective de x et y
                            unittest.TestCase().assertAlmostEqual(Curve.addition(a,bc)[0], Curve.addition(ab,c)[0], delta=1e-5)
                            unittest.TestCase().assertAlmostEqual(Curve.addition(a,bc)[1], Curve.addition(ab,c)[1], delta=1e-5)
                        except AssertionError:
                            associativité_check = False
                    else: 
                        associativité_check = Curve.addition(a,bc) == Curve.addition(ab,c)
                    k += 1
                j += 1
            i += 1
        return associativité_check

def closing(Curve):
        '''
        Vérifie si le résultat de tout opération de deux points de la courbe
        dans l'ensemble existe également sur la courbe
        '''
        i = 0
        fermeture_check = True
        #On parcour tout les éléments de la liste de point intelligemment pour pas faire plusieur foir le même calcule
        while(i<len(Curve.points) and fermeture_check == True):
            a = Curve.points[i]
            j = i
            while(j < len(Curve.points) and fermeture_check == True):
                b = Curve.points[j]
                #On vérifie si le résulta du calcule de a et b et bien sur la courbe
                if(not(Curve.is_on_curve(Curve.addition(a,b)))):
                    fermeture_check = False
                j += 1
            i += 1
        return fermeture_check

def neutral_element(Curve):
    '''
    Vérifie si l'ensemble comporte l'élément neutre: le point à l'infinit.
    Et vérifie par le calcule s'il ce comporte bien comme un élément neutre
    pour tout les autres élément . 
    '''
    #On vérifie si le point à l'infinit est bien dans l'ensemble
    if(None in Curve.points):
        neutre_élément_check = True
        i = 0
        #On parcour toute les point de la liste 
        while(i < len(Curve.points) and neutre_élément_check == True):
            #On vérifie aue le calcule de l'élément neutre et d'un élément renvois bien le dit élément
            a = Curve.points[i]
            if(Curve.addition(a,None) != None):
                try:
                    #On vérifie les valeurs respective de x et y
                    unittest.TestCase().assertAlmostEqual(Curve.addition(a,None)[0], a.x, delta=1e-5)
                    unittest.TestCase().assertAlmostEqual(Curve.addition(a,None)[1], a.y, delta=1e-5)
                except AssertionError:
                    neutre_élément_check = False
            else: neutre_élément_check = Curve.addition(a,None) == None
            i += 1
        return neutre_élément_check
    else: return False

def reverse(Curve):
    '''
    Vérifie si tout points de la courbe dans l'ensemble possède un inverse 
    également sur la courbe 
    '''
    reverse_élément_check = True
    i = 0
    #Parcourt tout les élément de l'ensemble tant que aucun point n'est sans inverse
    while(i < len(Curve.points) and reverse_élément_check == True):
        a = Curve.points[i]
        #L'élément neutre n'ayant ni réel coordonné ni inverse on ne vérifie pas avec lui
        if(a != None):
            #Vérifie si l'élément inverse du point a est bien sur la courbe
            if(not(Curve.is_on_curve((a.x, -a.y)))):
                reverse_élément_check = False
        i += 1
    return reverse_élément_check
     

# Define a new elliptic curve y^2 = x^3 + 2x + 3
curveS = EllipticNoneFiniteCurve(2, 4)
curveS.generate_one_point_on_curve()
curveS.generate_one_point_on_curve()
curveS.add_point(curveS.addition(curveS.points[0], curveS.points[1]))
curveS.add_point((curveS.points[3].x, -curveS.points[3].y))
curveS.plot_curve(points=curveS.points, x_range=(-10, 10))

#Abélien test
point_is_abélien(curveS)

#curveS.plot_curve(points=curveS.points, x_range=(-10, 10))

curveS = EllipticFiniteCurve(-7,10,97)
curveS.generate_one_point_on_curve()
curveS.generate_one_point_on_curve()
operation = curveS.addition(curveS.points[0], curveS.points[1])
curveS.add_point((operation[0],operation[1]))
curveS.add_point((curveS.points[3].x, -curveS.points[3].y))
curveS.plot_curve(points=curveS.points, x_range=(-10, 10))

point_is_abélien(curveS)