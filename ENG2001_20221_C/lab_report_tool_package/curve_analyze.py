import numpy as np
import scipy.stats as st


def linear_analyze(strain, stress, startIndex, ommitValue):
    
    dataIndex = -1
    for i in range(startIndex + 1, min(len(strain), len(stress))):
        slope_t, intercept_t, r_value_t, p_value_t, std_err = st.linregress(strain[0: i], stress[0: i])
        if((not 0.9993 < r_value_t**2 <= 1  or p_value_t > 0.05) and i > ommitValue):
            dataIndex = i
            break
        else:
            slope, intercept, r_value, p_value = slope_t, intercept_t, r_value_t, p_value_t

    return slope, intercept, r_value, p_value, dataIndex


def curve_fit_coeff(strain, stress, startIndex, endIndex, degree):
    
    coeff = np.polyfit(strain[startIndex: endIndex], stress[startIndex: endIndex], degree)
    return coeff

def curve_fit_generate(x_curve, coeff):
    y_curve = []
    for x in x_curve:
        val = 0
        for i in range(0, len(coeff)):
            val += coeff[i] * x**(len(coeff) - i - 1)
        y_curve.append(val)
    y_curve = np.array(y_curve)

    return y_curve

def tensile_point(strain, stress):
    t_strain, t_stress = 0, 0
    for i in range(0, min(len(strain), len(stress))):
        if(stress[i] > t_stress):
            t_stress = stress[i]
            t_strain = strain[i]

    return t_strain, t_stress

def fracture_point(strain, stress, tensile_strain, check_coeff = 0.05):
    
    sIndex = findIndex(strain, tensile_strain)

    for i in range(sIndex, len(strain)):
        check_strain = []
        check_stress = []
        stressSum = 0
        for j in range(int(len(strain) * check_coeff - 1), 0, -1):
            check_strain.append(strain[i - j])
            check_stress.append(stress[i - j])
            stressSum += stress[i - j]
        aver = stressSum / int(len(strain) * check_coeff - 1)
        slope_t, intercept_t, r_value_t, p_value_t, std_err = st.linregress(check_strain, check_stress)
        if(aver - stress[i] > aver * (check_coeff*3.5)):
            f_strain = strain[i - 1]
            f_stress = stress[i - 1]
            break
    return f_strain, f_stress

def findIndex(strain, tarStrain):
    sIndex = 0
    while(strain[sIndex] < tarStrain):
        sIndex += 1
    return sIndex



def cross_point_sync_x(x, func1, func2, precision = 0.01):

    crossp_x = []
    crossp_y = []

    for i in range(0, min(len(func1), len(func2))):
        if(-precision < func1[i] - func2[i] < precision):
            # print(func1[i] - func2[i])
            crossp_x.append(x[i])
            crossp_y.append((func1[i] + func2[i]) / 2)

    xSum = 0
    ySum = 0
    for i in range(0, len(crossp_x)):
        xSum += crossp_x[i]
        ySum += crossp_y[i]

    crossp_aver_x = xSum / len(crossp_x)
    crossp_aver_y = ySum / len(crossp_y)
    return crossp_aver_x, crossp_aver_y


if __name__ == '__main__':
    import read_report_file as lr
    dataLine = lr.read_file_split_data("C:\\Users\\qqj03\\Desktop\\Lab Result\\G04_Acrylic.txt")
    # print(data)

    stress = np.array(lr.get_colume_data(dataLine, 4))
    strain = np.array(lr.get_colume_data(dataLine, 5))

    slope, intercept, r_value, p_value, dataIndex = linear_analyze(strain, stress, 0, 100)

    print("Slope: {}, intercept: {}, r_value: {}, p_value: {}, dataIndex: {}".format(slope, intercept, r_value, p_value, dataIndex))

    # coeff = curve_fit_coeff(strain, stress, dataIndex, 1000)

    # print(coeff)

    # slope, intercept, r_value, p_value, dataIndex = linear_analyze(strain, stress, dataIndex, 100)

    