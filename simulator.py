"""
Instructions: 
    You will need to use command lines in the terminal to use the program.
    To start enter the following line:
        m = read_map('nyc_map.csv')
    Now you can view the map with the following command:
        m.display()
    To start the infection:
        m.cells[(39,82)].infect()
        m.time_step()
    To see how it progresses re-enter:
        m.time_step()
"""

import random
import math
from matplotlib import pyplot as plt


def normpdf(x, mean, sd):
    """
    Return the value of the normal distribution 
    with the specified mean and standard deviation (sd) at
    position x.
    @This function was provided by Professor Bauer.
    """
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

def pdeath(x, mean, sd):
    start = x-0.5
    end = x+0.5
    step =0.01    
    integral = 0.0
    while start<=end:
        integral += step * (normpdf(start,mean,sd) + normpdf(start+step,mean,sd)) / 2
        start += step            
    return integral    
    
recovery_time = 4  
# number of time-steps to recover.
virality = .5   
# probability that a neighbor cell is infected in each time step.
                                                                

class Cell(object):

    def __init__(self,x, y):
        self.x = x
        self.y = y 
        self.time_infected=0
        self.state = "S" 
        # can be "S" (susceptible), "R" (resistant = dead), or # "I" (infected)
        
    def infect(self):
        self.state="I"
        self.time_infected=0
        
        
    def recover(self):
        self.state="S"
        
    def death(self):
        self.state="R"
        
    def process(self,adjacent_cells):
        if self.state=="I":
            self.time_infected+=1
            mortality= random.random()
            mean= 3
            sd = 1
            p= pdeath(self.time_infected,mean,sd)
           
           

            if self.time_infected==recovery_time:
                self.recover()
                
                
            elif mortality <= p:
                self.death()
            
            else: 
                for cell in adjacent_cells:
                    if cell.state=="S":
                        infection= random.random()
                        if infection<=virality:
                            cell.infect()
        
        else:
            return
    
        
        
class Map(object):
    #Function to build map of New York for CSV data
    def __init__(self):
        self.height = 150
        self.width = 150           
        self.cells = {}

    def add_cell(self, cell):
           self.cells[cell.x,cell.y]=cell 
        
    #Colors each cell based on its current status
    def color_cell(self,cell):
        if cell.state== "S":
            return (0.0,1.0,0.0)
        if cell.state== "R":
            return (0.5,0.5,0.5)
        if cell.state=="I":
            return (1.0,0.0,0.0)
    
    def display(self):
        image= []
        for i in range(150):
            row=[]
            for j in range(150):
                if (i,j) in self.cells:
                    pixel=self.color_cell(self.cells[i,j])
                else:
                    pixel=(0.0,0.0,0.0)
                row.append(pixel)
            image.append(row)
          
        plt.imshow(image)
    #Function finds the adjacent cells for each cell
    def adjacent_cells(self, x,y):
        valid_neighbors=[]
        neighbors=[(x+1,y),(x-1,y),(x,y-1),(x,y+1)]
        for neighbor in neighbors:
            if neighbor in self.cells:
                valid_neighbors.append(self.cells[neighbor])
        return valid_neighbors
    #Used to simulate the next moment in the simulation.
    def time_step(self):
        for (x,y) in self.cells:
            self.cells[x,y].process(self.adjacent_cells(x,y))
        self.display()
            
                
#Gathers data from the CSV to build the map.           
def read_map(filename):
   filename=open(filename,'r')
   m = Map()
   for line in filename:
        line= line.replace(",", " ")
        line= line.split()
        x=int(line[0])
        y=int(line[1])
        new_cell=Cell(x,y)
        m.add_cell(new_cell)
   return m

read_map("nyc_map.csv")
    
    

    
    

    
    # ... Write this function
    
    
