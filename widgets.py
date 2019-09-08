# -*- coding: utf-8 -*-

 ##############################################
 ##                                            ##
 ##        Widgets for Purchase package         ##
 ##                                             ##
 ##                                             ##
 ##              from Basiq Series              ##
 ##           by Críptidos Digitales            ##
 ##                 GPL (c)2008                 ##
  ##                                            ##
    ##############################################

"""
"""

import sys
from decimal import Decimal

from PyQt4 import QtCore, QtGui

from cdWidgets import cdComboBox, cdDateEdit, cdLineEdit, cdNumberEdit



class PaymentFR(QtGui.QFrame):

    def __init__(self, *args, **kwds):
        self.mst = kwds.pop('mst')
        self.cnt = self.mst.cnt

        QtGui.QFrame.__init__(self, *args)

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(sizePolicy)

        self.setStyleSheet("color:#FFFFFF; background-color:#E4D46F; border-radius:6;")
        # self.setStyleSheet("background-color:#FFF8D0;")
        self.setFrameShape(QtGui.QFrame.Panel)
        self.setFrameShadow(QtGui.QFrame.Sunken)

        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setSpacing(4)
        self.layout.setMargin(4)


        ## Label
        self.labelFR = QtGui.QFrame(self)
        self.labelFR.setStyleSheet("background-color:#E4D460; border-radius:6;")

        self.labelFRLY = QtGui.QVBoxLayout(self.labelFR)
        self.labelFRLY.setSpacing(0)
        self.labelFRLY.setMargin(2)

        self.labelLA = QtGui.QLabel("Pagto", self.labelFR)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelLA.sizePolicy().hasHeightForWidth())
        self.labelLA.setSizePolicy(sizePolicy)

        self.labelLA.setStyleSheet("color:#FFFFFF;")
        self.labelLA.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelLA.setMargin(3)

        self.labelFRLY.addWidget(self.labelLA)

        self.layout.addWidget(self.labelFR)


        self.itemsFR = QtGui.QFrame(self)

        self.itemsFR.setStyleSheet("QFrame#frame{background-color:#FFF8D0; border-radius:8;}")
        # sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        # self.items.setSizePolicy(sizePolicy)

        self.itemsLY = QtGui.QVBoxLayout(self.itemsFR)
        self.itemsLY.setSpacing(2)
        self.itemsLY.setMargin(2)


        '''

        ## PAYMENT KIND
        self.kindFR = QtGui.QFrame(self.itemsFR)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.kindFR.sizePolicy().hasHeightForWidth())
        self.kindFR.setSizePolicy(sizePolicy)

        self.kindFR.setStyleSheet("background-color:#E4D460; border-radius:6;")
        # self.kindFR.setStyleSheet("color:#FFFFFF; background-color:#90D0E0; border-radius:2px;")
        # self.kindFR.setFrameShape(QtGui.QFrame.Panel)
        # self.kindFR.setFrameShadow(QtGui.QFrame.Raised)

        self.kindLY = QtGui.QVBoxLayout(self.kindFR)
        self.kindLY.setSpacing(4)
        # self.kindLY.setMargin(3)
        self.kindLY.setContentsMargins(6, 4, 6, 6)

        self.kindLA = QtGui.QLabel(u"Tipo", self.kindFR)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.kindLA.sizePolicy().hasHeightForWidth())
        self.kindLA.setSizePolicy(sizePolicy)

        self.kindLA.setFont(font)
        self.kindLA.setStyleSheet("color:#FFFFFF;")
        self.kindLA.setAlignment(QtCore.Qt.AlignCenter)
        self.kindLA.setMargin(3)

        self.kindLY.addWidget(self.kindLA)

        self.itemsLY.addWidget(self.kindFR)


        ## ACCOUNT
        self.accountFR = QtGui.QFrame(self.itemsFR)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.accountFR.sizePolicy().hasHeightForWidth())
        self.accountFR.setSizePolicy(sizePolicy)

        self.accountFR.setStyleSheet("background-color:#E4D460; border-radius:6;")

        self.accountLY = QtGui.QVBoxLayout(self.accountFR)
        self.accountLY.setSpacing(4)
        self.accountLY.setContentsMargins(6, 4, 6, 6)

        self.accountLA = QtGui.QLabel(u"Cuenta", self.accountFR)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.accountLA.sizePolicy().hasHeightForWidth())
        self.accountLA.setSizePolicy(sizePolicy)

        self.accountLA.setFont(font)
        self.accountLA.setAlignment(QtCore.Qt.AlignCenter)
        self.accountLA.setMargin(3)

        self.accountLY.addWidget(self.accountLA)

        self.itemsLY.addWidget(self.accountFR)


        self.numberFR = QtGui.QFrame(self.itemsFR)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numberFR.sizePolicy().hasHeightForWidth())
        self.numberFR.setSizePolicy(sizePolicy)
        self.numberFR.setStyleSheet("background-color:#E4D460; border-radius:2px;")

        self.numberLY = QtGui.QVBoxLayout(self.numberFR)
        self.numberLY.setSpacing(4)
        self.numberLY.setContentsMargins(6, 4, 6, 6)

        self.numberLA = QtGui.QLabel(u"Número", self.numberFR)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numberLA.sizePolicy().hasHeightForWidth())
        self.numberLA.setSizePolicy(sizePolicy)
        self.numberLA.setFont(font)
        self.numberLA.setStyleSheet("color:#FFFFFF;")
        self.numberLA.setAlignment(QtCore.Qt.AlignCenter)
        self.numberLA.setMargin(3)

        self.numberLY.addWidget(self.numberLA)

        self.itemsLY.addWidget(self.numberFR)

        ## PAYMENT DATE
        self.dateFR = QtGui.QFrame(self.itemsFR)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateFR.sizePolicy().hasHeightForWidth())
        self.dateFR.setSizePolicy(sizePolicy)
        self.dateFR.setStyleSheet("background-color:#E4D460; border-radius:2px;")

        self.dateLY = QtGui.QVBoxLayout(self.dateFR)
        self.dateLY.setSpacing(4)
        self.dateLY.setContentsMargins(6, 4, 6, 6)

        self.dateLA = QtGui.QLabel(u"Fecha", self.dateFR)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateLA.sizePolicy().hasHeightForWidth())
        self.dateLA.setSizePolicy(sizePolicy)
        self.dateLA.setFont(font)
        self.dateLA.setStyleSheet("color:#FFFFFF;")
        self.dateLA.setAlignment(QtCore.Qt.AlignCenter)
        self.dateLA.setMargin(3)

        self.dateLY.addWidget(self.dateLA)

        self.itemsLY.addWidget(self.dateFR)


        ## PAYMENT AMOUNT
        self.amountFR = QtGui.QFrame(self.itemsFR)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amountFR.sizePolicy().hasHeightForWidth())
        self.amountFR.setSizePolicy(sizePolicy)
        self.amountFR.setStyleSheet("background-color:#E4D460; border-radius:2px;")

        self.amountLY = QtGui.QVBoxLayout(self.amountFR)
        self.amountLY.setSpacing(4)
        self.amountLY.setContentsMargins(6, 4, 6, 6)

        self.amountLA = QtGui.QLabel(u"Monto", self.amountFR)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amountLA.sizePolicy().hasHeightForWidth())
        self.amountLA.setSizePolicy(sizePolicy)
        self.amountLA.setFont(font)
        self.amountLA.setStyleSheet("color:#FFFFFF;")
        self.amountLA.setAlignment(QtCore.Qt.AlignCenter)
        self.amountLA.setMargin(3)

        self.amountLY.addWidget(self.amountLA)

        self.itemsLY.addWidget(self.amountFR)


        ## PAYMENT RETURN
        self.returnFR = QtGui.QFrame(self.itemsFR)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.returnFR.sizePolicy().hasHeightForWidth())
        self.returnFR.setSizePolicy(sizePolicy)
        self.returnFR.setStyleSheet("background-color:#90D0E0; border-radius:2px;")

        self.returnLY = QtGui.QVBoxLayout(self.returnFR)
        self.returnLY.setSpacing(4)
        self.returnLY.setContentsMargins(6, 4, 6, 6)

        self.returnLA = QtGui.QLabel(u"Cambio", self.returnFR)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.returnLA.sizePolicy().hasHeightForWidth())
        self.returnLA.setSizePolicy(sizePolicy)
        self.returnLA.setFont(font)
        self.returnLA.setStyleSheet("color:#FFFFFF;")
        self.returnLA.setAlignment(QtCore.Qt.AlignCenter)
        self.returnLA.setMargin(3)

        self.returnLY.addWidget(self.returnLA)

        self.itemsLY.addWidget(self.returnFR)

        self.returnFR.setMaximumWidth(0)

        '''

        self.layout.addWidget(self.itemsFR)


        self.buttonFR = QtGui.QFrame(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonFR.sizePolicy().hasHeightForWidth())
        self.buttonFR.setSizePolicy(sizePolicy)

        self.buttonLY = QtGui.QVBoxLayout(self.buttonFR)
        self.buttonLY.setSpacing(0)
        self.buttonLY.setMargin(2)

        self.buttonLA = QtGui.QLabel(self.buttonFR)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonLA.sizePolicy().hasHeightForWidth())
        self.buttonLA.setSizePolicy(sizePolicy)
        self.buttonLA.setFont(font)
        self.buttonLA.setStyleSheet("color:#FFFFFF;")
        self.buttonLA.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonLA.setMargin(3)

        self.buttonLY.addWidget(self.buttonLA)


        ## PAYMENT ADDBUTTON
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aAdd = QtGui.QAction(icon, u"", self)
        self.aAdd.setIconText(u"")
        self.connect(self.aAdd, QtCore.SIGNAL("triggered()"), self.add)

        self.addTO = QtGui.QToolButton(self.buttonFR)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addTO.sizePolicy().hasHeightForWidth())
        self.addTO.setSizePolicy(sizePolicy)
        self.addTO.setFont(font)
        self.addTO.setIconSize(QtCore.QSize(32,32))

        self.addTO.setAutoRaise(True)
        self.addTO.setDefaultAction(self.aAdd)
        self.addTO.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.buttonLY.addWidget(self.addTO)

        # self.connect(self.addTO, QtCore.SIGNAL("triggered()"), self.add)


        # self.layout.addWidget(self.buttonFR)
        self.layout.insertWidget(0, self.buttonFR)


        self.count = 0

        self.kind = []
        self.account = []
        self.number = []
        self.date = []
        self.amount = []
        self.returnED = []
        # self.addTO = []

        self.clear()


    _messages4Modification = []
    def messages4Modification(self, index):
        return self._messages4Modification[index]
    def messages4Modification_set(self, index=None, value=''):
        if index is None:
            self._messages4Modification = []
        elif index == len(self._messages4Modification):
            self._messages4Modification.append(value)
        else:
            self._messages4Modification[index] = value


    _messages4Validity = []
    def messages4Validity(self, index):
        return self._messages4Validity[index]
    def messages4Validity_set(self, index=None, value=''):
        if index is None:
            self._messages4Validity = []
        elif index == len(self._messages4Validity):
            self._messages4Validity.append(value)
        else:
            self._messages4Validity[index] = value



    _status = u'normal'
    _status_previous = []
    def status(self):
        return self._status
    def status_is(self, value):
        return value == self._status
    def status_set(self, value):
        self._status_previous.insert(0, self._status)
        self._status = value
    def status_reset(self):
        self._status = self._status_previous.pop(0)




    def add(self):
        """purchases.widgets.PaymentFR.add()"""
        
        f=k
        
        frameFont = QtGui.QFont()
        frameFont.setPointSize(10 * self.mst.layoutZoom)
        frameFont.setBold(True)

        self.old.append(None)

        self.kind.append(PaymentKindCB(self.kindFR, mst=self.mst))
        self.kind[self.count].index = self.count
        self.kind[self.count].setFont(frameFont)
        self.kindLY.addWidget(self.kind[self.count])

        self.connect(self.kind[self.count], QtCore.SIGNAL('currentIndexChanged(int)'), self.kind_changed)

        self.account.append(paymentAccountCB(self.accountFR, mst=self.mst))
        self.account[self.count].index = self.count
        self.account[self.count].setFont(frameFont)
        self.account[self.count].setEmptyAllowed(False)
        self.accountLY.addWidget(self.account[self.count])


        self.number.append(cdLineEdit.CDLineEdit(self.numberFR))
        self.number[self.count].index = self.count
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.number[self.count].sizePolicy().hasHeightForWidth())
        self.number[self.count].setSizePolicy(sizePolicy)
        self.number[self.count].setStyleSheet("color:#006000; background-color:#FFFFFF; border-radius:2px;")
        self.number[self.count].setFont(frameFont)
        self.number[self.count].setFrame(False)
        self.number[self.count].setAlignment(QtCore.Qt.AlignCenter)
        self.number[self.count].setEmptyAllowed(False)
        self.numberLY.addWidget(self.number[self.count])

        self.connect(self.number[self.count], QtCore.SIGNAL('editingFinished()'), self.numberChanged)

        self.date.append(cdDateEdit.CDDateEdit(self.dateFR))
        self.date[self.count].index = self.count
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.date[self.count].sizePolicy().hasHeightForWidth())
        self.date[self.count].setSizePolicy(sizePolicy)
        self.date[self.count].setStyleSheet("color:#006000; background-color:#FFFFFF; border-radius:2px;")
        self.date[self.count].setDisplayFormat('dd MMM yyyy')
        self.date[self.count].setFont(frameFont)
        self.dateLY.addWidget(self.date[self.count])

        self.connect(self.date[self.count], QtCore.SIGNAL('editingFinished()'), self.dateChanged)


        self.amount.append(cdNumberEdit.CDNumberEdit(self.amountFR))
        self.amount[self.count].index = self.count
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amount[self.count].sizePolicy().hasHeightForWidth())
        self.amount[self.count].setSizePolicy(sizePolicy)
        self.amount[self.count].setStyleSheet("color:#006000; background-color:#FFFFFF; border-radius:2px;")
        self.amount[self.count].setFrame(False)
        self.amount[self.count].setFont(frameFont)
        self.amount[self.count].setAlignment(QtCore.Qt.AlignCenter)
        self.amount[self.count].setEmptyAllowed(False)
        self.amountLY.addWidget(self.amount[self.count])

        self.connect(self.amount[self.count], QtCore.SIGNAL('editingFinished()'), self.amountChanged)


        self.returnED.append(cdNumberEdit.CDNumberEdit(self.returnFR))
        self.returnED[self.count].index = self.count
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.returnED[self.count].sizePolicy().hasHeightForWidth())
        self.returnED[self.count].setSizePolicy(sizePolicy)
        self.returnED[self.count].setStyleSheet("color:#006000; background-color:#FFFFFF; border-radius:2px;")
        self.returnED[self.count].setFrame(False)
        self.returnED[self.count].setFont(frameFont)
        self.returnED[self.count].setAlignment(QtCore.Qt.AlignCenter)
        self.returnLY.addWidget(self.returnED[self.count])


        self.returnFR.hide()

        self.frame.show()

        self.messages4Modification_set(self.count)
        self.messages4Validity_set(self.count)

        self.count += 1


    def clear(self):
        for index in range(self.count):
            self.kind.pop(self.count-index-1).deleteLater()
            self.account.pop(self.count-index-1).deleteLater()
            self.number.pop(self.count-index-1).deleteLater()
            self.date.pop(self.count-index-1).deleteLater()
            self.amount.pop(self.count-index-1).deleteLater()
            self.returnED.pop(self.count-index-1).deleteLater()

        self.count = 0
        self.initialCount = 0

        self.messages4Modification_set()
        self.messages4Validity_set()

        self.old = []


    def isValid(self, index):
        # print "purchases.widgets.paymentFR.isValid()", index

        if not index is None:

            isValid = True
            messages = u''

            if not self.kind[index].isValid():
                isValid = False
                messages += u"Tipo de Pago no válido\n"

            if not self.accountFR.isHidden():
                if not self.account[index].isValid():
                    isValid = False
                    messages += u"Número de cuenta del pago %s no válido\n" % (index+1)
                elif self.account[index].currentIndex() == 0:
                    isValid = False
                    messages += u"Falta número de cuenta del pago %s\n" % (index+1)

            if not self.numberFR.isHidden():
                if self.number[index].isEmpty():
                    isValid = False
                    messages += u"Falta el Número de pago %s\n" % (index+1)
                elif not self.number[index].isValid():
                    isValid = False
                    messages += u"El Número de pago %s no es válido\n" % (index+1)

            if not self.dateFR.isHidden():
                if self.date[index].date() == QtCore.QDate(2000, 1, 1):
                    isValid = False
                    messages += u"Falta corregir la fecha\n"

            if not self.amountFR.isHidden():
                if not self.amount[index].value():
                    isValid = False
                    messages += u"Falta el monto de pago %s\n" % (index+1)
                elif not self.amount[index].isValid():
                    isValid = False
                    messages += u"El monto de pago %s no es válido\n" % (index+1)

            if not self.returnFR.isHidden():
                if not self.returnED[index].isValid():
                    isValid = False
                    messages += u"El cambio en el pago no es válido\n"

            self.messages4Validity_set(index, messages.rstrip("\n"))

            return isValid


    def kind_changed(self, index):
        # print("purchases.widgets.paymentFR.kind_changed()")
        paymentIndex = self.sender().index
        """
        if self.sender().itemText(index) == u'Efectivo':
            self.account[paymentIndex].hide()
            self.number[paymentIndex].hide()
            self.date[paymentIndex].show()
            self.amount[paymentIndex].show()
            self.returnED[paymentIndex].show()

        elif self.sender().itemText(index) == u'Cheque':
            self.account[paymentIndex].show()
            self.number[paymentIndex].show()
            self.date[paymentIndex].show()
            self.amount[paymentIndex].show()
            self.returnED[paymentIndex].hide()
        """

        self.update()

        self.emit(QtCore.SIGNAL('dataChanged()'))


    def amountChanged(self):
        self.update()
        self.emit(QtCore.SIGNAL('dataChanged()'))


    def dateChanged(self):
        self.update()
        self.emit(QtCore.SIGNAL('dataChanged()'))


    def exists(self, index):
        if self.kind[index].currentText() == u'Cheque':
            if self.account[index].isValid():
                if self.number[index].isValid():
                    return self.cnt.document(kind_code=self.cnt.documentKind_cheque['code'], number="{}".format(self.number[index].text()), reference='{}'.format(self.account[index].currentText()))


    def numberChanged(self):
        index = self.sender().index
        document = self.exists(index)
        if document:
            result = self.cnt.app.showMessage('warning', u"Ya existe", u"Quieres usarlo?")
            self.old[index] = document
            self.date[index].setDate(document['date'])
            self.amount[index].setValue(document['total'])
        self.update()
        self.emit(QtCore.SIGNAL('dataChanged()'))


    def modified_data(self, index):
        # print "purchases.widgets.paymentFR.modified_data(%s)" % index

        messages = u''
        data = {}

        document = self.exists(index)
        if document:
            data['id'] = document['id']
        else:
            if self.kind[index].isModified():
                data['kind'] = {'code':self.kind[index].currentData()}
                messages += u"Tipo de Pago %s modificado\n" % (index+1)

            if not self.accountFR.isHidden():
                if self.account[index].isModified():
                    data['reference'] = unicode(self.account[index].currentText())
                    messages += u"Se cambió de cuenta %s\n" % (index+1)

            if not self.numberFR.isHidden():
                if self.number[index].isModified():
                    data['number'] = unicode(self.number[index].text())
                    messages += u"Se cambió el número de pago %s\n" % (index+1)

            if not self.dateFR.isHidden():
                if self.date[index].isModified():
                    data['date'] = self.date[index].date().toPyDate()
                    messages += u"Se cambió la fecha de pago %s\n" % (index+1)

            if not self.amountFR.isHidden():
                if self.amount[index].isModified():
                    data['total'] = self.amount[index].value()
                    messages += u"Se cambió el monto del pago %s\n" % (index+1)

            if not self.returnFR.isHidden():
                if self.returnED[index].isModified():
                    data['subtotal'] = self.returnED[index].value()
                    messages += u"Se cambió el cambio %s\n" % (index+1)

            if data:
                if self.old[index]:
                    data['id'] = self.old[index]['id']

        self.messages4Modification_set(index, messages.rstrip("\n"))

        return data

    @property
    def total(self):
        total = Decimal('0')
        for index in range(self.count):
            total += self.amount[index].value()
        return total


    def setData(self, index, data):
        # print "purchases.widgets.paymentFR.setData()"

        self.old[index] = data
        
        # print(index, data)
        # print(self.kind)
        
        # for x in range(len(self.kind)):
            # print self.kind[index].itemText(x)
            # print self.kind[index].itemData(x)
        

        self.kind[index].setCurrentData(data.kind['code'], initialToo=True)
        if data.reference:
            self.account[index].setCurrentText(data.reference, initialToo=True)
        if data.number:
            self.number[index].setText(data.number, initialToo=True)
        self.date[index].setDate(data.date, initialToo=True)
        self.amount[index].setValue(data.total, initialToo=True)
        self.returnED[index].setValue(data.subtotal, initialToo=True)

        # self.kind[index].setCurrentData(data['kind']['code'], initialToo=True)
        # if data['reference']:
            # self.account[index].setCurrentText(data['reference'], initialToo=True)
        # if data['number']:
            # self.number[index].setText(data['number'], initialToo=True)
        # self.date[index].setDate(data['date'], initialToo=True)
        # self.amount[index].setValue(data['total'], initialToo=True)
        # self.returnED[index].setValue(data['subtotal'], initialToo=True)




    def update(self):
        # print "purchases.widgets.paymentFR.update()   {\n    %s" % self.status()

        if self.status() == u'normal':

            frameVisible = [0, 0, 0]
            
            # print(999077, self.kind)

            for index, kind in enumerate(self.kind):
                
                # print(index, kind, kind.currentIndex())
                
                # print [self.cnt.payment_documentKind('traspaso bancario')['code']]
                
                if kind.currentData() == self.cnt.documentKind_efectivo['code']:
                    self.account[index].setMaximumWidth(0)
                    self.number[index].setMaximumWidth(0)
                    self.date[index].setMaximumWidth(1000)
                    self.amount[index].setMaximumWidth(1000)
                    # self.returnED[index].setMaximumWidth(1000)
                    frameVisible[2] = 1

                elif kind.currentData() in [self.cnt.documentKind_cheque['code']]:
                    self.account[index].setMaximumWidth(1000)
                    frameVisible[0] = 1
                    self.number[index].setMaximumWidth(1000)
                    frameVisible[1] = 1
                    # self.ui.paymentNumber[index].setEnabled(True)
                    self.date[index].setMaximumWidth(1000)
                    self.amount[index].setMaximumWidth(1000)
                    # self.returnED[index].setMaximumWidth(0)
                    
                elif kind.currentData() in [self.cnt.payment_documentKind('traspaso bancario')['code']]:
                    frameVisible[0] = 1
                    self.account[index].setMaximumWidth(1000)
                    frameVisible[1] = 1
                    self.number[index].setMaximumWidth(1000)
                    self.date[index].setMaximumWidth(1000)
                    self.date[index].setMaximumDate(QtCore.QDate().currentDate())
                    self.amount[index].setMaximumWidth(1000)

                if frameVisible[0]:
                    self.accountFR.show()
                else:
                    self.accountFR.hide()

                if frameVisible[1]:
                    self.numberFR.show()
                    self.number[index].show()
                else:
                    self.numberFR.hide()

                if frameVisible[2]:
                    self.returnFR.show()
                else:
                    self.returnFR.hide()

            self.updateStatus()

            # self.updateStatus()

        # print "purchases.widgets.paymentFR.update()   }"


    def updateStatus(self):
        # print("purchases.widgets.paymentFR.updateStatus()")
        # print(len(self.kind))
        for index, kind in enumerate(self.kind):
            self.addTO.setEnabled(self.isValid(index))






