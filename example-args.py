from PyQt4.Qt import (QLabel, QString, qApp)

class Window(QLabel):
    def foo(self, value, tr=None):
        self.tr("Message %1").arg(self.getText())  # some comment
        tr("Message %1 and %2").arg(self.getText()).arg(value)
        qApp.translate("Message %1 and %2").arg(self.getText(), value)
        QString("Message %1 and %2").arg(self.getText(), value)
        print(tr("Some message %1").arg(value))
