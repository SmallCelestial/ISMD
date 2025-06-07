# Report: **Interactive Social Media Dashboard – Twitter Data Analysis**

# Part I: Application Description

### 1. Introduction

The objective of this project was to develop an interactive dashboard application using the **Streamlit** library to explore user interactions on the social media platform Twitter. The analysis focuses specifically on users’ opinions about various airlines—a critical aspect for the service sector, which continuously monitors customer satisfaction and responds to criticism in social media.

By utilizing an interactive analytical tool, users are able to explore data independently, filter based on selected criteria, and visualize results in real time. The project also incorporates basic graph visualization techniques to analyze communities and interactions between users.

### 2. Streamlit Interactive Application

The application was built using the **Streamlit** framework and features a user-friendly interface. Key features include:

- Filtering data by username

- **Interactive Components:**
  - Bar and pie charts (e.g., missing values, most frequent users)
  - Time series plots (e.g., number of tweets over time)
  - Filterable data table
  - Word cloud (most frequently used words in tweets)

### 3. Community Detection and Interaction Analysis

Although the dataset does not contain a complete network of user interactions, a simplified graph model was used:

- **Nodes**: Tweeting users  
- **Edges**: Mentions within tweets  

The libraries **NetworkX** and **Pyvis** were employed to visualize the user network. Influential users were identified based on retweet counts.

Methods applied:
- Visualization of user clusters using algorithms such as degree, closeness, and betweenness centrality
- Identification of key nodes
- Analysis of local structures and network cohesion


### 4. Limitations

- Incomplete interaction data (e.g., lack of replies and quote tweets)
- A small percentage of tweets contain geolocation information
- Potential errors in sentiment classification (e.g., sarcasm)
- The dataset is outdated, with most tweets from several years ago

### 5. Future Improvements

- Integrate the application with the **Twitter API** to enable real-time data analysis
- Expand the dashboard to include other platforms (e.g., Facebook, Reddit)
- Apply modern NLP models (e.g., **BERT**, **RoBERTa**) for better sentiment and context analysis
- Implement more advanced graph models (e.g., Graph Neural Networks)

### 6. Attachments

- [GitHub Repository with Application Code](https://github.com/SmallCelestial/ISMD)
- Data Source: [Kaggle – Twitter US Airline Sentiment](https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment)


---

# Part II: Data Analysis Examples

## Example 1: Twitter US Airline Sentiment

### Dataset Description

The data was sourced from **Kaggle** and consists of tweets containing opinions about several U.S. airline companies. The dataset includes the following columns:

- `tweet_id` – unique tweet identifier  
- `text` – tweet content  
- `tweet_created` – timestamp of creation  
- `airline` – airline name  
- `airline_sentiment` – sentiment classification (positive, neutral, negative)  
- `airline_sentiment_confidence` – confidence of the sentiment classification  
- `negativereason` – reason for negative sentiment (if applicable)  
- `negativereason_confidence` – confidence of the reason classification  
- `retweet_count` – number of retweets  
- `tweet_coord`, `tweet_location`, `user_timezone` – geographic location information  

The dataset includes over **11,000 tweets**, mostly from around March 2015.

### Exploratory Data Analysis (EDA)

#### Sentiment Analysis

Sentiment distribution:

- Negative: ~62%  
- Neutral: ~21%  
- Positive: ~17%  

#### Most Common Reasons for Negative Sentiment

The most frequent complaints were:
- **Customer Service Issue**
- **Late Flight**
- **Cancelled Flight**
- **Lost Luggage**

#### Posting Time

Tweeting activity was consistent over time, peaking on January 22, 2015.

#### Geolocation

Many tweets lacked coordinate data (`tweet_coord`). However, based on `tweet_location`, **Boston** was identified as the most common location.

#### Airline Popularity

Most frequently mentioned airlines:
- United
- US Airways
- AmericanAir
- SouthwestAir
- JetBlue

This is visualized in the interaction graph below:

![interaction graph](graph.png)

### Conclusions

- The majority of tweets expressed **negative sentiment**, indicating that Twitter is often used to voice dissatisfaction.
- The most common complaints concerned customer service and flight delays.
- United Airlines and US Airways received the most criticism.
- The interactive application enables dynamic analysis accessible even to non-technical users.
- A basic graph analysis revealed several highly influential users with broad reach.


## Example 1: Twitter US Airline Sentiment


Goal of data analysis is to ...

### Dataset Description





### Conclusions
