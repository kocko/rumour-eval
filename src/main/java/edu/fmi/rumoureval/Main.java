package edu.fmi.rumoureval;

import com.fasterxml.jackson.databind.ObjectMapper;
import edu.fmi.rumoureval.model.Tweet;

import java.io.File;
import java.io.IOException;

public class Main {

    public static void main(String[] args) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        ClassLoader classLoader = Main.class.getClassLoader();
        final String dir = "dataset/rumoureval-data/charliehebdo/552783667052167168/source-tweet/552783667052167168.json";
        Tweet tweet = mapper.readValue(new File(classLoader.getResource(dir).getFile()), Tweet.class);
        System.out.println(tweet.getText());
    }
    
}
