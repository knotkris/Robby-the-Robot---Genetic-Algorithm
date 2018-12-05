import random
from functools import reduce

def randomGenome(length):
    genome = ""
    for i in range(length):
        genome = genome + str(random.randint(0,1))
    return genome

def makePopulation(size, length):
    population = []
    for i in range(size):
        population.append(randomGenome(length))
    return population

def fitness(genome):
    return reduce((lambda x, y: int(x) + int(y)), list(genome))
            
def evaluateFitness(population):
    sums = list(map(lambda x: fitness(x), population))
    return [max(sums), sum(sums)/len(population)]
        
def crossover(genomeOne, genomeTwo):
    #swap strings
    crosspoint = random.randint(0, len(genomeOne)-1)
    genomeA = genomeOne[:crosspoint] + genomeTwo[crosspoint:]
    genomeB = genomeTwo[:crosspoint] + genomeOne[crosspoint:]
    return genomeA, genomeB

def mutate(genome, mutationRate):
    mutant = list(genome)
    for i in range(len(genome)):
        chanceVal = random.randint(1, 1000) * mutationRate
        if chanceVal == 1:
           mutant[i] = str(int(genome[i]) ^ 1)
    result = "".join(mutant)
    return "".join(mutant)

def pickRandomTwo(size):
    first = random.randint(0, size)
    second = random.randint(0, size)
    while(second == first):
        second = random.randint(0, size)
    return (first, second)

def weightedChoice(sumVal, population):
    for i in range(len(population)):
             sumVal = sumVal - fitness(population[i])
             if(sumVal <= 0):
                 return(population[i])
                
def selectPair(population, popSum):
    #roulette wheel algorithm
     chosenSumA, chosenSumB = pickRandomTwo(popSum)
     return (weightedChoice(chosenSumA, population), weightedChoice(chosenSumB, population))

def performCrossover(crossoverRate):
    maxVal = 100
    chanceVal = random.randint(1, maxVal)
    
    return chanceVal <= crossoverRate * maxVal  #70

def runGA(populationSize, crossoverRate, mutationRate, fileName):

    genomeLength = 20
    bestGen = -1
    population = makePopulation(populationSize, genomeLength)
    currentGen = 0
    #ask to save run information
    #if so
    saveRun = 1
    saveFile = open(fileName, 'a')
    saveFile.write("----new run----\n")
    print("Population Size ", populationSize)
    print("Genome Length ", genomeLength)
    
    while(bestGen == -1):
        newGen = []
        highest, avg = evaluateFitness(population)
        
        if(highest == genomeLength):
            bestGen = currentGen

        popSum = sum(list(map(lambda x: fitness(x), population)))
        print("Generation ", currentGen, ": average fitness ", avg, ", best fitness ", highest)
        
        saveFile.write(str("pop " + str(populationSize) + " genLen " + str(genomeLength) + " gen " + str(currentGen) + " avg " + str(avg) + " best " + str(highest)) + "\n")
        
        for i in range(int(populationSize/2)):
            
            newGenomeA, newGenomeB = selectPair(population, popSum)
            
            if(performCrossover(crossoverRate)):
                newGenomeA, newGenomeB = crossover(newGenomeA, newGenomeB)
            
            newGenomeA = mutate(newGenomeA, mutationRate)
            newGenomeB = mutate(newGenomeB, mutationRate)
            
            newGen.append(newGenomeA)
            newGen.append(newGenomeB)
            
        population = newGen
        
        currentGen = currentGen + 1
    if(saveRun == 1):
        saveFile.close()
    return bestGen

bestGens = []
iterations = 5
for i in range(iterations):
    bestGen = runGA(100, 0.7, 0.001, "runs.txt")
    print(bestGen)
    bestGens.append(bestGen)
print(sum(bestGens)/iterations)


'''
population = makePopulation(1000, 10)
popSum = sum(list(map(lambda x: fitness(x), population)))
for i in range(100):
    a, b = selectPair(population, popSum)
    print([a,b])
    print(crossover(a, b))
    print()
'''

    

