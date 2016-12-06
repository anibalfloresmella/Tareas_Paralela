from mpi4py import MPI
import random 
import math 
from time import time
#random generar cualquier numero, math para la raiz

def Lista_numero(n):
 #generamos la lista con tamano n  
	lista = [0] *n
#llenar la lista con datos random 
	for i in range(n):
		lista[i]=random.random()
	return lista	    


#coneccion con MPI
comm = MPI.COMM_WORLD 
#defino el valor de la suma de los cuadrados para sacar la varianza total
sumatoria=0.0
#largo de los nodos y el nodo en el que me situo
size = comm.Get_size() 
rank = comm.Get_rank()
#creo una variable para ver si quedan datos afuera de la muestra
pueba=0.0
num=100
suma=0.0
promedio=0.0
root = 0
div_tamano = num/ size
varianza=0.0
lista1=[]
asignacion=0.0
tiempo_inicial=0
tiempo_final=0
tiempo_ejecucion=0

#nos situamos en el nodo maestro que asignamos el nodo 0
if rank == root:
#generamos la lista dentro del nodo maestro
	tiempo_inicial = time() 
	lista1=Lista_numero(num)
	sumas=0.0
	for i in range(num):
		sumas=lista1[i]+sumas
	promedio=sumas/num
	
#envia la lista a todos los nodos desde el nodo maestro. 
lista1 = comm.bcast(lista1,root=root)
#envia la variable primedio a todos los nodos desde el nodo maestro.
promedio = comm.bcast(promedio,root=root)

#damos los rangos que trabajara cada nodo 
for i in range(div_tamano*rank, div_tamano*(rank+1)):
	#Seria la resta al cuadrado del valor de esa posicion con el promedio
	sumatoria=((lista1[i]-promedio)*(lista1[i]-promedio))+sumatoria




#generamos una lista con todos las sumatorias generadas y son enviadas al nodo maestro
sumatoria = comm.gather(sumatoria, root=root)

if rank == root:
	prueba=num-div_tamano*size
	if prueba > 0:
		 for i in range(num-prueba,num):
			asignacion=((lista1[i]-promedio)*(lista1[i]-promedio))+asignacion
#LE asginamos el valor que haya quedado fuera para obtener la varianza	
	varianza=asignacion
	for i in range(size):
#es para mostrar el nodo y la lista con el valor de la sumatoria en cada nodo
		print rank," ",sumatoria[i]
#sumamos la sumatoria de los datos recopilados en cada nodo 
		varianza=sumatoria[i]+varianza
#obtenemos la varianza de las sumas parciales dividiendo por el tamano de la muestra
	varianza=varianza/num
#le aplico la raiz a la varianza para obtener la desviacion estandar
	desviacion_estandar=math.sqrt(varianza)

	print "la varianza es ",varianza
 	print "la desviacion estandar es", desviacion_estandar
	tiempo_final = time() 
 
	tiempo_ejecucion = tiempo_final - tiempo_inicial
 
	print 'El tiempo de ejecucion fue:',tiempo_ejecucion
	

