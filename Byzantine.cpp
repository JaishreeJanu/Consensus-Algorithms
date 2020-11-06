 /* *   Program to implement Byzantine protocol
 *   using mpi
 * */

#include <iostream>
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <vector>
#include <math.h>
#include <unistd.h>
using namespace std;
MPI_Request send_request,recv_request;
    int world_size;
    int tag=200;
void distributeValues(int , int , int);
void receiveValues(int , int ,int [] , int);
void receiveVector(int , int ,int [] , int,vector< vector<int> >&);
void distributeVector(int , int , int ,int [],vector< vector<int> >& );
void check(vector< vector<int> > &,int , int ,int []);
void display(vector< vector<int> > &,int );
int glob=1;
int main(int argc, char** argv) {
		// Initialize the MPI environment
		MPI_Init(NULL, NULL);

		// Get the number of processes

		MPI_Comm_size(MPI_COMM_WORLD, &world_size);

		// Get the rank of the process
		int world_rank;
		
		MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
		
		int inBuffer[world_size];
		
		//int vectorBuffer[world_size][world_size];
		
		vector<vector<int> > vectorBuffer;
		
		int detect[world_size];
		
		vectorBuffer.resize(world_size);
		
		for (int i = 0; i < world_size; ++i)
		{
		
		vectorBuffer[i].resize(world_size);
	    
	    }
        // Get the name of the processor
        
         vector<vector<int> > vectorDetect;
	    
	         vectorDetect.resize(world_size);
        
        for (int i = 0; i < world_size; ++i)
        {
         
             vectorDetect[i].resize(world_size);
         }
		
		char processor_name[MPI_MAX_PROCESSOR_NAME];
		
		int name_len;
		
		MPI_Get_processor_name(processor_name, &name_len);
		
		for(int i=0;i<world_size;i++)
			{
				distributeValues(world_rank,world_size,i);
				// MPI_Barrier(MPI_COMM_WORLD);
				receiveValues(world_rank,world_size,inBuffer,i);
			}
	 
	    
	    MPI_Barrier(MPI_COMM_WORLD);
		
		for(int i =0;i<world_size;i++)
			{
				MPI_Barrier(MPI_COMM_WORLD);
				distributeVector(world_rank,world_size,i,inBuffer,vectorBuffer);
				//receiveVector(world_rank,world_size,inBuffer,i,vectorBuffer);
			}
        
        MPI_Barrier(MPI_COMM_WORLD);
		
		for(int i =0;i<world_size;i++)
			{
				MPI_Barrier(MPI_COMM_WORLD);
				// distributeVector(world_rank,world_size,i,inBuffer,vectorBuffer);
				receiveVector(world_rank,world_size,inBuffer,i,vectorBuffer);
			}	
     
		MPI_Barrier(MPI_COMM_WORLD);
		
		MPI_Barrier(MPI_COMM_WORLD);
		display(vectorBuffer,world_size);
		//Just Checking the lier note
		if(world_rank!=0 && world_rank < 3)
		{
			for(int i=1;i<world_size;i++)
			{
			vectorBuffer[i][1]=rand()%10;
			vectorBuffer[i][3]=rand()%10;
		    }
		}
		check(vectorBuffer,world_rank,world_size,detect);
        MPI_Barrier(MPI_COMM_WORLD);
         
		if(world_rank!=0)
			{ 
				MPI_Isend(detect,world_size,MPI_INT,0,999,MPI_COMM_WORLD,&send_request);
				for(int i=0;i<world_size;i++)
				{
					//cout<<detect[i]<<"  ";
				}
				//cout<<"from :"<<processor_name<<endl;
				//cout<<endl;
			}
	   MPI_Barrier(MPI_COMM_WORLD);
	   if(world_rank==0)
			{
				
				//cout<<"from :"<<processor_name<<endl;
				int tempVector[world_size];
				for(int j=0;j<world_size;j++)
				{
			     	vectorDetect[0][j]=detect[j];
				}
				for(int i=1;i<world_size;i++)
				{
			  
			   
						MPI_Irecv(tempVector,world_size, MPI_INT,i,999,MPI_COMM_WORLD,&recv_request);
						for(int j=0;j<world_size;j++)
							{   
								   // cout<<tempVector[j]<<" ";
									vectorDetect[i][j]=tempVector[j];
							}
					
				}
	                
			}
	    
		MPI_Barrier(MPI_COMM_WORLD);
	   
	   if(world_rank==0)
			{
				int traitor[world_size];
		        cout<<"from :"<<processor_name<<endl;
				display(vectorDetect,world_size);
		        for ( int i =0;i<world_size;i++)
		        {
					for(int j=0;j<world_size;j++)
					{
						
						if(vectorDetect[j][i]==1)
						{
							traitor[i]=1;
						}
						
						
					   
					}
				}
		        int count =0;
		        for(int i=0;i<world_size;i++)
		        {
					if(traitor[i]==1)
					{
						count++;
						cout<<i<<" is traitor"<<endl;
					}
				}
				if(count<(world_size/2))
				{
					cout<<"consensus reached"<<endl;
				}
				else
				{
					 cout<<"Consensus Not reached"<<endl;
				}
		   
			}
	   
		MPI_Finalize();
		exit(0);
}
	void check(vector< vector<int> > &vectorBuffer,int world_rank, int world_size,int detect[])
	{
		int changed;
		 int j=0;
	      for(int i=0;i<world_size;i++)
	      {
			  changed=0;
			  int check=vectorBuffer[0][i];
			  for(int j=0;j<world_size;j++)
			  {
				  if(check!=vectorBuffer[j][i])
				  {
					    changed=1;
				  }
			  }
			  if(changed!=0)
			  {
				  detect[i]=1;
			  }
			  else
			  {
			   
			     detect[i]=0;
			 }
		  }
	}
	void display(vector< vector<int> > &vectorBuffer,int world_size)
	{
		cout<<"-------------------------------------------------------";
		cout<<endl;
		cout<<"in the display"<<endl;
		cout<<"-------------------------------------------------------"<<endl;
		for(int i=0;i<world_size;i++)
		{
			for(int j=0;j<world_size;j++)
			{
			  cout<<vectorBuffer[i][j]<< "  " ;
			}
		     cout<<endl;
		}
	    cout<<endl;
	    cout<<"---------------------------------------------------------"<<endl;
	   
	}
