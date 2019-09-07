import time
import os
import math

# 
CEP_buscado = str(input('Digite o cep para busca: '))

# inicia contagem = time.clock()
f = open('cep_ordenado.dat','r')

#Divide o tamanho do arquivo pelo tamanho da structregistros = (os.path.getsize('cep_ordenado.dat') / 300)

bin_ini = 0
bin_meio = int(math.floor(registros/2))
bin_fim = registros

def ler_cep(index):
    f.seek(290 + (index * 300),0)
    cep = f.read(8)
    return cep

cep_meio = ler_cep(bin_meio)
controle = True
contador = -1
while(controle):
    contador +=1    
    if (cep_meio > CEP_buscado):
        bin_fim = bin_meio
        #bin_meio = int(math.floor((bin_ini + bin_fim)/2)-1)
        bin_meio = int(math.floor((bin_ini + bin_fim)/2))
        cep_meio = ler_cep(bin_meio)
        continue # acho que poderia remover 
    elif(cep_meio < CEP_buscado):
        bin_ini = bin_meio
        #bin_meio = int(math.ceil((bin_fim + bin_meio)/2+1))
        bin_meio = int(math.ceil((bin_fim + bin_meio)/2))
        cep_meio = ler_cep(bin_meio)
        continue        
    if cep_meio == CEP_buscado:
        # Se verdadeiro imprime os dados
        controle = False # poderia remover, mas fica didatico ja que usei no while
            # Endereco - tamanho 72
        f.seek(bni_meio * 300,0)
        endereco = f.read(72)
        print 'Endereco: ' + endereco.strip()
            # Bairro - tamanho 72 + remove espacos
        bairro = f.read(72)
        print 'Bairro: ' + bairro.strip()
            # Cidade - tamanho 72 + remove espacos
        cidade = f.read(72)
        print 'Cidade: ' + cidade.strip()
            # Estado - tamanho 72 + remove espacos
        estado = f.read(72)
        print 'Estado: ' + estado.strip()
            # Sigla - tamanho 2
        sigla = f.read(2)
        print 'sigla: ' + sigla
            # CEP print cep_meio
        print 'CEP: ' + cep_meio
            # numero de iteracoes que o programa levou
        print 'Iteracoes: ' + str(contador)
        break
    if (bin_ini > bin_fim):
        print 'CEP nao encontrado, verifique o CEP'
        break

f.close()
print 'Levou: ' + str(time.clock() - inicio)



