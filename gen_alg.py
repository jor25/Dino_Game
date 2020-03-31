# Genetic Algorithm to manage my nn's. This is borrowed from the genetic algorithm tuning directory.
# Random with Choices - https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.random.choice.html
import numpy as np

'''
Genetic algorithm class will manage network tuning.
'''
class Gen_alg:
    def __init__(self, pop_size, histories, genes):
        self.pop_num = pop_size                         # Population Number
        self.remaining = int(self.pop_num * .4)         # Number of survivors per generation
        self.mutation_rate = .20                        # How likely are we to mutate
        self.potential_mutations = int(genes * .10)     # Take 5% of the genes for potential mutation
        self.population = histories                     # Population
        self.removed = self.pop_num - self.remaining    # Number of dinos that need to be remade

    def check_fitness(self, dinos, brains):  # Take the top percentage of the population
        '''
        Check the fitness of all the dinosaurs from gen_dino_game, collects the top and bottom percentage of population.
        :param dinos: these are the dinoaur player objects
        :param brains: The actual Neural Networks of each of the brains
        :return: terminated indexes and the index of the best dino from the survivors
        '''

        pop_fits = np.zeros(self.pop_num, dtype=int)    # Holds all fitness values

        for i, pop in enumerate(self.population):       # Each individual in the population
            fit_score = dinos[i].fitness                # The dino's fitness value
            dinos[i].fitness = 0                        # Reset dinos fitness
            pop.fit_vals.append(fit_score)              # Each population member has a list of their fitnesses
            pop_fits[i] = fit_score                     # Update the pop's score for specific index

        # Identify who survived the generation and who didn't
        surv_ind = np.argpartition(pop_fits, -self.remaining)[-self.remaining:]     # Index of the survivors
        top_index = np.argmax(pop_fits[surv_ind])                                   # Index of largest from survivors
        top_dino = surv_ind[top_index]                                              # Value of the largest
        if self.pop_num == 1:
            term_ind = np.argpartition(pop_fits, self.remaining)[:self.remaining]   # In case population is just 1
        else:
            term_ind = np.argpartition(pop_fits, self.removed)[:self.removed]       # Index of the terminated

        # Used for DEBUG
        '''
        print("Survivor indexes: {}\tSurv_fit_vals: {}\ttop_dino index: {}\tval: {}".format(
            surv_ind, pop_fits[surv_ind], top_dino, pop_fits[top_dino]))
        print("Terminated indexes: {}\tTerm_fit_vals: {}".format(term_ind, pop_fits[term_ind]))
        '''

        # Pair off survivors given indexes
        parents = self.pair_off(surv_ind)

        # Perform genetic crossover - this is how babies are made...
        for i in range(len(parents)):
            # print("****** Old_child: {} ******".format(self.population[term_ind[i]].hidden_layers))
            self.cross_over(parents[i], term_ind[i], brains)  # Parent pair and the ID they replace
            # print("****** New_child: {} ******".format(self.population[term_ind[i]].hidden_layers))

        return term_ind, top_dino     # Let me know which ones to update, and the best of the population

    def pair_off(self, surv_index):
        '''
        Pair off the indexes of the survivors. Randomly select parents to breed with. May need to check for matching.
        Or just assume single parent can repopulate on its own like a frog.
        :param surv_index: All the indexes of the top percentage of dinos
        :return: 2d numpy array of pairs of parents
        '''
        par_v1 = np.random.choice(surv_index, size=(int(self.remaining / 2), 2), replace=False)  # Pair off v1
        par_v2 = np.random.choice(surv_index, size=(int(self.remaining / 2), 2), replace=False)  # Pair off v2
        parents = np.concatenate((par_v1, par_v2), axis=0)  # Full pop pairs
        # print("parv1: {}\nparv2: {}\npar_all: {}".format(par_v1, par_v2, parents))    # Verify
        return parents  # Give back a 2d array of pairs of parents

    def cross_over(self, parents, ch_id, brains):
        '''
        This is basically where the parents breed to create a new child. Making the baby.
        Initalize the parents and select a random number of times to cross their genetics.
        Cross the weights in each of their neural networks. Then perform mutation.
        :param parents: List of 2 parent dino id's
        :param ch_id: id of the dino they will replace with their offspring
        :param brains: The 2d global numpy array that holds all the weight values
        :return: N/A
        '''
        parent_1 = brains[parents[0]]   # Initialize parent 1 np array
        parent_2 = brains[parents[1]]   # Initialize parent 2 np array

        num_crosses = int(np.random.uniform(low=1, high=int(len(parent_1)/2 - 1)))  # How many times am I swapping
        splits = np.random.choice(len(parent_1)-1, num_crosses, replace=False)      # All the places to split the list
        parts = np.trim_zeros(np.sort(splits))                                      # Sort and remove Zero from start

        for i, part in enumerate(parts):
            if np.random.choice([1,2]):     # Select a random parent
                parent_x = parent_1
            else:
                parent_x = parent_2

            if i == 0:      # On the first index
                brains[ch_id][0:part] = parent_x[0:part]      # Load the first chunk from parent X
            elif i == len(parts) - 1:       # On the last index
                brains[ch_id][parts[i]:len(parent_x)] = parent_x[parts[i]:len(parent_x)]
            else:           # All our other cases
                brains[ch_id][parts[i-1]:part] = parent_x[parts[i-1]:part]

        self.mutation(ch_id, brains)

    def mutation(self, ch_id, brains):
        '''
        Function loops through the brain's genes and selects a percentage with a chance to mutate it by some amount.
        Directly modifies the global brain variable through argument.
        :param ch_id: Integer index of a specific dino brain.
        :param brains: The actual neural network used by the dinos
        :return: N/A
        '''

        # All of the potental indexes to mutate at
        mutation_indexes = np.random.choice(len(brains[ch_id]) - 1, self.potential_mutations, replace=False)

        for i in mutation_indexes:
            # if 1, then we mutate. Random chance of mutation
            if np.random.choice([0, 1], p=[1 - self.mutation_rate, self.mutation_rate]):    # Percent chance of mutation
                brains[ch_id][i] += np.random.choice(np.arange(-1, 1, step=0.001))          # Adjust index weight
