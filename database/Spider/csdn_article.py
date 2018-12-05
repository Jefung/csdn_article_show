from sqlalchemy import *
from sql_factory.base_table import BaseTable


class CsdnArticle(BaseTable):
    table_columns = [
        Column('id', String(50), primary_key=True),
        Column('title', String(50)),
        Column('author', String(50)),
        Column('time', String(50)),
        Column('read_count', String(50)),
        Column('tags', String(255)),
        Column('content', TEXT),
    ]
    page_nums = 1
    search_count = 0
    def is_exists(self, article_id: str, post_time: str = None) -> bool:
        res = self.get({"id": article_id})
        if len(res) > 0:
            if post_time is not None and res[0]["time"] < post_time:
                return False
            return True
        else:
            return False

    def page_count(self):
        return int(self.search_count/self.page_nums)

    def set_page_nums(self, nums):
        self.page_nums = nums

    def search(self,
               start_time=None,
               end_time=None,
               title=None,
               author=None,
               article_id=None,
               page_num=1, ):
        if page_num <= 0:
            raise Exception("page num must more than 0: " + page_num)
        stmt = (
            select([
                self.c['id'],
                self.c['author'].label("作者"),
                self.c['title'].label("标题")
            ]).select_from(
                self.connect
            ).limit(
                self.page_nums
            ).offset((page_num - 1) * self.page_nums)
        )

        count_stmt = select(
            [func.count()]
        ).select_from(
            self.connect)
        if start_time is not None and end_time is not None:
            stmt = stmt.where(text("time <= '{}' and time >= '{}'".format(end_time, start_time)))
            count_stmt = count_stmt.where(text("time <= '{}' and time >= '{}'".format(end_time, start_time)))
        if title is not None:
            stmt = stmt.where(text("title like '%{}%'".format(title)))
            count_stmt = count_stmt.where(text("title like '%{}%'".format(title)))
        if author is not None:
            stmt = stmt.where(text("author = '{}'".format(author)))
            count_stmt = count_stmt.where(text("author = '{}'".format(author)))
        if article_id is not None:
            stmt = stmt.where(text("id = '{}'".format(article_id)))
            count_stmt = count_stmt.where(text("id = '{}'".format(article_id)))
        res = self.engine.execute(stmt).fetchall()
        self.search_count = self.engine.execute(count_stmt).scalar()

        ls = []
        for row in res:
            ls.append(dict(row))
        return ls

        pass
