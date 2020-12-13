#Summer 2017 
#CourseName : Social Network Analysis
#CourseNo   : BIA 658 A
#Date       : 06-21-2017
#Name       : Vaibhav Desai
#Project


rm(list=ls())

install.packages("twitteR")
install.packages("igraph")

install.packages("devtools")
devtools::install_github("JohnCoene/GraphTweets")
library(graphTweets)
library(twitteR)
library(igraph)

# Declare Twitter API Credentials
api_key <- "lLNig9pjNka9XP0uuxTw6iLST" # From dev.twitter.com
api_secret <- "WQci4cHMIj47GdvorDUyoFjFlVVBEeVbXeN35GobeMmckcoZaL" # From dev.twitter.com
token <- "183965322-IfewMcvANZMJlWx6etfMYqg9UT4gNOJEaWED1xoO" # From dev.twitter.com
token_secret <- "yLBysNXWsyofgSIMaEQLxjW76N4hpS8KSQ2GuJRpklhY9" # From dev.twitter.com

# Create Twitter Connection
twitteR:::setup_twitter_oauth(api_key, api_secret, token, token_secret)
tweets <- searchTwitter("#yogaday OR #IDY2017 OR #InternationalYogaday OR #Yogaday2017", n=10000, lang="en", since="2017-06-20")
tweets

tw_df <- twitteR:::twListToDF(tweets)
nrow(tw_df)
View(tw_df)
write.csv(file="D:/VAIBHAV/SocialNetworkAnalysis/Yogagraph.csv", x=tw_df)
library(graphTweets)

edges <- getEdges(data = tw_df, tweets = "text", source = "screenName")
nodes <- getNodes(edges)

library(igraph)
graph <- graph.data.frame(edges[,1:2], directed=TRUE, vertices=nodes)
write.graph(graph, "D:/VAIBHAV/SocialNetworkAnalysis/Yogagraph.graphml", format="graphml")
plot(graph)
