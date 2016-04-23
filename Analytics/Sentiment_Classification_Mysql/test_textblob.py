from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import operator
#import MySQLdb
import mysql.connector
import sys


b= TextBlob(("You are horrible"),analyzer=NaiveBayesAnalyzer())
b1= TextBlob("You are horrible")
print b.sentiment
print b1.sentiment


# Open database connection
DATABASE_PORT = 3306

#db = MySQLdb.connect("localhost","root","maithili@123","cmpe295_test" )
db = mysql.connector.connect(host='Maithili',user='root',password='maithili@123',port=int(DATABASE_PORT),database='cmpe295b_webapp')

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print "Database version : %s " % data

print "***************************************"

cursor.execute("INSERT INTO cmpe295b_webapp.test_2(name) VALUES('Jack London')")

print "***************************************"

#add_sent = ("INSERT INTO sent_sentiment "
#            "(sentence,sent_classification,sent_positive, sent_negative,sent_polarity, sent_subjectivity ) "
#            "VALUES (%(sentence)s,%(sent_classification)s,%(sent_positive)s,%(sent_negative)s,%(sent_polarity)s,%(sent_subjectivity)s)")





with(open('sentiment_pos.txt', 'r'))as in_file:
    text = in_file.read()
    #sents = nltk.sent_tokenize(text,language='english')
    sents= text.splitlines();

#for sentence in sents:
for x in range(1,2):
   add_sent = ("INSERT INTO `cmpe295b_webapp`.`sent_sentiment` "
            "(sentence,sent_classification,sent_positive, sent_negative,sent_polarity, sent_subjectivity ) "
            "VALUES (%s,%s,%s,%s,%s,%s)")
   print sents[x]
   sentence = sents[x]
   vs = TextBlob((sentence),analyzer=NaiveBayesAnalyzer())
   print vs.sentiment
   print vs.sentiment.classification + " " + str(vs.sentiment.p_pos) + " " + str(vs.sentiment.p_neg)
   sent_classification = str(vs.sentiment.classification)
   sent_positive = str(vs.sentiment.p_pos)
   sent_negative = str(vs.sentiment.p_neg)
   vs1 = TextBlob((sentence))
   print vs1.sentiment

   sent_polarity =  str(vs1.sentiment.polarity)
   sent_subjectivity = str(vs1.sentiment.subjectivity)

   print "To be written in sql - "
   print sentence + " "+ sent_classification + " "+sent_positive + " "+sent_negative + " "+sent_polarity+ " "+ sent_subjectivity

   test_data=(sentence,sent_classification,sent_positive,sent_negative,sent_polarity,sent_subjectivity)

   # Insert new employee
   cursor.execute(add_sent, test_data)
   #cursor.execute("INSERT INTO `cmpe295b_webapp`.`sent_sentiment` VALUES () ")


# disconnect from server
db.close()


   #print max(vs.sentiment.iteritems(), key=operator.itemgetter(1))[0] , max(vs.iteritems(), key=operator.itemgetter(1))[1]



