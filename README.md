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

We further focalize on the data of Montreal alone for the analysis that would help us deduce our features for the eventual training of the models. 

<p align="center">
<img  width="65%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/kdd.png">
</p>
<p align="center"  ><em>Figure 2 - KDD inspired workflow.</em></p>


## Analysis and Feature engineering

<p align="center">
<img  src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/goldensquarevsvieuxport.png">
</p>
<p align="center"  ><em>Figure 3- Percentage of closed restaurants in the Golden Square area of Montreal Vs the Old Port.</em></p>

<p align="center">
<img  width="65%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/zonepourcentage.png">
</p>
<p align="center"  ><em>Figure 4 - Percentage of closed restaurants per region.</em></p>


<p align="center">
<img  width="65%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/categoryregion.PNG">
</p>
<p align="center"  ><em>Figure 5 - Restaurants per category for the regions of St Catherine and Old Port.</em></p>


<p align="center">
<img  width="65%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/closureyear.png">
</p>
<p align="center"  ><em>Figure 6 - Number of restaurants closing per Year vs Number of restaurants opening per Year.</em></p>

<p align="center">
<img  width="65%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/Trendstars.png">
</p>
<p align="center"  ><em>Figure 7 - Trend of the quality of the restaurants for Best vs Worst/Open vs Closed restaurants.</em></p>
                   
<p align="center">
<img  width="65%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/stars.png">
</p>
<p align="center"  ><em>Figure 8 - Avergage of stars received by Open vs Closed restaurants.</em></p>
                   
<p align="center">
<img  width="65%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/tips.png">
</p>
<p align="center"  ><em>Figure 9 - Average number of tips received by Open vs Closed restaurants.</em></p>

<p align="center">
<img  width="65%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/trendcheckin.png">
</p>
<p align="center"  ><em>Figure 10 - Trend of the visits to the restaurants for Best vs Worst/Open vs Closed restaurants.</em></p>

<p align="center">
<img  width="85%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/chain.png">
</p>
<p align="center"  ><em>Figure 11 - The percentrage of Open Vs Closed restaurants that are part or not of a chain.</em></p>


## Handling missing values

<p align="center">
<img  width="85%" src="https://github.com/MarounHaddad/Classifying-restaurants-by-state/blob/main/images/chain.png">
</p>
<p align="center"  ><em>Table 3 - .</em></p>

## Dimensionality reduction

## Experimental results

## Pattern extraction

## Background information
This work was presented as partial requirement for the course "INF7710 - Théorie et applications de la fouille d’associations" at UQAM (Université du Quebec à Montréal).  
Maroun Haddad (April 2020).

Complete report and presentation under: **\presentation and report in French**

## References

