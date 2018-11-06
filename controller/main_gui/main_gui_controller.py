import conf
import quite


class MainGuiController(quite.DialogUiController):
    def __init__(self):
        super().__init__(parent=None, ui_file='res/ui/main_gui/main_window.ui')

        if conf.system.is_debug:
            self.container().setWindowTitle('{} [Debug 模式]'.format(self.container().windowTitle()))

    @classmethod
    def main(cls):
        # Load Resources
        quite.load_qrc('res/res.qrc')
        return cls.class_exec()
