
#"""
def cuenta(t):
    
    tAux=' '.join(t.split())
    cant=len(t)-len(tAux)
    print(len(t),t)
    print(len(tAux),tAux)
    return cant
a='A B C  D son letras'
result=cuenta(a)

print(result)

"""

puntos = [1,1,1,1,1,1,1,1,1,2,2,]
mis_respuestas = [4,3,4,1,3,2,3,2,2,4,3]
corectas = [1,3,4,2,3,3,3,2,2,4,3,]
suma = []
respuestas_correctas = []
print(len(puntos),len(mis_respuestas),len(corectas))
for i in range(len(corectas)):
    if mis_respuestas[i] == corectas[i]:
        suma.append(puntos[i])
        al = f"el EJ {i+1} T"
        respuestas_correctas.append(al)
    else:
        al = f"EJ {i+1} F"
        respuestas_correctas.append(al)

print()
print(sum(suma))
print()
print(respuestas_correctas)

"""