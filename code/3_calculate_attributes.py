# -------------------------------------------------------
# In this file we build the attributes to be used for learning
# for the restaurants only
# the variable holding the attributes is "business_attributes"
# -------------------------------------------------------

import statistics as st

import pandas as pd

import pretreatment.utils as ut

# load data
business_rest = pd.read_pickle(ut.datapath + 'business_rest')
tip_rest = pd.read_pickle(ut.datapath + 'tip_rest')
review_rest = pd.read_pickle(ut.datapath + 'review_rest')
user_rest = pd.read_pickle(ut.datapath + 'user_rest')
checkin_rest = pd.read_pickle(ut.datapath + 'checkin_rest')

print("----------")
print("Restaurant data:")
print("----------")
print("Buisnesses", len(business_rest))
print("Tips", len(tip_rest))
print("Users", len(review_rest))
print("Review", len(user_rest))
print("checkin_rest", len(checkin_rest))

start_year = 2010
end_year = 2017
review_rest = review_rest[(review_rest.year >= start_year) & (review_rest.year <= end_year)]
business_rest = business_rest[business_rest.business_id.isin(review_rest.business_id)]
tip_rest = tip_rest[tip_rest.business_id.isin(business_rest.business_id)]
user_rest = user_rest[user_rest.user_id.isin(review_rest.user_id)]
checkin_rest = checkin_rest[checkin_rest.business_id.isin(business_rest.business_id)]

print("----------")
print("Restaurant data (" + str(start_year) + "-" + str(end_year) + "):")
print("----------")
print("Buisnesses", len(business_rest))
print("Tips", len(tip_rest))
print("Users", len(review_rest))
print("Review", len(user_rest))
print("checkin_rest", len(checkin_rest))

# stars
# review_count
# is_open (CLASS)
business_attributes = business_rest[['business_id', 'stars', 'review_count', 'is_open']].copy()

# good_reviews_count
good_reviews_by_business = review_rest[review_rest.stars >= 3].groupby(["business_id"]).size().reset_index(
    name='good_reviews_count')
business_attributes = pd.merge(business_attributes, good_reviews_by_business, how="left", on="business_id")
business_attributes['good_reviews_count'].fillna(0, inplace=True)

# bad_reviews_count
bad_reviews_by_business = review_rest[review_rest.stars < 3].groupby(["business_id"]).size().reset_index(
    name='bad_reviews_count')
business_attributes = pd.merge(business_attributes, bad_reviews_by_business, how="left", on="business_id")
business_attributes['bad_reviews_count'].fillna(0, inplace=True)

# good_reviews_ratio
business_attributes['good_reviews_ratio'] = business_attributes.good_reviews_count / business_attributes.review_count

# bad_reviews_ratio
business_attributes['bad_reviews_ratio'] = business_attributes.bad_reviews_count / business_attributes.review_count

# good_useful_review_count
good_usefull_reviews_by_business = review_rest[
    (review_rest.stars >= 3) & ((review_rest.useful > 1) | (review_rest.funny > 1) | (
            review_rest.cool > 1))].groupby(["business_id"]).size().reset_index(
    name='good_useful_review_count')

business_attributes = pd.merge(business_attributes, good_usefull_reviews_by_business, how="left", on="business_id")
business_attributes['good_useful_review_count'].fillna(0, inplace=True)

# bad_useful_review_count
bad_usefull_reviews_by_business = review_rest[
    (review_rest.stars < 3) & ((review_rest.useful > 1) | (review_rest.funny > 1) | (
            review_rest.cool > 1))].groupby(["business_id"]).size().reset_index(
    name='bad_useful_review_count')

business_attributes = pd.merge(business_attributes, bad_usefull_reviews_by_business, how="left", on="business_id")
business_attributes['bad_useful_review_count'].fillna(0, inplace=True)

# good_elite_review_count
elite_users = user_rest[(user_rest.elite != "") & (user_rest.review_count >= 100) & (user_rest.useful >= 100)]
elite_users_reviews = pd.merge(elite_users, review_rest, how="left", on="user_id")
good_elite_reviews_by_business = elite_users_reviews[elite_users_reviews.stars >= 3].groupby(
    ["business_id"]).size().reset_index(
    name='good_elite_review_count')

business_attributes = pd.merge(business_attributes, good_elite_reviews_by_business, how="left", on="business_id")
business_attributes['good_elite_review_count'].fillna(0, inplace=True)

# bad_elite_review_count
bad_elite_reviews_by_business = elite_users_reviews[elite_users_reviews.stars < 3].groupby(
    ["business_id"]).size().reset_index(
    name='bad_elite_review_count')

business_attributes = pd.merge(business_attributes, bad_elite_reviews_by_business, how="left", on="business_id")
business_attributes['bad_elite_review_count'].fillna(0, inplace=True)

# tips_count
tips_count_by_business = tip_rest.groupby(["business_id"]).size().reset_index(name='tips_count')
business_attributes = pd.merge(business_attributes, tips_count_by_business, how="left", on="business_id")
business_attributes['tips_count'].fillna(0, inplace=True)

