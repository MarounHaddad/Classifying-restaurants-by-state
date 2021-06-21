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


print("Nombre Restaurant Total:", len(business_rest))
print("Nombre Tip Total:", len(tip_rest))
print("Nombre Utilisateur Total:", len(user_rest))
print("Nombre Revue Total:", len(review_rest))

print("-------------")

# print Open Vs Closed Restaurants
print("Nombre Restaurant Ouvert:", len(business_rest[business_rest.is_open == 1]))
print("Nombre Restaurant Fermé:", len(business_rest[business_rest.is_open == 0]))

print("-------------")

# print years
print("years", sorted(set(review_rest.year)))

print("-------------")

# save kml data
ut.save_all_restaurants_to_kml(business_rest, "restaurants_all_locations")
ut.save_closed_restaurants_to_kml(business_rest, "restaurants_closed_locations")

print("-------------")
# good vs bad reviews
print("Good Reviews (>=3 stars)", len(review_rest[review_rest.stars >= 3]))
print("Bad Reviews (<3 stars)", len(review_rest[review_rest.stars < 3]))
print("-------------")

# Number Of Closures per Year
last_year_business = review_rest.groupby(["business_id"])['year'].max().reset_index(name='last_year')
business_rest = pd.merge(business_rest, last_year_business, how="left", on="business_id")
last_year_business = business_rest[business_rest.is_open == 0].groupby(["last_year"]).size().reset_index(name='counts')

axes = last_year_business.plot(kind="bar", figsize=(10, 7), x="last_year", y='counts', color='r')
plt.xlabel('Année', axes=axes)
plt.ylabel('Nombre de Restaurants', axes=axes)
plt.title('Nombre de Fermetures par Année', axes=axes)
plt.show()
print()
print("Number of closures per year")
print(last_year_business)
print("-------------")

# Number Of Openings per Year
first_year_business = review_rest.groupby(["business_id"])['year'].min().reset_index(name='first_year')
business_rest = pd.merge(business_rest, first_year_business, how="left", on="business_id")
first_year_business = business_rest.groupby(["first_year"]).size().reset_index(name='counts')

axes = first_year_business.plot(kind="bar", figsize=(10, 7), x="first_year", y='counts')
plt.xlabel('Année', axes=axes)
plt.ylabel('Nombre de Restaurants', axes=axes)
plt.title('Nombre d\'Ouvertures par Année', axes=axes)
plt.show()
print()
print("Number of openings per year")
print(first_year_business)
print("-------------")

# Good Reviews Vs Bad Reviews / Open Restaurants Vs Closed
good_reviews_by_business = review_rest[review_rest.stars >= 3].groupby(["business_id"]).size().reset_index(
    name='good_reviews_count')
bad_reviews_by_business = review_rest[review_rest.stars < 3].groupby(["business_id"]).size().reset_index(
    name='bad_reviews_count')
business_rest = pd.merge(business_rest, good_reviews_by_business, how="left", on="business_id")
business_rest = pd.merge(business_rest, bad_reviews_by_business, how="left", on="business_id")
business_rest['good_reviews_count'].fillna(0, inplace=True)
business_rest['bad_reviews_count'].fillna(0, inplace=True)

business_star_year = pd.merge(business_rest, review_rest, how="left", on="business_id")
business_open_star_year = \
    business_star_year[(business_star_year.is_open == 1) & (business_star_year.year > 2007)].groupby(["year"])[
        "stars_y"].mean().reset_index(name='ouvert')

business_closed_star_year = \
    business_star_year[(business_star_year.is_open == 0) & (business_star_year.year > 2007)].groupby(["year"])[
        "stars_y"].mean().reset_index(name='fermé')

plt.plot('year', 'ouvert', data=business_open_star_year, marker='o', markerfacecolor='blue', markersize=12,
         color='skyblue', linewidth=4)
plt.plot('year', 'fermé', data=business_closed_star_year, marker='o', markerfacecolor='red', markersize=12,
         color='pink', linewidth=4)

plt.xlabel('Année')
plt.ylabel('stars')
plt.legend()
plt.show()

print("Moyenne Etoiles par Année (Ouvert)")
print(business_open_star_year)
print("Moyenne Etoiles par Année (Fermé)")
print(business_closed_star_year)

print("-------------")

