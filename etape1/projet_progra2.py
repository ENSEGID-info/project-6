# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 09:04:04 2025

@author: jmartins007
"""

import rasterio 
import matplotlib.pyplot as plt 
import numpy as np #numpy est une bibliothèque qui permet d'effectuer des calculs sur des tableaux

fichier = "OrdosLoessPlateau_MNT_SRTM.tif"   

def open_data(fichier): #fonction qui prend un fichier.tif en entier 
    '''
   Ouvre un fichier GeoTIFF et extrait la première bande (altitude).

   Parameters
   ----------
   fichier : string
       Chemin vers un fichier TIFF (.tif) contenant un MNT.

   Returns
   -------
   elevation : array
       Tableau NumPy contenant les altitudes du MNT.

    '''
    with rasterio.open(fichier) as src: 
        elevation = src.read(1)        
        
    return elevation

def filtre_altitude(elevation, seuil=1250): #fonction qui applique un filtre pour ne garder que les altitudes inférieures à un seuil de 1250
    '''
    Applique un filtre sur un tableau d'altitudes pour ne conserver que les valeurs inférieures à un seuil donné.

   Parameters
   ----------
   elevation : array
       Tableau NumPy 2D contenant les altitudes du MNT.
   seuil : float, optional (default=1250)
       Valeur seuil d'altitude. Les pixels dont l'altitude est supérieure ou égale à ce seuil seront remplacés par NaN.

   Returns
   -------
   mask : array
       Tableau NumPy 2D de même dimension que `elevation`, où les valeurs supérieures ou égales au seuil sont remplacées par NaN.
      '''
    mask = np.where(elevation < seuil, elevation, np.nan) #test logique pour chaque pixel:si condition vraie alors garde la valeur sinon np.nan permet de rempler par NaN
    
    return (mask) #renvoie le tableau filtré, avec les zones trop élevées remplacées par NaN
    
def affichage(data): #fonction pour afficher les altitudes sous forme d'image
    '''
    Affiche un tableau d'altitudes sous forme de carte colorée.

    Parameters
    ----------
    data : array
        Tableau NumPy contenant les altitudes d'un MNT.

    Returns
    -------
    None.

    '''
    plt.figure(figsize=(8,6)) 
    plt.imshow(data, cmap="terrain")  
    plt.colorbar(label="Altitude (m)") 
    plt.title("Modèle Numérique de Terrain(MNT)") 
    plt.show()
    
data = open_data(fichier) #lit le MNT et stocke les altitudes dans data
data = filtre_altitude(data, 1250) #lit le MNT et stock toutes les altitudes ≥ 1250 m deviennent NaN
affichage (data) #affiche la carte filtrée, montrant uniquement les zones < 1250 m

