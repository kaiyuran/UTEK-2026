import matplotlib.pyplot as plt

def plot(xyLists):
    for i, xyList in enumerate(xyLists):
        x = [coord[0] for coord in xyList]
        y = [coord[1] for coord in xyList]
        plt.plot(x, y, marker='o', label=f'Droid {i+1}')
    plt.legend()
    return plt