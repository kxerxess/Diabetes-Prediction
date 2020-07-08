const express = require("express");
const bodyParser = require("body-parser");
const request = require("request");
const app = express();
const options = {
  uri: 'http://127.0.0.1:5000/',
  method: 'GET',
  json: true,
};

app.use(express.static("public"));
app.use(bodyParser.urlencoded({
  extended: true
}));
app.set('view engine', 'ejs');

app.get("/", function(req, res) {
  res.render("index", {});
});

app.post("/", function(req, res) {
  options.body = {
    'recieved_input': req.body.input.toString()
  };
  console.log('Data sent to api...\n' + options.body.recieved_input);
  request(options, function(error, response, result) {
    result_ = result;
    console.log("Response recieved...\n" + result_);
    app.get("/result", function(req, res) {
      res.render("result", {
        resultVal_html: result_
      });
    });
    res.redirect("/result");
  });
});

app.listen(3000, function() {
  console.log("server started on port 3000")
});
