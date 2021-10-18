from typing import List
from datadeal.orderAndDriver import Order
from preference.costSaving import cost_saving
from setting import *

def preTable(orders: List[Order]):
    T, relaId = cost_saving(orders)
    # for i in range(len(relaId)):
    #     orders[i].id = relaId.index(orders[i].id)
    # newT, newRelaId=cost_saving(orders)
    for i in T.keys():
        T[i].sort(key=lambda x: x.save_individual, reverse=True)
    prefs = {}
    for i in T.keys():
        li = []
        for j in T[i]:
            prefs.setdefault(relaId.index(i), li).append(relaId.index(j.match_id))
    return prefs


if __name__ == '__main__':
    from datadeal.problem import ProblemInstance
    problemInstance = ProblemInstance(data_path, 1000)
    currentTime = problemInstance.startTime+60
    orders, drivers = problemInstance.batch(currentTime)
    # for k in range(len(orders)):
    #     orders[k].id = curIdMap.index(orders[k].id)
    prefs = preTable(orders)

    # def change_prefs(prefs):
    #     ans = []
    #     count = 0
    #     a2b = {}
    #     b2a = []
    #     for i in prefs.keys():
    #         a2b[i] = count
    #         b2a.append(i)
    #         count += 1
    #     for i in prefs.keys():
    #         tmp = prefs[i]
    #         for j in range(len(tmp)):
    #             tmp[j] = a2b[tmp[j]]
    #         ans.append(tmp)
    #     return ans
    #
    # x = change_prefs(prefs)
    # maxx = 0
    # for i in x:
    #     maxx = max(maxx,max(i))
    # import pdb
    # pdb.set_trace()
    # print(len(x),max(x))
    print(len(prefs),len(orders),max(prefs))