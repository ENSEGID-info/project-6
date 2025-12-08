import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def normaliser_profondeurs(couches_F1, couches_F2, couches_F3):
    depth_min = min(couches_F1[0], couches_F2[0], couches_F3[0])

    def norm(lst):
        return [-(p - depth_min) for p in lst]

    return norm(couches_F1), norm(couches_F2), norm(couches_F3)


def calcul_normal(F1, F2, F3, couches_F1, couches_F2, couches_F3):
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
    a, b, c = normal
    d = ds[couche]
    return -(a*x + b*y + d) / c


def visualiser_3D(F1, F2, F3, couches_F1, couches_F2, couches_F3, normal, ds, x_user, y_user):
    xs = np.linspace(50, 350, 20)
    ys = np.linspace(100, 450, 20)
    X, Y = np.meshgrid(xs, ys)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Couche horizontale à z = 0
    Z0 = np.zeros_like(X)
    ax.plot_surface(X, Y, Z0, alpha=0.6, color='white', edgecolor='gray')

    n_couches = len(couches_F1)
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]

    for i in range(n_couches):
        Z = -(normal[0]*X + normal[1]*Y + ds[i]) / normal[2]
        Z_masked = np.where(Z > 0, np.nan, Z)

        ax.plot_surface(X, Y, Z_masked, alpha=0.4, color=colors[i % len(colors)])

        ax.scatter(F1[0], F1[1], couches_F1[i], color=colors[i % len(colors)])
        ax.scatter(F2[0], F2[1], couches_F2[i], color=colors[i % len(colors)])
        ax.scatter(F3[0], F3[1], couches_F3[i], color=colors[i % len(colors)])

    # POINT DE L'UTILISATEUR : posé sur la couche horizontale z = 0
    ax.scatter(x_user, y_user, 0, color='black', s=80, label="Point entré (sur couche 0)")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z (profondeur)")
    ax.set_title("Modélisation 3D : couches parallèles + couche horizontale")
    ax.legend()

    plt.show()


def main():
    F1 = np.array([100, 200])
    F2 = np.array([300, 150])
    F3 = np.array([250, 400])

    couches_F1 = [50, 70, 100]
    couches_F2 = [80, 100, 130]
    couches_F3 = [60, 85, 115]

    couches_F1, couches_F2, couches_F3 = normaliser_profondeurs(couches_F1, couches_F2, couches_F3)

    normal = calcul_normal(F1, F2, F3, couches_F1, couches_F2, couches_F3)
    ds = calcul_coefficients_d(normal, F1, couches_F1)

    x = float(input("Entrer X : "))
    y = float(input("Entrer Y : "))

    print("\n--- Profondeurs au point demandé ---")
    print("Couche horizontale : z = 0 m")
    for i in range(len(couches_F1)):
        z = profondeur(x, y, i, normal, ds)
        print(f"Couche inclinée {i} : z = {z:.2f} m")

    visualiser_3D(F1, F2, F3, couches_F1, couches_F2, couches_F3, normal, ds, x, y)


main()