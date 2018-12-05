# GUI显示CSDN爬虫所爬文章
基于[Jefung/csdn_article_spider: 基于scrapy的CSDN爬虫, 爬取包含关键词'区块链'的所有文章](https://github.com/Jefung/csdn_article_spider)
获取到的数据(用`sqlite`存放在一个数据库文件里)进行显示
## 效果图

![1543995962.jpg](http://images.jefung.cn/1543995962.jpg)

![1543995346.jpg](http://images.jefung.cn/1543995346.jpg)

![1543995393(1).jpg](http://images.jefung.cn/1543995393(1).jpg)

![1543995448(1).jpg](http://images.jefung.cn/1543995448(1).jpg)

![1543995613(1).jpg](http://images.jefung.cn/1543995613(1).jpg)

## 配置
在 conf/system.py 下配置数据库文件`db_file = r'路径'` 和
图片目录 `image_dir = r'目录'`

## 作业繁忙,懒得打包