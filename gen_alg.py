# Genetic Algorithm to manage my nn's. This is borrowed from the genetic algorithm tuning directory.
# Random with Choices - https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.random.choice.html
import numpy as np

'''
Genetic algorithm class will manage network tuning.
'''
class Gen_alg:
    def __init__(self, pop_size, networks):
        self.pop_num = pop_size #12  # 500               # Population Number
        self.remaining = int(self.pop_num * .5)#/ 2)
        self.gen_num = 100  # Number of generations
        self.mutation_rate = .20  # How likely are we to mutate
        self.mut_val = .50  # How much mutation
        self.chrom_num = 5  # 100                                 # How large is the DNA sequence?
        self.population = networks #[DNA(id, self.chrom_num) for id in range(self.pop_num)]
        self.survivors = np.zeros(self.remaining)  # Survivors per generation

    def check_fitness(self, dinos, brains):  # Take the top half of the population of them
        '''
        Check the fitness of all the dinosaurs from gen_dino_game
        :param dinos: these are the dinoaurs for the networks
        :return:
        '''

        pop_fits = np.zeros(self.pop_num, dtype=int)  # Holds all fitness values
        pop_ind = 0

        for i, pop in enumerate(self.population):     # Each individual in the population
            fit_score = dinos[i].fitness            # The dino's fitness value
            dinos[i].fitness = 0                    # Reset dinos fitness
            #fit_score = len(fit[0])
            pop.fit_vals.append(fit_score)  # Each population member has a list of their fitnesses
            pop_fits[pop_ind] = fit_score  # Update the pop's score for specific index
            pop_ind += 1  # Increment index
            #print("ID: {}\tFit Score: {}\tDNA: {}".format(pop.mod_id, fit_score, pop.hidden_layers))

        # Merge these two together later
        surv_ind = np.argpartition(pop_fits, -self.remaining)[-self.remaining:]  # Index of the survivors
        top_index = np.argmax(pop_fits[surv_ind])
        top_dino = surv_ind[top_index]
        print("Survivor indexes: {}\tSurv_fit_vals: {}\ttop_dino index: {}\tval: {}".format(surv_ind, pop_fits[surv_ind], top_dino, pop_fits[top_dino]))

        term_ind = np.argpartition(pop_fits, self.remaining)[:self.remaining]  # Index of the terminated
        print("Terminated indexes: {}\tTerm_fit_vals: {}".format(term_ind, pop_fits[term_ind]))

        parents = self.pair_off(surv_ind)
        for i in range(len(parents)):
            # print("****** Old_child: {} ******".format(self.population[term_ind[i]].hidden_layers))
            self.cross_over2(parents[i], term_ind[i], brains)  # Parent pair and the ID they replace
            # print("****** New_child: {} ******".format(self.population[term_ind[i]].hidden_layers))

        return term_ind, top_dino     # Let me know which ones to update, and the best of the population

    def pair_off(self, surv_index):
        # Pair off the survivors
        par_v1 = np.random.choice(surv_index, size=(int(self.remaining / 2), 2), replace=False)  # Pair off v1
        par_v2 = np.random.choice(surv_index, size=(int(self.remaining / 2), 2), replace=False)  # Pair off v2
        parents = np.concatenate((par_v1, par_v2), axis=0)  # Full pop pairs
        # print("parv1: {}\nparv2: {}\npar_all: {}".format(par_v1, par_v2, parents))    # Verify
        return parents

    def cross_over2(self, parents, ch_id, brains):
        parent_1 = brains[parents[0]]   # Initialize parent 1 np array
        parent_2 = brains[parents[1]]   # Initialize parent 2 np array

        #print("Before: {}".format(brains[ch_id]))
        # Basic split
        num_crosses = int(np.random.uniform(low=1, high=int(len(parent_1)/2 - 1)))      # How many times am I swapping
        splits = np.random.choice(len(parent_1)-1, num_crosses, replace=False)      # All the places to split the list
        parts = np.trim_zeros(np.sort(splits))      # Sort and remove Zero from start

        for i, part in enumerate(parts):
            if np.random.choice([1,2]):     # Select a random parent
                parent_x = parent_1
            else:
                parent_x = parent_2

            if i == 0:      # On the first index
                brains[ch_id][0:part] = parent_x[0:part]      # Load the first chunk from parent X
                #brains[ch_id][:split], brains[ch_id][split:] = parent_1[:split], parent_2[split:]   # Set the first & send half
            elif i == len(parts) - 1:       # On the last index
                brains[ch_id][parts[i]:len(parent_x)] = parent_x[parts[i]:len(parent_x)]
            else:           # All our other cases
                brains[ch_id][parts[i-1]:part] = parent_x[parts[i-1]:part]

        #print("After: {}".format(brains[ch_id]))
        self.mutation2(ch_id, brains)

    def mutation2(self, ch_id, brains):
        for i in range(len(brains)):
            # if 1, then we mutate. Random chance of mutation
            if np.random.choice([0, 1], p=[1 - self.mutation_rate, self.mutation_rate]):
                brains[ch_id][i] += np.random.choice(np.arange(-1, 1, step=0.001)) # Set the brain