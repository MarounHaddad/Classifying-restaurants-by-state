# Classifying restaurants by state
In this work, we use the Yelp research dataset to train classical machine learning models and neural networks for the purpose of classifying the restaurants into two categories (Permenantly closed or Open). Furthermore, we use FP-Growth in order to determine the attributes (or characteristics) that affect the state of the restaurants in several areas of Montreal.

## Introduction

<p align="center">
  <img  width="60%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/yelp.png">
</p>
 <p align="center"   ><em>Figure 1 - Yelp data components and relationships.</em></p>
 
Yelp is a mobile application that allows users to review the enterprises they have visited, in particular restaurants. The user of Yelp can write reviews about the restaurants they visited and score them on a scale from 1 to 5. Furthermore, they can write tips for other users (For example, bring a jacket when you visit this establishment). They can also inquire about the different categories of restaurants (for example, Bar, pub), cuisines (for example, Chinese, Italian), their location, opening hours, and the services they offer (for example, whether they have delivery or takeout option). The users can also signal their visit to the restaurant with a "Check-in" option. The app also has a small social network experience, where the users can befriend other users and comment/react to their reviews and tips. Yelp also designates some users are "Elite". It is unknown how the selection process of Elite users is made, however, it is suspected that the reviews of the Elite users have more weight than those of regular users. Figure 1 summarizes the components of the Yelp app experience concerning the restaurants.
 
## Dataset and Workflow

<p align="center">
<img  width="65%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/dataset.png">
</p>
<p align="center"  ><em>Table 1 - dataset tables.</em></p>

<p align="center">
<img  width="65%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/focalize.png">
</p>
<p align="center"  ><em>Table 2 - We focalize on the Montreal data for analysis.</em></p>


Yelp offers a dataset for researchers [] that is comprised of 5 XML files. Table 1 details the dataset with the different tables and columns that are of interest to our study.  The dataset covers the US and Canada. We only focus on the enterprises of type restaurants and process the dataset so it is compatible with our study objectives.  
- **Restaurant**: Has the list of restaurants and their characteristics.  
- **User**: Has the list of users and their status (Elite or not) and list of friends.  
- **Review**: Has the list of reviews written by users for restaurants and the number of stars granted per review. It also contains the reactions made by other users on the review.  
- **Tip**: Has the list of tips written by the users for restaurants and the reactions they received. 
- **Checkin**: Has the list of visits per restaurant.  

We further focalize on the data of Montreal (Table 2) for the analysis that would help us deduce our features for the eventual training of the models.  

<p align="center">
<img  width="65%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/kdd.png">
</p>
<p align="center"  ><em>Figure 2 - KDD inspired workflow.</em></p>

We loosely follow the KDD (Knowledge Data Discovery) workflow for data mining [], Figure 2. We first start by focalizing on a subset of data. Subsequently, we perform a series of queries to develop our knowledge and further our understanding of the different factors that affect the state of the restaurants. This acquired knowledge would allow us to properly engineer the features for training our models. After building our training dataset, we clean it and reduce its dimensionality. Next, we search for the best-performing models and parameters. Finally, we extract patterns from the data and visualize our results.  

## Analysis and Feature engineering

We perform a series of queries on the data and deduce the features that would help the training of our models.

<p align="center">
<img  src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/goldensquarevsvieuxport.png">
</p>
<p align="center"  ><em>Figure 3- Percentage of closed restaurants in the Golden Square area of Montreal Vs the Old Port.</em></p>

First, we start by looking at the stability of the different regions in Montreal. By stability, we mean the percentage of restaurants that are closed in a certain region. We divide Montreal into zones according to the first part of the postal codes in the area (for example, Old Port: H2Y). We notice that some zones are stable (Old Port), with a low number of closed restaurants, while others are not stable and have a high number of closures (Golden Square), Figure 3.

<p align="center">
<img  width="65%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/zonepourcentage.png">
</p>
<p align="center"  ><em>Figure 4 - Percentage of closed restaurants per region.</em></p>

