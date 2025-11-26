# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import rasterio
import topotoolbox
import matplotlib.pyplot as plt 


fichier_srtm = "OrdosLoessPlateau_MNT_SRTM.tif"  # ou .hgt

with rasterio.open(fichier_srtm) as src:
    elevation = src.read(1)              # Première bande
    transform = src.transform            # Matrice de transformation
    crs = src.crs                        # Système de coordonnées
    bounds = src.bounds

print("Dimensions :", elevation.shape)
print("CRS :", crs)
print("Emprise :", bounds)


plt.figure(figsize=(8,6))
plt.imshow(elevation, cmap="terrain")
plt.colorbar(label="Altitude (m)")
plt.title("MNT SRTM")
plt.show()

import topotoolbox as ttb  # si ça diffère, indique-moi l’erreur

# Charger le MNT dans un objet topographique
DEM = ttb.DEM(elevation, transform=transform, crs=crs)

# Calcul de la carte de pente
slope = DEM.slope()
plt.figure(figsize=(8,6))
plt.imshow(slope, cmap="viridis")
plt.colorbar(label="Pente (°)")
plt.title("Carte de pente - SRTM")
plt.show()
