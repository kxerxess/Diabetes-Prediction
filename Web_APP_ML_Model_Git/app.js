/**********************************************Importing Packages************************************************/

const express = require("express");
const bodyParser = require("body-parser");
const {
  spawn
} = require('child_process');
const _ = require('lodash');
const app = express();


/**********************************************SET/USE************************************************/

app.use(express.static("public"));
app.use(bodyParser.urlencoded({
  extended: true
}));
app.set('view engine', 'ejs');


/**********************************************Default GET/Post************************************************/

app.get("/", function(req, res) {
  res.render("index", {});
});


app.post("/", function(req, res) {
  let inputData = req.body.input;

  inputData_toNumber = []

  for (i = 0; i < inputData.length; i++) {
    inputData_toNumber.push(_.toNumber(inputData[i]))
  }
  console.log("Data sent to python script: " + inputData_toNumber)


  const spawn = require("child_process").spawn;
  const process = spawn('python', ["py_script.py",
    inputData_toNumber
  ]);

  process.stdout.on('data', function(data) {
    result_ = data.toString()
    console.log('Pipe data from python script: ' + result_);

    app.get("/result", function(req, res) {
      res.render("result", {
        resultVal_html: result_
      });
    });
    res.redirect("/result")
    process.on('close', (code) => {
      console.log('child process close all stdio with code ' + code);
    });
  });
});


/**********************************************Listen************************************************/

app.listen(3000, function() {
  console.log("server started on port 3000")
});