When we chart the total number of restaurants to ever open in a zone vs the percentage of closed restaurants in that zone, Figure 4, we notice that there is, to an extent, a positive correlation between the two numbers. This is normal, since the more restaurants we have in a zone, the more local competition we have and the more the risk for closure will increase. Therefore, we add the following attributes:

- **zone**: The zone of the restaurant in the city
- **zone_number_restaurants**: The number of restaurants in a zone.

<p align="center">
<img  width="80%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/categoryregion.PNG">
</p>
<p align="center"  ><em>Figure 5 - Restaurants per category for the regions of St Catherine and Old Port.</em></p>

However, we notice in Figure 4 that there are two exceptions to the rule: The Old Port and Little Italy. For these two zones, the number of restaurants is high, however, the percentage of closures is relatively low. Therefore, to identify the contributing factors for the stability of these zones, we look at the restaurant categories per zone. We plot the top 10 categories for open restaurants (blue bars, Figure 5) versus the top 10 categories for closed restaurants (orange bars, Figure 5). We notice that for the stable zones, such as Little Italy and the Old Port, the zones are dominated by a certain number of stable categories. For example, French restaurants in the Old Port and Italian restaurants in Little Italy. However, in the unstable regions, such as St Catherine and the Golden Square, we do not have an overly dominant category and to an extent all categories are unstable. We conclude that having a unique category as a restaurant or standing out is important in some zones while having a common cuisine or category is important in others. Therefore, we add the following attributes:  

- **categories**: The list of categories for the restaurant (one-hot-encoding).  
- **zone_category_itersection**: The number of restaurants in the same zone that share at least one category with the restaurant.  
- **city_category_itersection**: The number of restaurants in the same city that share at least one category with the restaurant.  


<p align="center">
<img  width="80%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/closureyear.png">
</p>
<p align="center"  ><em>Figure 6 - Number of restaurants closing per Year vs Number of restaurants opening per Year.</em></p>
Secondly, we look at the number of restaurants opening per year versus the number of restaurants closing per year, Figure 6. We notice that the opening and closing of restaurants follow to an extent a "Boom and Bust" cycle. Where the number of restaurants opening every year increases progressively until it reaches a peak, followed by a series of years with a decline in the number of opening restaurants and an increase in the number of closures. We conclude that the year of opening encodes certain information about the economic state of the city in that year and can help us determine the probability of the restaurant closure in the future. Therefore, we add:   

- **buisiness_first_year**: The opening year for the restaurant.  
- **business_first_year_count**: The number of restaurants opening in the same year with the restaurant.  

*Note: It would have been also beneficial to include the city in the count of restaurants opening per year for more specificity.    

<p align="center">
<img  width="80%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/Trendstars.png">
</p>
<p align="center"  ><em>Figure 7 - Trend of the quality of the restaurants for Best vs Worst/Open vs Closed restaurants.</em></p>

Next, we look at the trends in the quality of the restaurants over the year. We compare the best restaurants (stars>=4) and the worst restaurants (stars<=2). We also compare the open restaurants versus the closed ones. We notice that the quality of service of the best and open restaurants is more consistent than that of the worst and closed restaurants, as the quality of the latter tends to deteriorate over the years, Figure 7.  
Therefore we add the following attributes:  
- **std_stars**: The standard deviation of the stars per review across the years.  
- **trend_stars**: The average of stars of last year minus the average of stars of the first year per restaurant.  

<p align="center">
<img  width="80%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/stars.png">
</p>
<p align="center"  ><em>Figure 8 - Avergage of stars received by Open vs Closed restaurants.</em></p>

