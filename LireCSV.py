# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 16:47:54 2025

@author: rayan
"""
import csv

def lecture_csv(nom_fichier):
    
    """
    Cette fonction ouvre un fichier csv et renvoie les donnees contenu dans le csv.

    Parametres:
    nom_fichier(str): le fichier sous format "Sales_April_2019.csv" par exemple
    Renvoi / Return:
    mon_csv_manipulable(list): liste de liste organisee avec, pour chaque sous liste(=chaque ligne du csv), 
                              Order ID;Product;Quantity Ordered;Price Each;Order Date;Purchase Address). On peut la modifier dans la suite de l'exo.
    """
    
    #ouvrir.
    with open(nom_fichier, newline='') as fichier_csv:
        #lire et stocker dans une variable.
        mon_csv = csv.reader(fichier_csv, delimiter=',') #le delimiter sert a identifier quel caractere separe les elements de la ligne.
        #transformer en une liste de liste
        mon_csv = list(mon_csv)


    #je veux des valeurs distincts
    mon_csv_manipulable = []
    for liste in mon_csv:
        if liste not in mon_csv_manipulable:
            mon_csv_manipulable.append(liste)
    
    #supprimer les lignes inutiles
    vide = ['']*len(mon_csv_manipulable[0])
    if vide in mon_csv_manipulable:
        mon_csv_manipulable.pop(mon_csv_manipulable.index(vide))
        tete = "ID,AgeGroup,BikeTimeConverted,FullName,Gender,Country,EventStatus,FinishRankGender,FinishRankGroup,FinishRankOverall,FinishTimeConverted,RunTimeConverted,SwimTimeConverted,Transition1TimeConverted,Transition2TimeConverted".split(",")
    if tete in mon_csv_manipulable:
        mon_csv_manipulable.pop(mon_csv_manipulable.index(tete))

    return mon_csv_manipulable