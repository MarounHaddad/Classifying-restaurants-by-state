import pandas as pd
import predictclosure.models_utils as ut

# load data
business_attributes_final = pd.read_pickle('../../data/preprocess/business_attributes_final')

x = business_attributes_final.copy()
y = x["is_closed"]
x = x.drop('is_closed', axis=1)
captions = x.columns
x = ut.normalize_data(x)

# Chi2 features
# x = ut.feature_select("chi2",150,x, y,captions)

# mutual info features
x = ut.feature_select("mutual_info",150,x, y,captions)