Then, we look at the average of stars across the years for open and closed restaurants. We evaluate three types of reviews, **General** (written by all users), **Elite** (written by Elite users), and **Useful** (reviews that have received reactions from other users). We find that for the three categories, the open restaurants receive better evaluations than the closed ones, Figure 8. We conclude that the quality of service and evaluation of restaurants by the customers play an important role in the continuation of the business. Therefore, we add the following attributes:  
- **review_count**: The number of total reviews per restaurant.  
- **good_reviews_count**: The number of good reviews per restaurant (stars>=3).  
- **bad_reviews_count**: The number of bad reviews per restaurant (stars<3).  
- **good_reviews_ratio**: The proportion of good reviews out of all reviews per restaurant.
- **bad_reviews_ration**: The proportion of bad reviews out of all reviews per restaurant.
- **good_useful_review_count**: The number of good reviews that have received a reaction per restaurant.
- **bad_useful_review_count**: The number of bad reviews that have received a reaction per restaurant.  
- **good_elite_review_count**: The number of good reviews written by Elite users for the restaurant.
- **bad_elite_review_count**: The number of bad reviews written by Elite users for the restaurant.

<p align="center">
<img  width="80%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/tips.png">
</p>
<p align="center"  ><em>Figure 9 - Average number of tips received by Open vs Closed restaurants.</em></p>

We notice the same trends for the tips, where the open restaurants receive more interactions from the users than the closed ones, Figure 9:  
- **tips_count**: Total number of tips per restaurant.  
- **tips_usefull_count**: Number of tips that have received a reaction per restaurant.
- **tips_elite_count**: Number of tips written by Elite users per restaurant. 

<p align="center">
<img  width="80%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/trendcheckin.png">
</p>
<p align="center"  ><em>Figure 10 - Trend of the visits to the restaurants for Best vs Worst/Open vs Closed restaurants.</em></p>

Furthermore, we analyze the tendency of customers' visits to restaurants across the years. We notice that the average of customer checkins for open restaurants exceeds that of closed restaurants.  
Therefore, we add the following attributes:  
- **checkin_count**: Number of checkins per restaurant.  
- **average_checkin**: The mean of checkins across all years per restaurant.  
- **std_checkin**: The standard deviation of checkins across all years per restaurant.

<p align="center">
<img  width="80%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/chain.png">
</p>
<p align="center"  ><em>Figure 11 - The percentrage of Open Vs Closed restaurants that are part or not of a chain.</em></p>

According to [], the restaurants that are part of a chain are more secure than those that are not. Therefore, we look at the percentage of open versus closed for the chain and nonchain restaurants. For Montreal, we notice that there is not a big difference between the two. However, for North America in general, the restaurant that is part of a chain is 15% more secure than those that are not, Figure 11. Therefore, we add the following attribute:  
- **is_chain**: If the restaurant is part of a chain or not.  

We also add the following attributes that we consider relevant to the state of the restaurant:  
- **total_opening_hours**: Total number of open hours per week.  
- **is_open_saturday**: If the restaurant is open on Saturday.  
- **is_open_sunday**: If the restaurant is open on Sunday.  
- **is_open_monday**: If the restaurant is open on Monday.  
- **restauranttakeout**: If the restaurant offers a take-out option.
- **restaurantgoodforgroops**: If the restaurant is good for groups.
- **restaurantreservations**: If the restaurant requires a reservation.
- **restaruantpricerange**: The price range of the items in the restaurant (1: Affordable, 2: Average, 3: Expensive).
- **outdoorseating**: If the restaurant has outdoor seating.  
- **goodforkids**: If the restaurant is good for kids and families.  
- **restaurantdelivery**: If the restaurant offers the option of delivery.

## Handling missing values
We handle the missing values of the attributes hierarchically according to the restaurant location and categories. For example, for **total_opening_hours**, we take the average of the opening hours of the restaurants of the same category and in the same zone as the restaurant. If none were found, we take the average opening hours of the restaurants in the same zone. If none were found either, we take the average for all restaurants. 

## Dimensionality reduction  

We apply the Mutual Information method to reduce the dimensionality of the training dataset and take only the top 150 attributes. Table 3 lists the top 10 attributes with their scores.

## Experimental results

## Pattern extraction

## Background information
This work was presented as partial requirement for the course "INF7710 - Théorie et applications de la fouille d’associations" at UQAM (University of Quebec at Montreal).  
Maroun Haddad (April 2020).

Complete report and presentation under: **\presentation and report in French**  

## References

