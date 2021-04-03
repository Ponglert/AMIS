import DataStructure
import TwoOptAlgorithm
import time
import matplotlib.pyplot as plt
# --- CONSTANTS ----------------------------------------------------------------+

numNode = 20  # จำนวน Node ส่งและรับน้ำ
popsize = 1  # ขนาดประชากรในแต่ละรุ่น กรณี 2opt Algorithm จะใช้ประชากร 1 เท่านั้น
size_list = [50, 75, 100]  # ขนาดกำลังในการจ่าย
costopen = [1000, 1500, 2000]  # ต้นทุนในการเปิด Node พิจารณาตามขนาดตามลำดับ
disperunit = 10  # ต้นทุนระยะทางต่อหน่วย

bounds_wp = [0,1]
maxiter = 100

nodeList = DataStructure.CreateNode(numNode, bounds_wp)

start = time.time()
gen_sol,gen_avg_list = TwoOptAlgorithm.two_opt(nodeList, popsize, maxiter, size_list, costopen, bounds_wp, disperunit)
timetaken = time.time() - start

fitness,nodelocal_list = DataStructure.DecodeFitnessNonSort(gen_sol, size_list, costopen, disperunit)

startpolt = 0
for j in range(0, len(nodelocal_list)):
    lr = nodelocal_list[j]
    print(lr.route, ' ', "{:.2f}".format(lr.costlocal), ' ', "{:.2f}".format(lr.costdis), ' ', "{:.2f}".format(lr.costtotal))
    nodeopen = lr.route[0]
    for k in range(1, len(lr.route)):
        # plotting points as a scatter plot
        x = []
        y = []
        x.append(nodeopen.x)
        x.append(lr.route[k].x)
        y.append(nodeopen.y)
        y.append(lr.route[k].y)
        plt.plot(x, y, color='red',linewidth = 3)
        # plotting points as a scatter plot
        if startpolt == 0:
            plt.scatter(nodeopen.x, nodeopen.y, color="blue", label= "Pond Send",
                        marker="o", s=100)
            plt.scatter(lr.route[k].x, lr.route[k].y, color="green", label= "Pond Receive",
                        marker="o", s=100)
            startpolt = startpolt + 1
        else:
            plt.scatter(nodeopen.x, nodeopen.y, color="blue",
                        marker="o", s=100)
            plt.scatter(lr.route[k].x, lr.route[k].y, color="green",
                        marker="o", s=100)


# x-axis label
plt.xlabel('x - coordinate',fontsize=16)
# frequency label
plt.ylabel('y - coordinate',fontsize=16)
# plot title
plt.title('Local Search 2opt  \n' + 'N: ' + str(numNode) + ', Iteration: ' + str(maxiter) +
          ', Best Cost: ' + "{:.2f}".format(fitness) + ', Time (s): ' + "{:.4f}".format(timetaken),fontsize=18)
# showing legend
plt.legend()
# function to show the plot
plt.show()

print('Best Cost: ', "{:.2f}".format(fitness))
print('Time (s): ', "{:.4f}".format(timetaken))

plt.clf()
x = list(range(1, maxiter+1))
y = gen_avg_list

plt.plot(x, y, color='red',linewidth = 2)
# naming the x axis
plt.xlabel('Iteration',fontsize=16)
# naming the y axis
plt.ylabel('Cost average',fontsize=16)
# giving a title to my graph
plt.title('Local Search 2opt',fontsize=18)

# function to show the plot
plt.show()