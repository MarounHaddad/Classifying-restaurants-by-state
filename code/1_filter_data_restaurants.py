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
# Filter only restaurants
business_rest = business[business['categories'].str.contains("Restaurants", case=False, na=False)]
tip_rest = tip[tip.business_id.isin(business_rest.business_id)]
review_rest = review[review.business_id.isin(business_rest.business_id)]
user_rest = user[user.user_id.isin(review_rest.user_id)]
checkin_rest = checkin[checkin.business_id.isin(business_rest.business_id)]

# Save new dataframes (for Quebec Restaurants)
business_rest.to_pickle('../../data/restaurants/business_rest')
tip_rest.to_pickle('../../data/restaurants/tip_rest')
review_rest.to_pickle('../../data/restaurants/review_rest')
user_rest.to_pickle('../../data/restaurants/user_rest')
checkin_rest.to_pickle('../../data/restaurants/checkin_rest')

# sanity check: read data from files (for Quebec Restaurants)
business_rest = pd.read_pickle('../../data/restaurants/business_rest')
tip_rest = pd.read_pickle('../../data/restaurants/tip_rest')
review_rest = pd.read_pickle('../../data/restaurants/review_rest')
user_rest = pd.read_pickle('../../data/restaurants/user_rest')
checkin_rest = pd.read_pickle('../../data/restaurants/checkin_rest')

print("----------")
print("Restaurant data:")
print("----------")
print("Buisnesses",len(business_rest))
print("Tips",len(tip_rest))
print("Users",len(review_rest))
print("Review",len(user_rest))
print("checkin_rest",len(checkin_rest))
