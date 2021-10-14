import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_intake_data():
    """
    This function will acquire and prepare the intake data to be merged with the outcome data.
    """
    #Get the data from the saved .csv
    intakes = pd.read_csv('Austin_Animal_Center_Intakes.csv')

    #Create new column called 'intakes'
    #Since each row is considered a separate intake, I will just set the value for each row to be 1.
    intakes['intakes'] = 1

    #Convert 'DateTime' to datetime object and then set it to the index, and sort
    intakes['Date'] = pd.to_datetime(intakes.DateTime)

    #Set the index and sort
    intakes = intakes.set_index('Date').sort_index()

    #Now resample by day and sum the number of intakes.
    #Create a new df to store only that info
    num_intakes = pd.DataFrame(intakes.resample('D').intakes.sum())

    return num_intakes

def get_outcome_data():
    """
    This function will acquire and prepare the outcome data to be merged with the intake data.
    """
    #Get the data from the saved .csv
    outcomes = pd.read_csv('Austin_Animal_Center_Outcomes.csv')

    #Create dummy variables for 'Outcome Type'
    dummies = pd.get_dummies(outcomes['Outcome Type'], dummy_na=False, drop_first=False)
    outcomes = pd.concat([outcomes, dummies], axis = 1).drop(columns = ['Outcome Type'])

    #Convert DateTime to datetime object, set it to index, and order values
    outcomes['Date'] = pd.to_datetime(outcomes.DateTime)

    #Set DateTime to index and sort
    outcomes = outcomes.set_index('Date').sort_index()

    #Now resample by day and sum the number of outcome types
    #Create a new df to store only that info
    num_outcomes = outcomes.resample('D')['Adoption','Died','Euthanasia','Return to Owner', 'Rto-Adopt','Transfer'].sum()

    #Rename the columns
    num_outcomes.rename(columns = {
        'Adoption':'adoptions',
        'Died':'deaths',
        'Euthanasia':'euthanizations',
        'Return to Owner':'rto',
        'Rto-Adopt':'rto_adoptions',
        'Transfer':'transfers'
    }, inplace = True)

    #Since the num_intakes df only has data up to October 10th, 2021, I will remove the last entry in the num_outcomes df, which is October 11th, 2021.
    num_outcomes = num_outcomes[:'2021-10-10']

    return num_outcomes

def get_event_data():
    """
    This function will call the appropriate functions to acquire and prepare both the intake and outcome data.
    It will then merge those dataframes on the common datetime index
    """
    #Get and prepare the intake data
    num_intakes = get_intake_data()

    #Get and prepare the outcome data
    num_outcomes = get_outcome_data()

    #Merge the two dataframes together
    events = num_intakes.merge(right = num_outcomes, how = 'inner', on = 'Date')
    
    events = events.drop(columns = ['deaths', 'rto', 'rto_adoptions'])

    return events

def get_dists(df):
    """
    This function will plot the individual variable distributions for the given dataframe.
    """
    for col in df.columns:
            sns.histplot(x = col, data = df)
            plt.title(col)
            plt.show()
