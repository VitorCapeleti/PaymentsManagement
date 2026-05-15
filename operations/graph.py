import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
class Graph:
    def __init__(self, name: str, xlabel: str, ylabel: str):
        self.name = name
        self.xlabel = xlabel
        self.ylabel = ylabel
        
    def plotLineGraph(self, data):
        sns.set_style('whitegrid')
        plt.figure(figsize=(12,7))
        ax = data.sort_values(ascending = True).plot(kind = "barh", color = "red")
        ax.bar_label(ax.containers[0], padding=3, rotation=45)
        plt.title(self.name, fontsize = 16)
        plt.xlabel(self.xlabel, fontsize = 12)
        plt.ylabel(self.ylabel, fontsize = 12)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return base64.b64encode(buf.getvalue()).decode('utf-8')
    def plotPieGraph(self, data):
        data.sort_values(ascending = True).plot(kind = "pie", autopct = '%1.1f%%', figsize=(6,6), startangle=90)
        plt.title(self.name, fontsize = 16)
        plt.ylabel('')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return base64.b64encode(buf.getvalue()).decode('utf-8')
        