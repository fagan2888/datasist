'''
This module contains all functions relating to visualization.

'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from . import structdata
from IPython.display import display




def countplot(data=None, cat_features=None, separate_by=None, fig_size=(5,5), save_fig=False):
    '''
    Makes a bar plot of all categorical features to show their counts.
    
    Parameters
    ------------

    data : DataFrame, array, or list of arrays.
        The data to plot.
    cat_features: str, scalar, array, or list. 
        The categorical features in the dataset, if not provided, 
        we try to infer the categorical columns from the dataframe.
    separate_by: str, default None.
        The feature used to seperate the plot. Called hue in seaborn.
    fig_size: tuple, Default (5,5)
        The size of the figure object.
    save_fig: bool, Default False.
        Saves the plot to the current working directory

    Returns
    -------
    None
    '''

    if data is None:
        raise ValueError("data: Expecting a DataFrame or Series, got 'None'")

    if cat_features is None:
        cat_features = structdata.get_cat_feats(data)
        
    for feature in cat_features:
        #Check the size of categories in the feature: Anything greater than 20 is not plotted
        if len(data[feature].unique()) > 30:
            print("Unique Values in {} is too large to plot".format(feature))
            print('\n')
        else:
            fig = plt.figure(figsize=fig_size)
            ax = fig.gca()

            sns.countplot(x=feature, hue=separate_by, data=data)
            plt.xticks(rotation=90)
            ax.set_title("Count plot for " + feature)

            if save_fig:
                plt.savefig('Countplot_{}'.format(feature))




def plot_missing(data=None):
    '''
    Plots the data as a heatmap to show missing values

    Parameters
    ----------
    data: DataFrame, array, or list of arrays.
        The data to plot.
    '''

    if data is None:
        raise ValueError("data: Expecting a DataFrame or Series, got 'None'")

    sns.heatmap(data.isnull(), cbar=True)
    plt.show()



def boxplot(data=None, num_features=None, target=None, fig_size=(8,8), large_data=False, save_fig=False):
    '''
    Makes a box plot of all numerical features against a specified categorical target column.

    A box plot (or box-and-whisker plot) shows the distribution of quantitative
    data in a way that facilitates comparisons between variables or across
    levels of a categorical variable. The box shows the quartiles of the
    dataset while the whiskers extend to show the rest of the distribution,
    except for points that are determined to be "outliers" using a method
    that is a function of the inter-quartile range

    Parameters
    ------------

    data : DataFrame, array, or list of arrays.
        Dataset for plotting.
    num_features: Scalar, array, or list. 
        The numerical features in the dataset, if not None, 
        we try to infer the numerical columns from the dataframe.
    target: array, pandas series, list.
        A categorical target column. Maximun number of categories is 10 and minimum is 1
    fig_size: tuple, Default (8,8)
        The size of the figure object.
    large_data: bool, Default False.
        If True, then sns boxenplot is used instead of normal boxplot. Boxenplot is 
        better for large dataset.
    save_fig: bool, Default False.
        If True, saves the current plot to the current working directory
    '''


    if target is None:
        raise ValueError('Target value cannot be None')

    if len(data[target].unique()) > 10:
        raise AttributeError("Target categories must be less than 10")

    if data is None:
        raise ValueError("data: Expecting a DataFrame or Series, got 'None'")

    if num_features is None:
        num_features = structdata.get_num_feats(data)
    
    if large_data:
        #use advanced sns boxenplot
        for feature in num_features:
            fig = plt.figure(figsize=fig_size)
            ax = fig.gca()

            sns.set_style("whitegrid")
            sns.boxenplot(target, feature, data=data, ax=ax)
            plt.ylabel(feature) # Set text for the x axis
            plt.xlabel(target)# Set text for y axis
            plt.xticks(rotation=90)
            plt.title('Box plot of {} against {}'.format(feature, target))
            if save_fig:
                plt.savefig('fig_{}_vs_{}'.format(feature,target))
            plt.show()
    else:
        for feature in num_features:
            fig = plt.figure(figsize=fig_size)
            ax = fig.gca()

            sns.set_style("whitegrid")
            sns.boxplot(target, feature, data=data, ax=ax)
            plt.ylabel(feature) # Set text for the x axis
            plt.xlabel(target)# Set text for y axis
            plt.xticks(rotation=90)
            plt.title("Box plot of '{}' vs. '{}'".format(feature, target))
            if save_fig:
                plt.savefig('fig_{}_vs_{}'.format(feature,target))
            plt.show()




def violinplot(data=None, num_features=None, target=None, fig_size=(8,8), save_fig=False):
    '''
    Makes a violin plot of all numerical features against a specified categorical target column.

    A violin plot plays a similar role as a box and whisker plot. It shows the
    distribution of quantitative data across several levels of one (or more)
    categorical variables such that those distributions can be compared. Unlike
    a box plot, in which all of the plot components correspond to actual
    datapoints, the violin plot features a kernel density estimation of the
    underlying distribution.

    Parameters
    ------------

    data : DataFrame, array, or list of arrays.
        Dataset for plotting.
    num_features: Scalar, array, or list. 
        The numerical features in the dataset, if not None, 
        we try to infer the numerical columns from the dataframe.
    target: array, pandas series, list.
        A categorical target column. Maximun number of categories is 10 and minimum is 1
    fig_size: tuple, Default (8,8)
        The size of the figure object.
    save_fig: bool, Default False.
        If True, saves the current plot to the current working directory
   '''

    if target is None:
        raise ValueError('Target value cannot be None')

    if len(data[target].unique()) > 10:
        raise AttributeError("Target categories must be less than 10")


    if data is None:
        raise ValueError("data: Expecting a DataFrame or Series, got 'None'")

    if num_features is None:
        num_features = structdata.get_num_feats(data)

    for feature in num_features:
        fig = plt.figure(figsize=fig_size)
        ax = fig.gca()

        sns.set_style("whitegrid")
        sns.violinplot(target, feature, data=data, ax=ax)
        plt.xticks(rotation=90)
        plt.ylabel(feature) # Set text for the x axis
        plt.xlabel(target)# Set text for y axis
        plt.title("Violin plot of '{}' vs. '{}'".format(feature, target))
        if save_fig:
            #TODO Add function to save to a specified directory
            plt.savefig('fig_{}_vs_{}'.format(feature,target))
        plt.show()




def histogram(data=None, num_features=None, bins=None, show_dist_type=False, fig_size=(8,8), save_fig=False):
    '''
    Makes an histogram plot of all numerical features.
    Helps to show univariate distribution of the features.
    
    Parameters
    ------------
    data : DataFrame, array, or list of arrays.
        Dataset for plotting.
    num_features: Scalar, array, or list. 
        The numerical features in the dataset, if not None, 
        we try to infer the numerical columns from the dataframe.
    bins: int
        The number of bins to use.
    show_dist_type: bool, Default False
        If True, Calculates the skewness of the data and display one of (Left skewed, right skewed or normal) 
    fig_size: tuple, Default (8,8).
        The size of the figure object.
    save_fig: bool, Default False.
        If True, saves the current plot to the current working directory
    
    '''


    if data is None:
        raise ValueError("data: Expecting a DataFrame or Series, got 'None'")

    if num_features is None:
        num_features = structdata.get_num_feats(data)

    for feature in num_features:
        fig = plt.figure(figsize=fig_size)
        ax = fig.gca()

        sns.distplot(data[feature].values, ax=ax, bins=bins)
        ax.set_xlabel(feature) # Set text for the x axis
        ax.set_ylabel('Count')# Set text for y axis

        if show_dist_type:
            ##TODO Add Code to calculate skewness
            pass
        else:
            ax.set_title('Histogram of ' + feature)

        if save_fig:
            #TODO Add function to save to a user specified directory
            plt.savefig('fig_hist_{}'.format(feature))

        plt.show()



def catbox(data=None, cat_features=None, target=None, fig_size=(12,6), save_fig=False):
    '''
    Makes a side by side bar plot of all categorical features against a categorical target feature.

    Parameters
    ------------

    data: DataFrame, array, or list of arrays.
        Dataset for plotting.
    cat_features: Scalar, array, or list. 
        The categorical features in the dataset, if None, 
        we try to infer the categorical columns from the dataframe.
    target: Scalar, array or list.
        Categorical target to plot against.
    fig_size: tuple, Default (12,6)
        The size of the figure object.
    save_fig: bool, Default False.
        If True, saves the plot to the current working directory.
    '''

    if data is None:
        raise ValueError("data: Expecting a DataFrame or Series, got 'None'")

    if cat_features is None:
        cat_features = structdata.get_cat_feats(data)

    #remove target from cat_features
    try:
        cat_features.remove(target)
    except:
        pass
    
    if len(data[target].unique()) > 8:
        #TODO Plot only a subset of the features say top 10
        raise AttributeError("Target categories must be less than seven")

    #Create a dummy column to hold count of values
    data['dummy_count'] = np.ones(shape = data.shape[0])
    #Loop over each categorical featureure and plot the acceptance rate for each category.
    for feature in cat_features:
        #Plots are made for only categories with less than 10 unique values because of speed
        if len(data[feature].unique()) > 10 :
            print("{} feature has too many categories and will not be ploted".format(feature))
            
        else:     
            counts = data[['dummy_count', target, feature]].groupby([target, feature], as_index = False).count()
            #get the categories
            cats = list(data[target].unique())

            if len(cats) > 6:
                raise ValueError("Target column: '{}' must contain less than six unique classes".format(target))

            #create new figure
            _ = plt.figure(figsize = fig_size)

            for i, cat in enumerate(cats): 
                plt.subplot(1, len(cats), i+1)
                #Get the counts each category in target     
                temp = counts[counts[target] == cat][[feature, 'dummy_count']] 
                sns.barplot(x=feature, y='dummy_count', data=temp)
                plt.xticks(rotation=90)
                plt.title('Counts for {} \n class {}'.format(feature, cat))
                plt.ylabel('count')
                plt.tight_layout(2)

                if save_fig:
                    plt.savefig('fig_catbox_{}'.format(feature))


    #Drop the dummy_count column from data
    data.drop(['dummy_count'], axis=1, inplace = True)


def class_count(data=None, cat_features=None, plot=False, save_fig=False):
    '''
    Displays the number of classes in a categorical feature.

    Parameters:
    
    data: Pandas DataFrame or Series
        Dataset for plotting.
    cat_features: Scalar, array, or list. 
        The categorical features in the dataset, if None, 
        we try to infer the categorical columns from the dataframe.
    plot: bool, Default False.
        Plots the class counts as a barplot
    save_fig: bool, Default False.
        Saves the plot to the current working directory.
    '''

    if data is None:
        raise ValueError("data: Expecting a DataFrame or Series, got 'None'")

    if cat_features is None:
        cat_features = structdata.get_cat_feats(data)

                        

    for feature in cat_features:
        print('Class Count for', feature)
        display(pd.DataFrame(data[feature].value_counts()))

    if plot:
        countplot(data, cat_features, save_fig=save_fig)



def scatterplot(data=None, num_features=None, target=None, separate_by=None, fig_size=(10,10), save_fig=False):
    '''
    Makes a scatter plot of numerical features against a numerical target.
    Helps to show the relationship between features.
    
    Parameters
    ------------
    
    data : DataFrame, array, or list of arrays.
        The data to plot.
    num_features: int/floats, scalar, array, or list. 
        The numeric features in the dataset, if not provided, 
        we try to infer the numeric columns from the dataframe.
    target: int/float, scalar, array or list.
        Numerical target feature to plot against.
    separate_by: str, default None.
        The feature used to seperate the plot. Called hue in seaborn.
    fig_size: tuple, Default (10,10)
        The size of the figure object.
    save_fig: bool, Default False.
        Saves the plot to the current working directory'''

    if data is None:
        raise ValueError("data: Expecting a DataFrame or Series, got 'None'")

    if separate_by is None:
        pass
    elif separate_by not in data.columns:
            raise ValueError("{} not found in data columns".format(separate_by))

    
    if target is None:
        raise ValueError('Target value cannot be None')

    if num_features is None:
        num_features = structdata.get_num_feats(data)

    for feature in num_features:
        fig = plt.figure(figsize=fig_size) # define plot area
        ax = fig.gca() # define axis  
        sns.scatterplot(x=feature, y=target, data=data, hue=separate_by)
        ax.set_title("Scatter Plot of '{}' vs. '{}' \n Separated by: '{}'".format(feature, target, separate_by))
        if save_fig:
            plt.savefig('fig_scatterplot_{}'.format(feature))
