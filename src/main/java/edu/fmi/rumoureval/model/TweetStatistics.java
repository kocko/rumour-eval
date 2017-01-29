package edu.fmi.rumoureval.model;

public class TweetStatistics implements Comparable<TweetStatistics> {
    
    private Long tweetId;
    private Long reTweetCount;
    private Long favouriteCount;
    
    @Override
    public int compareTo(TweetStatistics o) {
        return Long.compare(tweetId, o.tweetId);
    }
    
    
}
