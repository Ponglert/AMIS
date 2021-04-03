import operator
import random
import numpy as np

#Create necessary classes and functions
class Node:
    def __init__(self, id, wp, req, x, y, risk):
        self.id = id
        self.req = req  #ค่าความต้องการ
        self.risk = risk    #ค่าความเสี่ยง
        self.wp = wp
        self.x = x
        self.y = y
    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance
    # getter method
    def get_wp(self):
        return self.wp
    # setter method
    def set_wp(self, wp):
        self.wp = wp
    def __repr__(self):
        return "(" + str(self.id) + "," + str(self.req) + "," + str(self.risk) + "," + "{:.2f}".format(self.wp) +")"

class LocalRoute:
    def __init__(self, route, costlocal, costdis):
        self.route = route
        self.costlocal = costlocal
        self.costdis = costdis
        self.costrisk = route[0].risk
        self.costtotal = costlocal + costdis - self.costrisk
    # getter method
    def get_cost(self):
        return self.costtotal
    # setter method
    def set_cost(self, c):
        self.costtotal = c
    def __repr__(self):
        return "(" + str(self.costlocal) + "," + str(self.costdis) + "," + "{:.2f}".format(self.costtotal) +")"

def getsize(wp,s,c):
    size = 0
    cost = 0
    if wp >= 0.0 and wp <= 0.33:
        size = s[0]
        cost = c[0]
    elif wp >= 0.33 and wp <= 0.67:
        size = s[1]
        cost = c[1]
    elif wp >= 0.67 and wp <= 1:
        size = s[2]
        cost = c[2]
    return size,cost

def routeDistance(route):
    pathDistance = 0
    fromCity = route[0]
    for i in range(1, len(route)):
        toCity = route[i]
        pathDistance += fromCity.distance(toCity)
    return pathDistance


def CreateNode(numNode,bounds_wp):
    # --- Create Node ----------------+
    nodeList = []
    print("ID\tx\ty\tDemand")
    for i in range(0, numNode):
        c = Node(id=i + 1, req=int(random.uniform(10, 30)), wp=float(random.uniform(bounds_wp[0], bounds_wp[1])),
                 x=int(random.random() * 100), y=int(random.random() * 100), risk=int(random.uniform(200, 1500)))
        print("%d\t%.2f\t%.2f\t%.2f" % (c.id, c.x, c.y, c.req))
        nodeList.append(c)
    return nodeList

def InitializePopulation(nodeList, popsize,bounds_wp):
    # --- INITIALIZE A POPULATION  ----------------+
    population = []
    print()
    print("Initialize Population and sort by wp")
    for i in range(0, popsize):
        indv = []
        for j in range(len(nodeList)):
            node = nodeList[j]
            c = Node(id=node.id, req=node.req, wp=float(random.uniform(bounds_wp[0], bounds_wp[1])), x=node.x, y=node.y, risk=node.risk)
            indv.append(c)
        indv_sort = sorted(indv, key=operator.attrgetter("wp"))
        population.append(indv)
        print(indv_sort)
    return population

def DecodePop(population, popsize, size_list, costopen, disperunit):
    # --- DeCode Wp to P-median   ----------------+
    alllocal = []
    allcost = []
    print()
    print("Local Node\tCost_Open\tCost_Distance")
    for i in range(0, popsize):
        pop = sorted(population[i], key=operator.attrgetter("wp"))
        nodelocal_list = []
        print('Population: ', i + 1)
        j = 0
        while j < len(pop):
            size, cost = getsize(pop[j].wp, size_list, costopen)
            route = []
            route.append(pop[j])
            j = j + 1
            while j < len(pop):
                toCity = pop[j]
                if size - toCity.req < 0:
                    break
                else:
                    size = size - toCity.req
                    route.append(toCity)
                    j = j + 1

            costdis = routeDistance(route) * disperunit

            lr = LocalRoute(route=route, costlocal=cost, costdis=costdis)
            nodelocal_list.append(lr)

            print(route, ' ', str(cost), ' ', "{:.2f}".format(costdis) , ' ', route[0].risk)

        fitness = sum(lr1.costtotal for lr1 in nodelocal_list)
        alllocal.append(nodelocal_list)
        allcost.append(fitness) # Fitness Cost
        print('Total Cost: ', "{:.2f}".format(fitness))
    return alllocal,allcost

def DecodeFitness(pop, size_list, costopen,disperunit):
    # --- DeCode Wp to P-median   ----------------+
    pop_sort = sorted(pop, key=operator.attrgetter("wp"))
    nodelocal_list = []
    j = 0
    while j < len(pop_sort):
        size, cost = getsize(pop_sort[j].wp, size_list, costopen)
        route = []
        route.append(pop_sort[j])
        j = j + 1
        while j < len(pop_sort):
            toCity = pop_sort[j]
            if size - toCity.req < 0:
                break
            else:
                size = size - toCity.req
                route.append(toCity)
                j = j + 1

        costdis = routeDistance(route) * disperunit

        lr = LocalRoute(route=route, costlocal=cost, costdis=costdis)
        nodelocal_list.append(lr)


    fitness = sum(lr1.costtotal for lr1 in nodelocal_list)
    return fitness,nodelocal_list

def DecodeFitnessNonSort(pop, size_list, costopen,disperunit):
    # --- DeCode Wp to P-median   ----------------+
    nodelocal_list = []
    j = 0
    while j < len(pop):
        size, cost = getsize(pop[j].wp, size_list, costopen)
        route = []
        route.append(pop[j])
        j = j + 1
        while j < len(pop):
            toCity = pop[j]
            if size - toCity.req < 0:
                break
            else:
                size = size - toCity.req
                route.append(toCity)
                j = j + 1

        costdis = routeDistance(route) * disperunit

        lr = LocalRoute(route=route, costlocal=cost, costdis=costdis)
        nodelocal_list.append(lr)

    fitness = sum(lr1.costtotal for lr1 in nodelocal_list)
    return fitness,nodelocal_list