import matplotlib.pyplot as plt
import math
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 100
y1 = [2500760, 2500760, 2500760, 2500760, 2500760, 2500760, 2500759, 2500759, 2500759, 2500759]
y2 = [2699928, 2699927, 2699927, 2699927, 2699928, 2681257, 2563552, 2283991, 2112517, 1866642]
y3 = [2500760, 2500759, 2500759, 2500759, 2500761, 2500759, 2500759, 2500758, 2500759, 2500763]
y4 = [2500727, 2500726, 2500726, 2500881, 2500726, 2500726, 2500732, 2500726, 2500777, 2500849]

# y1 = [math.log(y) for y in y1]
# y2 = [math.log(y) for y in y2]
# y3 = [math.log(y) for y in y3]
# y4 = [math.log(y) for y in y4]

l1 = plt.plot(x, y1, 'r--', label='RoundRobin')
l2 = plt.plot(x, y2, 'g--', label='OLScheduler')
l3 = plt.plot(x, y3, 'b--', label='DepRoute-1')
l4 = plt.plot(x, y3, 'y--', label='DepRoute-2')

plt.plot(x, y1, 'ro-', x, y2, 'g+-', x, y3, 'b^-', x, y4, 'y*-')
plt.title('Node Loads(100 Containers)')
plt.xlabel('Node ID')
plt.ylabel('Loads(Log)')
plt.legend()
plt.show()
