from typing import List
import os
from datadeal.orderAndDriver import Order
import numpy as np
from setting import *
from tqdm import tqdm


def ManhaPick2Pick(a:Order, b:Order):
    return abs(a.pickX-b.pickX)+abs(a.pickY-b.pickY)

def ManhaPick2Drop(a:Order, b:Order):
    return abs(a.pickX-b.dropX)+abs(a.pickY-b.dropY)

class myClass:
    def __init__(self, id, match_id, save_total, save_individual):
        self.id = id
        self.match_id = match_id
        self.save_total = save_total
        self.save_individual = save_individual

    def __repr__(self):
        return str(self.id)+' '+str(self.match_id)+' '+str(self.save_total)+' '+str(self.save_individual)+'\n'


def cost_saving(orders: List[Order]):
    # curIdMap = [None for x in range(len(orders))]
    # for i1 in range(len(orders)):
    #     curIdMap[i1] = orders[i1].id
    # for k in range(len(orders)):
    #     orders[k].id = curIdMap.index(orders[k].id)
    curIdmap=[]
    ptable = {}
    for i in tqdm(range(len(orders))):
        key = orders[i].id
        plist = []
        isnull = [True for x in range(len(orders))]
        for j in range(len(orders)):
            if i == j:
                # ptable.setdefault(key, plist).append(myClass(orders[i].id, orders[j].id, 0, 0))
                continue
            if ManhaPick2Pick(orders[i], orders[j])/orders[i].speed < orders[i].maxWait and ManhaPick2Pick(orders[i],orders[j])/orders[j].speed < orders[j].maxWait:
                d1 = ManhaPick2Drop(orders[i], orders[i])
                d2 = ManhaPick2Drop(orders[i], orders[j])
                d3 = ManhaPick2Drop(orders[j], orders[j])
                d4 = ManhaPick2Drop(orders[j], orders[i])
                d_sum = orders[i].absluteDistance + orders[j].absluteDistance
                if d_sum == 0:
                    save_total = 0
                    save_individual = 0
                else:
                    save_total = d_sum - max(d1, d2, d3, d4)
                    save_individual = save_total*(orders[i].absluteDistance/d_sum)

                ptable.setdefault(key, plist).append(myClass(orders[i].id, orders[j].id, save_total, save_individual))
                isnull[i]=False
        if isnull[i]==False:
            curIdmap.append(orders[i].id)
    return ptable, curIdmap





if __name__ == '__main__':
    from datadeal.problem import ProblemInstance
    problemInstance = ProblemInstance(data_path, 1000)
    currentTime = problemInstance.startTime+60
    orders, drivers = problemInstance.batch(currentTime)
    # import pdb
    # pdb.set_trace()
    t,idlist =cost_saving(orders)
    print(len(orders),len(idlist),len(t),max(t))
    for i in t.keys():
        print(i)
    # orders = []
    # with open(data_path, "r", encoding="utf8") as f:
    #     content = f.readline()
    #     while content:
    #         content = content.strip()
    #         order = Order(content)
    #         orders.append(order)
    #         content = f.readline()
    # cost_saving(orders)

    #target_folder = "D:/ExperimentData/new_data/%02d" % month
    #order = Order(content)
    #np.save("D:/ExperimentData/raw_data/%02d.npy" % month, cost_saving(orders))
    #print(cost_saving(orders))
    # with open(target_folder, "w", encoding="utf8") as f:
    #         f.write(cost_saving(order) + "\n")




