import os
os.system("pip install --upgrade topotoolbox")
import topotoolbox as ttb
import rasterio
import matplotlib.pyplot as plt


# Charger le fichier local
with rasterio.open("MNT.tif") as src:
    dem = src.read(1)
    plt.imshow(dem, cmap='terrain')
    plt.colorbar(label="Altitude (m)")
    plt.title("Modèle Numérique de Terrain (MNT)")
    plt.show()
    
dem=ttb.read_tif("MNT.tif")



eroded=dem.erode((3,3))
dem.plot(cmap='terrain')

plt.figure()
eroded.plot(cmap='terrain')

diff=dem-eroded
plt.figure()
diff.plot(cmap='terrain')