
var ejs = require("ejs");

var mysql = require('./mysql.js');

var sent_pos=null;
var sent_neg=null;
var count_data=null;
var analysis_data = null;

function homepage(req,res) {


    //var year=null;
    //year=req.param("year");

    //console.log("Year:-"+year);
    var query = "select * from cmpe295b_webapp.sent_sentiment where sent_classification = 'pos'  order by sent_positive LIMIT 10;";
    console.log("Query is:" + query);


    mysql.fetchData(function(err, results) {
        if (err) {
            throw err;
        } else {
            if (results.length > 0) {
                for ( var i = 0; i < results.length; i++) {
                    console.log("Sent_positive:"+results[i].sent_positive);
                }
                var getUser1 = "select sent_negative from cmpe295b_webapp.sent_sentiment where sent_classification = 'neg'  order by sent_negative LIMIT 10;";
                console.log(getUser1);
                mysql.fetchData(function(err, result) {
                    if (err) {
                        throw err;
                    } else {
                        if (result.length > 0) {
                            for ( var j = 0; j < result.length; j++) {
                                console.log("Negative sent:- "+result[j].sent_negative);
                            } ;
                            sent_neg=result;
                        }
                    }
                }, getUser1);

                var getUser2 = "select count(*) as c from cmpe295b_webapp.sent_sentiment ;";
                console.log(getUser2);
                mysql.fetchData(function(err, result) {
                    if (err) {
                        throw err;
                    } else {
                        if (result.length > 0) {
                                console.log("Count:- "+result);

                            count_data=result;
                            console.log(count_data);
                        }
                    }
                }, getUser2);

                sent_pos = results;

                //console.log(state);
                res.render('homepage', {
                    sent_pos : sent_pos,
                    sent_neg: sent_neg,
                    count_data:count_data

                });

            }

        }
    }, query);

}




function cyberbullyingFacts(req,res) {

    var query = "select * from cmpe295b_webapp.sent_sentiment where " +
        "sent_classification = 'neg'  order by sent_negative LIMIT 15; ";

    //"select * from sent_sentiment ;" ;

    console.log("Query is:" + query);


    mysql.fetchData(function(err, results) {
        if (err) {
            throw err;
        } else {
            if (results.length > 0) {
                for ( var i = 0; i < results.length; i++) {
                    console.log(results[i]);
                }
                analysis_data = results;
                console.log(analysis_data);
                res.render('cyberbullyingFacts', {
                    analysis_data : analysis_data
                });
            }
        }
    }, query);
}


exports.cyberbullyingFacts=cyberbullyingFacts;

exports.homepage=homepage;

