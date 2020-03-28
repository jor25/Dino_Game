# Genetic Algorithm to manage my nn's. This is borrowed from the genetic algorithm tuning directory.

import numpy as np
import random as rand
import gen_dino_game as gdg
'''
Genetic algorithm class will manage network tuning.
'''
class Gen_alg:
    def __init__(self, pop_size, networks):
        self.pop_num = pop_size #12  # 500               # Population Number
        self.remaining = int(self.pop_num / 2)
        self.gen_num = 100  # Number of generations
        self.mutation_rate = .45  # How likely are we to mutate
        self.mut_val = .50  # How much mutation
        self.chrom_num = 5  # 100                                 # How large is the DNA sequence?
        self.population = networks #[DNA(id, self.chrom_num) for id in range(self.pop_num)]
        self.survivors = np.zeros(self.remaining)  # Survivors per generation

    def check_fitness(self, dinos):  # Take the top half of the population of them
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
            self.cross_over(parents[i], term_ind[i])  # Parent pair and the ID they replace
            # print("****** New_child: {} ******".format(self.population[term_ind[i]].hidden_layers))

        return term_ind, top_dino     # Let me know which ones to update, and the best of the population

    def pair_off(self, surv_index):
        # Pair off the survivors
        par_v1 = np.random.choice(surv_index, size=(int(self.remaining / 2), 2), replace=False)  # Pair off v1
        par_v2 = np.random.choice(surv_index, size=(int(self.remaining / 2), 2), replace=False)  # Pair off v2
        parents = np.concatenate((par_v1, par_v2), axis=0)  # Full pop pairs
        # print("parv1: {}\nparv2: {}\npar_all: {}".format(par_v1, par_v2, parents))    # Verify
        return parents

    def cross_over(self, parents, ch_id):  # Recombine the existing survivors
        parent_1 = self.population[parents[0]].hidden_layers  # Initialize parent 1 np array
        parent_2 = self.population[parents[1]].hidden_layers  # Initialize parent 2 np array
        #'''
        # Merge the survivors at some crossover point - randomly?
        split = int(np.random.uniform(low=1, high=len(parent_1) - 1))   # Choose random point between 1 and parent length
        child = np.hstack([parent_1[:split], parent_2[split:]])         # Take first chunk from parent 1, 2nd chunk parent 2

        #print("Parent_id's: = {}\nParents are: {}, {}\nChild_id: {}\nThe Child: {}".format(parents, parent_1, parent_2, ch_id, child))

        self.population[ch_id].hidden_layers = child    # Check this works outside...
        #'''
        '''
        # Alternate crossover
        for i in range(len(parent_1)):
            self.population[ch_id].hidden_layers[i] = np.random.choice(
                [parent_1[i], parent_2[i]])  # Choose one of these randomly
        child = self.population[ch_id].hidden_layers
        '''
        self.mutation(child, ch_id)

    def mutation(self, child, ch_id):
        # if 1, then we mutate.
        if np.random.choice([0, 1], p=[1 - self.mutation_rate, self.mutation_rate]):

            num_cells = int(np.random.choice(len(child), 1) * self.mutation_rate)  # How many cells to replace, 5%
            mut_ind = np.random.choice(len(child), num_cells, replace=False)  # Choose from these indeces

            for ind in mut_ind:
                self.mut_val = rand.uniform(0, 1)  # Choose how random of a change, percentage
                operation = np.random.choice(['+', '-'])
                if operation == '+':  # Increase by 20%
                    self.population[ch_id].hidden_layers[ind] += int(
                        self.mut_val * self.population[ch_id].hidden_layers[ind])
                    # pass
                else:  # Decrease by 20%
                    self.population[ch_id].hidden_layers[ind] -= int(
                        self.mut_val * self.population[ch_id].hidden_layers[ind])
                    # pass
            #print("{}'s MUTATION: {}".format(ch_id, self.population[ch_id].hidden_layers))
