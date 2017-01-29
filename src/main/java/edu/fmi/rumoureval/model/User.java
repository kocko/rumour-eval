package edu.fmi.rumoureval.model;

public class User implements Comparable<User> {

    private Long id;
    private String name;
    private long followers;
    private String description;
    private long statusesCount;

    private User(Long id, String name, long followers, String description, long statusesCount) {
        this.id = id;
        this.name = name;
        this.followers = followers;
        this.description = description;
        this.statusesCount = statusesCount;
    }

    public Long getId() {
        return id;
    }

    public long getFollowers() {
        return followers;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public long getStatusesCount() {
        return statusesCount;
    }

    @Override
    public int compareTo(User o) {
        return Long.compare(this.id, o.id);
    }

    public class UserBuilder {
        
        private Long id;
        private String name;
        private long followers;
        private String description;
        private long statusesCount;

        public UserBuilder(Long id) {
            this.id = id;
        }

        public UserBuilder name(String text) {
            this.name = name;
            return this;
        }

        public UserBuilder followers(long followers) {
            this.followers = followers;
            return this;
        }

        public UserBuilder description(String description) {
            this.description = description;
            return this;
        }

        public UserBuilder statusesCount(long statusesCount) {
            this.statusesCount = statusesCount;
            return this;
        }

        public User build() {
            return new User(id, name, followers, description, statusesCount);
        }
        
    }
    
}
