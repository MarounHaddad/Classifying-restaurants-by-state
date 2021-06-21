"""
This file contains the list of functions used to extract patterns
"""
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder


def bin_feature(feature, feature_name, bin_count):
    """
    This function splits the feature values into bins
    :param feature: numpy array of values
    :param feature_name: name of the  feature
    :param bin_count: number of bins to split the values
    :return: labels of the features (to which bin they belong)
    """

    print(feature_name, ":")
    print("-----------")

    qc = pd.qcut(feature, q=bin_count, precision=1, duplicates='drop')
    bins = qc.categories
    print("bins:", bins)
    codes = qc.codes

    print("labels:", codes)
    (unique, counts) = np.unique(codes, return_counts=True)
    frequencies = np.asarray((unique, counts)).T

    print("frequencies:\n", frequencies)
    print("")

    # save the labels to a file path for each feature
    codes = [feature_name + "" + str(s + 1) for s in codes]
    return codes


# load the data
business_attributes = pd.read_pickle('../../data/preprocess/quebec/business_attributes_final')
business_attributes_original = pd.read_pickle('../../data/preprocess/quebec/business_attributes')

# setting the zone back to their names instead of the code
business_attributes['zone'] = business_attributes_original['zone']

# discretizing columns
numerical_columns = ['review_count',
                     'good_reviews_count',
                     'bad_reviews_count',
                     'good_reviews_ratio',
                     'bad_reviews_ratio',
                     'good_useful_review_count',
                     'bad_useful_review_count',
                     'good_elite_review_count',
                     'bad_elite_review_count',
                     'tips_count',
                     'tips_usefull_count',
                     'tips_elite_count',
                     'category_zone_inter',
                     'category_city_inter',
                     'total_opening_hours',
                     'std_stars',
                     'trend_stars',
                     'checkin_count',
                     'average_checkin',
                     'std_checkin',
                     'zone_count',
                     'business_first_year_count']

# binning the numerical features
apriori_dataset = pd.DataFrame()
for column in numerical_columns:
    discrete_column = bin_feature(np.array(business_attributes[column]), column, 3)
    apriori_dataset[column] = discrete_column

# setting the rest of the columns in the form (column_name:column value)
remaining_columns = list(set(business_attributes.columns) - set(numerical_columns))
for column in remaining_columns:
    column_name_prefix = [column for i in range(len(business_attributes))]
    apriori_dataset[column] = column_name_prefix
    business_attributes[column] = business_attributes[column].astype(str)
    apriori_dataset[column] = apriori_dataset[column].str.cat(business_attributes[column], sep='')

# dataset_filtered = apriori_dataset
# filter data by zone
zone_name = 'zoneH2X'
dataset_filtered = apriori_dataset[apriori_dataset.zone == zone_name]
print(len(dataset_filtered))

final_dataset = []
for restaurant in dataset_filtered.values.tolist():
    reduced = []
    for column in restaurant:
        if not '0.0' in column and not zone_name in column:
            reduced.append(column)
    final_dataset.append(reduced)

# apply FP-Growths
te = TransactionEncoder()
te_ary = te.fit(final_dataset).transform(final_dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)
frequent_itemsets = fpgrowth(df, min_support=0.2, use_colnames=True)
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
rules = association_rules(frequent_itemsets)
print(rules)

# save the extracetd rules
rules.to_csv('out.csv', index=False)
