import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth


def apply_apriori(dataset, min_support_value):
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=min_support_value, use_colnames=True)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    return frequent_itemsets


def apriori_augment(reviews, stars_filter):
    reviews = reviews[reviews.stars == stars_filter]
    users = reviews.user_id.unique()
    dataset = []
    for user in users:
        user_restaurant_list = []
        user_restaurants = reviews[reviews.user_id == user].business_id.unique()
        for restaurant in user_restaurants:
            user_restaurant_list.append(restaurant)
        dataset.append(user_restaurant_list)

    # we augment data using FP growth
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = fpgrowth(df, min_support=0.008, use_colnames=True)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    frequent_restaurants = []
    for index, pair in frequent_itemsets[frequent_itemsets.length == 2].head(5).iterrows():
        frequent_restaurants.append(list(pair.itemsets))
    return frequent_restaurants
