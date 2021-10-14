import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_events(events):
    """
    This function plots all of the event data over time.
    """
    events.resample('M').sum().plot(figsize = (12,6),)
    plt.ylabel('Number of Animals')
    plt.title('Steep Decline in 2020 Due to Covid-19 Pandemic')
    plt.show()

def plot_events_post_pandemic(events):
    """
    This function plots all of the event data from 2020 and beyond. The purpose is to 
    look specifically at the effects of the Covid-19 pandemic.
    """
    events['2020':'2021'].resample('M').sum().plot(figsize=(12,6))
    plt.ylabel('Number of Animals')
    plt.title('Steady Rise in Intakes and Adoptions, But Not Transfers After 2020 Decline')
    plt.show()

def plot_intake_trends(events):
    """
    This function only plots intakes, but provides a better look at the trends over time.
    """
    plt.figure(figsize=(12,6))
    events.intakes.plot(label = 'Daily', alpha = 0.2)
    events.intakes.resample('W').mean().plot(label = 'Weekly', alpha = 0.5)
    events.intakes.resample('M').mean().plot(label = 'Monthly', alpha = 0.8)
    events.intakes.resample('Q').mean().plot(label = 'Quarterly')
    events.intakes.resample('Y').mean().plot(label = 'Yearly')
    plt.legend()
    plt.ylabel('Number of Animals')
    plt.title('Repetitive Cycles Observed In Intakes Over Time')
    plt.show()

def plot_yearly_intake_trends(events):
    """
    This function plots the yearly seasonal trends over time.
    """
    y = events.intakes
    y.groupby([y.index.year, y.index.month]).mean().unstack(0).plot(figsize=(12,6))
    plt.ylabel('Number of Animals')
    plt.xlabel('Month')
    plt.title('Due to the Pandemic, Animal Intakes Have Dropped Significantly in 2020 and 2021')
    plt.show()

