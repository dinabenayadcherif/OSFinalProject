The purpose of this program is to analyze the amount of hate spreading across social media using parallelization as a way to optimize data analysis. 

The dicts directory in the folder contains our yaml files that have our basic sentiment dictionaries and our locations.yml file that holds our coordinates of where we will be analyzing public tweets from. On our local directory however, our locations.yml file also contained our sensitive information like access tokens and keys for the Twitter API. 

locations.yml contains 12 different locations and their coordinates:
Georgia, Ohio (Cleveland), New York, Alabama, Alaska, California, Arizona, Arkansas, Colorado, Connecticut, Delaware and Florida. 

The negative.yml file holds all of our words/phrases that carry around negative sentiment.

The positive.yml file holds all of our words/phrases that carry around positive sentiment.

singlethread_tweets.py and threaded_tweets.py both carry out the same process however one uses the main thread for doing all of the streaming and analysis while threaded_tweets.py uses multiple threads. 

These two programs output a couple things, for every location that we analyze, there is an output text file that writes the meter value of how positive or negative the tweets are. The tweets are individually streamed to standard out as well as the processing time. This can be seen in any text file formatted "{location}_meter.txt" in the repository.

To stream all of the tweets we used the method GetStreamFilter() from the Twitter API, which can be seen in both of the files. It opens a connection and listens for incoming tweets. 

We used mutex locks as a way of making sure that there were no conflicts in global variables in the multithreaded program. 

The directory report_pix shows the CPU usage of all the threads representing each individual location. 

To run the program:
    
    Run a multithreaded version of our project:
        python threaded_tweets.py
    
    Run a single threaded version of our project:
        python singlethread_tweets.py

Although we are running our analysis on 12 different locations, we decided to focus on two to gain a grasp of how multithreaded and singlethreaded programs impact our processing time. 

We analyzed the streaming and analysis times for a certain amount of tweets from Atlanta, GA and Cleveland, OH, (10, 20, 40, 60) for multithreaded and single threaded programs. Surprisingly, we found that on average for both cities, that the multithreaded programs took longer than alternating every so many tweets to streaming from another location. This can be seen in the Excel worksheet in the repository. 

On average for both types of programs, it took longer to stream X amount of tweets from Cleveland, Ohio than to stream X amount of tweets from Atlanta, Georgia. This was not as surprising, because Atlanta is a much more metropolitan city than Cleveland and higher population. Also, our geographical coordinates for location spanned a much larger area for Georgia than for Cleveland. A lot of the time also depends on the Twitter API where we are waiting for tweets to be streamed. As we are not 100% sure as to how the method GetStreamFilter() determines which public tweets it chooses to stream to us, we can only assume there is a higher number of accessible tweets from Atlanta, GA. 

An interesting thing to note was that multithreading did pose to be faster for streaming tweets from Cleveland for smaller amounts of tweets. However, as we need to process higher and higher amounts of tweets, we noticed that the processing time of multithreading surpassed the processing time of the single threaded program. 

Although implementing a single threaded program may be more time efficient, it also can impact the quality of our tweets that we are streaming. We have to alternate between streaming Cleveland, OH tweets and Atlanta, GA tweets which means that we may not catch any current incoming tweets from the connection that is sleeping that we would have caught with a multithreaded program. 

We still do not circumvent the issue, in either multithreaded or single threaded programs, where we are only allowed 2-3 connections open from a specific token, which means that we are also limited to how many cities and areas in the United States we can analyze. 

