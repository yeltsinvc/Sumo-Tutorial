Guide pour le logiciel SUMO
==============

**Table des matières**
1. [Introduction](#introduction)
1. [Installation](#installation)
1. [Liste des outils](#liste-des-outils)
1. [Réseaux de transport](#réseaux-de-transport)
1. [Configuration des carrefours](#configuration-des-carrefours)
1. [Demande de déplacements](#demande-de-déplacements)
1. [Simulation](#simulation)
1. [Collecte de données](#collecte-de-données)
1. [Annexes](#annexes)

 

# Introduction
SUMO, [Simulation of Urban MObility](http://sumo.dlr.de/index.html), is an open source, microscopic, multi-modal traffic simulation tool, which is created by the Institute of Transportation Systems of the German Aerospace Center(DLR). SUMO is purely microscopic: each vehicle is modeled specifically, has its own trajectory and moves individually in the network with SUMO, for example:  
- You can build the network and create routes.
- You can apply a traffic light algorithm.
- You can analyze your simulation result with SUMO.
All its documentations can be found in this [link](http://sumo.dlr.de/wiki).

Before starting doing the assignments and download SUMO packages, create a folder in local memory particularly only for this Tutorial.

# Installation

We need SUMO and Python for this Tutorial.

## Installation of SUMO
SUMO can be installed in Windows, Linux, as well as in Mac-OS. Follow the notices in this  [link](https://www.eclipse.org/sumo/)

## Installation of Anaconda
Anaconda is an open source python platform. Download and install Anaconda for Python 3 version : [Link Anaconda](https://www.anaconda.com/products/distribution).

# Assignment 1: Hello SUMO
This exercise aims at understanding SUMO how we can generate and simulate a traffic scenario.

A SUMO scenario is principally composed of a map (a street network) and traffics (vehicles and their routes). A map could be a real part of city map or a manual created map, represented like a network which consists of nodes (junctions) and edges (streets connecting the junctions). In order to put traffics on a map, we need give the information including the vehicle type, the vehicle trajectory, the number of vehicles.

In this hello assignment, we will simulate a simple scenario. Before doing all steps of this simulation, we create a folder named ’hello’ in the TP folder where we will put all pieces of files.

Note that SUMO read a set of .xml files to do the simulation, composed of information of streets, vehicles, and the traffics and declared as attributes in the corresponding .xml file. In this assignment, we need follow the steps:
- Creation of node file : .nod.xml
- Creation of edge file : .edg.xml
- Creation of network from node file and edge file : .net.xml
- Creation of traffic demands : .rou.xml
- Simulation scenario with SUMO-GUI : .sumocfg

## Generation of SUMO streets network
A network is composed of streets which are structurally built of nodes and edges. A street is composed of at least two nodes and one edge.

Let’s create the first SUMO network :
### Step 1
Create the node file named ”hello/hello.nod.xml”. It contains 2 nodes, in which all nodes are defined by its coordinates (x, y, describing distance to the origin in meters ) and its unique ID name:
```xml
<nodes>
    <node id="1" x="-300.0" y="0.0" />
    <node id="2" x="+300.0" y="0.0" />
</nodes>
```

### Step 2
Then, create the edges file named ”hello/hello.edg.xml”. Note that each edge is unidirectional, directing from one node ID to another node ID. We can define also the number of lanes that the edge has.

```xml
<edges>
    <edge from="1" id="1to2" to="2" numLanes="3"/>
    <edge from="2" id="2to1" to="1" numLanes="2"/>
</edges>
```

### Step 3
Now that we have nodes and edges, we can use a SUMO tool, NETCONVERT, which is used for combining nodes information and edges information, and generating network file where the vehicles can run along. This file is ended by an extention *.net.xml.
Use command lines in following steps to call NETCONVERT and create the network file :

### Step 4 
Open windows command-line interpreter (type CMD in windows research) and go to your folder repertory by the command line : 
```$ cd path_to_folder ```
dfd
