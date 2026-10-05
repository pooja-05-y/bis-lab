import math
import random

# 1. SETUP ENVIRONMENT & OBSTACLE
START = (0, 0)
GOAL = (10, 10)
OBSTACLE_CENTER = (5, 5)
OBSTACLE_RADIUS = 2.5
NUM_WAYPOINTS = 3  # Intermediate points along path

# 2. FITNESS FUNCTION
def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def evaluate_path(chromosome):
    # Express phenotype path: START -> Waypoints -> GOAL
    path = [START] + chromosome + [GOAL]
    total_length = 0
    collision_penalty = 0

    for i in range(len(path) - 1):
        p1, p2 = path[i], path[i + 1]
        total_length += distance(p1, p2)

        # Check if segment midpoint collides with obstacle
        mid_x, mid_y = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        if distance((mid_x, mid_y), OBSTACLE_CENTER) <= OBSTACLE_RADIUS:
            collision_penalty += 100  # Heavy penalty for hitting obstacle

    # Higher fitness for shorter, collision-free paths
    return 1 / (total_length + collision_penalty)


# 3. GENETIC ALGORITHM PARAMETERS
POP_SIZE = 40
GENERATIONS = 100
MUTATION_RATE = 0.2

# Initialize random waypoint coordinates
population = [
    [
        (random.uniform(0, 10), random.uniform(0, 10))
        for _ in range(NUM_WAYPOINTS)
    ]
    for _ in range(POP_SIZE)
]

# 4. EVOLUTION LOOP
for _ in range(GENERATIONS):
    fitnesses = [evaluate_path(ind) for ind in population]

    # Selection (Roulette Wheel)
    total_fit = sum(fitnesses)
    probs = [f / total_fit for f in fitnesses]
    parents = random.choices(population, weights=probs, k=POP_SIZE)

    new_population = []
    for i in range(0, POP_SIZE, 2):
        p1, p2 = parents[i][:], parents[i + 1][:]

        # Crossover (Swap waypoints)
        pt = random.randint(1, NUM_WAYPOINTS - 1)
        off1 = p1[:pt] + p2[pt:]
        off2 = p2[:pt] + p1[pt:]

        # Mutation (Slightly shift waypoint coordinates)
        for off in [off1, off2]:
            if random.random() < MUTATION_RATE:
                idx = random.randint(0, NUM_WAYPOINTS - 1)
                off[idx] = (
                    max(0, min(10, off[idx][0] + random.uniform(-1, 1))),
                    max(0, min(10, off[idx][1] + random.uniform(-1, 1))),
                )
            new_population.append(off)

    population = new_population

# 5. OUTPUT BEST PATH
best_chrom = max(population, key=evaluate_path)
best_path = [START] + best_chrom + [GOAL]

print("Optimal Collision-Free Path:")
for i, pt in enumerate(best_path):
    print(f" Point {i}: ({pt[0]:.2f}, {pt[1]:.2f})")
