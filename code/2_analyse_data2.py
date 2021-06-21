# -------------------------------------------------------
# In this file we perform  analysis on the data
# -------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pretreatment.utils as ut

# load data
business_rest = pd.read_pickle(ut.datapath + 'business_rest')
tip_rest = pd.read_pickle(ut.datapath + 'tip_rest')
review_rest = pd.read_pickle(ut.datapath + 'review_rest')
user_rest = pd.read_pickle(ut.datapath + 'user_rest')
checkin_rest = pd.read_pickle(ut.datapath + 'checkin_rest')

business_rest["zone"] = ""
business_rest["zone"] = business_rest["postal_code"].str.split(" ", n=1, expand=True)

print("-------------")

# Restaurant Categories
print("Nombre Total de Categories:320")

# one hot encoding Categories
business_categories = business_rest["categories"].str.split('\s*,\s*', expand=True).stack()
# business_categories.to_csv('../../data/preprocess/business_categories.csv')
business_categories = pd.crosstab(business_categories.index.get_level_values(0), business_categories.values).iloc[:, 1:]
business_categories.drop(columns=["Restaurants"])
business_categories.drop(columns=["Food"])
business_categories = pd.concat([business_rest, business_categories], axis=1)

# Categories list
business_category_list = pd.DataFrame(business_rest.categories.str.split(',').tolist(),
                                      index=business_rest.business_id).stack().reset_index(name='category')
business_category_list = business_category_list[~business_category_list.category.str.contains('Restaurants')]
business_category_list = business_category_list[~business_category_list.category.str.contains('Food')]
business_category_list['category'] = business_category_list['category'].str.strip()

business_category_full = pd.merge(business_rest, business_category_list, how="left", on="business_id")
zone_category = business_category_full.groupby(
    ["zone", "category"]).size().reset_index(name='count')
zone_open_category = business_category_full[business_category_full.is_open == 1].groupby(
    ["zone", "category"]).size().reset_index(name='count_open')
zone_close_category = business_category_full[business_category_full.is_open == 0].groupby(
    ["zone", "category"]).size().reset_index(name='count_closed')

print("-------------")
print("Category par zone Top 20 ")
print(zone_category.nlargest(20, 'count'))

print("-------------")
print("Category par zone Top 20  (Restaurants Ouverts)")
print(zone_open_category.nlargest(20, 'count_open'))

print("-------------")
print("Category par zone Top 20  (Restaurants Fermés)")
print(zone_close_category.nlargest(20, 'count_closed'))

print("-------------")
zone_name = "H2Y"

zone_H_category = business_category_full[business_category_full.zone == zone_name].groupby(
    ["zone", "category"]).size().reset_index(name='count_open')
zone_H_open_category = business_category_full[
    (business_category_full.zone == zone_name) & (business_category_full.is_open == 1)].groupby(
    ["zone", "category"]).size().reset_index(name='count_open')
zone_H_close_category = business_category_full[
    (business_category_full.zone == zone_name) & (business_category_full.is_open == 0)].groupby(
    ["zone", "category"]).size().reset_index(name='count_closed')

zone_H_businesses = business_category_full[business_category_full.zone == zone_name]

print("Nombre Total de Categories:", len(zone_H_category))
print("Nombre Total de Categories Ouvertes:", len(zone_H_open_category))
print("Nombre Total de Categories Fermées:", len(zone_H_close_category))
print("Categories dans Fermées Seulment", len(
    zone_H_close_category.merge(zone_H_open_category, indicator='i', how='outer').query('i == "left_only"').drop('i',
                                                                                                                 1)))

print("-------------")
print("Nombre Total Restaurant Ouverts par Categories pour:", zone_name)
print(zone_H_open_category.nlargest(10, 'count_open'))
print("-------------")
print("Nombre Total Restaurant Fermés par Categories pour:", zone_name)
print(zone_H_close_category.nlargest(10, 'count_closed'))

zone_H_open_close = pd.merge(zone_H_open_category.nlargest(10, 'count_open'),
                             zone_H_close_category.nlargest(10, 'count_closed'), how="outer", on="category")
