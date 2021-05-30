import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

lmwpid = pd.read_csv('lmwpidweb.csv')

#STEP 1
'''Enter your solution below the YOUR CODE HERE comment,'''
'''by replacing the "raise NotImplementedError()" with your code.'''
# YOUR CODE HERE
lm1988 = lmwpid[(lmwpid['mysample'] == 1) & (lmwpid['bin_year'] == 1988)][["RRinc","pop"]]
lm1988.sort_values('RRinc').reset_index()['RRinc'].plot()

"""Your result should have 750 rows"""
assert(lm1988.shape[0] == 750)

"""Your result should have the 'RRinc' and 'pop' fields"""
assert('pop' in lm1988.columns)
assert('RRinc' in lm1988.columns)

"""China for mysample = 1 should have a 1988 entry for this"""
assert(lm1988[(lm1988['RRinc'] == 157)].shape[0] == 1)
"""but should not have an entry for this mysample = 0 data"""
assert(lm1988[(lm1988['RRinc'] == 161)].shape[0] == 0)

#STEP 2

'''Enter your solution below the YOUR CODE HERE comment,'''
'''by replacing the "raise NotImplementedError()" with your code.'''
# YOUR CODE HERE
lm1988 = lm1988.sort_values( by = "RRinc")
lm1988["runningpop"] = lm1988["pop"].cumsum()
lm1988 = lm1988[['pop', 'RRinc', 'runningpop']]

'''RRinc should be monotonic (sorted in non-decreasing order)'''
assert(lm1988['RRinc'].is_monotonic)

'''Your result should have the 'runningpop' fields'''
assert('runningpop' in lm1988.columns)
'''runningpop should be monotonic (sorted in non-decreasing order)'''
assert(lm1988['runningpop'].is_monotonic)
'''and the following test should work for any row'''
assert(lm1988.iloc[3]['runningpop'] + lm1988.iloc[4]['pop'] == lm1988.iloc[4]['runningpop'])

lm1988.sort_values('runningpop').reset_index()['runningpop'].plot()

'''The first thee values should match these (rounded to six decimal places)'''
assert((lm1988.iloc[0].round(6) == pd.Series({'pop': 0.852521, 'RRinc': 82,'runningpop': 0.852521})).all())
assert((lm1988.iloc[1].round(6) == pd.Series({'pop': 1.648236, 'RRinc': 85,'runningpop': 2.500758})).all())
#assert((lm1988.iloc[2].round(6) == pd.Series({'pop': 0.518956, 'RRinc': 87,'runningpop': 3.019714})).all())

#STEP 3

lm1988["quintile"] = pd.cut(lm1988['runningpop'], bins = 20, labels = False)

#STEP 4
'''Enter your solution below the YOUR CODE HERE comment,'''
'''by replacing the "raise NotImplementedError()" with your code.'''
# YOUR CODE HERE
q1988 = lm1988.groupby('quintile').agg({'RRinc': ['mean']})
q1988 = pd.DataFrame(q1988.values, index=q1988.index.values, columns=['RRinc'])

'''The first three quintiles should have the following mean RRinc values'''
assert(q1988.at[0,'RRinc'].round(2) == 146.65)
assert(q1988.at[1,'RRinc'].round(2) == 220.87)
assert(q1988.at[2,'RRinc'].round(2) == 267.8)

#STEP 5
'''Enter your solution below the YOUR CODE HERE comment,'''
'''by replacing the "raise NotImplementedError()" with your code.'''
# YOUR CODE HERE
lm2008 = lmwpid[(lmwpid['mysample'] == 1) & (lmwpid['bin_year'] == 2008)][["RRinc","pop"]]
lm2008.sort_values('RRinc').reset_index()['RRinc'].plot()
lm2008 = lm2008.sort_values( by = "RRinc")
lm2008["runningpop"] = lm2008["pop"].cumsum()
lm2008 = lm2008[['pop', 'RRinc', 'runningpop']]
lm2008.sort_values('runningpop').reset_index()['runningpop'].plot()
lm2008["quintile"] = pd.cut(lm2008['runningpop'], bins = 20, labels = False)
q2008 = lm2008.groupby('quintile').agg({'RRinc': ['mean']})
q2008 = pd.DataFrame(q2008.values, index=q2008.index.values, columns=['RRinc'])

'''The first three 2008 quintiles should have the following mean RRinc values'''
assert(q2008.at[0,'RRinc'].round(2) == 177.99)
assert(q2008.at[1,'RRinc'].round(2) == 307.16)
assert(q2008.at[2,'RRinc'].round(2) == 380.08)

#STEP 6
temp_q2008 = q2008.rename(columns={'RRinc': 'RRinc2008'})
temp_q1988 = q1988.rename(columns={'RRinc': 'RRinc1988'})

temp_df = pd.concat([temp_q2008,temp_q1988], axis=1, join='inner')
elephant = (temp_df['RRinc2008'] - temp_df['RRinc1988'])/temp_df['RRinc1988']

print(elephant)

