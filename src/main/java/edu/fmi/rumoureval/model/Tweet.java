package edu.fmi.rumoureval.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Tweet implements Comparable<Tweet> {
    
    private Long id;
    private String text;
    private TweetStatistics statistics;
    private User author;
    private Long inReplyToTweetId;
    private BreakingNews about;
    
    public Tweet() {
        
    }
    
    private Tweet(Long id, String text, TweetStatistics statistics, User author, Long inReplyToTweetId, BreakingNews about) {
        this.id = id;
        this.text = text;
        this.statistics = statistics;
        this.author = author;
        this.inReplyToTweetId = inReplyToTweetId;
        this.about = about;
    }

    public Long getId() {
        return id;
    }

    public String getText() {
        return text;
    }

    public TweetStatistics getStatistics() {
        return statistics;
    }

    public User getAuthor() {
        return author;
    }

    public Long getInReplyToTweetId() {
        return inReplyToTweetId;
    }

    public BreakingNews getAbout() {
        return about;
    }

    @Override
    public int compareTo(Tweet o) {
        return Long.compare(this.id, o.id);
    }

    public static class TweetBuilder {
        private Long id;
        private String text;
        private TweetStatistics statistics;
        private User author;
        private Long inReplyToTweetId;
        private BreakingNews about;
        
        public TweetBuilder(Long id) {
            this.id = id;
        }
        
        public TweetBuilder text(String text) {
            this.text = text;
            return this;
        }
        
        public TweetBuilder statistics(TweetStatistics statistics) {
            this.statistics = statistics;
            return this;
        }
        
        public TweetBuilder author(User author) {
            this.author = author;
            return this;
        }
        
        public TweetBuilder inReplyToTweedId(Long inReplyToTweetId) {
            this.inReplyToTweetId = inReplyToTweetId;
            return this;
        }
        
        public TweetBuilder about(BreakingNews about) {
            this.about = about;
            return this;
        }
        
        public Tweet build() {
            return new Tweet(id, text, statistics, author, inReplyToTweetId, about);
        }
        
    }
    
}
