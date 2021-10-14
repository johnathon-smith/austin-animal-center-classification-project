import numpy as np
import pandas as pd

from sklearn.metrics import mean_squared_error
from math import sqrt

import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

import statsmodels.api as sm
from statsmodels.tsa.api import Holt

def plot_train_validate_test(train, validate, test, events):
    """
    This function will plot the data from train, validate, and test to show where they are separated.
    """
    #Plot the data
    plt.figure(figsize=(12,6))
    plt.plot(train['intakes'], label = 'Train', color = '#1f77b4')
    plt.plot(validate['intakes'], label = 'Validate', color = '#ff7f0e')
    plt.plot(test['intakes'], label = 'Test', color = '#2ca02c')
    #The following two plots fill in the gaps between each data set
    plt.plot(events['2020-03':'2020-04']['intakes'].resample('M').sum(), color = '#1f77b4')
    plt.plot(events['2021-03':'2021-04']['intakes'].resample('M').sum(), color = '#ff7f0e')
    plt.title('Intakes')
    plt.xlabel('Date')
    plt.ylabel('Number of Intakes')
    plt.legend()
    plt.show()

def evaluate(target_var, validate, yhat_df):
    """
        This function will calculate the RMSE and return it.
    """
    rmse = round(sqrt(mean_squared_error(validate[target_var], yhat_df[target_var])), 0)
    return rmse

def plot_and_eval(target_var, train, validate, events, yhat_df):
    """
        This function will use the evaluate function and also plot train 
        and validate values with the predicted values in order to compare performance.
    """
    plt.figure(figsize = (12,4))
    plt.plot(train[target_var], label = 'Train', linewidth = 1)
    plt.plot(validate[target_var], label = 'Validate', linewidth = 1)
    plt.plot(yhat_df[target_var], label = 'Prediction', linewidth = 1)
    plt.title(target_var)
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Number of Intakes')
    #The following plot fills in the gap between each data set
    plt.plot(events['2020-03':'2020-04']['intakes'].resample('M').sum(), color = '#1f77b4', linewidth = 1)
    rmse = evaluate(target_var, validate, yhat_df)
    print(target_var, '-- RMSE: {:.0f}'.format(rmse))
    plt.show()

def append_eval_df(model_type, target_var, validate, yhat_df, eval_df):
    """
        This function will append evaluation metrics for each model type, target variable, 
        and metric type, along with the metric value into our eval_df data frame object. 
    """
    rmse = evaluate(target_var, validate, yhat_df)
    d = {'model_type': [model_type], 'target_var': [target_var], 'rmse': [rmse]}
    d = pd.DataFrame(d)
    return eval_df.append(d, ignore_index = True)

def make_predictions(intakes, validate):
    """
    This function will apply the predictions made to the validate index and return that df as yhat_df
    """
    yhat_df = pd.DataFrame({'intakes': [intakes],
                           }, index = validate.index)
    return yhat_df

def get_simple_average(train, validate, events, eval_df):
    """
    This function will create a model using the Simple Average.
    """
    #Find the average
    intakes = round(train.intakes.mean(), 2)

    yhat_df = make_predictions(intakes, validate)

    plot_and_eval('intakes', train, validate, events, yhat_df)

    eval_df = append_eval_df(model_type='simple_average', target_var = 'intakes', validate = validate, yhat_df = yhat_df, eval_df = eval_df)

    return eval_df

def get_moving_average(train, validate, events, eval_df):
    """
    This function will use a loop to create several moving average models. It will also update and return the eval_df
    """
    periods = [1, 3, 6, 9, 12]

    for p in periods:
        intakes = round(train['intakes'].rolling(p).mean().iloc[-1], 2)
        yhat_df = make_predictions(intakes, validate)
        model_type = str(p) + 'm moving average'
        eval_df = append_eval_df(model_type = model_type, target_var = 'intakes',validate = validate, yhat_df = yhat_df, eval_df = eval_df)

    return eval_df

def get_holts_model(train, validate, events, eval_df):
    """
    This function will create a Holts Linear model. It will also plot the resulting predictions, update the eval_df, and return the eval_df
    """
    model = Holt(train['intakes'], exponential = False)

    model = model.fit(smoothing_level = .05, 
                    smoothing_trend = .11, 
                    optimized = False)

    yhat_counts = model.predict(start = validate.index[0], 
                            end = validate.index[-1])
    
    yhat_df = pd.DataFrame()
    
    yhat_df['intakes'] = round(yhat_counts, 2)
    
    yhat_df = yhat_df.set_index(validate.index)

    plot_and_eval('intakes', train, validate, events, yhat_df)

    eval_df = append_eval_df(model_type = 'Holts', target_var = 'intakes', validate = validate, yhat_df = yhat_df, eval_df = eval_df)

    return eval_df

def get_previous_cycle_model(train, validate, events, eval_df):
    """
    This function will calculate the average yearly difference and apply it to the validate index. It will also attempt to 
    account for the sudden drop due to the pandemic in 2020 by adding the average difference between the last two years of the train data set.
    """
    #This value is the average difference between the last two years of the train data set
    drop_off = -563

    #Add the average yearly difference to the last year's values in train and add the delta
    yhat_df = train['2019-04':'2020-03'] + train.diff(12).mean() + drop_off

    # set yhat_df to index of validate
    yhat_df.index = validate.index

    plot_and_eval('intakes', train, validate, events, yhat_df)

    eval_df = append_eval_df(model_type = 'previous year plus delta', target_var = 'intakes',validate = validate, yhat_df = yhat_df, eval_df = eval_df)

    return eval_df

def plot_and_eval_test(target_var, train, validate, test, events, yhat_df):
    """
        This function will use the evaluate function and also plot train, validate,  
        and test values with the predicted values in order to compare performance.
    """
    plt.figure(figsize = (12,4))
    plt.plot(train[target_var], label = 'Train', linewidth = 1)
    plt.plot(validate[target_var], label = 'Validate', linewidth = 1)
    plt.plot(test[target_var], label = 'Test', linewidth = 1)
    plt.plot(yhat_df[target_var], label = 'Prediction', linewidth = 1)
    plt.title(target_var)
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Number of Intakes')
    #The following plot fills in the gaps between each data set
    plt.plot(events['2020-03':'2020-04']['intakes'].resample('M').sum(), color = '#1f77b4', linewidth = 1)
    plt.plot(events['2021-03':'2021-04']['intakes'].resample('M').sum(), color = '#ff7f0e', linewidth = 1)
    rmse = evaluate(target_var, test, yhat_df)
    print(target_var, '-- RMSE: {:.0f}'.format(rmse))
    plt.show()
    

def eval_holts_model_on_test(train, validate, test, events, eval_df):
    """
    This function will create a Holts Linear model. It will also plot the resulting predictions, update the eval_df, and return the eval_df
    """
    model = Holt(train['intakes'], exponential = False)

    model = model.fit(smoothing_level = .05, 
                    smoothing_trend = .11, 
                    optimized = False)

    yhat_counts = model.predict(start = test.index[0], 
                            end = test.index[-1])
    
    yhat_df = pd.DataFrame()
    
    yhat_df['intakes'] = round(yhat_counts, 2)
    
    yhat_df = yhat_df.set_index(test.index)

    plot_and_eval_test('intakes', train, validate, test, events, yhat_df)

    eval_df = append_eval_df(model_type = 'Holts', target_var = 'intakes', validate = test, yhat_df = yhat_df, eval_df = eval_df)

    return eval_df
