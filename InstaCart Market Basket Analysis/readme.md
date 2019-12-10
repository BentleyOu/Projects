# InstaCart Market Basket Analysis

----------
In the business intelligence world, "market basket analysis" help retailers understand and uncover the purchasing patterns of their customers. Market Basket Analysis is a set of statistical affinity calculations that help managers better understand which sets of items are frequently bought together. These relationships can be used to increase profitability through cross-selling, recommendations, promotions, or even the placement of items on a menu or in a store.

In this project, I will be using InstaCart's 32+ million observations to perform market basket analysis.

**Project Objectives**

1. Uncover insights such as customer's buying patterns and their next frequent item based on what they bought.
2. Use the association rules created to make insightful recommendations on a product promotion


#### Approaches
1. Obtained InstaCart's 32+ million data points
	* “The Instacart Online Grocery Shopping Dataset 2017”, Accessed from https://www.instacart.com/datasets/grocery-shopping-2017 on <December 20198>
	* Processed data on an AWS instance
	
2. Exploratory Data Analysis 
3. Data Mining - form association rules by calculating support, confidence and lift for each product set (size 2)
4. Build Flask Helper Functions
	* find_Association.ipynb and AutoComplete.ipynb
	
4. Developed [Flask App](https://frequent-item-finder.herokuapp.com/) and deployed on Heroku

#### Files

1. EDA - images of graphs and analysis
2. Pickled files
3. .py files for running backend Flask
4. .ipynb files for data analysis and model training

