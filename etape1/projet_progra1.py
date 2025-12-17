# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import rasterio #rasterio est une bibliothèque permettant de manipuler des fichiers d'images géospatiales (ex:MNT)
import matplotlib.pyplot as plt #matplotlib.pyplot est un bibliothèque permettant d'afficher des cartes

fichier = "OrdosLoessPlateau_MNT_SRTM.tif"   #chemin vers le MNT

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
    with rasterio.open(fichier) as src: #ouvre le fichier TIFF (Tagged Image File Format)/ grâce au with le fichier se ferme tout seul après 
        elevation = src.read(1)        #lit la première bande raster (l’altitude)/ stocke les altitudes dans la variable elevation
        
    return elevation #renvoie les données d'altitude

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
    plt.figure(figsize=(8,6)) #crée une image de taille 8x6 pouces
    plt.imshow(data, cmap="terrain") #affiche le tableau d'altitudes comme une image / cmap="terrain" permet d'utiliser une colormap topographique 
    plt.colorbar(label="Altitude (m)") #affiche une légende indiquant la valeur altimétrique
    plt.title("Modèle Numérique de Terrain(MNT)") #aficher un titre à la carte
    plt.show() #afficher la carte
    
data = open_data(fichier) #lit le MNT et stocke les altitudes dans data
affichage (data) #affiche la carte avec les altitudes stockées dans data
