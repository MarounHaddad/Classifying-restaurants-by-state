import matplotlib.pyplot as plt
import pandas as pd

import pretreatment.utils as ut

# load data
business_rest = pd.read_pickle(ut.datapath + 'business_rest')
tip_rest = pd.read_pickle(ut.datapath + 'tip_rest')
review_rest = pd.read_pickle(ut.datapath + 'review_rest')
user_rest = pd.read_pickle(ut.datapath + 'user_rest')
checkin_rest = pd.read_pickle(ut.datapath + 'checkin_rest')

business_rest["zone"] = ""
business_rest["zone"] = business_rest["postal_code"].str.split(" ", n=1, expand=True)

business_rest['checkin_count'] = 0
business_rest['average_checkin'] = 0
business_rest['std_checkin'] = 0

print("business_rest",len(business_rest))
print("review_rest",len(review_rest))
print("tip_rest",len(tip_rest))
print("user_rest",len(user_rest))
print("checkin_rest",len(checkin_rest))

checkin_rest_year = pd.DataFrame({'business_id':'','year':int(),'chekins':float()},index=[1])

for index, business in business_rest.iterrows():
    date = checkin_rest[checkin_rest.business_id == business.business_id]
    if len(date) == 0:
        continue
    date = date.iloc[0]['date']
    checkins = []
    for year in range(2011, 2019):
        checkin_count = date.count(str(year))
        if checkin_count > 0:
            checkins.append(checkin_count)
            checkin_rest_year = checkin_rest_year.append(
                {'business_id': business.business_id, 'year': year, 'chekins': checkin_count}, ignore_index=True)

print(checkin_rest_year.dtypes)
print(checkin_rest_year)

# Trend Stars Open Vs Closed Businesses
business_closed = business_rest[(business_rest.is_open == 0)]
business_closed_checkin_year = \
    pd.merge(business_closed, checkin_rest_year[checkin_rest_year.year > 2011], how="left", on="business_id").groupby(
        ["year"])["chekins"].mean().reset_index(name='fermé')

business_open = business_rest[(business_rest.is_open == 1)]
business_open_checkin_year = \
    pd.merge(business_open, checkin_rest_year[checkin_rest_year.year > 2011], how="left", on="business_id").groupby(
        ["year"])["chekins"].mean().reset_index(name='ouvert')

plt.plot('year', 'fermé', data=business_closed_checkin_year, marker='o', markerfacecolor='red', markersize=12,
         color='pink', linewidth=4)
plt.plot('year', 'ouvert', data=business_open_checkin_year, marker='o', markerfacecolor='blue', markersize=12,
         color='skyblue', linewidth=4)
plt.legend()
plt.show()



bottom_business_closed = business_rest[(business_rest.is_open == 0) & (business_rest.stars <= 2)]
bottom_business_closed_checkin_year = \
    pd.merge(bottom_business_closed, checkin_rest_year[checkin_rest_year.year > 2011], how="left", on="business_id").groupby(
        ["year"])[
        "chekins"].mean().reset_index(name='bottom')

top_business_open = business_rest[(business_rest.is_open == 1) & (business_rest.stars >= 4)]
top_business_open_checkin_year = \
    pd.merge(top_business_open, checkin_rest_year[checkin_rest_year.year > 2011], how="left", on="business_id").groupby(["year"])[
        "chekins"].mean().reset_index(name='top')

plt.plot('year', 'bottom', data=bottom_business_closed_checkin_year, marker='o', markerfacecolor='red', markersize=12,
         color='pink', linewidth=4)
plt.plot('year', 'top', data=top_business_open_checkin_year, marker='o', markerfacecolor='blue', markersize=12,
         color='skyblue', linewidth=4)
plt.legend()
plt.show()


# chain
business_rest["is_chain"] = 0
for index, business in business_rest.iterrows():
    count = len(business_rest[business_rest.name == business_rest.at[index, 'name']])
    if count > 1:
        business['is_chain'] = 1
    else:
        business['is_chain'] = 0

    business_rest.at[index, 'is_chain'] = business['is_chain']


business_rest_chain = business_rest[business_rest.is_chain==1]
business_rest_notchain = business_rest[business_rest.is_chain==0]

perc_chain_open = len(business_rest_chain[business_rest_chain.is_open==1])
perc_chain_closed = len(business_rest_chain[business_rest_chain.is_open==0])

perc_notchain_open = len(business_rest_notchain[business_rest_notchain.is_open==1])
perc_notchain_closed = len(business_rest_notchain[business_rest_notchain.is_open==0])


print(perc_chain_open,perc_chain_closed)
print(perc_notchain_open,perc_notchain_closed)

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.axis('equal')
label = ['Ouvert','Fermé']
perc = [perc_chain_open,perc_chain_closed]
ax.pie(perc, labels = label,autopct='%1.2f%%')
plt.show()

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.axis('equal')
label = ['Ouvert','Fermé']
perc = [perc_notchain_open,perc_notchain_closed]
ax.pie(perc, labels = label,autopct='%1.2f%%')
plt.show()
