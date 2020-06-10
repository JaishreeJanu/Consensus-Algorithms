			
	
import random
from mpi4py import MPI
import datetime
import time
import filecmp
from shutil import copyfile

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
data = 0
count =0
k=0
balance = 500
flag=0
prop = [0]*10
value=0
seq=0
val=[0]*10

	
if rank == 0:	
	req= comm.recv(source=MPI.ANY_SOURCE)
	N=0
	for j in range(2,size):
		comm.send(N,dest=j)
		print "proposer sent "+str(N)
	
		
	for i in range(2,size):
		x = comm.recv(source = i)
		value,seq,y=x.split('$')
		val[k]=value
		k=k+1
		if y == 1 :
			count = count + 1
		else:
			count = 0
	if int(1*2):
		count = count + 1
	a = comm.bcast(count,root = 0)
	if a == size-1:
		opr,amt=req.split('$')
		if opr=='1':
			balance = balance+int(amt)
		else:
			balance = balance-int(amt) 
		current_time = datetime.datetime.now().time()	 
		with open("/home/mpiusr/store.txt", 'a') as file:
   	       		file.write('\n'+str(rank)+'$'+str(balance)+'$'+'Timestamp'+current_time.isoformat()+'\n')
		print "master commited"
		for k in range(1,size):
			comm.send(str(N)+str(val[k])+req,dest=k)
			print "commit request sent"
	else:
		print "Aborting at node :",rank
	N=N+1

	
elif rank == 1:
	data="Transaction request"
	comm.send("1$10",dest = 0) #add 10 to balance
	print "node ",rank," send ",data," to node 0"
	

else:
	print "hii"
	x = comm.recv(source=0)
	print "\nproposer value = "+str(x)+"received"
	for i in range(0,9):
		if prop[i]<x:		
			continue
	if i==9:
		proc[k]=x
		k=k+1
		comm.send(str(value)+str(seq)+1,source=0) #accepted
		print "accepted"+str(x)+"by node"+rank	
	else:
		print "request rejected"
	
	
	
	y = comm.recv(source=0)
	sq,v,opr,amt = y.split('$')
	seq = sq
	value = v
	print "commit request received"
	if opr=='1':
		balance = balance+int(amt)
	else:
		balance = balance-int(amt) 
	current_time = datetime.datetime.now().time()	 
	with open("/home/mpiusr/store.txt", 'a') as file:
   	        file.write('\n'+str(rank)+'$'+str(balance)+'$'+'Timestamp'+current_time.isoformat()+'\n')
		print  "\n"+str(rank)+"commited"






	




