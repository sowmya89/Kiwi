var mysql = require('mysql');

function getConnection() {
    var connection = mysql.createConnection({
        host : 'cmpe280.chowxkprohlg.us-west-1.rds.amazonaws.com',
        user : 'ciphers',
        password: 'ciphers280',
        database : 'cmpe295b_webapp',
        port: 3306
    });

   /* var connection = mysql.createConnection({
        host : 'localhost',
        user : 'root',
        password: 'maithili@123',
        database : 'cmpe295b_webapp',
        port: 3306
    });*/
    return connection;  
}

function fetchData(callback, sqlQuery) {

    //console.log("\nSQL Query::" + sqlQuery);

    var connection = getConnection();

    connection.query(sqlQuery, function(err, rows, fields) {
        if (err) {
            console.log("ERROR: " + err.message);
        } else { // return err or result
            callback(err, rows);
        }
    });
    console.log("\nConnection closed..");
    connection.end();
}





exports.fetchData = fetchData;
