import random
from mpi4py import MPI

import datetime as datetime
import time
import filecmp
from shutil import copyfile

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
data = 0
count =0
timeout = 5

balance = 500
tout = 5

if rank == 0:
	
	#array for storing latest process to grant request
	

	#recieving request of two process simultaneously	

	req= comm.recv(source=MPI.ANY_SOURCE)
		
	

	#stop working of other process except
	
	
	for j in range(2,size):
		comm.send(balance,dest=j)
		current_time = datetime.datetime.now().time()	 
		with open("/home/mpiusr/store.txt", 'a') as file:
   	       		file.write('\n'+str(rank)+'$'+str(balance)+'$'+current_time.isoformat()+'$prepare')


	for i in range(2,size):
		x = comm.recv(source = i)
		if x == 1 :
			count = count + 1
		else:
			count = 0
	if int(1*2):
		count = count + 1
	a = comm.bcast(count,root = 0)
	
	if a == size-1:
		current_time = datetime.datetime.now().time()	 
		with open("/home/mpiusr/store.txt", 'a') as file:
   	       		file.write('\n'+str(rank)+'$'+str(balance)+'$'+str(current_time)+'$commit')
		print "master updated balance log\n\n\n MASTER FAILED"
		time.sleep(1)
		print "master recovered"   #need to add prepare msg in log, other case of fault
		with open("/home/mpiusr/store.txt",'r') as f: 
			last = None
			for line in (line for line in f if line.rstrip('\n')):
        			last = line
		lines=line.split('$')
		status=lines[3]
		failure_time=(lines[2].replace(":", "")).split('.') 
		if(status=='commit'):			
			current_time = datetime.datetime.now().time()
			current_time = (str(current_time).replace(":", "")).split('.')

			c = int(current_time[0]) - int(failure_time[0])
			print '-----------------------'
			if(c>=timeout):			
				print "timeout crossed"
			else: #comparing timestamps n find differnece then check with timeout-> commit or abort			
				for k in range(1,5):
					comm.send("commit",dest=k)
		
		elif(status=='prepare'):
			for k in range(1,size):
				comm.send("commit",dest=k)
	else:
		print "Aborting at node :",rank

#failure of transaction manager


	
elif rank == 1:
	data="Transaction request"
	comm.send(rank,dest = 0)
	print "node ",rank," send ",data," to node 0"
	

else:
	print "\n",rank,"process working...."
	print "\n",rank,"process not working...."
	x = comm.recv(source=0)
	with open("/home/mpiusr/store.txt", 'a') as file:
			current_time = datetime.datetime.now().time()
   	        	file.write('\n'+str(rank)+'$'+str(balance)+'$'+current_time.isoformat()+'$prepare')
	comm.send(1,dest=0) #prepare msg received 
	
	#assume node fails after going to prepared state and before commit state
	time.sleep(1)
	print "node recovered"   #need to add prepare msg in log, other case of fault
	with open("/home/mpiusr/store.txt",'r') as f: 
		last = None
		for line in (line for line in f if line.rstrip('\n')):
       			last = line
	lines=line.split('$')
	status=lines[3]
	failure_time=(lines[2].replace(":", "")).split('.') 
	if(status=='commit'):			#if node has commited already do nothing		
			print "\n",rank,"process working...."
	elif(status=='prepare'):
		current_time = datetime.datetime.now().time()
		current_time = (str(current_time).replace(":", "")).split('.')

		c = int(current_time[0]) - int(failure_time[0])
		print '-----------------------'
		if(c>=timeout):			
			print "timeout crossed"
		else:
			print "process has recovered and timeout hasnt been passed, notify the master and wait"
						
			
	#completed recovery


	y = comm.recv(source=0)
	if y=="commit":
		current_time = datetime.datetime.now().time()	 
		with open("/home/mpiusr/store.txt", 'a') as file:
   	        	file.write('\n'+str(rank)+'$'+str(balance)+'$'+current_time.isoformat()+'$commit')
		print  "\n"+str(rank)+"commited"


