import pandas as pd
class Archive:
    def __init__(self, name: str):
        self.name = name
        self.pandasData = pd.DataFrame()
        
    def set_dados(self, dataLine: dict):
        self.pandasData = pd.concat([self.pandasData, pd.DataFrame(dataLine)], ignore_index=True)
        
    def export_csv_file(self):
        self.pandasData.to_csv(self.name, index=False)
    
    def load_csv_file(self, path):
        self.pandasData = pd.read_csv(path)
    
    def __str__(self):
        return f"Arquivo com o nome: {self.name}, criado!"