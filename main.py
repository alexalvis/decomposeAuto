import decompostAutomata
import gridworld
import preprocess
from reachabilityGame import *
from itertools import product
import pickle


NORTH = lambda st: (st[0] - 1, st[1])
NORTH.__name__ = 'North'
SOUTH = lambda st: (st[0] + 1, st[1])
SOUTH.__name__ = 'South'
EAST = lambda st: (st[0], st[1] + 1)
EAST.__name__ = 'East'
WEST = lambda st: (st[0], st[1] - 1)
WEST.__name__ = 'West'
NORTHEAST = lambda st: (st[0] - 1, st[1] + 1)
NORTHWEST = lambda st: (st[0] - 1, st[1] - 1)
SOUTHEAST = lambda st: (st[0] + 1, st[1] + 1)
SOUTHWEST = lambda st: (st[0] + 1, st[1] - 1)
STAY = lambda st: (st[0],st[1])
# Connected-ness Definition
FOUR_CONNECTED = [NORTH, SOUTH, EAST, WEST]                         #: FOUR_CONNECTED = [NORTH, SOUTH, EAST, WEST]
DIAG_CONNECTED = [NORTHEAST, NORTHWEST, SOUTHEAST, SOUTHWEST]             #:
EIGHT_CONNECTED = FOUR_CONNECTED + DIAG_CONNECTED

# Turns
TURN_ROBOT = 'robot'
TURN_ENV = 'env'

def getReachSet(target, dist,length, height):
    res = set()
    for i, j in product(range(length), range(height)):
        if (abs(i - target[0]) + abs(j - target[1])) > dist:
            res.add((target, (i, j)))
    return res
if __name__ == "__main__":
    auto = decompostAutomata.test()
    myobs = []
    length = 11
    height = 11
    mygridWorld = gridworld.gridworld(dim=(11, 11), deterministic=False, r1conn=FOUR_CONNECTED, r2conn=FOUR_CONNECTED, obs=set(myobs))
    grf = mygridWorld.concurrentGraph()
    autoList = auto.decomposeAll()
    finalresult = []
    finalpolicy = []
    finaltarget = []
    for subauto in autoList:
        tempresult = []
        temppolicy = []
        temptarget = []
        resTarget, resDist = preprocess.analyse(subauto)
        # print(resTarget)
        # print(resDist)
        resTargetSet = []
        for i in range(len(resTarget)):
            tempSet = getReachSet(resTarget[i], resDist[i], length, height)
            resTargetSet.append(tempSet)
            print(len(tempSet))
        # input("111")
        for i in range(len(resTargetSet)):
            result, policy = reachability_game_solver(grf, resTargetSet[i], resDist[i], FOUR_CONNECTED, FOUR_CONNECTED, i)
            tempresult.append(result)
            temppolicy.append(policy)
            temptarget.append(resTarget[i])
            filename = "./stochastic/recordReachability/" + str(i) + "/"+ str(resTarget[i]) + ".pkl"
            picklefile = open(filename, "wb")
            pickle.dump(result, picklefile)
            picklefile.close()
        finalresult.append(tempresult)
        finalpolicy.append(temppolicy)
        finaltarget.append(temptarget)

        ##save results


