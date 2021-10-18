from typing import List
from datadeal.orderAndDriver import Order
from preference.costSaving import cost_saving
from setting import *

def GFRM(orders: List[Order]):
    T = cost_saving(orders)
    M_fair=[]
    # count = 0
    while T:
        compL=[]
        for i in T.keys():
            T[i].sort(key=lambda x: x.save_total, reverse=True)
            compL.append(T[i][0])
        compL.sort(key=lambda x: x.save_total, reverse=True)
        M_fair.append(compL[0])
        del T[compL[0].id]
        try:
            del T[compL[0].match_id]
        except:
            print(compL[0].match_id)
        for pi in T.keys():
            plist = T[pi]
            plist_len = len(plist)
            for k in range(plist_len):
                k = plist_len-k-1 #为防止越界，删除倒着删

                if plist[k].match_id == compL[0].id or plist[k].match_id == compL[0].match_id:
                    del plist[k]

        ls = list(T.keys())

        for pi in ls:
            if len(T[pi]) == 0:
                # count += 1
                del T[pi]

    # import pdb
    # pdb.set_trace()
    return M_fair


if __name__ == '__main__':
    from datadeal.problem import ProblemInstance
    problemInstance = ProblemInstance(data_path, 1000)
    currentTime = problemInstance.startTime+60
    orders, drivers, mapId = problemInstance.batch(currentTime)
    print(GFRM(orders))
