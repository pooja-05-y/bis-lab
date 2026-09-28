import random

# 1. Define the Objective Function (Revenue)
def calculate_revenue(price):
    demand = 101 - price
    return price * demand

# Hyperparameters
POPULATION_SIZE = 20
GENERATIONS = 50
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8
PRICE_MIN = 1
PRICE_MAX = 100

# 2. Create Initial Population
population = [random.randint(PRICE_MIN, PRICE_MAX) for _ in range(POPULATION_SIZE)]

best_price = None
best_revenue = 0

# Main Genetic Algorithm Loop
for gen in range(GENERATIONS):
    # 3. Evaluate Fitness
    fitness = [calculate_revenue(price) for price in population]

    # Update Best Solution Found So Far
    gen_max_revenue = max(fitness)
    if gen_max_revenue > best_revenue:
        best_revenue = gen_max_revenue
        best_price = population[fitness.index(gen_max_revenue)]

    # 4. Selection
    total_fitness = sum(fitness)
    probabilities = [f / total_fitness for f in fitness]

    new_population = []
    for _ in range(POPULATION_SIZE):
        parents = random.choices(population, weights=probabilities, k=2)
        parent1, parent2 = parents[0], parents[1]

        # 5. Crossover
        if random.random() < CROSSOVER_RATE:
            offspring = int((parent1 + parent2) / 2)
        else:
            offspring = parent1 if random.random() < 0.5 else parent2

        # 6. Mutation
        if random.random() < MUTATION_RATE:
            offspring = random.randint(PRICE_MIN, PRICE_MAX)

        new_population.append(offspring)

    population = new_population

# Output Results
print(f"Optimal Price (x): ${best_price}")
print(f"Maximum Daily Revenue f(x): ${best_revenue}")
