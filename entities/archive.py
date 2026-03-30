class Archive:
    def __init__(self, name: str):
        self.name = name
        self.data = []
        
    def adicionar_dados(self, dataLine: dict):
        self.data.append(dataLine)
    
    def __str__(self):
        return f"Arquivo com o nome: {self.name}, criado!"