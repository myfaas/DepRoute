import matplotlib.pyplot as plt
x = [100, 200, 300, 400]

# y1 = [0.175, 0.263, 0.316, 0.351]
# y2 = [0.157, 0.277, 0.365, 0.431]
# y3 = [0.612, 0.742, 0.784, 0.795]
# y4 = [0.629, 0.831, 0.882, 0.882]

y1 = [0.202, 0.315, 0.395, 0.456]
y2 = [0.184, 0.33, 0.444, 0.537]
y3 = [0.638, 0.795, 0.863, 0.901]
y4 = [0.655, 0.884, 0.961, 0.988]

l1 = plt.plot(x, y1, 'r--', label='RoundRobin')
l2 = plt.plot(x, y2, 'g--', label='OLScheduler')
l3 = plt.plot(x, y3, 'b--', label='DepRoute-1')
l4 = plt.plot(x, y3, 'y--', label='DepRoute-2')

plt.plot(x, y1, 'ro-', x, y2, 'g+-', x, y3, 'b^-', x, y4, 'y*-')
plt.title('Total Hit Rate of Different Strategies')
plt.xlabel('Container Number')
plt.ylabel('Total Hit Rate')
plt.legend()
plt.show()
