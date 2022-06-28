# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 10:43:03 2018

@author: a022927
"""


from __future__ import absolute_import
from __future__ import print_function


import os
import subprocess
import sys
import optparse #Chercher cette bibliothèque elle sert à quoi?
import random
import numpy as np
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', "tools")) # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(os.path.dirname(__file__), "..", "..", "..")), "tools")) # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

#Rediriger le résultat vers un fichier txt
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
        
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

import traci
PORT=8873

def getDistance_driving(origin, destination):
        """ return the distance between two stops 
        (Stop, Stop) -> float"""
        origin_road = origin[0]
        origin_pos = origin[1]
        des_road = destination[0]
        des_pos = destination[1]
        return float(traci.simulation.getDistanceRoad(
            origin_road, origin_pos,
            des_road, des_pos,
            True))

        
def run():
    traci.init(PORT)
    step=0
    
    person_in_car = False
    
    'The person position'
    person_position_x = 4244.71
    person_position_y = 6181.09
    traci.poi.add( 'person_origin', person_position_x, person_position_y, (255,0,0))
    person= traci.simulation.convertRoad(person_position_x,person_position_y,isGeo=True)
    print('person position : ', person)
    person_road = person[0]
    person_pos = (person[1],person[2])
    
    'Destionatin of the demand'
    x_destination = 4340.98
    y_destination = 5985.48
    traci.poi.add( 'person_destination', x_destination, y_destination, (255,0,0))
    destination = traci.simulation.convertRoad(x_destination,y_destination ,isGeo=True)
    destination_road = destination[0]
    destination_pos = (destination[1],destination[2])
    
    while traci.simulation.getMinExpectedNumber()>0:
        traci.simulationStep()#réaliser la simulation pour un timestep
        step+=1
        print("Time in ms:" , traci.simulation.getCurrentTime())
        
        if traci.simulation.getCurrentTime() == 29000:
            """
            A traffic demnad release at 29s
            """
            distance_person2cars = np.zeros(len(traci.vehicle.getIDList()))
            'Find the nearest car'
            for idex_car in np.arange(len(traci.vehicle.getIDList())):
                pos_car_x, pos_car_y = traci.vehicle.getPosition(traci.vehicle.getIDList()[idex_car])
                car_road_pos = traci.simulation.convertRoad(pos_car_x, pos_car_y ,isGeo=True)
                edge_car = car_road_pos[0]
                pos_car = (car_road_pos[1],car_road_pos[2])
                distance_person2cars[idex_car]=traci.simulation.getDistanceRoad(edge_car, pos_car[0], person_road, person_pos[0],True)
            index_min = np.argmin(distance_person2cars)
            id_closest_car = traci.vehicle.getIDList()[index_min]
            'Let the car go to pick up the person'
            print('the nearest car and its route : ')
            print (id_closest_car, traci.vehicle.getRoute(id_closest_car))
            traci.vehicle.changeTarget(id_closest_car,person_road)
            print('Let the car go to pick up the person, new route :')
            print (id_closest_car, traci.vehicle.getRoute(id_closest_car))
            traci.vehicle.setVia(id_closest_car, person_road)
            
            
        if traci.simulation.getCurrentTime() > 29000 :
            if (id_closest_car in traci.vehicle.getIDList()) and not person_in_car:
                pos_car_x, pos_car_y = traci.vehicle.getPosition(id_closest_car)
                car_road_pos = traci.simulation.convertRoad(pos_car_x, pos_car_y ,isGeo=True)
                edge_car = car_road_pos[0]
                pos_car = (car_road_pos[1],car_road_pos[2])

                if (edge_car == person_road):
                    traci.vehicle.setStop(id_closest_car,person_road, person_pos[0], person_pos[1], duration=30)
                    print('the car picks up the person')
                    person_in_car = True
                    traci.vehicle.changeTarget(id_closest_car, destination_road)
                    
                    
        if traci.simulation.getCurrentTime() > 29000 and person_in_car :
            if id_closest_car in traci.vehicle.getIDList() :
                pos_car_x, pos_car_y = traci.vehicle.getPosition(id_closest_car)
                car_road_pos = traci.simulation.convertRoad(pos_car_x, pos_car_y ,isGeo=True)
                edge_car = car_road_pos[0]
                pos_car = (car_road_pos[1],car_road_pos[2])
                if traci.simulation.getDistanceRoad(edge_car, pos_car[0], destination_road, destination_pos[0],True) < 2:
                    print ('Car arrives the destination')

    traci.close()
    sys.stdout.flush()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options
    
if __name__ == "__main__":
    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
        
    sumoProcess = subprocess.Popen([sumoBinary, "-c", "paris.sumocfg", "--tripinfo-output", "tripinfo_1.xml", "--remote-port", str(PORT)])
    list_position = run()
    sumoProcess.wait()
    
