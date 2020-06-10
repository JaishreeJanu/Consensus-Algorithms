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

balance = 500
flag=0

if rank == 0:
	
	#array for storing latest process to grant request
	

	#recieving request of two process simultaneously	

	req= comm.recv(source=MPI.ANY_SOURCE)
		
	

	#stop working of other process except
	
	
	for j in range(2,5):
		comm.send(str(balance)+"$"+req,dest=j)


	for i in range(2,5):
		x = comm.recv(source = i)
		if x == 1 :
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
		with open("/home/mpiuser/store.txt", 'a') as file:
   	       		file.write('\n'+str(rank)+'$'+str(balance)+'$'+'Timestamp'+current_time.isoformat()+'\n')
		print "master commited"
		for k in range(1,5):
			comm.send("commit",dest=k)
	else:
		print "Aborting at node :",rank

	
elif rank == 1:
	data="Transaction request"
	comm.send("1$10",dest = 0) #add 10 to balance
	print "node ",rank," send ",data," to node 0"
	

else:
	print "\n",rank,"process working...."
	print "\n",rank,"process not working...."
	x = comm.recv(source=0)
	print balance
	bal,opr,amt=x.split('$')
	
	comm.send(1,dest=0) #prepare msg received 
	y = comm.recv(source=0)
	if y=="commit":
		if opr=='1':
			balance = balance+int(amt)
		else:
			balance = balance-int(amt) 
		current_time = datetime.datetime.now().time()	 
		with open("/home/mpiuser/store.txt", 'a') as file:
   	        	file.write('\n'+str(rank)+'$'+str(balance)+'$'+'Timestamp'+current_time.isoformat()+'\n')
		print  "\n"+str(rank)+"commited"






	




