#!/usr/bin/env python2.7

import psycopg2

'''
You must create all the required views in order to run this code correctly
See README.md for instructions
'''


class Database:
    def __init__(self):
        self.db = None
        self.cursor = None

        self.queries = [
            ("What are the most popular three articles of all time?",
                "SELECT articles.title , count(*) AS cnt \
                FROM articles INNER JOIN log ON \
                concat('/article/', articles.slug) = log.path \
                GROUP BY articles.title ORDER BY cnt DESC LIMIT 3"),

            ("Who are the most popular article authors of all time?",
                "SELECT authors.name, sum(cnt) AS total FROM articles \
                INNER JOIN article_count ON articles.id = article_count.id \
                INNER JOIN authors ON author = authors.id \
                GROUP BY authors.name ORDER BY total DESC;"),

            ("On which days did more than 1% of requests lead to errors?",
                "SELECT error_count_by_date.date_trunc, \
                error_count_by_date.count AS error, \
                connection_count_by_date.count AS total, \
                ((error_count_by_date.count + .0) / \
                connection_count_by_date.count) * 100 AS error_rate \
                FROM connection_count_by_date \
                INNER JOIN error_count_by_date ON \
                connection_count_by_date.date_trunc \
                    = error_count_by_date.date_trunc \
                WHERE ((error_count_by_date.count + .0) / \
                connection_count_by_date.count) * 100 > 1 \
                ORDER BY error_rate DESC;")
        ]

    def connect(self):
        self.db = psycopg2.connect("dbname=news")
        self.cursor = self.db.cursor()

    def close(self):
        self.db.close()

    def process(self):
        for i, (question, query) in enumerate(self.queries):
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            print("===============  Question {}  ================".format(i+1))
            print question
            print ""
            # For the first 2 questions
            if i < 2:
                for attribute, count in results:
                    padding = " "*(40 - len(attribute))
                    num_pad = " "*(6 - len(str(count)))
                    print "{} {} --- {}{} views". \
                        format(attribute, padding, num_pad, count)

            # Question 3
            else:
                for datetime, _, _, error_rate in results:
                    print "{} --- {:.2f}% errors". \
                        format(datetime.strftime("%B %d, %Y"), error_rate)
            print "\n\n"

    def run(self):
        self.connect()
        self.process()
        self.close()


print "=============== LOG ANALYSIS PROJECT ================="
print "\n\n"
database = Database()
database.run()

print("=============== END OF REPORT =====================")
