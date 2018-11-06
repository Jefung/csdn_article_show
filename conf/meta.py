# 项目元属性
from .system import project_name

default_alert_message = '软件即将退出，请重新检查设备连接后，启动软件！'
about_information = ''.join([
    '<h1>{}</h1>'.format(project_name),
    '<h2>开发商：广州市昆德科技有限公司</h2>',
    '<br/>',
    '联系开发者: [请在conf/meta.py这里修改你的联系方式]'
])
