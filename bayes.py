
class Die:
    def __init__(self, diegen):
        self.numdict = {}
        for i in diegen:
            self.numdict[i] = self.numdict.get(i, 0) + 1
        
        self.chncs = {}
        for k in self.numdict.iterkeys():
            self.chncs[k] = self.numdict[k] / (len(diegen) * 1.0)
    
    def c(self, num):
        return self.chncs.get(num, 0)
    
    def __str__(self):
        rounded = map(lambda a: (a[0],round(a[1],3)),self.chncs.items())
        return 'Die' + str(rounded)



#@param die_chance: dict, die as key, number of occur in set as val 
def bayes_dice(die_chance, rolled):
    chance_on_die = {}
    for die in die_chance:
#        print die
        chance_on_die[die] = reduce(lambda prod, r: prod * die.c(r), rolled, 1)
    
    chance_of_die = {}
    alloccurs = float(sum(die_chance.values()))
    for die, occurs in die_chance.iteritems():
        chance_of_die[die] = occurs / alloccurs
    
    mults_on_of = { die : chance_on_die[die] * chance_of_die[die] for die in die_chance}
    
    rolled_by_die = {die : mults_on_of[die] / sum(mults_on_of.values()) for die in die_chance}
    return rolled_by_die

if __name__ == '__main__':
    
    rolled = [1, 3, 4, 5, 1, 4, 6, 5, 1, 5, 4, 5]
    d1 = Die(range(1, 7))
    d2 = Die([1, 2, 3, 4, 5, 6, 6])
    d3 = Die([1, 5, 3, 4, 5, 6])
    d4 = Die([1, 5, 3, 4, 5, 5])
    
    d_chcs = {d1:1,
              d2:1,
              d3:1,
              d4:1}
    
    by_die = bayes_dice(d_chcs, rolled)
    for die,chc in by_die.iteritems():
        print die, round(chc,3)
    
    
