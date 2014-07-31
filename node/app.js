"use strict";

var express = require('express');

var app = express();

app.get('/', function (req, res) {
  res.sendfile('html/twitter_map.html');
});

app.get('/tweets', function (req, res) {
  res.send('tweet, tweet');
});

app.listen(3123);