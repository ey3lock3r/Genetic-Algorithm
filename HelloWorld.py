#Hello World
import random
import copy
import matplotlib.pyplot as plt
#%matplotlib inline

alpha = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwzyz" #52
target = "Hello World"
generations = []
pop_size = 1024
max_gen = 2048
mate_factor = 512

#print(alpha[0])
#print(alpha[random.randrange(0,52)])
def initialize_population():
    initial_population = []
    generation = []
    temp_str = []
    for i in range(pop_size):
        for j in range(len(target)):
            temp_str.append(alpha[random.randrange(0,53)])
        #print(temp_str)
        initial_population.append(temp_str)
        print(temp_str)
        temp_str = []

    for chromosome in initial_population:
        generation.append({
            "generation":0,
            "fitness": calculate_chromosome_fitness(chromosome),
            "chromosome": chromosome,
            "active": True
        })
    return generation

def calculate_chromosome_fitness(chromosome):
    fitness = 0
    #print(chromosome)
    for a, b in zip(''.join(map(str,chromosome)),target):
        #print(a + " " + b + ": " + str(ord(a)) + " - " + str(ord(b)) + " = " + str(ord(a) - ord(b)))
        fitness += abs(ord(a) - ord(b))
    
    #fitness = abs(fitness)
    #print("Fitness: " + str(fitness))
    return fitness

def get_current_generation(generations, generation_num):
    # Get only the chromosomes in this generation
    generation = list(filter(lambda k: k['generation'] == generation_num, 
                             generations))
    return sorted(generation, key=lambda k: k['fitness'])

def copy_fit_chromo_2next(generation, generations, itir):
    """
    Copy the surviving chromosomes in generation to a
    new generation and append this new generation to
    our generations list.
    """
    new_generation = copy.deepcopy(generation)

    for i in range(-itir, 0):
        new_generation[i]['active'] = False

    active = list(filter(lambda k: k['active'] == True, new_generation))
    for chromosome in active:
        chromosome['generation'] += 1

    generations.extend(active)
    return generations

def mate_chromosomes(generation, generations, generation_num, itir):
    """
    Mate the two most fit chromosomes and add their
    children to the generation.
    """
    for i in range(0,itir):
        child = recombine(generation, itir)
        child = mutate_chromosome(child)
        generations.append({
            "active": True,
            "chromosome": child,
            "generation": generation_num + 1,
            "fitness": calculate_chromosome_fitness(child)
        })
    return generations

def recombine(generation, itir):
    idx1 = random.randrange(0,itir)
    while True:
        idx2 = random.randrange(0,itir)
        if idx2 != idx1:
            break

    mother = generation[idx1]['chromosome']
    father = generation[idx2]['chromosome']

    pivot = random.randint(0, len(mother) - 1)
    child = mother[:pivot] + father[pivot:]
    return child

def mutate_chromosome(chromosome):
    first = random.randrange(0, len(chromosome), 1)
    second = random.randrange(0, len(chromosome), 1)

    chromosome[first]  = alpha[random.randrange(0,53)]
    chromosome[second] = alpha[random.randrange(0,53)]
    
    return chromosome

def show_result(generation, most_fit_list):
    max_fitness = generation[0]['fitness']
    most_fit_list.append(max_fitness)
    fittest_chromosome = generation[0]['chromosome']
    return most_fit_list, fittest_chromosome, max_fitness

def evolve(generations):
    max_fitness = None
    fittest_chromo = None
    most_fit_list = []

    for generation_num in range(max_gen):
        if max_fitness == 0:
            break
        
        current_generation = get_current_generation(generations, generation_num)
        generations = copy_fit_chromo_2next(current_generation, generations, mate_factor)
        generations = mate_chromosomes(current_generation, generations, generation_num, mate_factor)
        most_fit_list, fittest_chromo, max_fitness = show_result(current_generation, most_fit_list)
        print("Generation " + str(generation_num) + ": Fitness = " + str(max_fitness) + " Fittest Chromo = " + str(fittest_chromo))

    generation = list(filter(lambda k: k['generation'] == max_gen-1, 
                             generations))
    for chromosome in generation:
        print(chromosome['chromosome'])

    plt.plot(most_fit_list)
    plt.title("Most Fit Trend")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.show()

generations = initialize_population()
evolve(generations)
#print(ord(''.join(map(str,initial_population[0]))))