from __future__ import print_function
from random import randint as rand
from tools import generate_blocks, generate_string, merge, overlap, prefix

# reso = overlap(x:="bacbca",y:="cacbc")
# resp = prefix(x,y)
# print("Strings: ", x, y)
# print("prefix: ",resp,"overlap: ",reso)
# reso = overlap(y,x)
# resp = prefix(y,x)
# print("prefix: ",resp,"overlap: ",reso, "\n")
# print("superstring: ", merge(x,y))
blocks = generate_blocks(50)
for string in blocks:
    print(string)

# class GA(object):
#     def __init__(self, s1, s2):
#         self._s1 = s1
#         self._s2 = s2
#         self._chrs = sorted(set(s1 + s2))
#         self._len = len(self._chrs)
#         self._len_lower = min(len(self._s1), len(self._s2))
#         self._len_upper = max(len(self._s1), len(self._s2))

#     def random_char(self):
#         return self._chrs[rand(0, self._len-1)]

#     def random_length(self):
#         return rand(self._len_upper, self._len_lower + self._len_upper)

#     def random_individual(self):
#         return ''.join( [self.random_char() for _ in range(self.random_length())] )

#     def mutate(self, ind):
#         if len(ind) <= 2:
#             return ind
#         ind = list(ind)
#         idx = rand(1, len(ind)-2)
#         ch = self.random_char()
#         # okay ... add, delete, or modify depends on this:
#         left = rand(0,1)
#         right = rand(0,1)
#         return ''.join(
#             ind[:idx - left] +
#             ind[idx - 1 + right:]
#         )

#     def fitness(self, ind):
#         supseq_score = overlap(ind, self._s1)[0] + overlap(ind, self._s2)[0]
#         return -(supseq_score - len(ind)//4)

#     def crossover(self, ind1, ind2):
#         def randelt(a, b):
#             return a if rand(0, 1) else b
#         return ''.join([randelt(ind1[i], ind2[i]) for i in range(min(len(ind1),
#                                                                      len(ind2)))])

#     def run(self, size=100, its=100):
#         pool = [ self.random_individual() for _ in range(size) ]
#         for i in range(its):
#             for i in range(size//2):
#                 pool.append(self.mutate(pool[i]))
#             for i in range(10):
#                 for j in range(10):
#                     if i != j:
#                         pool.append(self.crossover(pool[i], pool[j]))
#             pool = sorted(set([p for p in pool if p]), key=self.fitness)[:size]
#         return pool


# def main(s1, s2):
#     ga = GA(s1, s2)
#     pool = ga.run()
#     for e in pool:
#         print(ga.fitness(e), '\t', e)

# if __name__ == '__main__':
#     from sys import argv
#     if len(argv) != 3:
#         exit('Usage: scs s1 s2')
#     main(argv[1], argv[2])