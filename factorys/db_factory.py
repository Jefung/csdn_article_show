import conf
from sql_factory import SqliteFactory

db_factory = SqliteFactory("database")
csdn_article_table = db_factory.db("Spider", conf.db_file).table("CsdnArticle")
# db.insert({"id":"0","title":"1","content":"2","time":"3","author":"4","tags":"5","read_count":"6"})
# print(csdn_article_table.is_exists("53423634","2016年12月01日 17:00:31"))
# print(csdn_article_table.get({"id":"82920072"})[0]["content"])