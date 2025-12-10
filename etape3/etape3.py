import topotoolbox
import matplotlib.pyplot as plt
import os

# === 1. Charger ton MNT ===
path = "mnt2.tif"
if not os.path.exists(path):
    raise FileNotFoundError(f"Fichier introuvable : {path}")

dem = topotoolbox.read_tif(path)
print("✅ MNT chargé :", dem.shape)

# === 2. Remplir les cuvettes ===
dem_filled = dem.fillsinks()
print("✅ Cuvettes comblées")

# === 3. Créer l'objet de flux ===
fd = topotoolbox.FlowObject(dem_filled)

# === 4. Calculer l’accumulation du flux ===
A = fd.flow_accumulation()
print("✅ Aire de drainage calculée")

# === 5. Calculer la pente ===
S = dem_filled.gradient8(unit='tangent')

# === 6. Simulation d’érosion simplifiée sans accéder à la matrice ===
# Utilisation de la fonction intégrée `erode()` de GridObject
# Ici on utilise un structuring element pour simuler l’érosion morphologique
eroded = dem_filled.erode(size=(12,12))  # petite taille = érosion légère
print("✅ Érosion morphologique appliquée")

# === 7. Affichage ===
plt.figure(figsize=(10,5))
dem_filled.plot(cmap='terrain')
plt.title("MNT initial")

plt.figure(figsize=(10,5))
eroded.plot(cmap='terrain')
plt.title("MNT érodé (méthode TopoToolbox)")

plt.show()