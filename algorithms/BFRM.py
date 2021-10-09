from datadeal.orderAndDriver import Order
from preference.costSaving import cost_saving
from setting import *
import sys
from preference.passenger import Passenger


def getRanking(preference):
    length=max(preference)+1
    rank = [[None for j in range(length)] for i in range(length)]

    for i in preference.keys():
        for j in range(len(preference[i])):
            rank[i][preference[i][j]] = j
    # for i in range(len(rank)):
    #     while None in rank[i]:
    #         rank[i].remove(None)

    return rank


def stable_roommates_phase_1(preference, rank):
    length = max(preference)+1
    proposal = [None for x in range(length)]
    first = [0 for x in range(length)]  # the first element's index of each list
    last = [0 for x in range(length)]
    for x in preference.keys():
        last[x] = len(preference[x])  # the last element's index of each list
    free = [x for x in range(length)]

    while len(free) > 0:
        i = free[0]

        # update first pointer if necessary
        while preference[i][first[i]] == None:
            first[i] = first[i] + 1

        top_pick = preference[i][first[i]]

        # top pick hasn't been proposed to yet, so they accept
        if proposal[top_pick] == None:
            proposal[top_pick] = i  # match i to his top_pick

            match_rank = preference[top_pick].index(i)  # the rank of i in top_pick's preference list

            # all candidates worse than i are rejected, must remove top_pick from their preference list
            for x in range(match_rank + 1, last[top_pick]):
                # import pdb
                # pdb.set_trace()
                reject = preference[top_pick][x]
                preference[reject][rank[reject][top_pick]] = None

                # update last pointer
            last[top_pick] = match_rank  # delete all sucessors of i on top_pick's list, so its length should change
            del free[0]

            continue

        # top pick has been proposed
        curr_match_idx = rank[top_pick][proposal[top_pick]]  # the rank of assigned partner on top_pick's list
        potential_match_idx = rank[top_pick][i]  # the rank of proposing partner on top_pick's list

        if curr_match_idx < potential_match_idx:  # current matching is preferred, i is rejected
            preference[top_pick][potential_match_idx] = None

            first[i] += 1  # start at next spot

            continue
        else:  # accept proposal, so old match has to return to their preference list again
            preference[top_pick][curr_match_idx] = None

            # old match is rejected by top_pick, must update their list
            top_pick_idx = rank[proposal[top_pick]][top_pick]
            preference[proposal[top_pick]][top_pick_idx] = None

            del free[0]
            # add old match to free
            free.insert(0, proposal[top_pick])  # previous partner become free

            proposal[top_pick] = i
            last[top_pick] = potential_match_idx

    return first, last, preference


# delete symmetric pairs
def clean_preferences(first, last, preferences):
    for i in preferences.keys():
        for j in range(len(preferences[i])):
            if j < first[i] or j > last[i]:
                preferences[i][j] = None

    return preferences


def find_second_favorite(i, first, last, pref):
    count = 0
    for j in range(first[i], last[i] + 1):
        if not pref[j] == None:
            count += 1
        elif count == 0:  # pref[j] is empty then move to the next
            first[i] += 1
        if count == 2:
            return pref[j]
    return None


def find_rotation(i, p, q, first, last, preferences):  # p is the preference list of person i
    second_favorite = find_second_favorite(p[i], first, last, preferences[p[i]])
    next_p = preferences[second_favorite][last[second_favorite]]  # next_p is the last one on i's second_favorite's list

    if next_p in p:
        # rotation found!
        j = p.index(next_p)
        q[j] = second_favorite

        return p[j:], q[j:]  # p is X-set, q is Y-set

    q.append(second_favorite)
    p.append(next_p)
    return find_rotation(i + 1, p, q, first, last, preferences)


def eliminate_rotation(p, q, first, last, preferences, rank):
    for i in range(len(p)):
        # q_i rejects p_i so that p_i proposes to q_i+1
        preferences[p[i]][rank[p[i]][q[i]]] = None

        # all successors of p_i-1 are removed from q_i's list, and q_i is removed from their lists
        for j in range(rank[q[i]][p[i - 1]] + 1, last[q[i]]):
            reject = rank[q[i]].index(j)  # preferences[q[i]][j]
            preferences[reject][rank[reject][q[i]]] = None

        last[q[i]] = rank[q[i]][p[i - 1]]


def stable_roommates_phase_2(first, last, preferences, rank):
    while True:
        p, q = None, None
        # find first p_0 to get a rotation from
        # preference list of p_0 must contain at least 2 elements
        for i in preferences.keys():
            if last[i] - first[i] > 0 and find_second_favorite(i, first, last, preferences[i]) != None:
                p, q = find_rotation(0, [i], [None], first, last, preferences)
                break

        if not p and not q:
            return preferences

        # eliminate rotation
        eliminate_rotation(p, q, first, last, preferences, rank)


def match_roommates(preferences):
    rank = getRanking(preferences)
    first, last, preferences = stable_roommates_phase_1(preferences, rank)
    stable_roommates_phase_2(first, last, preferences, rank)
    clean_preferences(first, last, preferences)

    matches = []
    length = len(preferences)
    visited = set()
    i = 0

    for i in range(len(preferences)):
        if not i in visited:
            pair = (i, preferences[i][last[i]])
            visited.add(last[i])
            matches.append(pair)

    return matches

if __name__ == '__main__':
	from datadeal.problem import ProblemInstance
	problemInstance = ProblemInstance(data_path, 1000)
	currentTime = problemInstance.startTime+60
	orders, drivers = problemInstance.batch(currentTime)
	T = cost_saving(orders)
	prefs = {}
	for i in T.keys():
		li = []
		for j in T[i]:
			prefs.setdefault(i,li).append(j.match_id)

	# execute the match!!
	print(match_roommates(prefs))



