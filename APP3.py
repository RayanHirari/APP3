# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 11:47:55 2025

@author: rayan,alexis,aymeric,Gaetan,Hugo
"""
import os,csv
from LireCSV import lecture_csv
from pathlib import Path
import Les_3_tri as L3T
from time import time
import numpy as np


def chercher_csv(nom_csv, dossier_depart):
    # Convertit le chemin en objet Path
    dossier = Path(dossier_depart)

    # Recherche récursive dans tous les sous-dossiers
    for fichier in dossier.rglob(nom_csv):
        return fichier.resolve()  # Retourne le chemin complet dès qu'on trouve

    return None  # Si pas trouvé

def corriger_chem(chem):
    chem = str(chem)
    mon_path = ""
    for char in chem:
        if char == "\\":
            mon_path += "/"
        else:
            mon_path += char
    mon_path= mon_path.strip(chem)
    return mon_path
    
#print(corriger_chem(chercher_csv("results.csv", Path.home())))
def temps_en_secondes(temps_str):
    
    """
    Convertit une durée au format 'hh:mm:ss' en secondes.

    Paramètre :
    - temps_str (str) : chaîne de caractères au format "hh:mm:ss"

    Retour :
    - int : le temps total en secondes
    """

    # On sépare les heures, minutes et secondes
    parties = temps_str.split(":")
    heures = int(parties[0])
    minutes = int(parties[1])
    secondes = int(parties[2])

    # On convertit tout en secondes
    total_secondes = heures * 3600 + minutes * 60 + secondes
    return total_secondes



def scores_par_ligne(donnees, colonnes_utiles, poids):

    """
    Calcule la moyenne pondérée ligne par ligne à partir des colonnes choisies.

    Paramètres :
    - donnees : liste de listes (le contenu CSV avec l'en-tête)
    - colonnes_utiles : liste des noms de colonnes à utiliser pour le calcul
    - poids : liste des poids(ponderations) associés à chaque colonne

    Retour :
    - Une liste de moyennes pondérées (une par ligne de données)
    """

    # On récupère l'en-tête
    en_tete = donnees[0]

    # On identifie les positions des colonnes choisies
    indices_colonnes = []
    for nom_colonne in colonnes_utiles:
        for i in range(len(en_tete)):
            if en_tete[i] == nom_colonne:
                indices_colonnes.append(i)

    # Liste pour stocker les résultats
    moyennes = []

    # On parcourt les lignes de données (en sautant l'en-tête)
    for ligne in donnees[1:]:
        total = 0
        somme_poids = 0

        for j in range(len(indices_colonnes)):
            index = indices_colonnes[j]
            poids_colonne = float(poids[j])

            valeur = ligne[index]
            valeur_num = float(temps_en_secondes(valeur))

            total = total + valeur_num * poids_colonne
            somme_poids = somme_poids + poids_colonne

        moyenne = total / somme_poids
        moyennes.append(moyenne)

    return moyennes
def extraire_scores(donnees, index_colonne):
    """
    Extrait une liste de scores (en secondes) à partir d'une liste de listes,
    en utilisant l'index de la colonne qui contient les temps 'hh:mm:ss'.

    Paramètres :
    - donnees : liste de listes (avec ou sans en-tête)
    - index_colonne : index de la colonne à convertir

    Retour :
    - liste d'entiers représentant les temps en secondes
    """

    scores = []
    for ligne in donnees:
        temps_str = ligne[index_colonne]
        score = temps_en_secondes(temps_str)
        scores.append(score)

    return scores

def former_equipes(classement, entete, taille_max=3, par_sexe=False):
    """
    Forme des équipes équilibrées à partir du classement.

    - classement : liste des lignes (sans l'en-tête)
    - entete : liste des noms de colonnes (donnes[0])
    - par_sexe : active ou non la séparation par sexe
    """
    equipes = []

    # Index de la colonne "Gender"
    if par_sexe:
        try:
            index_sexe = entete.index("Gender")
        except ValueError:
            print("⚠️ Erreur : la colonne 'Gender' est introuvable.")
            return []

        hommes = []
        femmes = []

        for participant in classement:
            if participant[index_sexe] == "M":
                hommes.append(participant)
            else:
                femmes.append(participant)

        equipes += former_equipes(hommes, entete, taille_max, False)
        equipes += former_equipes(femmes, entete, taille_max, False)
        return equipes

    # Répartition simple en équipes (par groupe de taille_max)
    i = 0
    while i < len(classement):
        equipe = []
        for _ in range(taille_max):
            if i < len(classement):
                equipe.append(classement[i])
                i += 1
        equipes.append(equipe)

    return equipes

def interface():
    nom_csv = input("Nom du fichier .csv ")
    donn_path = chercher_csv(nom_csv, Path.home())
    donn_path = corriger_chem(donn_path)
    os.chdir(donn_path)
    
    donnes = lecture_csv(nom_csv)
    #donn_matrice = np.array(donnes, dtype=object)
    
    #print(donn_matrice)
    #print(donn_matrice[:, 0])
    
    #choisir la ponderation des 5 temps
    pond = []
    for disci in ["Velo","Nage","Pied","Repos 1", "Repos 2"]:
        pond.append(input("Entrez Les coefficients que vous voulez appliquer sur: "+disci))
    
    #Score par discipline
    choix = input("Calculons le score.Choix de la discipline:Nage(1) / Pied(2) / Velo(3) / Globale(4)")
    if choix =="1":
        score = extraire_scores(donnes[1:], donnes[0].index("SwimTimeConverted"))
    if choix =="2":
        score = extraire_scores(donnes[1:], donnes[0].index("RunTimeConverted"))
    if choix =="3":
        score = extraire_scores(donnes[1:], donnes[0].index("BikeTimeConverted"))
    if choix == "4":
        utile = ["BikeTimeConverted","RunTimeConverted","SwimTimeConverted","Transition1TimeConverted","Transition2TimeConverted"]
        score = scores_par_ligne(donnes,utile,pond)
    
    #Classement
    c = input("Faire le classement avec tri par insertion ou selection? [i / s]: ")
    debut = time()
    if c == "i":
        tri = L3T.tri_insertion(score, donnes[1:])[1]
    elif c == "s":
        tri = L3T.tri_selection(score, donnes[1:])[1]
    else:
        tri = L3T.tri_fusion(score)
    qualif = donnes[0].index("EventStatus")
    classement = []
    for ligne in tri:
        if ligne[qualif]=="Finish":
            print(ligne)
            classement.append(ligne)
    fin = time()
    print(f"\nLe temps d'execution est: {fin-debut} secondes\n")
    
    # Répartition en équipes
    rep = input("Souhaitez-vous former des équipes équilibrées ? [o/n] ")
    if rep.lower() == "o":
        sexe = input("Souhaitez-vous équilibrer aussi par sexe ? [o/n] ")
        par_sexe = sexe.lower() == "o"
        equipes = former_equipes(classement,donnes[0], taille_max=3, par_sexe=par_sexe)

    print("\nÉquipes formées :")
    for idx, equipe in enumerate(equipes):
        print(f"Équipe {idx + 1} :")
        for membre in equipe:
            print("  -", membre)
        print()

    
interface()
