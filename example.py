
from taurus.external.qt import QtCore
import weakref

_DEBUG = False


class DataModel(QtCore.QObject):
    '''
    An object containing one piece of data which is intended to be shared. The
    data will be identified by its UID (a unique identifier known to objects
    that intend to access the data)

    In general, you are not supposed to instantiate objects of this class
    directly. Instead, you should interact via the :class:`SharedDataManager`,
    which uses :meth:`SharedDataManager.__getDataModel` to ensure that the
    DataModels are singletons.
    '''

    def __init__(self, parent, dataUID, defaultData=None):
        '''
        creator
        :param parent: (QObject) the object's parent
        :param dataUID: (str) a unique identifier for the Data Model
        '''
        QtCore.QObject.__init__(self, parent)
        self.__dataUID = dataUID
        self.__data = defaultData
        self.__isDataSet = False

        self.__readerSlots = []
        self.__writerSignals = []

    def connectReader(self, slot, readOnConnect=True):
        '''
        Registers the given slot method to receive notifications whenever the
        data is changed.

        :param slot: (callable) a method that will be called when the data changes.
                     This slot will be the receiver of a signal which has the
                     data as its first argument.
        :param readOnConnect: (bool) if True (default) the slot will be called
                              immediately with the current value of the data
                              if the data has been already initialized

        .. seealso:: :meth:`connectWriter`, :meth:`getData`
        '''
        self.connect(self.foo.bar.baz, QtCore.SIGNAL("dataChanged"), goo.gaa.slot)
        self.connect(self, QtCore.SIGNAL("dataChanged"), slot)
        self.connect(self, QtCore.SIGNAL(SIGSIGNATURE), slot)
        self.connect(self, QtCore.SIGNAL(foo.SIGSIGNATURE), slot)
        self.connect(self, SIGNALOBJ1, slot)

        self.foo.bar.baz.emit(QtCore.SIGNAL("dataChanged"))
        self.emit(QtCore.SIGNAL("dataChanged"))
        foo.emit(QtCore.SIGNAL("dataChanged"))
        foo.emit(QtCore.SIGNAL("dataChanged"), ARG1, ARG2)
        self.foo.bar.baz.emit(QtCore.SIGNAL("dataChanged"), ARG1, ARG2)

        foo.emit(QtCore.SIGNAL(SIGSIGNATURE))
        foo.emit(QtCore.SIGNAL(SIGSIGNATURE), ARG1, ARG2)
        foo.emit(QtCore.SIGNAL(foo.SIGSIGNATURE))
        foo.emit(QtCore.SIGNAL(foo.SIGSIGNATURE), ARG1, ARG2)
        foo.emit(SIGNALOBJ)
        foo.emit(SIGNALOBJ, ARG1, ARG2)

        if readOnConnect and self.__isDataSet:
            slot(self.__data)
        obj = getattr(slot, '__self__', slot)
        self.Emit((weakref.ref(obj), slot.__name__))

