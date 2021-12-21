import math

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def main():
    times = {1: 5.359699935070239e-05,
             11: 0.0017659000004641712,
             21: 0.0901462010006071,
             31: 0.4314318680008,
             41: 1.2706175809980778,
             51: 2.841816342999664,
             61: 5.4242443760012975,
             71: 9.225940856998932,
             81: 14.462372097001207,
             91: 21.517040542003087}
    results = {1: 27,
               11: 19612618,
               21: 105619718613031,
               31: 518295575789482417419,
               41: 2674444981899569877000237869,
               51: 14062064215101208361591017398917158,
               61: 75006828441029745774458611519686991867159,
               71: 404330720064877512899776690731906852687312453668,
               81: 2197131792364585482019241497391149511016381844236493309,
               91: 12014921645723434641815176353562014547173044675841245867971316}
    extrapolate_cubic(times)
    results = {key: float(val) for key, val in results.items()}
    extrapolate_exponential(results)


def extrapolate_cubic(times):
    time_series = pd.Series(times)
    time_fit = np.polyfit(time_series.index, time_series.values, 3)
    predicted_time = np.polyval(time_fit, time_series.index)
    predicted_series = pd.Series(predicted_time, index=time_series.index)
    time_series.plot()
    predicted_series.plot()
    print("Predicted time: ", np.polyval(time_fit, 1000) / 60 / 60, "hours")
    plt.show()


def extrapolate_exponential(values):
    series = pd.Series(values)
    fit = np.polyfit(series.index, np.log(series.values), 1)
    prediction = np.exp(np.polyval(fit, series.index))
    predicted_series = pd.Series(prediction, index=series.index)
    series.plot(logy=True)
    predicted_series.plot(logy=True)
    full_exponent = np.polyval(fit, 1000) * 0.43429
    log_mantissa, exponent = math.modf(full_exponent)
    mantissa = 10**log_mantissa
    print(f"Predicted value: {mantissa} * 10^{int(exponent)}")
    plt.show()


if __name__ == "__main__":
    main()