# tips_usefull_count
tips_useful_count_by_business = tip_rest[tip_rest.compliment_count > 0].groupby(["business_id"]).size().reset_index(
    name='tips_usefull_count')
business_attributes = pd.merge(business_attributes, tips_useful_count_by_business, how="left", on="business_id")
business_attributes['tips_usefull_count'].fillna(0, inplace=True)

# tips_elite_count
elite_users_tips = pd.merge(elite_users, tip_rest, how="left", on="user_id")
tips_elite_count_by_business = elite_users_tips.groupby(["business_id"]).size().reset_index(name='tips_elite_count')
business_attributes = pd.merge(business_attributes, tips_elite_count_by_business, how="left", on="business_id")
business_attributes['tips_elite_count'].fillna(0, inplace=True)

# Zone
business_rest["zone"] = ""
business_rest["zone"] = business_rest["postal_code"].str.split(" ", n=1, expand=True)
business_attributes = pd.merge(business_attributes, business_rest[['business_id', 'zone']], how="left",
                               on="business_id")

# category_zone_inter
business_category_list = pd.DataFrame(business_rest.categories.str.split(',').tolist(),
                                      index=business_rest.business_id).stack().reset_index(name='category')
business_category_list = business_category_list[~business_category_list.category.str.contains('Restaurants')]
business_category_list = business_category_list[~business_category_list.category.str.contains('Food')]
business_category_list['category'] = business_category_list['category'].str.strip()

business_category_full = pd.merge(business_rest, business_category_list, how="left", on="business_id")
city_category = business_category_full.groupby(["category"]).size().reset_index(name='count')
zone_category = business_category_full.groupby(["zone", "category"]).size().reset_index(name='count')

business_category_zone_inter = pd.merge(business_category_full, zone_category, how="left", on=['zone', 'category'])
business_category_zone_inter = business_category_zone_inter.groupby(["business_id"])["count"].sum().reset_index(
    name='category_zone_inter')
business_attributes = pd.merge(business_attributes, business_category_zone_inter, how="left", on="business_id")

# category_city_inter
business_category_city_inter = pd.merge(business_category_full, city_category, how="left", on=['category'])
business_category_city_inter = business_category_city_inter.groupby(["business_id"])["count"].sum().reset_index(
    name='category_city_inter')
business_attributes = pd.merge(business_attributes, business_category_city_inter, how="left", on="business_id")

# total_opening_hours
business_rest["total_opening_hours"] = business_rest.apply(ut.calc_total_open_hours, axis=1)
business_attributes = pd.merge(business_attributes, business_rest[['business_id', 'total_opening_hours']], how="left",
                               on="business_id")

# is_open_saturday , is_open_sunady, is_open_Monday
business_rest["is_open_saturday"] = business_rest.apply(ut.is_open_week_day, args=("Saturday",), axis=1)
business_rest["is_open_sunday"] = business_rest.apply(ut.is_open_week_day, args=("Sunday",), axis=1)
business_rest["is_open_monday"] = business_rest.apply(ut.is_open_week_day, args=("Monday",), axis=1)

business_attributes = pd.merge(business_attributes,
                               business_rest[['business_id', 'is_open_saturday', 'is_open_sunday', 'is_open_monday']],
                               how="left", on="business_id")

# std_stars
review_business_year = review_rest.groupby(['business_id', 'year'])['stars'].mean().reset_index(name='stars_year')
review_business_std = review_business_year.groupby('business_id')['stars_year'].std().reset_index(name='std_stars')
review_business_std['std_stars'].fillna(0, inplace=True)

business_attributes = pd.merge(business_attributes, review_business_std, how="left", on="business_id")

# trend_stars
review_business_first_year = review_business_year.groupby(['business_id'])['year'].min()
review_business_last_year = review_business_year.groupby(['business_id'])['year'].max()
review_business_first_year = pd.merge(review_business_first_year, review_business_year, on=['business_id', 'year'],
                                      how='left')
review_business_last_year = pd.merge(review_business_last_year, review_business_year, on=['business_id', 'year'],
                                     how='left')
review_business_trend = pd.merge(review_business_first_year, review_business_last_year, on=['business_id'], how='left')
review_business_trend['trend_stars'] = review_business_trend['stars_year_y'] - review_business_trend['stars_year_x']
business_attributes = pd.merge(business_attributes, review_business_trend[['business_id', 'trend_stars']],
                               on=['business_id'], how='left')

