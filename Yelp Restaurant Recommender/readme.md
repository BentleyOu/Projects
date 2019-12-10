# Yelp Restaurant Recommender

----------
For Yelp, customer satisfaction is one of their top priorities. Happy customers will leave good reviews which benefits restaurant businesses while unhappy customers will leave bad reviews at the expense of the restaurant's reputation. It is crucial for Yelp to be able match customer search with relevant results. 

**Problem Statement**

Currently, yelp's matching algorithm is unable to break down the granularity of the user's search. As a result, Yelp will return the same top restaurants. 
For example, these two queries will yield the same results...

1. Burgers and fries for lunch
2. Burgers and fries for dinner with good service

In order for Yelp to understand the details of each user's search, we need to utilize the Yelp's complicated filtering feature. **This is both time consuming and user-unfriendly**

**Project Objective**

1. Simplify user searches
2. To consider and compare all relecant restaurants reviews
3. Automatic filtering by understanding the user queries


#### Approaches
1. Obtain Yelp Open dataset and managed it on MongoDB
2. Performed topic modeling 
3. Build content based recommender
4. Developed [Flask App](https://yelp-reinvented.herokuapp.com/) and deployed on Heroku

#### Files

1. Notebook - data preprocessing 
2. Recommendation Engine 

