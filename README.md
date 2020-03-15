# Stock News
Welcome to the Reddit `!stocknews` bot repository

## Introduction 
A serverless Reddit bot that fetches news articles of a requested stock ticker. 


To use this service, post a comment in the /r/investing subreddit with the format `!stocknews $TICKER`
### Examples 

`!stocknews $TSLA`

`!stocknews $AAPL`

`!stocknews $UBER`


## How It Works
1. Send GET requests to the Reddit API to retrieve the last 500 comments posted in the /r/investing subreddit. 
2. Iterate through the comments and extract those with the key word "!stocknews"
3. Parse the stock ticker out of the extracted comments and make a request to the IEX Cloud Financial API to retrieve news for that ticker. 
4. Reply to the extracted comment with the news articles, formatted using markdown tables. 

### Challenges 
How to make sure the bot doesn't reply to a comment that it already responded to? 

After responding to the comment, save the comment via Reddit API. Always check if the comment has been saved before replying. 

## Technologies Used
- Python 
- PRAW
- Reddit API
- IEX Cloud Financial API 
- AWS Lambda
- AWS Cloudwatch Events 
- REST API
