import DataStructure

def two_opt(nodeList,popsize, maxiter,size_list,costopen,bounds_wp,disperunit):
    gen_sol = []
    gen_avg_list = []
    gen_best = 0
    for i in range(1, maxiter + 1):
        print('GENERATION: ', i)
        population = DataStructure.InitializePopulation(nodeList, popsize, bounds_wp)
        if (len(gen_sol) == 0):
            gen_sol = population[0]

        pop = population[0]
        best = pop
        improved = True
        while improved:
            improved = False
            for i in range(1, len(pop) - 2):
                for j in range(i + 1, len(pop)):
                    if j - i == 1: continue  # changes nothing, skip then
                    new_route = pop[:]
                    new_route[i:j] = pop[j - 1:i - 1:-1]  # this is the 2woptSwap

                    score_trial, nodelocal_trial = DataStructure.DecodeFitnessNonSort(new_route, size_list, costopen, disperunit)
                    score_target, nodelocal_target = DataStructure.DecodeFitnessNonSort(best, size_list, costopen, disperunit)

                    if score_trial < score_target:
                        best = new_route
                        improved = True
            pop = best
        score_trial, nodelocal_trial = DataStructure.DecodeFitnessNonSort(best, size_list, costopen, disperunit)
        score_target, nodelocal_target = DataStructure.DecodeFitnessNonSort(gen_sol, size_list, costopen, disperunit)
        if score_trial < score_target:
            gen_sol = best
            gen_best = score_trial
        gen_avg_list.append(gen_best)
        print('      > GENERATION BEST:', gen_best)
        print('         > BEST SOLUTION:', gen_sol, '\n')
    return gen_sol,gen_avg_list



