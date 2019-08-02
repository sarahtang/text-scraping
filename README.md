# text-scraping
Using the reddit API to scrape through text and see where conversation hot spots exist. Conversation hot spots are where there is high amounts of engaged conversation = posts with >= 2 comments per post. Limit to 1000 posts. Posts grabbed from current day minus 31 days.

Twitter API to grab followers and their descriptions.


## Output
CSV titled reddit_SUBREDDIT.csv

## Resources
Subreddit API documentation
https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html

Twitter documentation
https://developer.twitter.com/en/docs/api-reference-index


## TODO
1. Term frequency, entity = parse company names, people (pre-trained) how often is ___ mentioned?
2. What big words are being used?
3. Training classification models ==> knime; fuzzy match, keyword search; NLP/LDA ==> Watson
4. Frontend
5. Count Twitter followers that mention "IBM, ibmer, etc." and student
<!-- 6. Think about what is the effect? Business impact - competitive intellignece, audience intelligence; improvement on Sprinklr -->
