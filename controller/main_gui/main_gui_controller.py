import conf
from datetime import datetime
import quite
from factorys import csdn_article_table
from os.path import splitext
from urllib.parse import urlparse
from quite import *


class MainGuiController(quite.DialogUiController):
    def __init__(self):
        super().__init__(parent=None, ui_file='res/ui/main_gui/main_window.ui')

        if conf.system.is_debug:
            self.container().setWindowTitle('{} [Debug 模式]'.format(self.container().windowTitle()))

        csdn_article_table.set_page_nums(24)

        self.table('search_result').set_just_show_mode()
        self.table('search_result').set_headers(['标题', '作者', 'id'])
        # self.table('search_result').column(0).setTextAlignment()

        self.page_count = csdn_article_table.page_count()
        self.cur_page = 1

        self.show_page()

        self.table("search_result").row_changed.connect(self.show_content)

        @quite.connect_with(self.button("next_page").excited)
        def show_next_page():
            if self.cur_page + 1 > self.page_count:
                self.warning("超出页数")
                return
            self.cur_page += 1
            query()

        @quite.connect_with(self.button("pre_page").excited)
        def show_previous_page():
            if self.cur_page - 1 < 1:
                self.warning("页数不能为0")
                return
            self.cur_page -= 1
            query()

        @quite.connect_with(self.button("goto").excited)
        def goto_page():
            self.cur_page = int(self.double("page").float.value)
            query()

        @quite.connect_with(self.button("query").excited)
        def query():
            start_time = self.date_edit("start").string.value
            end_time = self.date_edit("end").string.value
            date_obj = datetime.strptime(start_time, '%Y-%m-%d')
            start_time = datetime.strftime(date_obj, "%Y{y}%m{m}%d{d} %H:%M:%S").format(y="年", m="月", d="日")
            date_obj = datetime.strptime(end_time, '%Y-%m-%d')
            end_time = datetime.strftime(date_obj, "%Y{y}%m{m}%d{d} %H:%M:%S").format(y="年", m="月", d="日")
            author = self.edit("author").string.value if self.edit("author").string.value.strip() != "" else None
            title = self.edit("title").string.value if self.edit("title").string.value.strip() != "" else None
            article_id = self.edit("article_id").string.value if self.edit(
                "article_id").string.value.strip() != "" else None

            self.show_page(start_time=start_time,
                           end_time=end_time,
                           author=author,
                           title=title,
                           article_id=article_id,
                           page_num=self.cur_page)

        @quite.connect_with(self.button("clear_condition").excited)
        def clear_condition():
            self.edit("title").string.value = ""
            self.edit("author").string.value = ""
            self.edit("article_id").string.value = ""

    def show_page(self, **kwargs):
        res = csdn_article_table.search(**kwargs)
        # res = csdn_article_table.search(self.cur_page)
        self.page_count = csdn_article_table.page_count()
        self.label("current_page").string.value = "第{}页".format(self.cur_page)
        self.label("show_count").string.value = "总{}页".format(self.page_count)
        self.double("page").setRange(0, self.page_count)
        self.update_table(res)

        for row in range(0, self.table('search_result').rowCount()):
            item = self.table('search_result').item(row, 0)
            item.setTextAlignment(Qt.AlignVCenter)

    def show_content(self, row_number):
        article_id = self.table("search_result").item(row_number, 2).text()
        self.text_edit("article").string.value = ""
        cursor = self.text_edit("article").textCursor()
        article_info = csdn_article_table.get("id=" + str(article_id))[0]
        content = article_info["content"]
        self.label("title").string.value = article_info["title"]
        self.label("time").string.value = "时间: " + article_info["time"]
        self.label("author").string.value = "作者: " + article_info["author"]
        self.label("tags").string.value = "标签: " + article_info["tags"]
        self.label("read_count").string.value = "阅读数: " + article_info["read_count"]
        import re
        # \xa0 是不间断空白符 &nbsp;
        content = re.sub('\xa0', " ", content)
        # \u3000 是全角的空白符
        content = re.sub('\u3000', " ", content)

        content = re.sub('[ ]+', " ", content)
        content = re.sub('\n ', '\n', content)
        content = re.sub('\n+', "\n", content)
        content = re.sub('\t+', "\t", content)
        content = re.sub('(\n\t)+', "\n\t", content)
        content = re.sub('^[\n\t]*', "", content)
        start = 0
        for match in re.finditer('<img src="(.*?)".*?>', content):
            cursor.insertText(content[start:match.span()[0]])
            start = match.span()[1]
            parse_url = urlparse(match.group(1))
            ext = splitext(parse_url.path)[1]
            path = parse_url.path
            if ext == "":
                path += ".jpeg"
            image_name = parse_url.scheme + "://" + parse_url.netloc + path
            image_name = image_name.replace("/", "_")
            # 过滤windows字符串，不经过这么一个步骤，你会发现有乱码或无法下载
            image_name = re.sub(r'[？\\*|“<>:/]', '', image_name)
            filename = '{root}/{dir}/{name}'.format(root=conf.image_dir, dir=article_id, name=image_name)
            try:
                import imghdr
                actual_ext = imghdr.what(filename)
                Pixmap = quite.QPixmap(filename, actual_ext)
                cursor.insertImage(Pixmap.toImage())
            except FileNotFoundError as e:
                save_color = self.text_edit("article").textColor()
                format = QTextCharFormat()
                format.setForeground(QColor("red"))
                cursor.setCharFormat(format)
                cursor.insertText("\n[{}未找到]\n".format(str(match.group(1))))
                format.setForeground(save_color)
                cursor.setCharFormat(format)
        cursor.insertText(content[start:])

    def update_table(self, result_list):
        self.table("search_result").dict_list.value = result_list

    @classmethod
    def main(cls):
        # Load Resources
        quite.load_qrc('res/res.qrc')
        return cls.class_exec()