zone_H_open_close.plot.bar(x="category", rot=45, alpha=0.75)
plt.xlabel("")
plt.show()
print("-------------")

# Correlation Category Zone City with Number of Stars
city_category = business_category_full.groupby(["category"]).size().reset_index(name='count')
zone_category = business_category_full.groupby(["zone", "category"]).size().reset_index(name='count')

business_category_zone_inter = pd.merge(business_category_full, zone_category, how="left", on=['zone', 'category'])
business_category_zone_inter = business_category_zone_inter.groupby(["business_id"])["count"].sum().reset_index(
    name='category_zone_inter')
zone_H_businesses = pd.merge(zone_H_businesses, business_category_zone_inter, how="left", on="business_id")

business_category_city_inter = pd.merge(business_category_full, city_category, how="left", on=['category'])
business_category_city_inter = business_category_city_inter.groupby(["business_id"])["count"].sum().reset_index(
    name='category_city_inter')
zone_H_businesses = pd.merge(zone_H_businesses, business_category_city_inter, how="left", on="business_id")

print("Correlation entre Uniqueness zone vs ville:",
      round(ut.pearson_correlation(zone_H_businesses.category_city_inter, zone_H_businesses.category_zone_inter), 3))
print("Correlation entre zone Uniqueness et nombre de stars:",
      round(ut.pearson_correlation(zone_H_businesses.stars, zone_H_businesses.category_zone_inter), 3))
print("Correlation entre ville Uniqueness et nombre de stars:",
      round(ut.pearson_correlation(zone_H_businesses.stars, zone_H_businesses.category_city_inter), 3))
print("-------------")

ut.save_all_restaurants_to_kml(business_rest[business_rest.zone==zone_name],"restaurants_H2Y")

# Trend Stars Top Vs Bottom Businesses
first_year_business = review_rest.groupby(["business_id"])['year'].min().reset_index(name='first_year')
business_rest = pd.merge(business_rest, first_year_business, how="left", on="business_id")

last_year_business = review_rest.groupby(["business_id"])['year'].max().reset_index(name='last_year')
business_rest = pd.merge(business_rest, last_year_business, how="left", on="business_id")

bottom_business_closed = business_rest[(business_rest.is_open == 0) & (business_rest.stars <= 2)]
bottom_business_closed_reviews_year = \
    pd.merge(bottom_business_closed, review_rest[review_rest.year > 2011], how="left", on="business_id").groupby(
        ["year"])[
        "stars_y"].mean().reset_index(name='bottom')

top_business_open = business_rest[(business_rest.is_open == 1) & (business_rest.stars >= 4)]
top_business_open_reviews_year = \
    pd.merge(top_business_open, review_rest[review_rest.year > 2011], how="left", on="business_id").groupby(["year"])[
        "stars_y"].mean().reset_index(name='top')

plt.plot('year', 'bottom', data=bottom_business_closed_reviews_year, marker='o', markerfacecolor='red', markersize=12,
         color='pink', linewidth=4)
plt.plot('year', 'top', data=top_business_open_reviews_year, marker='o', markerfacecolor='blue', markersize=12,
         color='skyblue', linewidth=4)
plt.legend()
plt.show()

# Trend Stars Open Vs Closed Businesses
business_closed = business_rest[(business_rest.is_open == 0)]
business_closed_reviews_year = \
    pd.merge(business_closed, review_rest[review_rest.year > 2011], how="left", on="business_id").groupby(["year"])[
        "stars_y"].mean().reset_index(name='fermé')

business_open = business_rest[(business_rest.is_open == 1)]
business_open_reviews_year = \
    pd.merge(business_open, review_rest[review_rest.year > 2011], how="left", on="business_id").groupby(["year"])[
        "stars_y"].mean().reset_index(name='ouvert')

plt.plot('year', 'fermé', data=business_closed_reviews_year, marker='o', markerfacecolor='red', markersize=12,
         color='pink', linewidth=4)
plt.plot('year', 'ouvert', data=business_open_reviews_year, marker='o', markerfacecolor='blue', markersize=12,
         color='skyblue', linewidth=4)
plt.legend()
plt.show()

