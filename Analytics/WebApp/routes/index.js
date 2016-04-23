/*
var express = require('express');
var router = express.Router();
var mysql = require('mysql');
/!* GET home page. *!/
var app = express();
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/test', function(req, res) {
  console.log('Inside app.get');

  var con = mysql.createConnection({
    host: "127.0.0.1",
    port: '3306',
    user: "root",
    password: "maithili@123",
    database: "cmpe295b_webapp"
  });

  con.connect(function (err) {
    if (err) {
      throw err;
    }
    else {
      console.log('Connected');
    }
  });

  var combinedString= "";

  //function findCount(req,res,next) {
    console.log("findCount");
    var q2 = "SELECT COUNT(*) FROM ??";
    var t2 = ["sent_sentiment"];
    q2 = mysql.format(q2, t2);
    con.query(q2, function (err, rows) {
      if (err) {
        return res.json({"Error": true, "Message": "Error executing MySQL query"});
      } else {
        //return res.json({"Error": false, "Message": "Success", "Count": rows});
        req.count = rows;
        console.log(rows);
        combinedString +=rows;
        //return next();
      }
    });
  //}

  //function findsent(req,res,next) {
    console.log("findsent");
    var query = "SELECT * FROM ?? ORDER BY sent_positive LIMIT 10";
    var table = ["sent_sentiment"];
    query = mysql.format(query, table);
    con.query(query, function (err, rows) {
      if (err) {
        return res.json({"Error": true, "Message": "Error executing MySQL query"});
      } else {
        //return res.json({"Error": false, "Message": "Success", "Users": rows});
        req.sent=rows;
        console.log(rows);
        combinedString+=rows;
      }
    });
  //}

  console.log(combinedString);


// function renderPage(req,res){
//   res.render('test',{
//     count:req.count,
//     sent: req.sent
//
//   });
// }

//app.get('/test',findCount,findsent,renderPage);

});

module.exports = router;
*/



/*
 * GET home page.
 */

exports.index = function(req, res){
  res.render('Homepage', { title: 'Express' });
};
