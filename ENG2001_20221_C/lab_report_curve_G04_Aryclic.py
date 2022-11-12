

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import lab_report_tool_package.read_report_file as lr
import lab_report_tool_package.curve_analyze as lc

x_min = -0.05
x_max = 5.
y_min = 0.
y_max = 75.


dataLine = lr.read_file_split_data("C:\\Users\\qqj03\\Desktop\\Lab Result\\G04_Acrylic.txt")
# print(data)

stress = np.array(lr.get_colume_data(dataLine, 4))
strain = np.array(lr.get_colume_data(dataLine, 5))

slope, intercept, r_value, p_value, dataIndex = lc.linear_analyze(strain, stress, 0,  100)

# x = np.arange(0.2, x_max, 0.00001)
x_crsp, y_crsp = lc.cross_point_sync_x(strain, slope * (strain - 0.2) + intercept, stress, 0.01)

x_tensile, y_tensile = lc.tensile_point(strain, stress)

x_fracture, y_fracture = lc.fracture_point(strain, stress, x_tensile)

degree = 10
sIndex = lc.findIndex(strain, x_fracture)
coeff = lc.curve_fit_coeff(strain, stress, dataIndex, sIndex, degree)

x_linear = np.arange(0., x_max, 0.25)
y_linear = slope * x_linear + intercept
x_offset = x_linear
y_offset = slope * (x_linear - 0.2) + intercept
x_curve = np.arange(strain[dataIndex], x_max, 0.001)
y_curve = lc.curve_fit_generate(x_curve, coeff)




# stress = stress[0: ]
# strain = strain[0: ]

print(len(stress))
print(len(strain))

plt.figure(figsize=(16, 7.5))
plt.title("G04_Aryclic")
plt.xlabel("Strain(%)")
plt.ylabel("Stress(MPa)")
plt.style.use('seaborn')

plt.grid(True)


y_min = stress[0]


plt.axis([x_min, x_max, y_min, y_max])

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
plt.plot(x_linear, y_linear, c='g', linestyle='--',)
plt.plot(x_offset, y_offset, c='g', linestyle='--',)
plt.plot(x_curve, y_curve, c='orange', linestyle='--',)

plt.scatter(x_crsp, y_crsp, c='black',)
plt.annotate("Yield Point\nStrain = " + str(round(x_crsp, 4)) + "(%)\n" + "Stress = " + str(round(y_crsp, 4)) + "(MPa)", 
        xy=(x_crsp, y_crsp), xytext=(x_crsp + 0.2, y_crsp - 10), arrowprops=dict(facecolor='k', headwidth=5, width=1))

plt.scatter(x_tensile, y_tensile, c='black',)
plt.annotate("Tensile Point\nStrain = " + str(round(x_tensile, 4)) + "(%)\n" + "Stress = " + str(round(y_tensile, 4)) + "(MPa)", 
        xy=(x_tensile, y_tensile), xytext=(x_tensile, y_tensile - 10), arrowprops=dict(facecolor='k', headwidth=5, width=1))

plt.scatter(x_fracture, y_fracture, c='black',)
plt.annotate("Fracture Point\nStrain = " + str(round(x_fracture, 4)) + "(%)\n" + "Stress = " + str(round(y_fracture, 4)) + "(MPa)", 
        xy=(x_fracture, y_fracture), xytext=(x_fracture - 0.8, y_fracture - 10), arrowprops=dict(facecolor='k', headwidth=5, width=1))

plt.xticks(np.arange(0., x_max, x_max / 25))
plt.yticks(np.arange(y_min, y_max, y_max / 25))
# plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.6f'))
for i in range(0, len(strain)):
    print("strain: {}  |  stress: {}".format(strain[i], stress[i]))
plt.show()

os.system("PAUSE")