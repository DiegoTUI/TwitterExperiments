"use strict";
// requires
var express = require("express");
var Log = require("log");
var Twitter = require("twitter");
// globals
var app = express();
var http = require("http").Server(app);
var log = new Log("debug");
var io = require("socket.io")(http);
var twitter = new Twitter({
    consumer_key: "u1ath7If8JKMqeT6gkuaBa0Fj",
    consumer_secret: "IEB8e5T00E6vCfwC9BNzHayXSQPyCLqpIEPcYznfegXHfMG3PR",
    access_token_key: "11309872-rHGyjky6pOvcgKjGKb7JoN2Tks1KZuzl98QDbfHl7",
    access_token_secret: "SzNijdXAET8iMQhVKh8KswhabcTgzhPJpkYdxtAjI6CCA"
});
// static server 
app.use(express.static(__dirname + '/html'));
// start listening
http.listen(3123, function() {
    //twitter.stream("statuses/filter",{locations:"-11.733398,35.763229,5.009766,42.970492"}, function(stream) {
    //twitter.stream("statuses/filter",{locations:"2.17804,39.105488,3.641968,40.323383"}, function(stream) {
    twitter.stream("statuses/filter",{locations:"-1.900635,37.37425,5.839233,41.155781"}, function(stream) {
        stream.on("data", function(tweet) {
            //only broadcast the tweet if it's geolocated and it is a point
            if (tweet.coordinates && tweet.coordinates.type == "Point" && tweet.coordinates.coordinates && tweet.coordinates.coordinates.length == 2) {
                var broadcast = {
                    lang: tweet.lang,
                    text: tweet.text,
                    coordinates: tweet.coordinates.coordinates
                };
                io.emit("tweet", broadcast);
            }
        });
    });
});
// socket stuff
io.on("connection", function(/*socket*/) {
    log.debug("a user connected");
});