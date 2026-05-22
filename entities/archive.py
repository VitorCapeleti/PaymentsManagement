import pandas as pd
class Archive:
    def __init__(self, name: str):
        self.name = name
        self.pandasData = pd.DataFrame()
        
    def set_dados(self, dataLine: dict):
        new_data = pd.DataFrame(dataLine)
        new_data['Data'] = pd.to_datetime(new_data['Data'], format='%Y-%m-%d', exact=False)
        if self.pandasData.empty:
            self.pandasData = new_data
        else:
            self.pandasData = pd.concat([self.pandasData, new_data], ignore_index=True)
            self.pandasData['Data'] = pd.to_datetime(self.pandasData['Data'], exact=False)
            self.pandasData['Data'] = self.pandasData['Data'].dt.normalize()
        
    def export_csv_file(self):
        self.pandasData.to_csv(self.name, index=False)
    
    def load_csv_file(self, path):
        self.pandasData = pd.read_csv(path)
        self.pandasData['Data'] = pd.to_datetime(self.pandasData['Data'], format='%Y-%m-%d', exact=False)
    
    def __str__(self):
        return f"Arquivo com o nome: {self.name}, criado!"