# Good Reviews Vs Bad Reviews / Open Restaurants Vs Closed (only usefull reviews)
good_reviews_by_business = pd.merge(business_rest, review_rest, how="left", on="business_id")
business_open_star_year = \
    business_star_year[(business_star_year.is_open == 1) & (business_star_year.year > 2007) & (
            (business_star_year.useful > 1) | (business_star_year.funny > 1) | (
            business_star_year.cool > 1))].groupby(["year"])[
        "stars_y"].mean().reset_index(name='ouvert')

business_closed_star_year = \
    business_star_year[(business_star_year.is_open == 0) & (business_star_year.year > 2007) & (
            (business_star_year.useful > 1) | (business_star_year.funny > 1) | (
            business_star_year.cool > 1))].groupby(["year"])[
        "stars_y"].mean().reset_index(name='fermé')

plt.plot('year', 'ouvert', data=business_open_star_year, marker='o', markerfacecolor='blue', markersize=12,
         color='skyblue', linewidth=4)
plt.plot('year', 'fermé', data=business_closed_star_year, marker='o', markerfacecolor='red', markersize=12,
         color='pink', linewidth=4)

plt.xlabel('Année')
plt.ylabel('stars')
plt.legend()
plt.show()

print("Moyenne Etoiles Utiles par Année (Ouvert)")
print(business_open_star_year)
print("Moyenne Etoiles Utiles par Année (Fermé)")
print(business_closed_star_year)

print("-------------")

# Open/Closed per zone
business_rest["zone"] = ""
business_rest["zone"] = business_rest["postal_code"].str.split(" ", n=1, expand=True)
zone_isopen = business_rest[business_rest.is_open == 1].groupby(["zone"]).size().reset_index(name='nb_ouvert')
print("Nombre de Restaurants Ouvert par Zone")
print(zone_isopen)
zone_isclosed = business_rest[business_rest.is_open == 0].groupby(["zone"]).size().reset_index(name='nb_fermé')
print("Nombre de Restaurants Fermés par Zone")
print(zone_isclosed)

zone_perc = pd.merge(zone_isclosed, zone_isopen, how="left", on="zone")
zone_perc["perc_fermé"] = (zone_perc.nb_fermé / (zone_perc.nb_fermé + zone_perc.nb_ouvert)) * 100.00
zone_perc['nb_ouvert'].fillna(0, inplace=True)
zone_perc['nb_fermé'].fillna(0, inplace=True)
zone_perc['perc_fermé'].fillna(0, inplace=True)
zone_perc['total_restaurant'] = zone_perc.nb_fermé + zone_perc.nb_ouvert
zone_perc = zone_perc[zone_perc.total_restaurant > 5]
zone_perc = zone_perc.nlargest(20, 'total_restaurant')
zone_perc = zone_perc.sort_values(by='total_restaurant', ascending=True)

print(zone_perc)
plt.plot('zone', 'perc_fermé', data=zone_perc, marker='o', markerfacecolor='red', markersize=12,
         color='pink', linewidth=4)
plt.xlabel('zone')
plt.ylabel('Pourcentage Fermés')
plt.legend()

for x, y in zip(zone_perc.zone, zone_perc.perc_fermé):
    label = zone_perc[zone_perc.zone == x].iloc[0]["total_restaurant"].astype(int)
    plt.annotate(label,  # this is the text
                 (x, y),  # this is the point to label
                 textcoords="offset points",  # how to position the text
                 xytext=(0, 10),  # distance from text to points (x,y)
                 ha='center')  # plt.show()
plt.show()
print("-------------")

# Total tip Open Vs Closed
business_tip_year = tip_rest.groupby(["business_id", "year"]).size().reset_index(name='tip_year')
business_tip_year = pd.merge(business_rest, business_tip_year, how="left", on="business_id")
business_tip_year["year"] = pd.to_numeric(business_tip_year["year"], downcast='integer')
business_open_tip_year = \
    business_tip_year[(business_tip_year.is_open == 1) & (business_tip_year.year > 2007)].groupby(["year"])[
        "tip_year"].mean().reset_index(name='ouvert')

business_closed_tip_year = \
    business_tip_year[(business_tip_year.is_open == 0) & (business_tip_year.year > 2007)].groupby(["year"])[
        "tip_year"].mean().reset_index(name='fermé')

plt.plot('year', 'ouvert', data=business_open_tip_year, marker='o', markerfacecolor='blue', markersize=12,
         color='skyblue', linewidth=4)
plt.plot('year', 'fermé', data=business_closed_tip_year, marker='o', markerfacecolor='red', markersize=12,
         color='pink', linewidth=4)
