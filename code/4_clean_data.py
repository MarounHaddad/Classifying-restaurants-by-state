# -------------------------------------------------------
# In this file we clean the data by removing duplicates, filling empty/na columns
# -------------------------------------------------------


import pandas as pd
import pretreatment.utils as ut

# load prepared attributes
business_attributes = pd.read_pickle('../../data/preprocess/business_attributes')

business_attributes_final = business_attributes.copy()

# Check zero and nan values
# for column in business_attributes_final.columns:
#     print(column + " zero values:",len(business_attributes_final[business_attributes_final[column]==0]))
#     print(column + " nan values:",len(business_attributes_final)-len(pd.isna(business_attributes_final[column])))
#     print("--------------")

# # -------------------------------------------------------------
# # -------------------------------------------------------------
# HANDLE OPEN HOURS ZERO
# # -------------------------------------------------------------
# -------------------------------------------------------------
business_rest = pd.read_pickle(ut.datapath+'business_rest')
business_rest["zone"] = ""
business_rest["zone"] = business_rest["postal_code"].str.split(" ", n=1, expand=True)

business_category_list = pd.DataFrame(business_rest.categories.str.split(',').tolist(),
                                      index=business_rest.business_id).stack().reset_index(name='category')
business_category_list = business_category_list[~business_category_list.category.str.contains('Restaurants')]
business_category_list = business_category_list[~business_category_list.category.str.contains('Food')]
business_category_list['category'] = business_category_list['category'].str.strip()

business_category_full = pd.merge(business_rest, business_category_list, how="left", on="business_id")

business_category_full["total_opening_hours"] = business_category_full.apply(ut.calc_total_open_hours, axis=1)
business_category_full["is_open_saturday"] = business_category_full.apply(ut.is_open_week_day, args=("Saturday",),
                                                                          axis=1)
business_category_full["is_open_sunday"] = business_category_full.apply(ut.is_open_week_day, args=("Sunday",), axis=1)
business_category_full["is_open_monday"] = business_category_full.apply(ut.is_open_week_day, args=("Monday",), axis=1)

business_zero_hour = business_category_full[business_category_full.total_opening_hours == 0]
for index, business in business_zero_hour.iterrows():
    # For total hours: we take the mean of the opening hours of the businesses of the same category in the same zone
    business['total_opening_hours'] = round(
        business_category_full[(business_category_full.business_id != business.business_id) &
                               (business_category_full.category == business.category) &
                               (business_category_full.total_opening_hours != 0) &
                               (business_category_full.zone == business.zone)]['total_opening_hours'].mean(), 2)

    # For is open on week day : we take the mode openning pattern of the businesses of the same category in the same zone
    business['is_open_saturday'] = business_category_full[(business_category_full.business_id != business.business_id) &
                                                          (business_category_full.category == business.category) &
                                                          (business_category_full.total_opening_hours != 0) &
                                                          (business_category_full.zone == business.zone)][
        'is_open_saturday'].mode().max()

    business['is_open_sunday'] = business_category_full[(business_category_full.business_id != business.business_id) &
                                                          (business_category_full.category == business.category) &
                                                          (business_category_full.total_opening_hours != 0) &
                                                          (business_category_full.zone == business.zone)][
        'is_open_sunday'].mode().max()

    business['is_open_monday'] = business_category_full[(business_category_full.business_id != business.business_id) &
                                                        (business_category_full.category == business.category) &
                                                        (business_category_full.total_opening_hours != 0) &
                                                        (business_category_full.zone == business.zone)][
        'is_open_monday'].mode().max()

    # if no business with same category is found in area we take the mean of the zone as a whole
    # and if not we take that of the city
    if pd.isna(business['total_opening_hours']):
        business['total_opening_hours'] = round(
            business_category_full[(business_category_full.business_id != business.business_id) &
                                   (business_category_full.total_opening_hours != 0) &
                                   (business_category_full.zone == business.zone)]['total_opening_hours'].mean(), 2)

    if pd.isna(business['is_open_saturday']):
        business['is_open_saturday'] = \
        business_category_full[(business_category_full.business_id != business.business_id) &
                               (business_category_full.total_opening_hours != 0) &
                               (business_category_full.zone == business.zone)]['is_open_saturday'].mode().max()

    if pd.isna(business['is_open_saturday']):
        business['is_open_saturday'] = \
            business_category_full[(business_category_full.business_id != business.business_id) &
                                   (business_category_full.total_opening_hours != 0)]['is_open_saturday'].mode().max()

    if pd.isna(business['is_open_sunday']):
        business['is_open_sunday'] = \
        business_category_full[(business_category_full.business_id != business.business_id) &
                               (business_category_full.total_opening_hours != 0) &
                               (business_category_full.zone == business.zone)]['is_open_sunday'].mode().max()

    if pd.isna(business['is_open_sunday']):
        business['is_open_sunday'] = \
            business_category_full[(business_category_full.business_id != business.business_id) &
                                   (business_category_full.total_opening_hours != 0)]['is_open_sunday'].mode().max()

    if pd.isna(business['is_open_monday']):
        business['is_open_monday'] = \
        business_category_full[(business_category_full.business_id != business.business_id) &
                               (business_category_full.total_opening_hours != 0) &
                               (business_category_full.zone == business.zone)]['is_open_monday'].mode().max()

    if pd.isna(business['is_open_monday']):
        business['is_open_monday'] = \
            business_category_full[(business_category_full.business_id != business.business_id) &
                                   (business_category_full.total_opening_hours != 0)]['is_open_monday'].mode().max()

    business_zero_hour.at[index, 'total_opening_hours'] = business['total_opening_hours']
    business_zero_hour.at[index, 'is_open_saturday'] = business['is_open_saturday']
    business_zero_hour.at[index, 'is_open_sunday'] = business['is_open_sunday']
    business_zero_hour.at[index, 'is_open_monday'] = business['is_open_monday']

