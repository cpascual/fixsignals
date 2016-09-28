from PyQt4 import Qt

MY_SIGNATURE = 'some_signal_name'
MY_SIG = Qt.SIGNAL('some_other_signal_name')

class MyWidget(Qt.QWidget):

    def m1(self):
        self.connect(self, Qt.SIGNAL('mysigname'), self.myslot)
        self.emit(Qt.SIGNAL('mysigname'), 1, 2)

    def m2(self):
        self.connect(self, Qt.SIGNAL(MY_SIGNATURE), self.myslot)
        self.emit(Qt.SIGNAL(MY_SIGNATURE), 3, 4)

    def m3(self):
        self.connect(self, MY_SIG, self.myslot)
        self.emit(MY_SIG, 5, 6)

    def myslot(self, a, b):
        print a, b, a + b