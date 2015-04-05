import numpy as np
import scipy
import scipy.stats
import pandas
def t_critical_value(alpha, degrees_of_freedom, tail='both'):
        """
        tail: string: "upper", "lower", "both"
        alpha: float/int
        degrees_of_freedom: float/int
        rtype: float: t critical value

        """
        t = {'upper' : 1 - alpha, 'lower' : alpha, 'both'  : alpha/2}[tail]

        return scipy.stats.t.isf(t, degrees_of_freedom)


def mann_whitney_plus_means(turnstile_weather):
    '''
    This function will consume the turnstile_weather dataframe containing
    our final turnstile weather data. 
    
    You will want to take the means and run the Mann Whitney U-test on the 
    ENTRIESn_hourly column in the turnstile_weather dataframe.
    
    This function should return:
        1) the mean of entries with rain
        2) the mean of entries without rain
        3) the Mann-Whitney U-statistic and p-value comparing the number of entries
           with rain and the number of entries without rain
    
    '''
    
    ### YOUR CODE HERE ###
    #turnstile_weather = turnstile_weather[['rain','ENTRIESn_hourly']]
    withoutRain = turnstile_weather[turnstile_weather['rain']==0]
    without_rain_mean = withoutRain['ENTRIESn_hourly'].mean()
    
    withRain = turnstile_weather[turnstile_weather['rain']==1]
    with_rain_mean = withRain['ENTRIESn_hourly'].mean()
    with_rain_std = withRain[['ENTRIESn_hourly']].std()
    no_of_rainy_days = len(withRain['ENTRIESn_hourly'])
    
    overall_mean = turnstile_weather['ENTRIESn_hourly'].mean()
    #print with_rain_mean, without_rain_mean,  with_rain_std
    [U,p] = scipy.stats.mannwhitneyu(withoutRain['ENTRIESn_hourly'],withRain['ENTRIESn_hourly'] )
    
    return with_rain_mean, with_rain_std, without_rain_mean, U, p, no_of_rainy_days, overall_mean # leave this line for the grader


filename = 'turnstile_data_master_with_weather.csv'
weather_data = pandas.read_csv(filename)
[with_rain_mean, with_rain_std, without_rain_mean, U,p, number_of_rainy_days, overall_mean] = mann_whitney_plus_means(weather_data)

print 'p-value is :', p, 'mean ridership on rainy days ', with_rain_mean, 'mean ridership on non rainy days', without_rain_mean, 'U ', U


alpha = 0.001
t_critical = t_critical_value(alpha, number_of_rainy_days - 1, tail='both')

t = (float)((with_rain_mean - overall_mean)/(with_rain_std/(np.sqrt(number_of_rainy_days))))

if(t>t_critical):
    print
    print
    print 't_critical', t_critical, '   t ', t
    print 'In this case t > t-critical, hence this increase in ridership is statistically significant and could not have happened because of chance'