# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 11:47:55 2025

@author: rayan
"""
import os,csv
from LireCSV import lecture_csv
from pathlib import Path
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
    
print(corriger_chem(chercher_csv("results.csv", Path.home())))


def interface():
    nom_csv = input("Nom du fichier .csv ")
    donn_path = chercher_csv(nom_csv, Path.home())
    donn_path = corriger_chem(donn_path)
    os.chdir(donn_path)
    
    donnees = lecture_csv(nom_csv)
    donn_matrice = np.array(donnees, dtype=object)
    
    print(donn_matrice)
    print(donn_matrice[:, 0])

interface()