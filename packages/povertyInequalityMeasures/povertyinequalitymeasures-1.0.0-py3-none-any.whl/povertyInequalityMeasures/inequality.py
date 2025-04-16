import pandas as pd

def get_gini(data,target_col,weight_col):
    nrows = data.shape[0] # count of rows
    if nrows == 0:
        return 0.0
    gini=0.0
    #sort by target column - this could be income, expenditure etc
    sorted_data = data.sort_values(by=target_col).reset_index(drop=True)
    #print(sorted_data)
    #now do accuumulation for the thing you are sorting, because this is all about cumulative income/expenditure/whatever
    #baseline the first row
    sorted_data.loc[0,"POPN_ACCUM"] = sorted_data.loc[0,weight_col]
    sorted_data.loc[0, "TARGET_ACCUM"] = sorted_data.loc[0, target_col]*sorted_data.loc[0, weight_col]

    #now start accumulating 
    for i in range(1,nrows):
        sorted_data.loc[i,"POPN_ACCUM"] = sorted_data.loc[i-1,"POPN_ACCUM"] + sorted_data.loc[i, weight_col]
        sorted_data.loc[i, "TARGET_ACCUM"] = sorted_data.loc[i-1, "TARGET_ACCUM"] + sorted_data.loc[i, target_col]*sorted_data.loc[i, weight_col]

    #print(sorted_data)
    # now work out the gini
    lastr = sorted_data.iloc[-1:] # last entry, which contains total of the target and total population
    total_area = lastr["TARGET_ACCUM"] * lastr["POPN_ACCUM"] 
    lorenz_area = sorted_data.loc[0,"POPN_ACCUM"] * sorted_data.loc[0,"TARGET_ACCUM"] #initialize with the first (0th) value
    for i in range(1,nrows):
        lorenz_area +=  (sorted_data.loc[i,"POPN_ACCUM"]-sorted_data.loc[i-1,"POPN_ACCUM"]) * (sorted_data.loc[i,"TARGET_ACCUM"] + sorted_data.loc[i-1,"TARGET_ACCUM"])
            
    #print(total_area, lorenz_area)
    gini = (total_area-lorenz_area) / total_area
    return float(round(gini.iloc[0],2))

def get_palma(data,target_col,weight_col):
    nrows = data.shape[0] # count of rows
    if nrows == 0:
        return 0.0
    palma=0.0
    #sort by target column - this could be income, expenditure etc
    sorted_data = data.sort_values(by=target_col).reset_index(drop=True)
    #print(sorted_data)
    #now do accuumulation for the thing you are sorting, because this is all about cumulative income/expenditure/whatever
    
    #baseline the first row
    sorted_data.loc[0,"POPN_ACCUM"] = sorted_data.loc[0,weight_col] # population accumulator
    sorted_data.loc[0, "TARGET_ACCUM"] = sorted_data.loc[0, target_col]*sorted_data.loc[0, weight_col]  # the thing you are measuring, accumulated
    sorted_data.loc[0, "TARGET_WEIGHTED"] = sorted_data.loc[0, target_col]*sorted_data.loc[0, weight_col] #the thing you are measuring, but weighted


    #now start accumulating 
    for i in range(1,nrows):
        sorted_data.loc[i,"POPN_ACCUM"] = sorted_data.loc[i-1,"POPN_ACCUM"] + sorted_data.loc[i, weight_col]
        sorted_data.loc[i, "TARGET_ACCUM"] = sorted_data.loc[i-1, "TARGET_ACCUM"] + sorted_data.loc[i, target_col]*sorted_data.loc[i, weight_col]
        sorted_data.loc[i, "TARGET_WEIGHTED"] = sorted_data.loc[i, target_col]*sorted_data.loc[i, weight_col]
    #print(sorted_data)

    #now work out the palma
    sorted_data['bins'] = pd.cut(x=sorted_data['POPN_ACCUM'],bins=10) #split into ten bins by population
    #print(sorted_data)
    accumulated_target_per_decile = sorted_data.groupby(['bins'], observed=False)['TARGET_ACCUM'].agg(['max'])
    #print (accumulated_income_per_decile)
    target_per_decile = (sorted_data.groupby(['bins'],observed=False)['TARGET_WEIGHTED'].agg(['sum']))  
    #print(income_per_decile)
    print(type(target_per_decile))
    palma = float(target_per_decile.iloc[9].iloc[0]) / float(accumulated_target_per_decile.iloc[3].iloc[0])
    # in other words the amount that the top decile has of the thing you are measuring divided by the amount that the bottom 4 deciles have
    return round(palma,2)
    # also, not to future self: that strange double iloc notation was used to get rid of this warning:
    # FutureWarning: Calling float on a single element Series is deprecated and will raise a TypeError in the future. Use float(ser.iloc[0]) instead
    # was following this article: https://stackoverflow.com/questions/76256618/how-to-deal-with-futurewarning-regarding-applying-int-to-a-series-with-one-item#76848560
    # it works, but I don't understand why!
    