class PaymentKindCB(cdComboBox.CDComboBox):

    def __init__(self, *args, **kwds):
        self.mst = kwds.pop('mst', None)
        self.cnt = self.mst.cnt

        cdComboBox.CDComboBox.__init__(self, *args)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.setStyleSheet("color:#006000; background-color:#FFFFFF; border-radius:2px;")

        self.load()


    def load(self):
        self.clear()
        # kinds = self.cnt.documentKinds(**{'referenceLIKE':u'pago'})
        kinds = self.cnt.documentKinds_pull(cast_='payment')
        # print(kinds)
        self.addItem(u"pendiente", -1)
        for kind in kinds:
            self.addItem(kind['name'].capitalize(), kind['code'])
        if len(kinds) == 1:
            # print(998001)
            self.setCurrentIndex(1)
        else:
            # print(998002)
            self.setCurrentIndex(0)
            # print(999003, self.currentIndex())


class paymentAccountCB(cdComboBox.CDComboBox):

    def __init__(self, *args, **kwds):
        self.mst = kwds.pop('mst')
        self.cnt = self.mst.cnt

        cdComboBox.CDComboBox.__init__(self, *args)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.setStyleSheet("color:#006000; background-color:#FFFFFF; border-radius:2px;")

        self.load()


    def load(self):        
        self.clear()
        holder = self.cnt.app.holder
        if holder['accounts']:
            self.addItem(u"", -1)
            for account in holder['accounts']:
                bank = self.cnt.origin(id=int(account['reference']))
                self.addItem("%s %s" % (bank['person']['alias'], account['value']), account['id'])
        else:
            self.setToolTip(u"No se han dado de alta las cuentas bancarias")


