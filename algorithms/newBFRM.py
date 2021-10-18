import random  # Used in illustrative text case
from preference.preferenceTable import preTable
from setting import *

class UnstableTableError(Exception):
    """ Error for unstable table when no stable pairings are possible. """

#PHASE1
def make_proposals(preferences):
    proposal_record = {}
    proposers = []  # using non-optimal list here to represent priority queue

    # Create list of proposers and empty proposal_record for each
    for participant in preferences:
        proposers.append(participant)
        proposal_record[participant] = ["", ""]

    # breakpoint()
    # to show proposers and empty proposal_record

    while proposers:
        current_proposer = proposers.pop(0)

        # Get current proposer's preference list of proposees
        current_proposer_prefs = preferences[current_proposer][:]

        # Propose to each proposee in order until accepted
        for proposee in current_proposer_prefs:
            proposee_prefs = preferences[proposee]
            current_proposer_ranking = proposee_prefs.index(current_proposer)

            # get proposal_record for proposee and proposer
            proposee_proposal_to, proposee_proposal_from = proposal_record[proposee]
            proposer_proposal_to, proposer_proposal_from = proposal_record[current_proposer]

            # breakpoint()

            # if proposee has not accepted a proposal yet
            if not proposee_proposal_from:
                proposal_record[proposee][1] = current_proposer
                proposal_record[current_proposer][0] = proposee
                break

            # if current proposal is better than accepted proposal
            elif proposee_prefs.index(proposee_proposal_from) > current_proposer_ranking:
                proposal_record[proposee][1] = current_proposer
                proposal_record[current_proposer][0] = proposee

                # Reject previously accepted proposal symmetrically
                # Step 1: reset rejected participant's proposal record
                proposal_record[proposee_proposal_from][0] = ""
                # Step 2: put rejected participant at front of priority queue
                proposers.insert(0, proposee_proposal_from)
                # Step 3: remove rejected pairing symmetrically from the preference list
                preferences[proposee].remove(proposee_proposal_from)
                preferences[proposee_proposal_from].remove(proposee)
                break

            # Otherwise, proposee prefers previously accepted proposal
            else:
                # Update preference lists for rejected proposal
                preferences[proposee].remove(current_proposer)
                preferences[current_proposer].remove(proposee)

    return proposal_record


def is_stable_table(proposal_record):
    proposers = set()
    proposees = set()
    for (proposee, proposer) in proposal_record.values():
        if not proposee or not proposer:
            return False
        if (proposer in proposers) or (proposee in proposees):
            return False

        proposers.add(proposer)
        proposees.add(proposee)

    return True


def remove_trailing_prefs(proposal_record, preferences):
    for proposer in proposal_record:
        proposee = proposal_record[proposer][0]
        proposee_prefs = preferences[proposee]
        proposer_ranking = proposee_prefs.index(proposer)

        successors = proposee_prefs[proposer_ranking+1:]

        # Updated proposee's preferences, removing successors
        preferences[proposee] = proposee_prefs[:proposer_ranking+1]

        # Iterate over successors, deleting proposee from own preference list
        for successor in successors:
            if proposee in preferences[successor]:
                preferences[successor].remove(proposee)

    return preferences

#PHASE2
def get_stable_match(preferences):
    for participant in preferences:
        p = [participant, ]
        q = []

        while len(preferences[participant]) > 1:
            def find_cycle():
                new_q = preferences[p[-1]][1]
                q.append(new_q)
                q_pref_list = preferences[new_q]
                new_p = q_pref_list[-1]

                if new_p in p:
                    p.append(new_p)
                    return

                p.append(new_p)
                find_cycle()

            find_cycle()

            # start at beginning of found cycle, create list representing cycle path
            start = p.index(p[-1])
            cycle = [(p[i + 1], q[i]) for i in range(start, len(p) - 1)]
            # breakpoint()

            # from cycle path, find pairs to remove
            elimination_pairs = find_pairs_to_remove(cycle, preferences)

            try:
                preferences = remove_pairs(elimination_pairs, preferences)
            except UnstableTableError:
                return UnstableTableError

            # reset p and q for next iteration
            p = [participant, ]
            q = []

    return preferences


#Elimination of rotations
def find_pairs_to_remove(cycle, preferences):
    pairs = []
    for i, (_, participant) in enumerate(cycle):
        # grab the preference list for participant
        participant_prefs = preferences[participant]
        # first_pref is a pointer for where to start successors list
        first_pref = cycle[(i - 1) % len(cycle)][0]
        # successors is the tail of the cycle which needs to be removed
        successors = participant_prefs[participant_prefs.index(first_pref) + 1:]
        # breakpoint()

        for successor in successors:
            pair = (participant, successor)
            if pair not in pairs and pair[::-1] not in pairs:
                pairs.append((participant, successor))
    return pairs


def remove_pairs(pairs, preferences):
    for (left, right) in pairs:
        preferences[left].remove(right)
        preferences[right].remove(left)
        if not preferences[left] or not preferences[right]:
            raise UnstableTableError

    return preferences


def find_stable_pairings(preferences):
    proposal_record = make_proposals(preferences)

    if not is_stable_table(proposal_record):
        return UnstableTableError("No stable pairings possible")

    updated_preferences = remove_trailing_prefs(
        proposal_record,
        preferences
    )

    #try:
    return get_stable_match(updated_preferences)
    #except UnstableTableError:
        #return UnstableTableError("No stable pairings possible")

if __name__ == '__main__':
    from datadeal.problem import ProblemInstance
    problemInstance = ProblemInstance(data_path, 1000)
    currentTime = problemInstance.startTime+60
    # orders, drivers = problemInstance.batch(currentTime)
    orders, drivers = problemInstance.batch(currentTime)
    # for k in range(len(orders)):
    #     orders[k].id = curIdMap.index(orders[k].id)
    prefs = preTable(orders)



    # execute the match!!
    print(find_stable_pairings(prefs))