const express = require('express');
const app = express();
const read = require('./functions/read')
const play = require('./functions/play')
const paint = require('./functions/paint')

app.get("/api", (req, res) => {
    res.json({"users": ["userOne", "userTwo", "userThree"]})
})
app.get("/read", (req, res) => {
    read()
})
app.get("/play", (req, res) => {
    play()
})
app.get("/play", (req, res) => {
    plaint()
})

app.listen(5000, () => {
    console.log("Server started on port 5000")
});