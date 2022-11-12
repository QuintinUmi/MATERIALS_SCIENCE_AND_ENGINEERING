

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import lab_report_tool_package.read_report_file as lr

dataLine = lr.read_file_split_data("C:\\Users\\qqj03\\Desktop\\Lab Result\\G04_Acrylic.txt")
# print(data)

stress = np.array(lr.get_colume_data(dataLine, 4))
strain = np.array(lr.get_colume_data(dataLine, 5))

# stress = stress[0: ]
# strain = strain[0: ]

print(len(stress))
print(len(strain))

plt.figure(figsize=(16, 8))
plt.title("G04_Aryclic")
plt.xlabel("Strain(%)")
plt.ylabel("Stress(MPa)")
plt.style.use('seaborn')

plt.grid(True)

x_min = 0.
x_max = 5.
y_min = 0.
y_max = 75.

# xtick_spacing = 100
# ytick_spacing = 100
# #通过修改tick_spacing的值可以修改x轴的密度
# #1的时候1到16，5的时候只显示几个
# fig, cur = plt.subplots(1,1)
# cur.plot(strain, stress)
# cur.xaxis.set_major_locator(ticker.MultipleLocator(xtick_spacing))
# cur.yaxis.set_major_locator(ticker.MultipleLocator(ytick_spacing))
# plt.xlabel("Strain")
# plt.ylabel("Stress")
# cur.grid()



plt.plot(strain, stress)

plt.axis([x_min, x_max, y_min, y_max])
plt.xticks(np.arange(0., x_max, x_max / 25))
plt.yticks(np.arange(0., y_max, y_max / 25))
# plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.6f'))
for i in range(0, len(strain)):
    print("strain: {}  |  stress: {}".format(strain[i], stress[i]))
plt.show()

os.system("PAUSE")