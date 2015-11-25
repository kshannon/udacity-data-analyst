# Lesson 3: Data Analysis Notes:
import numpy
import scipy.stats
import pandas

def compare_averages(filename):
    """
    Write a function that will read that the csv file into a pandas data frame,
    and run Welch's t-test on the two cohorts defined by handedness.
    
    One cohort should be a data frame of right-handed batters. And the other
    cohort should be a data frame of left-handed batters.
    
    We have included the scipy.stats library to help you write
    or implement Welch's t-test:
    http://docs.scipy.org/doc/scipy/reference/stats.html
    
    With a significance level of 95%, if there is no difference
    between the two cohorts, return a tuple consisting of
    True, and then the tuple returned by scipy.stats.ttest.  
    
    If there is a difference, return a tuple consisting of
    False, and then the tuple returned by scipy.stats.ttest.
    
    For example, the tuple that you return may look like:
    (True, (9.93570222, 0.000023))
    """
    csv_data = pandas.read_csv(filename)
    df = csv_data.drop(['height','weight','HR'], axis=1)
    right_handed = df[df['handedness'] == 'R']
    left_handed = df[df['handedness'] == 'L']
    test_result = scipy.stats.ttest_ind(right_handed['avg'], left_handed['avg'], equal_var=False)
    if test_result[1] > 0.05:
        return True, test-result
    else:
        return False, test_result
# Output: 
# due to such a low p-value we must reject the null in favor of the hypothesis.
(False (statistic=-9.9357022262420944, pvalue=3.8102742258887383e-23))
# --------------------------------------------------------------------------------------------
# In the following exercise, you will calculate the parameters or weights, that is, 
# the values of theta, to predict how many home runs a baseball player will hit 
# given their height and weight
import statsmodels.api as sm
import numpy

def linear_regression(features, values):  
    features = sm.add_constant(features)
    model = sm.OLS(values,features)
    results = model.fit()
    results.params
    return   (results.params[0], [results.params[1], results.params[2]])
# Output:
Your intercept: 199.07125028
Your parameters: [-4.4412484679065303, 0.91818241446970983]
This means homeruns will be predicted using the equation
homeruns = -4.44 * height + 0.92 * weight + 199.07
# Note that add_constant adds the constant feature as the first feature, so the intercept is at 
# index 0 of the array results.params. The remaining values of results.params, from index 1 to the 
# end, are the parameters, or weights, of the real features.
# Also note that values comes before features when creating the OLS model, just as Y came before X 
# in the example code.
# --------------------------------------------------------------------------------------------
import numpy as np
from scipy import stats

def compute_r_squared(data, predictions):
    num = ((data - predictions)**2).sum()
    denom = ((data - np.mean(data))**2).sum()
    r_squared = 1 - num/denom

    # using Scipy ------------
    x = data
    y = predictions
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    print r_value**2
    # ------------------------
    
    return r_squared
            # import statsmodels.api as sm
            # y = data
            # X = predictions
            # X = sm.add_constant(X)
            # model = sm.OLS(y,X)
            # results = model.fit()
            # r_squared = results.rsquared
            # new_predictions = results.predict()
            # print compute_r_squared(y, new_predictions)
# Output: 
0.472978316446 # <-- from scipy
You calculated R^2 value correctly!
Your calculated R^2 value is: 0.318137233709
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 3.1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
import pandas
import matplotlib.pyplot as plt

def entries_histogram(turnstile_weather):

    print turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==1].describe()
    print turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==0].describe()
    plt.figure()
    plt.title('HIST of ENTRIESn_hourly')
    #plt.axis([0,6000, 0,45000])
    plt.xlabel('ENTRIESn_hourly')
    plt.ylabel('Frequency')
    turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==1]
                    .plot(kind='hist',alpha=0.5, bins=20, range=(0, 4500))
    turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==0]
                    .plot(kind='hist',alpha=0.5, bins=20, range=(0, 4500))
    return plt
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 3.3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
import scipy
import scipy.stats
import pandas

def mann_whitney_plus_means(turnstile_weather):
    '''
    This function will consume the turnstile_weather dataframe containing
    our final turnstile weather data. 
    You will want to take the means and run the Mann Whitney U-test on the 
    ENTRIESn_hourly column in the turnstile_weather dataframe.
    '''
    with_rain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==1]
    without_rain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==0]
    with_rain_mean = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==1].mean()
    without_rain_mean = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==0].mean()
    U, p = scipy.stats.mannwhitneyu(with_rain, without_rain)
    
    return with_rain_mean, without_rain_mean, U, p
# Output:
#    mean with_rain   mean w/o rain       U value          p value
(1105.4463767458733, 1090.278780151855, 1924409167.0, 0.024999912793489721)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 3.5 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
import pandas
import statsmodels.api as sm

def linear_regression(features, values):
    
    features = sm.add_constant(features)
    model = sm.OLS(values,features)
    results = model.fit()
    intercept, params = results.params[0], results.params[1:]
    return intercept, params

def predictions(dataframe):
    print list(dataframe)
    features = dataframe[['rain', 'Hour', 'meantempi', 'maxtempi', 'meanwindspdi', 'meandewpti', 'meanpressurei', 'maxdewpti']]
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    
    # Values
    values = dataframe['ENTRIESn_hourly']

    # Perform linear regression
    intercept, params = linear_regression(features, values)
    
    predictions = intercept + np.dot(features, params)

    return predictions
# Output:
['Unnamed: 0', 'UNIT', 'DATEn', 'TIMEn', 'Hour', 'DESCn', 'ENTRIESn_hourly', 'EXITSn_hourly', 
'maxpressurei', 'maxdewpti', 'mindewpti', 'minpressurei', 'meandewpti', 'meanpressurei', 'fog', 
'rain', 'meanwindspdi', 'mintempi', 'meantempi', 'maxtempi', 'precipi', 'thunder']
Your r^2 value is 0.481638164572
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 3.6 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
import scipy
import matplotlib.pyplot as plt

def plot_residuals(turnstile_weather, predictions):
    '''
    Using the same methods that we used to plot a histogram of entries
    per hour for our data, why don't you make a histogram of the residuals
    (that is, the difference between the original hourly entry data and the predicted values).
    Try different binwidths for your histogram.

    Based on this residual histogram, do you have any insight into how our model
    performed?  Reading a bit on this webpage might be useful:

    http://www.itl.nist.gov/div898/handbook/pri/section2/pri24.htm
    '''
    print np.std(turnstile_weather['ENTRIESn_hourly'] - predictions)
    plt.figure()
    (turnstile_weather['ENTRIESn_hourly'] - 
     predictions).plot(kind='hist',alpha=0.5, bins=500, range=(-7500, 7500))
    return plt
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 3.7 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
