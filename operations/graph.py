import matplotlib.pyplot as plt
import seaborn as sns
class Graph:
    def __init__(self, name: str, xlabel: str, ylabel: str):
        self.name = name
        self.xlabel = xlabel
        self.ylabel = ylabel
        
    def plotLineGraph(self, data):
        sns.set_style('whitegrid')
        plt.figure(figsize=(12,7))
        data.sort_values(ascending = True).plot(kind = "barh", color = "red")
        plt.title(self.name, fontsize = 16)
        plt.xlabel(self.xlabel, fontsize = 12)
        plt.ylabel(self.ylabel, fontsize = 12)
        plt.tight_layout()
        return plt.show()
        