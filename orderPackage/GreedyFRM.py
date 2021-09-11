from typing import List
from datadeal.orderAndDriver import Order
from preference.costSaving import cost_saving

def GFRM(orders: List[Order]):
    T = cost_saving(orders)
    M_fair=[]
    while len(T)!=0:
        compL=[]
        for i in range(len(T)):
            T[i].sort(key=lambda x: x.save_total)
            compL.append(T[i][0])
        compL.sort(key=lambda x: x.save_total)
        M_fair.append(compL[0])
        for plist in T:
            if plist[0].id == compL[0].id or plist[0].id == compL[0].match_id:
                del plist
            for k in range(len(plist)):
                k = len(plist)-k-1 #为防止越界，删除倒着删
                if plist[k].match_id == compL[0].id or plist[k].match_id == compL[0].match_id:
                    del plist[k]
        while [] in T:
            T.remove([])
    return M_fair



