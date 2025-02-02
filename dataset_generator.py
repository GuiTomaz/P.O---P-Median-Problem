import random

def gerar_dataset(num_locais, num_medianas, capacidade_maxima, nome_arquivo):
  dataset = f"{num_locais}\n{num_medianas}\n{capacidade_maxima}\n"
  
  # Gerar a matriz completa
  matriz_distancias = [[0 for _ in range(num_locais)] for _ in range(num_locais)]
  for i in range(num_locais):
    for j in range(i+1):
      if(i != j):
        distancia = random.randint(0, 100)
      else:
        distancia = 0
      matriz_distancias[i][j] = distancia
      matriz_distancias[j][i] = distancia

  
  for linha in matriz_distancias:
    linha_formatada = " ".join(map(str, linha))
    dataset += linha_formatada + "\n"

  with open(nome_arquivo, 'w') as arquivo:
    arquivo.write(dataset)

# Exemplo de uso:
gerar_dataset(100, 10,20, "gen_example4.txt")