for index, business in business_attributes_final[business_attributes_final.total_opening_hours==0].iterrows():
    business['total_opening_hours'] = round(
        business_zero_hour[(business_zero_hour.business_id != business.business_id)]['total_opening_hours'].mean(), 2)
    business['is_open_saturday'] = business_zero_hour[(business_zero_hour.business_id != business.business_id)]['is_open_saturday'].mean()
    business['is_open_sunday'] = business_zero_hour[(business_zero_hour.business_id != business.business_id)]['is_open_sunday'].mode().max()
    business['is_open_monday'] = business_zero_hour[(business_zero_hour.business_id != business.business_id)]['is_open_monday'].mode().max()

    business_attributes_final.at[index, 'total_opening_hours'] = business['total_opening_hours']
    business_attributes_final.at[index, 'is_open_saturday'] = business['is_open_saturday']
    business_attributes_final.at[index, 'is_open_sunday'] = business['is_open_sunday']
    business_attributes_final.at[index, 'is_open_monday'] = business['is_open_monday']

print('After Handling:')
print('total_opening_hours zero values:',len(business_attributes_final[business_attributes_final['total_opening_hours']==0]))


# remove business_id
business_attributes_final = business_attributes_final.drop('business_id', axis=1)
print("--------------")
print("removed id")
print("--------------")

# Remove duplicates
print("Dropping duplicate instances")
print("Number of records before removing duplicates:" + str(len(business_attributes_final)))
data = business_attributes_final.drop_duplicates(subset=list(business_attributes_final.columns.values), keep='first')
print("Number of records after removing duplicates:" + str(len(data)))

# Set Zone code
print("setting zone codes")
business_attributes_final.zone = pd.Categorical(business_attributes_final.zone)
business_attributes_final['zone'] = business_attributes_final.zone.cat.codes

# add is_closed instead of is_open
print("replacing is_open with is_closed")
business_attributes_final['is_closed'] = business_attributes_final['is_open'] -1
business_attributes_final['is_closed'] = business_attributes_final['is_closed'].abs()
business_attributes_final = business_attributes_final.drop('is_open', axis=1)


print("--------------")

# fill category columns with 0 instead of NAN
for column in business_attributes_final.columns:
    business_attributes_final[column].fillna(0, inplace=True)

business_attributes_final.to_pickle('../../data/preprocess/business_attributes_final')
