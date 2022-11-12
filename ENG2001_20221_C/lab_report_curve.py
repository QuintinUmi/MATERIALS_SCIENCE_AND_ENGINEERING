

import os
import numpy as np
import matplotlib.pyplot as plt
from lab_report_tool_package.read_report_file import read_file_split_data

data = read_file_split_data("C:\\Users\\qqj03\\Desktop\\Lab Result\\G04_Acrylic.txt")
# print(data)

stress = data[4]
strain = data[5]

# plt.plot(strain, stress)