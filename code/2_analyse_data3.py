# -------------------------------------------------------
# In this file we perform  analysis on the data
# -------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pretreatment.utils as ut
import statistics as st

# load data
business_rest = pd.read_pickle(ut.datapath + 'business_rest')
tip_rest = pd.read_pickle(ut.datapath + 'tip_rest')
review_rest = pd.read_pickle(ut.datapath + 'review_rest')
user_rest = pd.read_pickle(ut.datapath + 'user_rest')
checkin_rest = pd.read_pickle(ut.datapath + 'checkin_rest')

# business_rest["zone"] = ""
# business_rest["zone"] = business_rest["postal_code"].str.split(" ", n=1, expand=True)
# business_rest["RestaurantsTakeOut"] = business_rest.apply(ut.get_attribute, args=("RestaurantsTakeOut", 0,), axis=1)
# business_rest["RestaurantsGoodForGroups"] = business_rest.apply(ut.get_attribute, args=("RestaurantsGoodForGroups", 0,),
#                                                                 axis=1)
# business_rest["RestaurantsReservations"] = business_rest.apply(ut.get_attribute, args=("RestaurantsReservations", 0,),
#                                                                axis=1)
# business_rest["RestaurantsPriceRange2"] = business_rest.apply(ut.get_attribute, args=("RestaurantsPriceRange2", 0,),
#                                                               axis=1)
# business_rest["OutdoorSeating"] = business_rest.apply(ut.get_attribute, args=("OutdoorSeating", 0,), axis=1)
# business_rest["GoodForKids"] = business_rest.apply(ut.get_attribute, args=("GoodForKids", 0,), axis=1)
# business_rest["RestaurantsDelivery"] = business_rest.apply(ut.get_attribute, args=("RestaurantsDelivery", 0,), axis=1)
#
# # chain
# business_rest["is_chain"] = 0
# for index, business in business_rest.iterrows():
#     count = len(business_rest[business_rest.name == business_rest.at[index, 'name']])
#     if count > 1:
#         business['is_chain'] = 1
#     else:
#         business['is_chain'] = 0
#
#     business_rest.at[index, 'is_chain'] = business['is_chain']
#
# print("-------------")


# checkin_count
# business_rest['checkin_count'] = 0
# business_rest['average_checkin'] = 0
# business_rest['std_checkin'] = 0
#
# for index, business in business_rest.iterrows():
#     date = checkin_rest[checkin_rest.business_id == business.business_id]
#     if len(date)==0:
#         continue
#     date = date.iloc[0]['date']
#     checkins = []
#     for year in range(2004, 2019):
#         checkin_count = date.count(str(year))
#         if checkin_count > 0:
#             checkins.append(checkin_count)
#
#     business_rest.at[index, 'checkin_count'] = sum(checkins)
#     business_rest.at[index, 'average_checkin'] = st.mean(checkins)
#     if len(checkins)>1:
#         business_rest.at[index, 'std_checkin'] = st.stdev(checkins)



print("-------------")
