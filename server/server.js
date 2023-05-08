const express = require('express');
const app = express();
const read = require('./functions/read')

app.get("/api", (req, res) => {
    res.json({"users": ["userOne", "userTwo", "userThree"]})
})
app.get("/read", (req, res) => {
    read()
})

app.listen(5000, () => {
    console.log("Server started on port 5000")
});