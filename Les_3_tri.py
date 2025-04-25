# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 23:11:17 2025

@author: rayan, alexis, aymeric, gaetan, hugo
"""

def tri_insertion(t, associee):
    j = 2
    while j <= len(t):
        i = j - 1
        k = t[j - 1]
        ligne_k = associee[j - 1]  # On copie aussi l'élément associé
        i -= 1
        while i >= 0 and t[i] > k:
            t[i + 1] = t[i]
            associee[i + 1] = associee[i]  # On décale aussi
            i -= 1
        t[i + 1] = k
        associee[i + 1] = ligne_k
        j += 1
    return t, associee

def tri_selection(t, associee):
    i = 0
    while i < len(t):
        j = i + 1
        min_index = i
        while j < len(t):
            if t[j] < t[min_index]:
                min_index = j
            j += 1
        if min_index != i:
            t[i], t[min_index] = t[min_index], t[i]
            associee[i], associee[min_index] = associee[min_index], associee[i]
        i += 1
    return t, associee

def fusion(gauche, droite):
    # Cas de base : si une des deux listes est vide,
    # on retourne l'autre (elle est déjà triée)
    if gauche == []:
        return droite
    elif droite == []:
        return gauche

    # Cas général : on compare les premiers éléments
    if gauche[0] < droite[0]:
        # On garde l'élément de gauche[0] et on fusionne le reste
        return [gauche[0]] + fusion(gauche[1:], droite)
    else:
        # On garde l'élément de droite[0] et on fusionne le reste
        return [droite[0]] + fusion(gauche, droite[1:])

def tri_fusion(t):
    if len(t) <= 1:
        return t  # Liste déjà triée (ou vide)

    milieu = len(t) // 2
    gauche = tri_fusion(t[:milieu])
    droite = tri_fusion(t[milieu:])

    return fusion(gauche, droite)

print(tri_fusion([7,6,5,4,3,2,1]))
