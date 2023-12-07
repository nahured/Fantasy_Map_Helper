

class ciudad():
    def __init__(self,tipo,poblacion,area,gobierno):
        self.tipo = tipo
        self.poblacion = poblacion
        self.area = area
        self.gobierno = gobierno
        self.tipo_poblacion = {
            100: "acentamiento pequeño",
            300: "acentamiento",
            500: "acentamiento Grande",
            1_000: "Villa Pequeña",
            3_000: "Villa",
            5_000: "Villa Grande",
            10_000: "Pueblo Pequeña",
            30_000: "Pueblo",
            50_000: "Pueblo Grande",
            100_000: "Ciudad Pequeña",
            300_000: "Ciudad",
            500_000: "Ciudad Grande",
            1_000_000: "Metropolis Pequeño",
            3_000_000: "Metropolis",
            5_000_000: "Metropolis Grande",
            10_000_000: "Megatropolis Pequeña",
            30_000_000: "Megatropolis",
            50_000_000: "Megatropolis grande"
        }
    
    def definir_tipo(self):
        lista = [100,300,500,1_000,3_000,5_000,10_000,30_000,50_000,100_000,300_000,500_000,1_000_000,3_000_000,5_000_000,10_000_000,30_000_000,50_000_000]
        pob2 = max(lista)
        i_2 = 0
        for i,num in enumerate(lista):
            
            pob = num - self.poblacion
            if pob < pob2 and pob > 0:
                pob2 = pob
                i_2 = i

        self.tipo = self.tipo_poblacion[lista[i_2]]

af = ciudad("Na",200_900,83,"merui")

print(af.tipo)

af.definir_tipo()

print(af.tipo)
print()
print(af.poblacion)