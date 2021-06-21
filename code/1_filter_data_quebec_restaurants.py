# -------------------------------------------------------
# This file loads the json file (input data) into
# dataframes and filters Restaurants of Montreal Data
# -------------------------------------------------------

# Import Libraries
import pretreatment.utils as ut
import pandas as pd

# load files
user = ut.read_json('../../data/input/user.json')
tip = ut.read_json('../../data/input/tip.json')
review = ut.read_json('../../data/input/review.json')
business = ut.read_json('../../data/input/business.json')
checkin = ut.read_json('../../data/input/checkin.json')

# add year field to review and tip
review["date"] = pd.to_datetime(review["date"], format='%Y-%m-%d')
review['year'] = review.date.dt.year
tip["date"] = pd.to_datetime(tip["date"], format='%Y-%m-%d')
tip['year'] = tip.date.dt.year

# check number of records per dataframe
print("----------")
print("All data:")
print("----------")
print(len(business))
print(len(tip))
print(len(user))
print(len(review))
print(len(checkin))

# ----------------------------------------------
# Filter Data for Quebec only
business_QC = business[business.state == 'QC']
tip_QC = tip[tip.business_id.isin(business_QC.business_id)]
review_QC = review[review.business_id.isin(business_QC.business_id)]
user_QC = user[user.user_id.isin(review_QC.user_id)]
checkin_QC = checkin[checkin.business_id.isin(business_QC.business_id)]

# Save new dataframes
business_QC.to_pickle('../../data/qcrestaurants/business_QC')
tip_QC.to_pickle('../../data/qcrestaurants/tip_QC')
review_QC.to_pickle('../../data/qcrestaurants/review_QC')
user_QC.to_pickle('../../data/qcrestaurants/user_QC')
checkin_QC.to_pickle('../../data/qcrestaurants/checkin_QC')

# sanity check: read data from files
business_QC = pd.read_pickle('../../data/qcrestaurants/business_QC')
tip_QC = pd.read_pickle('../../data/qcrestaurants/tip_QC')
review_QC = pd.read_pickle('../../data/qcrestaurants/review_QC')
user_QC = pd.read_pickle('../../data/qcrestaurants/user_QC')

# print number of records for Quebec data
print("----------")
print("Quebec data:")
print("----------")
print("Buisnesses", len(business_QC))
print("Tips", len(tip_QC))
print("Users", len(user_QC))
print("Review", len(review_QC))

# ----------------------------------------------
# Filter only restaurants in Quebec
business_rest = business_QC[business_QC['categories'].str.contains("Restaurants", case=False, na=False)]
tip_rest = tip_QC[tip_QC.business_id.isin(business_rest.business_id)]
review_rest = review_QC[review_QC.business_id.isin(business_rest.business_id)]
user_rest = user_QC[user_QC.user_id.isin(review_rest.user_id)]
checkin_rest = checkin_QC[checkin_QC.business_id.isin(business_rest.business_id)]

# Save new dataframes (for Quebec Restaurants)
business_rest.to_pickle('../../data/qcrestaurants/business_rest')
tip_rest.to_pickle('../../data/qcrestaurants/tip_rest')
review_rest.to_pickle('../../data/qcrestaurants/review_rest')
user_rest.to_pickle('../../data/qcrestaurants/user_rest')
checkin_rest.to_pickle('../../data/qcrestaurants/checkin_rest')

# sanity check: read data from files (for Quebec Restaurants)
business_rest = pd.read_pickle('../../data/qcrestaurants/business_rest')
tip_rest = pd.read_pickle('../../data/qcrestaurants/tip_rest')
review_rest = pd.read_pickle('../../data/qcrestaurants/review_rest')
user_rest = pd.read_pickle('../../data/qcrestaurants/user_rest')
checkin_rest = pd.read_pickle('../../data/qcrestaurants/checkin_rest')


print("----------")
print("Restaurant data:")
print("----------")
print("Buisnesses",len(business_rest))
print("Tips",len(tip_rest))
print("Users",len(review_rest))
print("Review",len(user_rest))
print("checkin_rest",len(checkin_rest))
