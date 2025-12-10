import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def normaliser_profondeurs(couches_F1, couches_F2, couches_F3):
    depth_min = min(couches_F1[0], couches_F2[0], couches_F3[0])

    def norm(lst):
        return [-(p - depth_min) for p in lst]

    return norm(couches_F1), norm(couches_F2), norm(couches_F3)


def calcul_normal(F1, F2, F3, couches_F1, couches_F2, couches_F3):
    """
    renvoie le produit vectoriel de 2 vecteurs decrivant le plan de la 1ere couche inclinée afin de créer le vecteur orthoganal au plan

    Parameters
    ----------
    F1 : np.array de longueur 2
         Coordonnées du forage 1
    F2 : np.array de longueur 2
         Coordonnées du forage 2
    F3 : np.array de longueur 2
         Coordonnées du forage 3
    couches_F1 : list de longueur 3
        Liste des différentes profondeurs auxquelles les sommets 
        des couches ont été rencontrés par le forage 1
    couches_F2 : list de longueur 3
        Liste des différentes profondeurs auxquelles les sommets 
        des couches ont été rencontrés par le forage 2
    couches_F3 : list de longueur 3
        Liste des différentes profondeurs auxquelles les sommets 
        des couches ont été rencontrés par le forage 3


    """
    P1 = np.array([F1[0], F1[1], couches_F1[0]])
    P2 = np.array([F2[0], F2[1], couches_F2[0]])
    P3 = np.array([F3[0], F3[1], couches_F3[0]])

    v1 = P2 - P1
    v2 = P3 - P1
    return np.cross(v1, v2)


def calcul_coefficients_d(normal, F1, couches_F1):
    ds = []
    for z in couches_F1:
        P = np.array([F1[0], F1[1], z])
        ds.append(-np.dot(normal, P))
    return ds


def profondeur(x, y, couche, normal, ds):
    """
    

    Parameters
    ----------
    x : int
        Coordonnée X choisi par l'utilisateur pour le forage fictif
    y : int
        Coordonnée Y choisi par l'utilisateur pour le forage fictif
    couche : TYPE
        DESCRIPTION.
    normal : TYPE
        DESCRIPTION.
    ds : list de longueur le nombre de couches rencontrées par le forage 
    F1 soit 3
        Calcul les différents coefficients d de l'équation d'un 
        plan du type ax+by+cz+d pour chacun des plans

    """
    a, b, c = normal
    d = ds[couche]
    return -(a*x + b*y + d) / c
    


def visualiser_3D(F1, F2, F3, couches_F1, couches_F2, couches_F3, normal, ds, 
                  x_user, y_user):
    """
    Visualistation 3D des points où les forages ont rencontrés une nouvelle 
    couche géologique et des surfaces correspondant au sommet de la couche 
    géologique

    Parameters
    ----------
    F1 : np.array de longueur 2
         Coordonnées du forage 1
    F2 : np.array de longueur 2
         Coordonnées du forage 3
    F3 : np.array de longueur 2
         Coordonnées du forage 3
    couches_F1 : list de longueur 3
        Liste des différentes profondeurs auxquelles les sommets 
        des couches ont été rencontrés par le forage 1
    couches_F2 : list de longueur 3
        Liste des différentes profondeurs auxquelles les sommets 
        des couches ont été rencontrés par le forage 2
    couches_F3 : list de longueur 3
        Liste des différentes profondeurs auxquelles les sommets 
        des couches ont été rencontrés par le forage 3
    normal : np.ndarray
        tableau numpy correspondant au vecteur du plan de la 
        couche géologique
    ds : list de longueur le nombre de couches rencontrées par le forage 
    F1 soit 3
        Calcul les différents coefficients d de l'équation d'un 
        plan du type ax+by+cz+d pour chacun des plans
    x_user : int
        Coordonnée sur l'axe X à laquelle l'utilisateur souhaite
        réaliser le forage fictif
    y_user : int
        Coordonnée sur l'axe Y à laquelle l'utilisateur souhaite 
        réaliser le forage fictif

    """
    xs = np.linspace(0, 500, 20)
    ys = np.linspace(0, 500, 20)
    X, Y = np.meshgrid(xs, ys)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    
    # Création d'une surface topographique horizontale à l'altitude z = 0
    Z0 = np.zeros_like(X)
    ax.plot_surface(X, Y, Z0, alpha=0.5, facecolor='white', edgecolor='gray')
    
    
    n_couches = len(couches_F1)
    colors = ["red", "orange", "yellow"]

    for i in range(n_couches):
        Z = -(normal[0]*X + normal[1]*Y + ds[i]) / normal[2]
        Z_masked = np.where(Z > 0, np.nan, Z)

        ax.plot_surface(X, Y, Z_masked, alpha=0.4, 
                        color=colors[i % len(colors)])

        ax.scatter(F1[0], F1[1], couches_F1[i], color=colors[i % len(colors)])
        ax.scatter(F2[0], F2[1], couches_F2[i], color=colors[i % len(colors)])
        ax.scatter(F3[0], F3[1], couches_F3[i], color=colors[i % len(colors)])

    # Point choisi par l'utilisateur au niveau de la surface topographique pour
    réaliser le forage fictif
    ax.scatter(x_user, y_user, 0, color='black', s=80, label="Point de sondage 
               fictif")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Modélisation 3D des différentes couches rencontrées par les 
                 forages")
    ax.legend()

    plt.show()


def main():
    F1 = np.array([100, 200])
    F2 = np.array([300, 150])
    F3 = np.array([250, 400])

    couches_F1 = [50, 70, 100]
    couches_F2 = [80, 100, 130]
    couches_F3 = [60, 85, 115]

    couches_F1, couches_F2, couches_F3 = normaliser_profondeurs(couches_F1, 
                                                        couches_F2, couches_F3)

    normal = calcul_normal(F1, F2, F3, couches_F1, couches_F2, couches_F3)
    ds = calcul_coefficients_d(normal, F1, couches_F1)

    x = float(input("Donnez la coordonnée X : "))
    y = float(input("Donnez la coordonnée Y : "))

    print("\n--- Profondeurs au point demandé ---")
    print("Couche horizontale : z = 0 m")
    for i in range(len(couches_F1)):
        z = profondeur(x, y, i, normal, ds)
        print(f"Couche inclinée {i} : z = {z:.2f} m")

    visualiser_3D(F1, F2, F3, couches_F1, couches_F2, couches_F3, normal, ds,
                  x, y)


main()
