
To run the program:
    
    Run a multithreaded version of our project:
        python threaded_tweets.py
    
    Run a single threaded version of our project:
        python singlethread_tweets.py

Writing a program that analyzes the increase in bigoted tweets post-2016 presidential election.

We analyzed the streaming and analysis times for a certain amount of tweets from Atlanta, GA and Cleveland, OH, (10, 20, 40, 60) for multithreaded and not multithreaded programs. Surprisingly, we found that on average for both cities, that the multithreaded programs took longer than alternating every so many tweets to streaming from another location. This can be seen in the Excel worksheet in the repository. 

On average for both types of programs, it took longer to stream X amount of tweets from Cleveland, Ohio than to stream X amount of tweets from Atlanta, Georgia. This was not as surprising, because Atlanta is a much more metropolitan city than Cleveland and higher population. Also, our geographical coordinates for location spanned a much larger area for Georgia than for Cleveland. A lot of the time also depends on the Twitter API where we are waiting for tweets to be streamed. As we are not 100% sure as to how the method GetStreamFilter() determines which public tweets it chooses to stream to us, we can only assume there is a higher number of accessible tweets from Atlanta, GA. 

An interesting thing to note was that multithreading did pose to be faster for streaming tweets from Cleveland for smaller amounts of tweets. However, as we need to process higher and higher amounts of tweets, we noticed that the processing time of multithreading surpassed when they were not multithreading. 

Although implementing a single threaded program may be more time efficient, it also can impact the quality of our tweets that we are streaming. We have to alternate between streaming Cleveland, OH tweets and Atlanta, GA tweets which means that we may not catch any current incoming tweets from the connection that is sleeping that we would have caught with a multithreaded program. 

We still do not circumvent the issue, in either multithreaded or single threaded programs, where we are only allowed 2-3 connections open from a specific token, which means that we are also limited to how many cities and areas in the United States we can analyze. 

