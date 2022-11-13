

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import lab_report_tool_package.read_report_file as lr
import lab_report_tool_package.curve_analyze as lc

x_min = -0.05
x_max = 25.
y_min = 0.
y_max = 500.
isSteel = True


dataLine = lr.read_file_split_data("C:\\Users\\qqj03\\Desktop\\Lab Result\\G04_Steel.txt")
# print(data)

stress = np.array(lr.get_colume_data(dataLine, 4))
strain = np.array(lr.get_colume_data(dataLine, 5))

slope, intercept, r_value, p_value, dataIndex = lc.linear_analyze(strain, stress, 0,  400)

x_elaslim, y_elaslim = lc.elastic_to_plastic(strain, stress, slope * strain + intercept, 400)

x_tensile, y_tensile = lc.tensile_point(strain, stress)

if(isSteel):
    x_yield, y_yield = lc.steel_yield(strain, stress, x_elaslim, x_tensile)
else:
    x_yield, y_yield = lc.non_steel_yield(strain, slope * (strain - 0.2) + intercept, stress, 10)

x_fracture, y_fracture = lc.fracture_point(strain, stress, x_tensile)

res_mod = lc.resilience_modulus(strain, stress, x_fracture)

degree = 50
sIndex = lc.findIndex(strain, x_fracture)
coeff = lc.curve_fit_coeff(strain, stress, dataIndex, sIndex, degree)

x_linear = np.arange(-1.0, x_max, 0.001)
y_linear = slope * x_linear + intercept
x_offset = x_linear
y_offset = slope * (x_linear - 0.2) + intercept
x_curve = np.arange(strain[lc.findIndex(strain, x_elaslim)], x_max, 0.001)
y_curve = lc.curve_fit_generate(x_curve, coeff)



# stress = stress[0: ]
# strain = strain[0: ]

print(len(stress))
print(len(strain))

plt.figure(figsize=(16, 7.5))
plt.title("G04_Steel")
plt.xlabel("Strain(%)")
plt.ylabel("Stress(MPa)")
plt.style.use('seaborn')

plt.grid(True)


y_min = stress[0]


plt.axis([0, x_max, 0, y_max])



plt.plot(strain, stress, label="Experimental data")
plt.plot(x_linear, y_linear, c='g', linestyle='--', label="Elastic Modulus")
if(not isSteel):
    plt.plot(x_offset, y_offset, c='g', linestyle='--', label="0.2% Proof Strength")
plt.plot(x_curve, y_curve, c='orange', linestyle='--', label="Fit curve")

plt.fill_between(x_linear[lc.findIndex(y_linear, 0): lc.findIndex(x_linear, x_elaslim)], 0, 
                y_linear[lc.findIndex(y_linear, 0): lc.findIndex(x_linear, x_elaslim)], color="gray", alpha = 0.5)
plt.fill_between(strain[lc.findIndex(strain, x_elaslim): lc.findIndex(strain, x_fracture)], 0, 
                stress[lc.findIndex(strain, x_elaslim): lc.findIndex(strain, x_fracture)],
                    color="gray", alpha = 0.5)
plt.text((x_min + x_max) / 2.2, (y_min + y_max) / 2, "Resilience of Modulus\n\nE = {}".format(res_mod), size=10,
            bbox=dict(boxstyle='round', facecolor='#A9D7E7', alpha=0.7))

plt.legend(loc='lower right', prop=None, fontsize = 12, frameon=True)

plt.scatter(x_elaslim, y_elaslim, c='black',)
plt.annotate("Elastic Limit\nStrain = " + str(round(x_elaslim, 4)) + "(%)\n" + "Stress = " + str(round(y_elaslim, 4)) + "(MPa)", 
        xy=(x_elaslim, y_elaslim), xytext=(x_elaslim + 2, y_elaslim - 160), arrowprops=dict(facecolor='k', headwidth=5, width=1))

plt.scatter(x_yield, y_yield, c='black',)
plt.annotate("Yield Point\nStrain = " + str(round(x_yield, 4)) + "(%)\n" + "Stress = " + str(round(y_yield, 4)) + "(MPa)", 
        xy=(x_yield, y_yield), xytext=(x_yield + 1, y_yield - 80), arrowprops=dict(facecolor='k', headwidth=5, width=1))

plt.scatter(x_tensile, y_tensile, c='black',)
plt.annotate("Tensile Point\nStrain = " + str(round(x_tensile, 4)) + "(%)\n" + "Stress = " + str(round(y_tensile, 4)) + "(MPa)", 
        xy=(x_tensile, y_tensile), xytext=(x_tensile, y_tensile - 80), arrowprops=dict(facecolor='k', headwidth=5, width=1))

plt.scatter(x_fracture, y_fracture, c='black',)
plt.annotate("Fracture Point\nStrain = " + str(round(x_fracture, 4)) + "(%)\n" + "Stress = " + str(round(y_fracture, 4)) + "(MPa)", 
        xy=(x_fracture, y_fracture), xytext=(x_fracture - 5, y_fracture - 80), arrowprops=dict(facecolor='k', headwidth=5, width=1))

plt.xticks(np.arange(0., x_max, x_max / 25))
plt.yticks(np.arange(y_min, y_max, y_max / 25))
# plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.6f'))
for i in range(0, len(strain)):
    print("strain: {}  |  stress: {}".format(strain[i], stress[i]))
plt.show()

os.system("PAUSE")