# Correlation open vs std_stars
review_business_year = review_rest.groupby(['business_id', 'year'])['stars'].mean().reset_index(name='stars_year')
review_business_std = review_business_year.groupby('business_id')['stars_year'].std().reset_index(name='std_stars')

business_rest = pd.merge(business_rest, review_business_std, how="left", on="business_id")
business_rest['std_stars'].fillna(0, inplace=True)
print("Correlation entre stars et la stabilité des stars",
      ut.pearson_correlation(business_rest.stars, business_rest.std_stars))
print("Correlation entre ouvert/fermé et la stabilité des stars",
      ut.pearson_correlation(business_rest.is_open, business_rest.std_stars))
print("Correlation entre ouvert/fermé et stars ", ut.pearson_correlation(business_rest.is_open, business_rest.stars))
print("-------------")
# Correlation open vs stars trend
review_business_first_year = review_business_year.groupby(['business_id'])['year'].min()
review_business_last_year = review_business_year.groupby(['business_id'])['year'].max()
review_business_first_year = pd.merge(review_business_first_year, review_business_year, on=['business_id', 'year'],
                                      how='left')
review_business_last_year = pd.merge(review_business_last_year, review_business_year, on=['business_id', 'year'],
                                     how='left')
review_business_trend = pd.merge(review_business_first_year, review_business_last_year, on=['business_id'], how='left')
review_business_trend['trend_stars'] = review_business_trend['stars_year_y'] - review_business_trend['stars_year_x']
business_rest = pd.merge(business_rest, review_business_trend[['business_id', 'trend_stars']], on=['business_id'],
                         how='left')

print("Correlation entre trend des stars et les stars",
      ut.pearson_correlation(business_rest.stars, business_rest.trend_stars))
print("Correlation entre trend des stars et ouvert/fermé",
      ut.pearson_correlation(business_rest.is_open, business_rest.trend_stars))

checkin_list = pd.DataFrame(checkin_rest.date.str.split(',').tolist(),
                            index=checkin_rest.business_id).stack().reset_index(name='date_checkin')
checkin_list['date_checkin'] = checkin_list['date_checkin'].str.strip()
checkin_list["date_checkin_date_only"] = pd.to_datetime(checkin_list["date_checkin"], format='%Y-%m-%d')
checkin_list['year'] = checkin_list.date_checkin_date_only.dt.year
checkin_count_year = checkin_list.groupby(['business_id', 'year']).size().reset_index(name='checkin_count_year')
checkin_count = checkin_list.groupby(['business_id']).size().reset_index(name='checkin_count')

business_rest = pd.merge(business_rest, checkin_count, on='business_id', how='left')
business_rest['checkin_count'].fillna(0, inplace=True)

# average_checkin
average_checkin = checkin_count_year.groupby(['business_id'])['checkin_count_year'].mean().reset_index(
    name='average_checkin')
business_rest = pd.merge(business_rest, average_checkin, on='business_id', how='left')
business_rest['average_checkin'].fillna(0, inplace=True)

# std_checkin
std_checkin = checkin_count_year.groupby(['business_id'])['checkin_count_year'].std().reset_index(name='std_checkin')
business_rest = pd.merge(business_rest, std_checkin, on='business_id', how='left')
business_rest['std_checkin'].fillna(0, inplace=True)
print("-------------")
print("Correlation entre nombre checkin et les stars",
      ut.pearson_correlation(business_rest.stars, business_rest.checkin_count))
print("Correlation entre moyenne checkin et les stars",
      ut.pearson_correlation(business_rest.stars, business_rest.average_checkin))
print("Correlation entre  std checkin  et les stars",
      ut.pearson_correlation(business_rest.stars, business_rest.std_checkin))
print("-------------")
print("Correlation entre nombre checkin et ouvert/fermé",
      ut.pearson_correlation(business_rest.is_open, business_rest.checkin_count))
print("Correlation entre moyenne checkin et ouvert/fermé",
      ut.pearson_correlation(business_rest.is_open, business_rest.average_checkin))
print("Correlation entre std checkin et ouvert/fermé",
      ut.pearson_correlation(business_rest.is_open, business_rest.std_checkin))
print("-------------")