plt.xlabel('Année')
plt.ylabel('Moyenne Commentaire')
plt.legend()
plt.show()

# Total useful tips Open Vs Closed
business_tip_year = tip_rest[tip_rest.compliment_count > 0].groupby(["business_id", "year"]).size().reset_index(
    name='tip_year')
business_tip_year = pd.merge(business_rest, business_tip_year, how="left", on="business_id")
business_tip_year["year"] = pd.to_numeric(business_tip_year["year"], downcast='integer')
business_open_tip_year = \
    business_tip_year[(business_tip_year.is_open == 1) & (business_tip_year.year > 2007)].groupby(["year"])[
        "tip_year"].mean().reset_index(name='ouvert')

business_closed_tip_year = \
    business_tip_year[(business_tip_year.is_open == 0) & (business_tip_year.year > 2007)].groupby(["year"])[
        "tip_year"].mean().reset_index(name='fermé')

plt.plot('year', 'ouvert', data=business_open_tip_year, marker='o', markerfacecolor='blue', markersize=12,
         color='skyblue', linewidth=4)
plt.plot('year', 'fermé', data=business_closed_tip_year, marker='o', markerfacecolor='red', markersize=12,
         color='pink', linewidth=4)
plt.xlabel('Année')
plt.ylabel('Moyenne Commentaire')
plt.legend()
plt.show()

# Average Stars Open Vs Closed (elite Users)
elite_users = user_rest[(user_rest.elite != "") & (user_rest.review_count >= 100) & (user_rest.useful >= 100)]
print("Nombre Utilisateurs Total:", len(user_rest))
print("Nombre utilisateurs Elites:", len(elite_users),
      "(" + str(round(len(elite_users) / len(user_rest) * 100.00, 2)) + ")%")

print("-------------")

elite_users_reviews = pd.merge(elite_users, review_rest, how="left", on="user_id")

business_star_year = pd.merge(business_rest, elite_users_reviews, how="left", on="business_id")
business_open_star_year = \
    business_star_year[(business_star_year.is_open == 1) & (business_star_year.year > 2007)].groupby(["year"])[
        "stars_y"].mean().reset_index(name='ouvert')

business_closed_star_year = \
    business_star_year[(business_star_year.is_open == 0) & (business_star_year.year > 2007)].groupby(["year"])[
        "stars_y"].mean().reset_index(name='fermé')

plt.plot('year', 'ouvert', data=business_open_star_year, marker='o', markerfacecolor='blue', markersize=12,
         color='skyblue', linewidth=4)
plt.plot('year', 'fermé', data=business_closed_star_year, marker='o', markerfacecolor='red', markersize=12,
         color='pink', linewidth=4)

plt.xlabel('Année')
plt.ylabel('stars elite users')
plt.legend()
plt.show()

print("Moyenne Etoiles par Année par les Utilisateurs Elites (Restaurants Ouverts)")
print(business_open_star_year)
print("-------------")

print("Moyenne Etoiles par Année par les Utilisateurs Elites (Restaurants Fermés)")
print(business_closed_star_year)
print("-------------")

# Total tip Open Vs Closed (elite Users)
elite_users_tips = pd.merge(elite_users, tip_rest, how="left", on="user_id")
business_tip_year = elite_users_tips.groupby(["business_id", "year"]).size().reset_index(name='tip_year')
business_tip_year = pd.merge(business_rest, business_tip_year, how="left", on="business_id")
business_tip_year["year"] = pd.to_numeric(business_tip_year["year"], downcast='integer')
business_open_tip_year = \
    business_tip_year[(business_tip_year.is_open == 1) & (business_tip_year.year > 2007)].groupby(["year"])[
        "tip_year"].mean().reset_index(name='ouvert')

business_closed_tip_year = \
    business_tip_year[(business_tip_year.is_open == 0) & (business_tip_year.year > 2007)].groupby(["year"])[
        "tip_year"].mean().reset_index(name='fermé')

plt.plot('year', 'ouvert', data=business_open_tip_year, marker='o', markerfacecolor='blue', markersize=12,
         color='skyblue', linewidth=4)
plt.plot('year', 'fermé', data=business_closed_tip_year, marker='o', markerfacecolor='red', markersize=12,
         color='pink', linewidth=4)
plt.xlabel('Année')
plt.ylabel('Moyenne Commentaire')
plt.legend()
plt.show()
