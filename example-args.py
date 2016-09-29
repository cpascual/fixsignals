from PyQt4.Qt import (QLabel, qApp)

class Window(QLabel):
    def foo(self, value, tr=None):
        self.tr("Messaggio %1").arg(self.getText())  # cose
        tr("Messaggio %1 e %2").arg(self.getText()).arg(value)
        qApp.translate("Messaggio %1 e %2").arg(self.getText(), value)
