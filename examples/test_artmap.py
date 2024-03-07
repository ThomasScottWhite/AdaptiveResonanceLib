import numpy as np
from sklearn.datasets import load_iris, make_blobs
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import umap
import umap.plot
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm


import path
import sys

# directory reach
directory = path.Path(__file__).abspath()

print(directory.parent)
# setting path
sys.path.append(directory.parent.parent)

from elementary.FuzzyART import FuzzyART, prepare_data
from supervised.ARTMAP import SimpleARTMAP

def cluster_iris():
    data, target = load_iris(return_X_y=True)
    print("Data has shape:", data.shape)

    X = prepare_data(data)
    print("Prepared data has shape:", X.shape)

    X_train, X_test, y_train, y_test = train_test_split(X, target, test_size=0.33, random_state=0)

    params = {
        "rho": 0.0,
        "alpha": 0.0,
        "beta": 1.0
    }
    art = FuzzyART(params)

    cls = SimpleARTMAP(art)

    cls = cls.fit(X_train, y_train)

    print(f"{len(np.unique(cls.labels_a))} clusters found")

    _, y_pred = cls.predict(X_test)

    print(classification_report(y_test, y_pred))

    mapper = umap.UMAP().fit(X_test)

    umap.plot.points(mapper, labels=y_pred, color_key_cmap='Paired', background='black')
    umap.plot.plt.show()


def cluster_blobs():
    data, target = make_blobs(n_samples=150, centers=3, cluster_std=0.50, random_state=0, shuffle=False)
    print("Data has shape:", data.shape)

    X = prepare_data(data)
    print("Prepared data has shape:", X.shape)

    params = {
        "rho": 0.8,
        "alpha": 0.0,
        "beta": 1.0
    }
    art = FuzzyART(params)

    cls = SimpleARTMAP(art)

    cls = cls.fit(X, target)
    y = cls.labels_a

    n = len(np.unique(y))

    print(f"{n} clusters found")

    fig, ax = plt.subplots()
    colors = cm.rainbow(np.linspace(0, 1, n))

    for k, col in enumerate(colors):
        cluster_data = y == k
        plt.scatter(X[cluster_data, 0], X[cluster_data, 1], color=col, marker=".", s=10)

    cls.module_a.plot_bounding_boxes(ax, colors)

    plt.show()


def main():
    cluster_iris()
    # cluster_blobs()



if __name__ == "__main__":
    main()