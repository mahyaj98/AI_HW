from random import random, choice
from math import *
from time import time
import matplotlib.pyplot as plt


class MaxSAT:
    def __init__(self, n, clauses):
        self.clauses = clauses
        self.n = n

    def max_sat(self, method):

        return {'SA': lambda: self.simulated_annealing(),
                'HC': lambda: self.hill_climbing()
                }[method]()

    @staticmethod
    def evaluate_clause(clause, solution):
        return any([solution[position] == value for position, value in clause])

    def evaluate_cnf(self, solution):
        return sum([self.evaluate_clause(clause, solution) for clause in self.clauses])

    def evaluate_delta(self, solution, i):
        new = [(solution[j] + 1) % 2 if j == i else solution[j] for j in range(self.n)]
        return self.evaluate_cnf(new) - self.evaluate_cnf(solution)

    def simulated_annealing(self):

        max_iterations = 250000
        t0 = 5
        tf = 0.001
        temperature = t0
        iterations = 0
        scores = []
        times = []
        sols = []
        solution = [choice([1, 0]) for _ in range(self.n)]
        score = self.evaluate_cnf(solution)
        time_0 = time()

        while iterations < max_iterations:
            new_solution = [(1 + var) % 2 if random() < 0.01 else var for var in solution]
            new_score = self.evaluate_cnf(new_solution)
            scores.append(new_score)
            times.append(time()-time_0)
            delta = new_score - score
            if delta > 0 or random() < exp(-delta / temperature):
                solution = new_solution
                score = new_score
            iterations += 1
            if score == len(self.clauses):
                return len(self.clauses), solution, scores, times
            temperature = (t0 - tf) / (cosh(10 / max_iterations)) + t0
            sols.append(solution)

        eval_sol = [self.evaluate_cnf(s) for s in sols]
        mm = max(eval_sol)
        j = eval_sol.index(mm)
        return mm, sols[j], scores, times

    def hill_climbing(self):

        scores = []
        times = []
        time_0 = time()
        improves = 0
        x = [choice([1, 0]) for _ in range(self.n)]
        score = self.evaluate_cnf(x)
        scores.append(score)
        times.append(time()-time_0)
        while improves < 100:
            delta = [self.evaluate_delta(x, i) for i in range(self.n)]
            j = delta.index(max(delta))
            if delta[j] > 0:
                x[j] = (x[j] + 1) % 2
                score = self.evaluate_cnf(x)
                if score == len(self.clauses):
                    return len(self.clauses), x, scores, times
                improves = 0
                scores.append(score)
                times.append(time()-time_0)
            else:
                improves += 1
                x = [choice([1, 0]) for _ in range(self.n)]
                score = self.evaluate_cnf(x)
                scores.append(score)
                times.append(time()-time_0)

        return self.evaluate_cnf(x), x, scores, times


def read_data(path):
    f = open(path, 'r')
    variables = []
    clauses = []
    for line in f.readlines():
        var = line.split()
        l = []
        for v in var:
            l.append(((abs(int(v))) - 1, int(v) >= 0))
            variables.append((abs(int(v))))
        clauses.append(l)

    f.close()

    return clauses, max(variables)


if __name__ == '__main__':

    clauses_1027, n_1027 = read_data('Sample/sat1027.txt')
    max_sat_1027 = MaxSAT(n_1027, clauses_1027)

    score_sa_1027, solution_sa_1027, scores_sa_1027, times_sa_1027 = max_sat_1027.max_sat(method='SA')
    print('Simulated Annealing 1027 clauses : ', score_sa_1027, solution_sa_1027)

    clauses_3321, n_3321 = read_data('Sample/sat3321.txt')
    max_sat_3321 = MaxSAT(n_3321, clauses_3321)

    score_sa_3321, solution_sa_3321, scores_sa_3321, times_sa_3321 = max_sat_3321.max_sat(method='SA')
    print('Simulated Annealing 3321 clauses : ', score_sa_3321, solution_sa_3321)

    score_hc_1027, solution_hc_1027, scores_hc_1027, times_hc_1027 = max_sat_1027.max_sat(method='HC')
    print('Hill Climbing 1027 clauses: ', score_hc_1027, solution_hc_1027)

    score_hc_3321, solution_hc_3321, scores_hc_3321, times_hc_3321 = max_sat_3321.max_sat(method='HC')
    print('Hill Climbing 3321 clauses: ', score_hc_3321, solution_hc_3321)

    fig = plt.figure()

    ax_sa_1027 = fig.add_subplot(221)
    ax_sa_1027.scatter(times_sa_1027, scores_sa_1027)
    ax_sa_1027.set_title('Simulated Annealing 1027 clauses')
    ax_sa_3321 = fig.add_subplot(222)
    ax_sa_3321.scatter(times_sa_3321, scores_sa_3321)
    ax_sa_3321.set_title('Simulated Annealing 3321 clauses')
    ax_hc_1027 = fig.add_subplot(223)
    ax_hc_1027.scatter(times_hc_1027, scores_hc_1027)
    ax_hc_1027.set_title('Hill Climbing 1027 clauses')
    ax_hc_3321 = fig.add_subplot(224)
    ax_hc_3321.scatter(times_hc_3321, scores_hc_3321)
    ax_hc_3321.set_title('Hill Climbing 3321 clauses')

    fig.show()