# # checkin_count
# checkin_list = pd.DataFrame(checkin_rest.date.str.split(',').tolist(),
#                             index=checkin_rest.business_id).stack().reset_index(name='date_checkin')
# checkin_list['date_checkin'] = checkin_list['date_checkin'].str.strip()
# checkin_list["date_checkin_date_only"] = pd.to_datetime(checkin_list["date_checkin"], format='%Y-%m-%d')
# checkin_list['year'] = checkin_list.date_checkin_date_only.dt.year
# checkin_count_year = checkin_list.groupby(['business_id', 'year']).size().reset_index(name='checkin_count_year')
# checkin_count = checkin_list.groupby(['business_id']).size().reset_index(name='checkin_count')
#
# business_attributes = pd.merge(business_attributes, checkin_count, on='business_id', how='left')
# business_attributes['checkin_count'].fillna(0, inplace=True)
#
# # average_checkin
# average_checkin = checkin_count_year.groupby(['business_id'])['checkin_count_year'].mean().reset_index(
#     name='average_checkin')
# business_attributes = pd.merge(business_attributes, average_checkin, on='business_id', how='left')
# business_attributes['average_checkin'].fillna(0, inplace=True)
#
# # std_checkin
# std_checkin = checkin_count_year.groupby(['business_id'])['checkin_count_year'].std().reset_index(name='std_checkin')
# business_attributes = pd.merge(business_attributes, std_checkin, on='business_id', how='left')
# business_attributes['std_checkin'].fillna(0, inplace=True)

business_attributes['checkin_count'] = 0
business_attributes['average_checkin'] = 0
business_attributes['std_checkin'] = 0

for index, business in business_attributes.iterrows():
    date = checkin_rest[checkin_rest.business_id == business.business_id]
    if len(date) == 0:
        continue
    date = date.iloc[0]['date']
    checkins = []
    for year in range(2004, 2019):
        checkin_count = date.count(str(year))
        if checkin_count > 0:
            checkins.append(checkin_count)

    business_attributes.at[index, 'checkin_count'] = sum(checkins)
    business_attributes.at[index, 'average_checkin'] = st.mean(checkins)
    if len(checkins) > 1:
        business_attributes.at[index, 'std_checkin'] = st.stdev(checkins)

# categories
business_categories = business_rest["categories"].str.split('\s*,\s*', expand=True).stack()
business_categories = pd.crosstab(business_categories.index.get_level_values(0), business_categories.values).iloc[:, 1:]
business_categories.drop(columns=["Restaurants"])
business_categories.drop(columns=["Food"])
business_attributes = pd.concat([business_attributes, business_categories.reindex(business_attributes.index)], axis=1)

# attributes
business_rest["RestaurantsTakeOut"] = business_rest.apply(ut.get_attribute, args=("RestaurantsTakeOut", 0,), axis=1)
business_rest["RestaurantsGoodForGroups"] = business_rest.apply(ut.get_attribute, args=("RestaurantsGoodForGroups", 0,),
                                                                axis=1)
business_rest["RestaurantsReservations"] = business_rest.apply(ut.get_attribute, args=("RestaurantsReservations", 0,),
                                                               axis=1)
business_rest["RestaurantsPriceRange2"] = business_rest.apply(ut.get_attribute, args=("RestaurantsPriceRange2", 0,),
                                                              axis=1)
business_rest["OutdoorSeating"] = business_rest.apply(ut.get_attribute, args=("OutdoorSeating", 0,), axis=1)
business_rest["GoodForKids"] = business_rest.apply(ut.get_attribute, args=("GoodForKids", 0,), axis=1)
business_rest["RestaurantsDelivery"] = business_rest.apply(ut.get_attribute, args=("RestaurantsDelivery", 0,), axis=1)
business_attributes = pd.merge(business_attributes, business_rest[
    ['business_id', 'RestaurantsTakeOut', 'RestaurantsGoodForGroups', 'RestaurantsReservations',
     'RestaurantsPriceRange2', 'OutdoorSeating', 'GoodForKids', 'RestaurantsDelivery']], on='business_id', how='left')

# chain
business_rest["is_chain"] = 0
for index, business in business_rest.iterrows():
    count = len(business_rest[business_rest.name == business_rest.at[index, 'name']])
    if count > 1:
        business['is_chain'] = 1
    else:
        business['is_chain'] = 0

    business_rest.at[index, 'is_chain'] = business['is_chain']

business_attributes = pd.merge(business_attributes, business_rest[['business_id', 'is_chain']], on='business_id',
                               how='left')

# zone_number_restaurants
zone_number_restaurants = business_rest.groupby("zone").size().reset_index(name='zone_count')
business_attributes = pd.merge(business_attributes, zone_number_restaurants[['zone', 'zone_count']], on='zone',
                               how='left')

# business_first_year
business_first_year = review_rest.groupby(["business_id"])['year'].min().reset_index(name='first_year')
business_attributes = pd.merge(business_attributes, business_first_year, how="left", on="business_id")

# business_first_year_count
business_count_first_year = business_attributes.groupby(["first_year"]).size().reset_index(
    name='business_first_year_count')
business_attributes = pd.merge(business_attributes, business_count_first_year, how="left", on="first_year")

print(business_attributes)

print("attributes calculated successfully")
business_attributes.to_pickle('../../data/preprocess/business_attributes')
