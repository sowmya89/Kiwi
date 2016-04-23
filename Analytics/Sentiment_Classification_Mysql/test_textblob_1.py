from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import operator
#import MySQLdb
import mysql.connector
from mysql.connector import errorcode
import sys


# Open database connection
DATABASE_PORT = 3306

try:

    #db = MySQLdb.connect("localhost","root","maithili@123","cmpe295_test" )
    db = mysql.connector.connect(host='localhost',user='root',password='maithili@123',port=int(DATABASE_PORT),database='cmpe295b_webapp')

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = db.cursor()
  #cursor.execute("INSERT INTO cmpe295b_webapp.test_2(name) VALUES('Jack London5')")

  print "************************"
  with(open('negative.txt', 'r'))as in_file:
    text = in_file.read()
    #sents = nltk.sent_tokenize(text,language='english')
    sents= text.splitlines();

  #for sentence in sents:
  for x in range(1,100):
   add_sent = ("INSERT INTO cmpe295b_webapp.sent_sentiment "
            "(sentence,sent_classification,sent_positive, sent_negative,sent_polarity, sent_subjectivity ) "
            "VALUES (%s,%s,%s,%s,%s,%s)")
   #print sents[x]
   sentence = sents[x]
   vs = TextBlob((sentence),analyzer=NaiveBayesAnalyzer())
   #print vs.sentiment
   #print vs.sentiment.classification + " " + str(vs.sentiment.p_pos) + " " + str(vs.sentiment.p_neg)
   sent_classification = str(vs.sentiment.classification)
   sent_positive = str(vs.sentiment.p_pos)
   sent_negative = str(vs.sentiment.p_neg)
   vs1 = TextBlob((sentence))
   #print vs1.sentiment
   sent_polarity =  str(vs1.sentiment.polarity)
   sent_subjectivity = str(vs1.sentiment.subjectivity)
   #print "To be written in sql - "
   print sentence
   print sent_classification + " "+sent_positive + " "+sent_negative + " "+sent_polarity+ " "+ sent_subjectivity
   test_data=(sentence,sent_classification,sent_positive,sent_negative,sent_polarity,sent_subjectivity)
   # Insert new employee
   cursor.execute(add_sent, test_data)


  print "************************"
  # Make sure data is committed to the database
  db.commit()



  cursor.close()
  db.close()