void distributeVector(int world_rank,int world_size,int i,int inBuffer[],vector< vector<int> > &vectorBuffer)
{
	
	                            int tempVector[world_size];
	                      
								//MPI_Send(inBuffer,world_size,MPI_INT,i,i,MPI_COMM_WORLD);
		                   
                         
                                MPI_Isend(inBuffer,world_size,MPI_INT,i,tag,MPI_COMM_WORLD,&send_request);
					           
             
         
	
	
	
}
void distributeValues(int world_rank,int world_size,int i)
{
	int val;
	
	
		
		 
             val =rand()%100;
             
			//cout<<val<<" ";
			 if(world_rank!=1)
			 MPI_Isend(&val,1,MPI_INT,i,i,MPI_COMM_WORLD,&send_request);
            // cout<<val<<" ";
          
		 
		
    
    
	
	
	
	
	
}
void receiveValues(int world_rank,int world_size,int inBuffer[],int i)
{
	
	//inBuffer[world_rank]=99999;
	

		 
			 int val;
			    
		    	MPI_Irecv(&val,1, MPI_INT,i,i,MPI_COMM_WORLD,&recv_request);
		    	//cout<<val<<" ";
                inBuffer[i]=val;
               
               
		 
		
    
    
	
	
	
	
	
}


void receiveVector(int world_rank,int world_size,int inBuffer[],int i,vector< vector<int> > &vectorBuffer)
{
	     
	
	           
                   int tempVector[world_size];
                   
		          //MPI_Barrier(MPI_COMM_WORLD);
			      
		    	  // MPI_Recv(tempVector,world_size, MPI_INT,i,i,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
		             MPI_Irecv(tempVector,world_size, MPI_INT,i,tag,MPI_COMM_WORLD,&recv_request);
                   for(int j=0;j<world_size;j++)
					{
					  //cout<<tempVector[j]<<" ";
				   
						vectorBuffer[i][j]=tempVector[j];
				      
					}
                     
                     
	                
	              
	              
	
	
	
}

