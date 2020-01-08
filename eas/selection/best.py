
def best(fitness_list, is_minimal):
    fitness = min(fitness_list) if is_minimal else max(fitness_list)
    return fitness_list.index(fitness)