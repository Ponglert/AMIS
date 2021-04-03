import random
import copy
import DataStructure

def ensure_bounds(vec, bounds_wp):
    vec_new = []
    # cycle through each variable in vector
    for i in range(len(vec)):

        # variable exceedes the minimum boundary
        if vec[i] < bounds_wp[0]:
            vec_new.append(bounds_wp[0])

        # variable exceedes the maximum boundary
        if vec[i] > bounds_wp[1]:
            vec_new.append(bounds_wp[1])

        # the variable is fine
        if bounds_wp[0] <= vec[i] <= bounds_wp[1]:
            vec_new.append(vec[i])

    return vec_new

def dealgorithm(numNode,population,popsize, mutate, recombination, maxiter,size_list,costopen,bounds_wp,disperunit):
    gen_avg_old = 0
    gen_avg_min = 0.00001
    gen_avg_list = []
    #--- SOLVE --------------------------------------------+

    # cycle through each generation
    for i in range(1,maxiter+1):
        print('GENERATION: ',i)

        gen_scores = [] # score keeping

        # cycle through each individual in the population
        for j in range(0, popsize):

            #--- MUTATION  ---------------------+
            # select three random vector index positions [0, popsize), not including current vector (j)
            canidates = list(range(0, popsize))
            canidates.remove(j)
            random_index = random.sample(canidates, 3)

            x_1_node = population[random_index[0]]
            x_2_node = population[random_index[1]]
            x_3_node = population[random_index[2]]
            x_t_node = population[j]

            x_1 = []
            x_2 = []
            x_3 = []
            x_t = []
            for k in range(0, numNode):
                x_1.append(x_1_node[k].wp)
                x_2.append(x_2_node[k].wp)
                x_3.append(x_3_node[k].wp)
                x_t.append(x_t_node[k].wp)

            # subtract x3 from x2, and create a new vector (x_diff)
            x_diff = [x_2_i - x_3_i for x_2_i, x_3_i in zip(x_2, x_3)]

            # multiply x_diff by the mutation factor (F) and add to x_1
            v_donor = [x_1_i + mutate * x_diff_i for x_1_i, x_diff_i in zip(x_1, x_diff)]
            v_donor = ensure_bounds(v_donor, bounds_wp)

            # --- RECOMBINATION  ----------------+
            updatepop = []
            v_trial = []
            for k in range(len(x_t)):
                p = copy.deepcopy(x_t_node[k])
                crossover = random.random()
                if crossover <= recombination:
                    v_trial.append(v_donor[k])
                    p.wp = v_donor[k]
                else:
                    v_trial.append(x_t[k])
                    p.wp = x_t[k]
                updatepop.append(p)

            # --- GREEDY SELECTION  -------------+

            score_trial,nodelocal_trial = DataStructure.DecodeFitness(updatepop, size_list, costopen, disperunit)
            score_target,nodelocal_target = DataStructure.DecodeFitness(x_t_node, size_list, costopen, disperunit)
            if score_trial < score_target:
                population[j] = updatepop
                gen_scores.append(score_trial)
                print ('   >',score_trial, v_trial)

            else:
                print ('   >',score_target, x_t)
                gen_scores.append(score_target)

        # --- SCORE KEEPING --------------------------------+

        gen_avg = sum(gen_scores) / popsize  # current generation avg. fitness
        gen_best = min(gen_scores)  # fitness of best individual
        gen_sol = population[gen_scores.index(min(gen_scores))]  # solution of best individual

        print('      > GENERATION AVERAGE: ', gen_avg)
        print('      > GENERATION BEST:', gen_best)
        print('         > BEST SOLUTION:', gen_sol, '\n')

        '''''
        if (abs(gen_avg - gen_avg_old) < gen_avg_min):
            break
        '''''

        gen_avg_old = gen_avg
        gen_avg_list.append(gen_avg)

    return gen_sol,gen_avg_list