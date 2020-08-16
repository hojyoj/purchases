# -*- coding: utf-8 -*-

 ##############################################
 ##                                            ##
 ##              Purchases package              ##
 ##                     View                    ##
 ##                                             ##
 ##              from Basiq Series              ##
 ##           by Críptidos Digitales            ##
 ##                 GPL (c)2008                 ##
  ##                                            ##
	##############################################

"""
"""

from __future__ import print_function

__version__ = "0.1.1"

import sys

import logging

from decimal import Decimal
import datetime

from PyQt4 import QtCore, QtGui
from basiq import utilities
from cdWidgets import cdFrame
from cdWidgets import cdTableWidgetItem
from cdWidgets import cdSliderFrame

from purchases import manager_ui
from purchases import capture_ui
from purchases import details_ui
#from purchases import payments_ui
from purchases import tools_ui

#from purchases import widgets
#from purchases import widgets

from basiq import itemsTable
from products import selector as productSelector

from processes import view


class Master(view.Master):

	captureViews = []

	def __init__(self, *args, **kwds):
		# print("""\n        purchases.view.Master.__init__()""")

		view.Master.__init__(self, *args, **kwds)

		self.theme['text']['color'] = '#C0C000'
		self.theme['background']['color'] = '#FFD040'
		self.theme['background']['color2'] = '#FFFDC0'

		self.imports_pending_set(False)

		## Details
		self.details = Details(self)
		self.details.hide()

		self.ui.innerSplitter.insertWidget(1, self.details)

		self.connect(self.eventRouter, QtCore.SIGNAL('suppliersChanged()'), self.loadSuppliers)
		self.connect(self.eventRouter, QtCore.SIGNAL('supplierAdded'), self.supplierAdded)

		self.imported = None

		# print("""        purchases.view.Master.__init__() - END""")


	'''
	def captureView_new(self, *args, **kwds):
		""" Returns an instance of CaptureView
			This method must be replaced not inherited.
		"""
		# print ("        purchases.Master.captureView_new()")

		captureView = CaptureView(self, *args, **kwds)
		self.connect(captureView, QtCore.SIGNAL("captureViewClosed()"), self.manager_update)
		self.ui.outerSplitter.insertWidget(1, captureView)
		captureViews.append(CaptureView(self, *args, **kwds))

		# print ("        purchases.Master.captureView_new() - END")

		return captureView
	'''


	def init(self):
		# print("""        puchases view Master.init()""")

		view.Master.init(self)

		self.loadSuppliers()

		####  Tools Form  ####
		toolsForm = OptionsFR(None, mst=self)
		self.app.master.tools_addForm(toolsForm, self.cnt.cast)


		# print("""        puchases view Master.init() - END""")


	def supplierAdded(self, supplier):
		pass

		# if self.imports_pending:

			# self.import__()


	def loadSuppliers(self):
		# print("""    purchases.view.Master.loadSuppliers()""")

		self.suppliers = self.cnt.suppliers()

		# old = self.manager.ui.cbProveedor.currentData()
		# self.manager.ui.cbProveedor.clear()

		# if self.suppliers:
			# self.manager.ui.cbProveedor.addItem(u"", self.app.holder['id'])
			# for supplierIndex, supplier in enumerate(self.suppliers):
				# self.manager.ui.cbProveedor.addItem("%s %s" % (supplier['person']['name'], supplier['person']['name2']), supplier['id'])
			# if self.manager.ui.frProveedor.isEnabled():
				# self.manager.ui.frProveedor.setToolTip(u"Seleccione uno para filtrar la lista")
		# else:
			# self.manager.ui.cbProveedor.addItem("No hay proveedores", -1)
			# self.manager.ui.frProveedor.setToolTip(u"No hay proveedores capturados")

		# self.manager.ui.cbProveedor.setCurrentData(old)

		self.emit(QtCore.SIGNAL("suppliers_pulled()"))

		# print("""    purchases.view.Master.loadSuppliers() - END""")


	def manager_new(self):
		# print("""    purchases.Master.manager_new()""")

		self.manager = Manager(self)

		self.connect(self.manager, QtCore.SIGNAL('doubleClicked()'), self.details_toggle)

		self.ui.innerSplitter.insertWidget(0, self.manager)

		# self.connect(self.ui.innerSplitter.handle(1), QtCore.SIGNAL("handlePressed"), self.innerHandlePressed)
		self.connect(self.eventRouter, QtCore.SIGNAL("purchasesChanged()"), self.manager.data_update)

		# print("""    purchases.Master.manager_new() - END""")


	def synchronize(self):
		# print("\n    purchases.Master.Synchronize()""")

		try:
			self.manager.ui.extraFR.show()
		except:
			self.manager.ui.extraFR = cdSliderFrame.Form(self.manager, orientation='left')

			# self.manager.ui.FormLY.addWidget(self.manager.ui.extraFR)
			self.app.master.extra_add(self.manager.ui.extraFR)

			self.manager.ui.extraFR.lock_set(True)
			self.manager.ui.extraFR.lock_hide()

			self.manager.ui.messagesTE = QtGui.QTextEdit(self.manager.ui.extraFR)
			self.manager.ui.messagesTE.setText("")

			sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
			sizePolicy.setHorizontalStretch(0)
			sizePolicy.setVerticalStretch(1)
			sizePolicy.setHeightForWidth(self.manager.ui.messagesTE.sizePolicy().hasHeightForWidth())
			self.manager.ui.messagesTE.setSizePolicy(sizePolicy)

			self.manager.ui.extraFR.addWidget(self.manager.ui.messagesTE)

			self.manager.ui.extraFR.addSpacing(8)


			self.manager.ui.acceptBU = QtGui.QPushButton(self.manager.ui.extraFR)
			self.manager.ui.acceptBU.setText("OK")
			self.manager.ui.extraFR.addWidget(self.manager.ui.acceptBU)
			self.connect(self.manager.ui.acceptBU, QtCore.SIGNAL('clicked()'), self.close_import_messages)

			self.connect(self.eventRouter, QtCore.SIGNAL('import_message(QString)'), self.import_messages_update)

		self.imported = self.cnt.newCfdis_pull()

		if self.imported:
			self.app.master.emit(QtCore.SIGNAL("import_message(QString)"), u"Processing documents ...\n")

		self.import__()

		# print("\n    purchases.Master.Synchronize() - END""")


	def close_import_messages(self):
		self.manager.ui.extraFR.hide()
		self.manager.ui.messagesTE.clear()


	def import_messages_update(self, message):
		self.manager.ui.messagesTE.setText(self.manager.ui.messagesTE.toPlainText() + message)



	def import__(self):
		# oldLevel = self.app.stdoutLog.level
		# self.app.stdoutLog.setLevel(logging.INFO)
		self.app.log2sys ( 'info', "    purchases view Master.import__()" )

		if self.imported:

			document = self.imported.pop(0)

			self.app.log2sys ( 'error', "    purchases view Master.import__()\n        document.data: {}\n".format(document.data) )

			self.imports_pending_set()

			## SUPPLIER DATA
			try:
				if document.rol and not document.state_is_stROL_CURRENT:

					result = self.app.showMessage('warning', u"El proveedor {} no existe en el sistema\n\n¿Quieres darlo de alta?".format(document.rol['person']['name']))

					if result == QtGui.QMessageBox.Ok:

						personsPackages = [ x for x in self.app.packages['maintenance'].controllers if x.cast == 'person' ]

						suppliersPackage = [ x for x in personsPackages if x.subCast[1] == 'supplier' ][0]

						self.imports_pending_set()

						suppliersPackage.master.addPerson(document.rol)

						suppliersPackage.master.form_show()

			except:
				self.app.log2sys ( 'error', "!!! purchases.Master.import__()\n        Error: Could not process inexistent supplier\n" )
				raise

			self.app.master.emit(QtCore.SIGNAL("import_message(QString)"), u"    Date: {}, Number: {}, Supplier: {}, UUID: {}\n\n".format(document.date.date(), document.number, document.rol['person']['name'], document.sat['uuid']))

			document.new()

		else:
			self.app.master.emit(QtCore.SIGNAL("import_message(QString)"), "No imports pending\n")

		self.app.log2sys ( 'info', "    purchases view Master.import__() - END" )
		# self.app.stdoutLog.setLevel(oldLevel)

	def imports_pending(self):
		return self._imports_pending
	def imports_pending_set(self, value=True):
		self._imports_pending = value

	def manager_update(self):
		# oldLevel = self.app.stdoutLog.level
		# self.app.stdoutLog.setLevel(logging.INFO)
		self.app.log2sys ( 'info', "    purchases.view  Master.manager_update()" )

		view.Master.manager_update(self)
		self.import__()

		self.app.log2sys ( 'info', "    purchases.view  Master.manager_update() - END" )
		# self.app.stdoutLog.setLevel(oldLevel)


class Manager(view.Manager):

	def __init__(self, *args, **kwds):
		# print("""\n    purchases.view.Manager.__init__()""")

		view.Manager.__init__(self, *args, **kwds)

		## FILTROS

		self.ui.cbProveedor.setMaxVisibleItems(15)
		self.connect(self.ui.cbProveedor, QtCore.SIGNAL("currentIndexChanged(int)"), self.currentProveedorChanged)

		self.connect(self.ui.ch1, QtCore.SIGNAL('stateChanged(int)'), self.data_update)
		self.connect(self.ui.ch2, QtCore.SIGNAL('stateChanged(int)'), self.data_update)
		self.connect(self.ui.ch3, QtCore.SIGNAL('stateChanged(int)'), self.data_update)

		self.connect(self.ui.tipoMercanciaCH, QtCore.SIGNAL('stateChanged(int)'), self.data_update)
		self.connect(self.ui.tipoGastosCH, QtCore.SIGNAL('stateChanged(int)'), self.data_update)

		## TABLA DE CONSULTA
		self.labels = [u"Documento", u"Fecha",  u"Proveedor", u"Monto", u"Saldo", u"Status", u""]
		self.ui.listTA.setColumnCount(len(self.labels))
		self.ui.listTA.setHorizontalHeaderLabels(self.labels)
		self.ui.listTA.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
		self.ui.listTA.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
		self.ui.listTA.horizontalHeader().setResizeMode(6, QtGui.QHeaderView.Stretch)

		# self.ui.listTA.setToolTip(u"ALT+D muestra detalles de la Compra seleccionada")

		## BUTTONS

		iconTextLayout = QtCore.Qt.ToolButtonTextBesideIcon

		font = QtGui.QFont()
		font.setPointSize(10 * self.mst.layoutZoom)
		font.setBold(True)

		self.ui.toAgregar.setFont(font)
		self.ui.toAgregar.setDefaultAction(self.aAdd)
		self.ui.toAgregar.setIconSize(QtCore.QSize(44, 40))
		self.ui.toAgregar.setToolButtonStyle(iconTextLayout)

		## EDIT
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap(":/Edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.aEdit = QtGui.QAction(icon1, u"&Modificar", self)
		self.aEdit.setCheckable(True)
		self.aEdit.setIconText(u"&Modificar")
		self.connect(self.aEdit, QtCore.SIGNAL("triggered()"), self.edit)

		self.ui.toModificar.setFont(font)
		self.ui.toModificar.setDefaultAction(self.aEdit)
		self.ui.toModificar.setIconSize(QtCore.QSize(44, 40))
		self.ui.toModificar.setToolButtonStyle(iconTextLayout)

		## REMOVE
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap(":/Minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.aRemove = QtGui.QAction(icon2, u"&Eliminar", self)
		self.aRemove.setCheckable(True)
		self.aRemove.setIconText(u"&Eliminar")
		self.connect(self.aRemove, QtCore.SIGNAL("triggered()"), self.elimina)


		self.ui.toEliminar.setFont(font)
		self.ui.toEliminar.setDefaultAction(self.aRemove)
		self.ui.toEliminar.setIconSize(QtCore.QSize(44, 40))
		self.ui.toEliminar.setToolButtonStyle(iconTextLayout)

		## PAY
		# icon = QtGui.QIcon()
		# icon.addPixmap(QtGui.QPixmap(":/Cash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		# self.aPay = QtGui.QAction(icon, u"Pa&gar", self)
		# self.aPay.setCheckable(True)
		# self.aPay.setIconText(u"Pa&gar")
		# self.connect(self.aPay, QtCore.SIGNAL("triggered()"), self.pay)


		self.ui.paymentTO.setFont(font)
		self.ui.paymentTO.setDefaultAction(self.aPay)
		self.ui.paymentTO.setIconSize(QtCore.QSize(44, 40))
		self.ui.paymentTO.setToolButtonStyle(iconTextLayout)

		## PRINT
		# icon = QtGui.QIcon()
		# icon.addPixmap(QtGui.QPixmap(":/Print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		# self.aPrint = QtGui.QAction(icon, u"Imprimir", self)
		# self.aPrint.setIconText(u"&Imprimir")
		# self.connect(self.aPrint, QtCore.SIGNAL("triggered()"), self.imprime)


		self.ui.toImprimir.setFont(font)
		self.ui.toImprimir.setDefaultAction(self.aPrint)
		self.ui.toImprimir.setIconSize(QtCore.QSize(44, 40))
		self.ui.toImprimir.setToolButtonStyle(iconTextLayout)
		self.ui.toImprimir.setToolTip(u"Se imprime sólo los renglones mostrados en la lista")

		## SYNCHRONIZE

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/Download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.aSynchronize = QtGui.QAction(icon, u"&Sincronizar", self)
		self.aSynchronize.setCheckable(True)
		self.aSynchronize.setIconText(u"&Sincronizar")
		self.connect(self.aSynchronize, QtCore.SIGNAL("triggered()"), self.mst.synchronize)

		self.ui.synchronizeTO.setFont(font)
		self.ui.synchronizeTO.setDefaultAction(self.aSynchronize)
		self.ui.synchronizeTO.setIconSize(QtCore.QSize(44, 40))


		## MENU

		font = QtGui.QFont()
		font.setPointSize(12 * self.mst.layoutZoom)
		font.setBold(True)

		self.listMN = QtGui.QMenu(self)
		self.listMN.setFont(font)

		self.listMN.addAction(self.aAdd)
		self.listMN.addAction(self.aEdit)
		self.listMN.addAction(self.aRemove)

		self.connect(self, QtCore.SIGNAL('showed()'), self.showed)

		self.connect(self.mst.eventRouter, QtCore.SIGNAL('purchasesChanged()'), self.listChanged)
		self.connect(self.mst.eventRouter, QtCore.SIGNAL('productsChanged()'), self.updateButtons)
		self.connect(self.mst, QtCore.SIGNAL('suppliers_pulled()'), self.suppliers_update)

		# self.upToDate = False

		self.setFocusPolicy(QtCore.Qt.StrongFocus)

		# print("""    purchases.view.Manager.__init__() - END""")


	def ui_load(self):
		# print("""    purchases.view.Manager.ui_load()""")

		self.ui = manager_ui.Ui_Form()
		self.ui.setupUi(self)

		# print("""    purchases.view.Manager.ui_load() - END""")


	def init(self):
		# print("""purchases.view.manager.init()""")



		self.data_update()
		# print("""purchases.view.manager.init() - END""")


	# def pay(self):
		# if self.ui.listTA.currentRow() == -1:
			# result = QtGui.QMessageBox.information(self, u"Empresa Básica - Pagar compra", u"Selecciona la COMPRA que quieres PAGAR", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
		# else:
			# item = self.ui.listTA.item(self.ui.listTA.currentRow(), 0)
			# id = item.data(self.ui.listTA.DOCUMENT_ID)
			# self.mst.captureView.pay(id)


	def currentId(self):
		if self.ui.listTA.currentRow() != -1:
			item = self.ui.listTA.item(self.ui.listTA.currentRow(), 0)
			id = item.data(self.ui.listTA.DOCUMENT_ID)
		else:
			id = None
		return id


	def currentProveedorChanged(self, index):
		# print("""    purchases.view.Manager.currentProveedorChanged()""")
		# self.upToDate = False
		self.data_update()
		# print("""    purchases.view.Manager.currentProveedorChanged() - END""")


	def data_update(self, *args):
		# print("\n    purchases view     Manager.data_update()")

		if not self.isVisible():
			self.app.log2sys ( 'info', "			Manager.data_update()    skipped				@ purchases.view" )
		else:
			self.app.log2sys ( 'info', "			Manager.data_update()    passed					@ purchases.view" )

			self.mst.appCursor_set(QtCore.Qt.WaitCursor)

			filtros = {}

			if self.ui.cbProveedor.currentIndex() > 0:
				filtros['rol_id'] = self.ui.cbProveedor.currentData()

			old = self.currentId()

			all = 0
			status = []
			if self.ui.ch1.isChecked():
				status.append('open')
				all += 1
			if self.ui.ch2.isChecked():
				status.append('closed')
				all += 1
			if self.ui.ch3.isChecked():
				status.append('cancelled')
				all += 1

			if not all == 3:
				filtros['status'] = status

			codes = []
			if self.ui.tipoMercanciaCH.isChecked():
				codes.append(12113)

			if self.ui.tipoGastosCH.isChecked():
				codes.append(12115)

			if codes:
				filtros['kind'] = {'code':codes}
			else:
				filtros['kind'] = {'code':12113}


			purchases = self.cnt.get_processes_using(**filtros)

			self.ui.listTA.setSortingEnabled(False)

			self.ui.listTA.setRowCount(0)

			color = QtGui.QColor(1,1,1)
			saldo = Decimal('0.00')

			kindCheque = self.cnt.attribute(category='documentKind', name=u'cheque')
			kindEfectivo = self.cnt.attribute(category='documentKind', name=u'efectivo')

			purchases.reverse()

			processed = []

			for indexProceso, proceso in enumerate(purchases):

				if indexProceso%2:
					color.setNamedColor('#E0E0FF')
				else:
					color.setNamedColor('#FFFFE0')

				subProcesos = []

				documents = proceso.documents[:]

				cheques = [x for x in documents if x.kind['code'] == kindCheque['code']]

				traspasosBancarios = [x for x in documents if x.kind['code'] == self.cnt.documentKinds_pull(name='traspaso bancario')[0]['code']]

				efectivo = [x for x in documents if x.kind['code'] == self.cnt.documentKinds_pull(name='efectivo')[0]['code']]

				firm = [x for x in documents if x.kind['code'] in [12515, 12517]]

				if not firm:
					firm = documents

				firm.sort()

				## Documentos desplegables
				for document in firm:
					try:
						processed.append(document.id)

						subProcess = [document.id, document.kind, document.number, document.date, "%s %s" % (document.rol['person']['name'], document.rol['person']['name2']), document.total, document.status.capitalize(), proceso.id, "", document]

						if cheques:

							subProcess[8] = ""
							for cheque in cheques:
								try:
									if cheque.id in document.relations:

										if cheque.status.capitalize() != u'Cancelled':
											subProcess[8] += "{}  {}  {}  {}   ".format(cheque.reference, cheque.number, cheque.total, cheque.date.strftime("%d %b %Y"))

											if cheque.id not in processed:
												processed.append(cheque.id)

												saldo += abs(cheque.total)
								except:
									print ("    purchases view     Manager.data_update()")
									print ('    cheque:', cheque)

						if traspasosBancarios:
							subProcess[8] = ""
							for traspaso in traspasosBancarios:
								if traspaso.id in document.relations:

									if traspaso.status.capitalize() != u'Cancelled':
										subProcess[8] += "{}  {}  {}  {}  ||  ".format(traspaso.reference, traspaso.number, traspaso.total.quantize(Decimal('0.01')), traspaso.date.strftime("%d %b %Y")).strip(' ').strip('||')

										if traspaso.id not in processed:
											processed.append(traspaso.id)

											saldo += abs(traspaso.total)

						if efectivo:
							efectivo = efectivo[0]
							subProcess[8] = "efectivo"
							saldo += abs(efectivo.total)

						subProcesos = [subProcess]

						for indexSubproceso, subProceso in enumerate(subProcesos):

							self.ui.listTA.insertRow(0)

							if subProceso[1]['code'] in [12515, 12517]:     # receipt, invoice
								if subProceso[6] != u'Cancelled':
									saldo -= abs(subProceso[5])

							elif not subProceso[1]['code'] in [12513]:              # order
								saldo += abs(subProceso[5])

							## COLUMN 0

							item = cdTableWidgetItem.CDTableWidgetItem(u"{} {}".format(self.cnt.translate(subProceso[1]['name']).capitalize(), subProceso[2]))
							item.setFlags(item.flags().__xor__(QtCore.Qt.ItemIsEditable))
							""" Process documents do not contain items to reduce memory usage and init time """
							## Se incluye ya la instancia de Document
							## Se deben eliminar los datos superfluos
							item.setData(self.ui.listTA.DOCUMENT, subProceso[9])
							item.setData(self.ui.listTA.DOCUMENT_ID, subProceso[0]) # Documento.id
							item.setData(self.ui.listTA.PROCESS_ID, subProceso[7])  # Proceso.id
							item.setData(self.ui.listTA.PROCESS, proceso)
							item.setData(self.ui.listTA.DOCUMENT_KIND_NAME, subProceso[1]['name'])
							item.process = proceso
							self.ui.listTA.setItem(0, 0, item)


							item = QtGui.QTableWidgetItem(subProceso[3].strftime("%d %b %Y"))
							item.setFlags(item.flags().__xor__(QtCore.Qt.ItemIsEditable))
							item.setTextAlignment(QtCore.Qt.AlignCenter)
							self.ui.listTA.setItem(0, 1, item)

							item = QtGui.QTableWidgetItem(subProceso[4])
							item.setFlags(item.flags().__xor__(QtCore.Qt.ItemIsEditable))
							self.ui.listTA.setItem(0, 2, item)

							item = QtGui.QTableWidgetItem("%.2f" % subProceso[5])
							item.setFlags(item.flags().__xor__(QtCore.Qt.ItemIsEditable))
							item.setTextAlignment(QtCore.Qt.AlignCenter)
							self.ui.listTA.setItem(0, 3, item)

							item = QtGui.QTableWidgetItem("%.2f" % saldo)
							item.setFlags(item.flags().__xor__(QtCore.Qt.ItemIsEditable))
							item.setTextAlignment(QtCore.Qt.AlignCenter)
							self.ui.listTA.setItem(0, 4, item)

							item = QtGui.QTableWidgetItem(subProceso[6])
							item.setFlags(item.flags().__xor__(QtCore.Qt.ItemIsEditable))
							item.setTextAlignment(QtCore.Qt.AlignCenter)
							self.ui.listTA.setItem(0, 5, item)

							item = QtGui.QTableWidgetItem(subProceso[8])
							item.setFlags(item.flags().__xor__(QtCore.Qt.ItemIsEditable))
							self.ui.listTA.setItem(0, 6, item)
					except:

						raise

			# self.ui.listTA.setSortingEnabled(True)

			# self.ui.listTA.resizeColumnToContents(0)
			# self.ui.listTA.resizeColumnToContents(2)

			self.setCurrentId(old)

			self.updateButtons()

			#! Sustituir setRowCount por insertRow

			# self.upToDate = True

			self.mst.appCursor_set(QtCore.Qt.ArrowCursor)

		# print("        purchases view Manager.data_update() - END")


	def elimina(self):
		if self.ui.listTA.currentRow() < 0:
			result = QtGui.QMessageBox.information(self, u"Empresa Básica - Eliminar compra", u"Selecciona la COMPRA que quieres ELIMINAR", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
		else:
			item = self.ui.listTA.item(self.ui.listTA.currentRow(), 0)
			id = item.data(self.ui.listTA.DOCUMENT_ID).toInt()[0]
			dato = manejador.documento(documento_id=id)
			result = QtGui.QMessageBox.warning(self, u"Empresa Básica - Eliminar compra", u"¿Realmente quieres ELIMINAR la COMPRA %s %s?" % (dato.folio, dato.fecha), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			if result == QtGui.QMessageBox.Yes:
				manejador.elimina(documento_id=id)
				self.mst.eventRouter.emit(QtCore.SIGNAL('comprasChanged()'))
			self.updateButtons()


	def findData(self, data):
		index = -1
		for row in range(self.ui.listTA.rowCount()):
			item = self.ui.listTA.item(row, 0)
			if item.data(self.ui.listTA.DOCUMENT_ID) == data:
				index = row
		return index


	def imprime(self):
		dialogoImpresora = QtGui.QPrintDialog(self.impresor)
		if dialogoImpresora.exec_() == QtGui.QDialog.Accepted:
			painter = QtGui.QPainter(self.impresor)
			margenHorizontal, margenVertical = [10, 10]

			font1 = QtGui.QFont("courier", 10)
			font1.setBold(True)
			font2 = QtGui.QFont("courier", 9)
			font3 = QtGui.QFont("Courier", 12)
			font3.setBold(True)

			margenX, margenY = [25, 75]
			pageWidth, pageHeight = (self.impresor.paperRect().width(), self.impresor.paperRect().height())
			pageNo = 1

			## HEADER
			header = []
			x, y = [25, 0]
			header.append([pageWidth/2-100, margenY+y, u"Catálogo de Empleados", font3])
			x, y = [400, 25]
			header.append([pageWidth-200, margenY+y, u"Fecha: %s" % QtCore.QDate().currentDate().toString('dd MMM yyyy'), font1])

			# x, y = [0, 100]
			# header.append([margenX+x, margenY+y, u"    Nombre                                     RFC            Teléfonos", font1])

			tabla = self.ui.listTA

			x, y = [0, 75]
			contenido = []
			footer = []
			offset = 0
			for row in range(tabla.rowCount()):
				if offset == 0:
					contenido.extend(header)
				posX, posY = (margenX + x, margenY + y + offset)
				contenido.append([posX    , posY, str(row+1), font2])
				contenido.append([posX+40 , posY, tabla.item(row, 0).text(), font2])    # Nombre
				contenido.append([posX+90 , posY+18, tabla.item(row, 4).text(), font2]) # Domicilio
				contenido.append([posX+90 , posY+36, tabla.item(row, 3).text(), font2]) # Lugar
				contenido.append([posX+90 , posY+54, u"RFC: %s   Teléfonos: %s" % (tabla.item(row, 1).text(), tabla.item(row, 2).text()), font2]) # RFC, Teléfono
				# if tabla.item(row, 5):
					# contenido.append([posX+690, posY, tabla.item(row, 5).text(), font2])# Importe
				offset += 80
				if posY+190 >= pageHeight:
					contenido.append([pageWidth/2-50, pageHeight-50, "Hoja %s" % pageNo, font2])
					for item in contenido:
						painter.setFont(item[3])
						painter.drawText(QtCore.QPoint(margenHorizontal + item[0], margenVertical + item[1]), item[2])
					offset = 0
					contenido = []
					footer = []
					pageNo += 1
					self.impresor.newPage()

			contenido.append([pageWidth/2-50, pageHeight-50, "Hoja %s" % pageNo, font2])
			for item in contenido:
				painter.setFont(item[3])
				painter.drawText(QtCore.QPoint(margenHorizontal + item[0], margenVertical + item[1]), item[2])


	def listChanged(self):
		# print("""purchases.view.Manager.listChanged()""")
		# self.upToDate = False
		self.data_update()
		# print("""purchases.view.Manager.listChanged() - END""")


	def showListMenu(self, pos):
		pos = self.ui.listTA.mapToGlobal(pos)
		self.listMN.popup(pos)


	def listResized(self, event):
		headerWidth = self.ui.listTA.width()-self.ui.listTA.verticalHeader().width()-self.ui.listTA.verticalScrollBar().width()-1
		self.ui.listTA.horizontalHeader().setMinimumWidth(headerWidth)

		porcentajes = [0, 10, 10, 15, 12, 12]
		overflow = 0

		# for index in range(self.ui.listTA.horizontalHeader().count()-1):
			# if not self.ui.listTA.isColumnHidden(index):
				# self.ui.listTA.resizeColumnToContents(index)

				# porContenido = self.ui.listTA.columnWidth(index)
				# calculado = headerWidth * porcentajes[index] / 100

				# if porContenido < calculado:
					# if overflow:
						# offset = calculado - porContenido
						# if offset > overflow:
							# calculado = calculado - overflow
							# overflow = 0
						# else:
							# overflow -= offset
							# calculado = porContenido
					# self.ui.listTA.setColumnWidth(index, calculado)
				# else:
					# overflow += porContenido - calculado


	def selectionChanged(self):
		if self.ui.listTA.currentRow() != -1:
			item = self.ui.listTA.item(self.ui.listTA.currentRow(), 0)
			process = item.process
			id = item.data(self.ui.listTA.DOCUMENT_ID)

			self.mst.current_set(process, id)

			# if self.mst.details.isVisible():
				# self.mst.details.doShow(process, id)
			# if self.mst.capture.isVisible():
				# if self.mst.capture.task == self.EDIT:
					# if self.mst.capture.id != id:
						# if self.mst.capture.isModified():
							# result = QtGui.QMessageBox.warning(self, u"Empresa Básica - Modificación de Compra", u"La captura de Compra tiene cambios\n\n¿Quieres Guardar los cambios para %s %s %s?" % (self.mst.capture.initial.tipo, self.mst.capture.initial.folio, self.mst.capture.initial.fecha), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

							# if result == QtGui.QMessageBox.Yes:
								# self.mst.capture.save()
						# self.mst.process_edit(id)

		self.updateButtons()


	def setCurrentId(self, id):
		self.ui.listTA.setCurrentItem(self.ui.listTA.item(self.findData(id), 0))


	def showed(self):
		# print("""    purchases.view.Manager.showed()""")
		self.data_update()
		self.cnt.information_set(u"")
		# print("""    purchases.view.Manager.showed() - END""")


	def suppliers_update(self):

		old = self.ui.cbProveedor.currentData()
		self.ui.cbProveedor.clear()

		if self.mst.suppliers:
			self.ui.cbProveedor.addItem(u"", self.app.holder['id'])
			for supplierIndex, supplier in enumerate(self.mst.suppliers):
				self.ui.cbProveedor.addItem("%s %s" % (supplier['person']['name'], supplier['person']['name2']), supplier['id'])
			if self.ui.frProveedor.isEnabled():
				self.ui.frProveedor.setToolTip(u"Seleccione uno para filtrar la lista")
		else:
			self.ui.cbProveedor.addItem("No hay proveedores", -1)
			self.ui.frProveedor.setToolTip(u"No hay proveedores capturados")

		self.ui.cbProveedor.setCurrentData(old)


	def theme_update(self):
		buttonsStyle = "border:2px outset #908878; border-top:0px; border-top-left-radius:0px; border-top-right-radius:0px; border-bottom-left-radius:12px; border-bottom-right-radius:12px; background-color:qradialgradient(cx:.5, cy:.75, radius:1.5,fx:.5, fy:.75, stop:0 {}, stop:1 {});".format(self.mst.theme['background']['color'], self.mst.theme['background']['color2'])
		self.ui.toAgregar.setStyleSheet(buttonsStyle)
		self.ui.toModificar.setStyleSheet(buttonsStyle)
		self.ui.toEliminar.setStyleSheet(buttonsStyle)
		self.ui.paymentTO.setStyleSheet(buttonsStyle)
		self.ui.toImprimir.setStyleSheet(buttonsStyle)
		self.ui.synchronizeTO.setStyleSheet(buttonsStyle)

		self.listMN.setStyleSheet("QMenu{{border:2px outset #F0C038; border-top-left-radius:4px; background-color:QRadialGradient(cx:.5, cy:.5, radius:1, fx:.5, fy:.5, stop:0 {}, stop:1 {});}} QMenu::item{{color:#202020;}} QMenu::item:selected{{color:#000000; background-color:#F0C038;}} QMenu::item:disabled{{color:#808080; background-color:rgba(0,0,0,80);}}".format(self.mst.theme['background']['color2'], self.mst.theme['background']['color']))




	def updateButtons(self):
		# print("""        purchases.view.Manager.updateButtons()""")

		view.Manager.updateButtons(self)

		# if not self.mst.capture.isVisible():
			# self.aAdd.setChecked(False)
			# self.aEdit.setChecked(False)

		self.aRemove.setChecked(False)
		self.aPay.setChecked(False)
		self.aPrint.setChecked(False)

		mensajesFiltros = u""
		mensajesAlta = u""
		mensajesModifica = u""
		mensajesElimina = u""
		mensajesPaga = u""
		mensajesImprime = u""

		if self.cnt.productsCount() == 0:
			mensajesAlta += u"No hay productos registrados\n"

		# if self.cnt.suppliersCount() == 0:
		if not self.ui.cbProveedor.count():
			mensajesAlta += u"No hay proveedores registrados\n"
			mensajesFiltros += u"No hay proveedores registrados\n"

		if self.cnt.purchasesCount == 0:
			mensajesFiltros += u"No hay compras registradas\n"
			mensajesModifica += u"No hay compras registradas\n"
			mensajesElimina += u"No hay compras registradas\n"
			mensajesPaga += u"No hay compras registradas\n"
			mensajesImprime += u"No hay compras para imprimir\n"

		elif self.ui.listTA.rowCount() == 0:
			mensajesModifica += u"No hay compras desplegadas\n"
			mensajesElimina += u"No hay compras desplegadas\n"
			mensajesPaga += u"No hay compras desplegadas\n"
			mensajesImprime += u"No hay compras desplegadas\n"

		elif self.ui.listTA.rowCount() > 0:
			if self.ui.listTA.currentRow() == -1:
				mensajesModifica += u"Selecciona la Compra que quieres Modificar"
				mensajesElimina += u"Selecciona la Compra que quieres Eliminar"
				mensajesPaga += u"Selecciona la Compra que quieres Pagar"
			else:
				if self.ui.listTA.item(self.ui.listTA.currentRow(), 4).text() == u'cerrado':
					mensajesPaga += u"Esta compra ya está pagada"
				elif self.ui.listTA.item(self.ui.listTA.currentRow(), 0).data(self.ui.listTA.DOCUMENT_KIND_NAME).lower() == 'order':
					mensajesModifica += u"No se ha capturado documento de Compra, sólo Pedido"

		if mensajesFiltros:
			self.ui.frFiltros.setToolTip(mensajesFiltros.rstrip("\n"))
			self.ui.frFiltros.setEnabled(False)
			self.ui.frProveedor.setToolTip(u"")
		else:
			self.ui.frFiltros.setEnabled(True)
			self.ui.frFiltros.setToolTip(u"")

		if mensajesAlta:
			self.aAdd.setEnabled(False)
			self.aAdd.setToolTip(mensajesAlta.rstrip("\n"))
		else:
			self.aAdd.setEnabled(True)
			self.aAdd.setToolTip(u"Presiona para registrar una Compra nueva")

		# self.aEdit.setEnabled(False)
		# self.aEdit.setToolTip(u"La modificación de compras no está implementada")

		if mensajesModifica:
			self.aEdit.setEnabled(False)
			self.aEdit.setToolTip(mensajesModifica.rstrip("\n"))
		else:
			self.aEdit.setEnabled(True)
			self.aEdit.setToolTip(u"Presiona para modificar los datos de la Compra seleccionada")

		self.aRemove.setEnabled(False)
		self.aRemove.setToolTip(u"El borrado de compras no está autorizado")

		if mensajesPaga:
			self.aPay.setEnabled(False)
			self.aPay.setToolTip(mensajesPaga.rstrip("\n"))
		else:
			self.aPay.setEnabled(True)
			self.aPay.setToolTip(u"Presiona para pagar la Compra seleccionada")

		if mensajesImprime:
			self.aPrint.setEnabled(False)
			self.aPrint.setToolTip(mensajesImprime.rstrip("\n"))
		else:
			self.aPrint.setEnabled(True)
			self.aPrint.setToolTip(u"Presiona para Imprimir las compras mostradas")

		# print("""        purchases.view.Manager.updateButtons() - END""")




class CaptureView(view.CaptureView):

	_fase = "formalize"

	def __init__(self, *args, **kwds):

		view.CaptureView.__init__(self, *args, **kwds)

		frameStyle = "color:#404000; background-color:#E4D460;"

		labelStyle = "color:#FFFFFF; border-top-left-radius:6; border-top-right-radius:6; border-bottom-left-radius:0; border-bottom-right-radius:0;"

		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		self.setSizePolicy(sizePolicy)
		self.setBaseSize(QtCore.QSize(50, 0))

		self.app.log2sys ( 'info', "    purchases view  CaptureView.__init__()" )

		self.supplier_pending_set(False)


		## Import from file (cfd)
		self.ui.importTO = QtGui.QToolButton(self.ui.headerFR)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/Download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.ui.importTO.setIcon(icon)
		self.ui.importTO.setIconSize(QtCore.QSize(32, 32))
		self.ui.importTO.setObjectName("importTO")
		self.ui.headerFRLY.insertWidget(0, self.ui.importTO)

		self.connect(self.ui.importTO, QtCore.SIGNAL('clicked()'), self.import_)

		## Process kind
		self.ui.kindLA.setFont(self.labelFont)
		self.ui.kindSE.setFont(self.frameFont)

		self.connect(self.ui.kindSE, QtCore.SIGNAL('changed()'), self.kind_update)

		## Pedido
		self.ui.orderFR.setStyleSheet(frameStyle)
		self.ui.orderLA.setFont(self.labelFont)
		self.ui.orderLA.setStyleSheet(labelStyle)

		self.ui.orderCB.lineEdit().setFont(self.frameFont)
		self.ui.orderCB.lineEdit().setAlignment(QtCore.Qt.AlignHCenter)
		self.ui.orderCB.lineEdit().setReadOnly(True)
		self.connect(self.ui.orderCB, QtCore.SIGNAL("activated(int)"), self.order_selected)
		self.connect(self.mst.eventRouter, QtCore.SIGNAL("pedidosChanged()"), self.orders_reset)


		## Document Kind
		self.ui.documentKindFR.setStyleSheet(frameStyle)

		self.ui.documentKindLA.setFont(self.labelFont)
		self.ui.documentKindLA.setStyleSheet(labelStyle)
		self.ui.documentKindLA.bit = 2
		self.connect(self.ui.documentKindLA, QtCore.SIGNAL("clicked()"), self.documentKind_update)

		self.ui.cbTipoDocumento.lineEdit().setFont(self.frameFont)
		self.ui.cbTipoDocumento.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
		self.ui.cbTipoDocumento.lineEdit().setReadOnly(True)

		## Folio
		self.ui.numberFR.setStyleSheet(frameStyle)
		# self.ui.numberLA.setFont(labelFont)
		# self.ui.numberLA.setStyleSheet(labelStyle)

		self.ui.serieED.setStatusLabel(False)
		self.ui.serieED.setFont(self.frameFont)
		self.ui.serieED.setSymbols(' ')
		self.ui.serieED.bit = 3
		self.connect(self.ui.serieED, QtCore.SIGNAL('textEdited(QString)'), self.number_validate)

		self.ui.numberED.setFont(self.frameFont)
		self.ui.numberED.setSymbols(' ')
		self.ui.numberED.bit = 4
		self.connect(self.ui.numberED, QtCore.SIGNAL('textEdited(QString)'), self.number_validate)


		## Fecha
		self.ui.dateLYFR.setStyleSheet(frameStyle)
		self.ui.dateLYLA.setStyleSheet(labelStyle)
		self.ui.dateED.bit = 5


		## Tabla partidas (tipos de documento lo requiere)
		# self.ui.itemsTA = itemsTable.Form(self, self.ui.captureFR, cnt=self.cnt, task=self.task)
		self.ui.itemsTA.setTabKeyNavigation(False)
		self.ui.itemsTA.setStyleSheet("background-color:#FFFFFF;")
		self.ui.itemsTA.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		self.ui.itemsTA.bit = 6
		self.ui.captureLY.addWidget(self.ui.itemsTA)

		## - Partida nueva capturada > recalculo requerido, solicitud de nueva captura
		## - Partida existente modificada > posible recalculo requerido

		self.connect(self.ui.itemsTA, QtCore.SIGNAL('editingFinished()'), self.partidaCapturada)

		self.state_set(self.cnt.BUSY)

		## Supplier
		self.ui.supplierFR.setStyleSheet(frameStyle)

		self.ui.supplierLA.setFont(self.labelFont)
		self.ui.supplierLA.setStyleSheet(labelStyle)

		self.ui.addSupplierBU.bit = 7
		self.connect(self.ui.addSupplierBU, QtCore.SIGNAL('clicked()'), self.supplier_add)

		self.ui.supplierCB.setMaxVisibleItems(15)
		self.ui.supplierCB.lineEdit().setFont(self.frameFont)
		self.ui.supplierCB.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
		self.ui.supplierCB.lineEdit().setReadOnly(True)
		self.ui.supplierCB.FULLDATA = QtCore.Qt.UserRole + 2
		self.ui.supplierCB.bit = 8
		self.connect(self.ui.supplierCB, QtCore.SIGNAL("currentIndexChanged(int)"), self.supplier_update)

		self.ui.captureFR.setStyleSheet("QFrame#captureFR{background-color:QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFF8D0, stop:1 #FCF490); border-top-left-radius:3px; border-top-right-radius:3px;}")


		## PRODUCT SELECTOR
		# self.ui.productSelector = productSelector.Form(self)
		# self.ui.productSelector.ui.scrollArea.hide()
		self.ui.productSelector.setStyleColor("#FFDC48")
		# self.ui.productSelector.bit = 9

		# self.ui.captureLY.insertWidget(0, self.ui.productSelector)

		# self.connect(self.ui.productSelector, QtCore.SIGNAL('originChanged()'), self.origin_update)
		# self.connect(self.ui.productSelector, QtCore.SIGNAL('productSelected()'), self.setItem)




		# self.status_set(u'init')

		# self.loadPaymentConditions()


		## Origen de datos
		#~ self.cargaOrigenes()

		# self.connect(self.ui.cbOrigen, QtCore.SIGNAL('activated(int)'), self.origenChanged)

		"""
		## Lineas
		self.ui.cbLinea.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
		self.ui.cbLinea.lineEdit().setReadOnly(True)
		self.loadLines()
		"""

		## Server Access
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/Down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.aAccessServer = QtGui.QAction(icon, "Accesar Central", self)
		self.aAccessServer.setCheckable(True)
		self.connect(self.aAccessServer, QtCore.SIGNAL("triggered()"), self.accessServer)

		'''
		self.ui.accessServerTO.setDefaultAction(self.aAccessServer)
		self.ui.accessServerTO.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
		'''

		self.ui.footerFR.setStyleSheet("QFrame#footerFR{background-color:QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFF8D0, stop:1 #FCF490); border-top-left-radius:3px; border-top-right-radius:3px;}")

		## Subtotal

		## Discount
		self.ui.discountED.bit = 10

		## Discount Factor
		self.ui.discountFactorED.bit = 11

		## Subtotal2
		self.ui.subtotal2ED.setMaximumWidth(self.ui.itemsTA.columnWidth(5))
		self.ui.subtotal2ED.setAlignment(QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

		## Tax
		self.ui.taxED.bit = 12

		## Tax Factor
		self.ui.taxFactorED.bit = 13

		## Total
		self.ui.totalED.bit = 14
		self.connect(self.ui.totalED, QtCore.SIGNAL('textEdited(QString)'), self.totalEdited)

		self.ui.textTotalLA.setFont(self.frameFont)

		## Condiciones de pago
		self.ui.paymentConditionFR.setStyleSheet(frameStyle)

		self.ui.paymentConditionLA.setFont(self.labelFont)
		self.ui.paymentConditionLA.setStyleSheet(labelStyle)

		self.ui.cbCondiciones.lineEdit().setFont(self.frameFont)
		self.ui.cbCondiciones.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
		self.ui.cbCondiciones.lineEdit().setReadOnly(True)
		self.ui.cbCondiciones.bit = 15

		self.connect(self.ui.cbCondiciones, QtCore.SIGNAL('activated(int)'), self.update_status)

		## Ajuste
		self.ui.chAjustes.setChecked(False)
		self.connect(self.ui.chAjustes, QtCore.SIGNAL('stateChanged(int)'), self.toggleAjustes)
		self.connect(self.ui.cbTipoAjuste, QtCore.SIGNAL('activated(int)'), self.update_status)
		self.connect(self.ui.cbTipoDocumentoAjuste, QtCore.SIGNAL('activated(int)'), self.update_status)
		self.connect(self.ui.fechaAjuste, QtCore.SIGNAL('dateChanged(QDate)'), self.update_status)
		self.connect(self.ui.numberED, QtCore.SIGNAL('textEdited(QString)'), self.update_status)
		self.connect(self.ui.edMontoAjuste, QtCore.SIGNAL('textEdited(QString)'), self.update_status)

		self.ui.frTipoAjuste.hide()
		# self.adjustDocumentKinds_reset()
		self.ui.frAjustes0.hide()
		self.ui.frAjustes.hide()

		self.ui.frAjuste.hide()

		#### BUTTONS ####

		radius = int(12 * self.mst.layoutZoom)

		buttonsFont = QtGui.QFont()
		buttonsFont.setPointSize(12 * self.mst.layoutZoom)
		buttonsFont.setBold(True)

		buttonsStyle = "border:2px outset #908878; border-top-left-radius:{}px; border-top-right-radius:8px; border-bottom-left-radius:{}px; border-bottom-right-radius:8px; background-color:qradialgradient(cx:.5, cy:.5, radius:1.25,fx:.5, fy:.25, stop:0 {}, stop:1 {});".format(radius, radius, self.mst.theme['background']['color'], self.mst.theme['background']['color2'])

		buttonsIconSize = QtCore.QSize(32 * self.mst.layoutZoom, 32 * self.mst.layoutZoom)

		## Save
		self.ui.saveBU.setIconSize(buttonsIconSize)
		self.ui.saveBU.setStyleSheet(buttonsStyle)
		self.ui.saveBU.setEnabled(False)

		## Cancelar
		self.ui.cancelBU.setIconSize(buttonsIconSize)
		self.ui.cancelBU.setStyleSheet(buttonsStyle)

		# self.connect(app.eventRouter, QtCore.SIGNAL('cuentasChanged()'), self.loadAccounts)
		self.connect(self.mst.eventRouter, QtCore.SIGNAL('productAdded'), self.productAdded)

#        self.mensajes2 = u""

		self.connect(self, QtCore.SIGNAL('showed()'), self.showed)

		self.connect(self.mst, QtCore.SIGNAL("suppliers_pulled()"), self.suppliers_update)
		self.connect(self.mst.eventRouter, QtCore.SIGNAL('supplierAdded'), self.supplier_added)

		self.setTabOrder(self.ui.orderCB, self.ui.cbTipoDocumento)
		self.setTabOrder(self.ui.cbTipoDocumento, self.ui.numberED)
		self.setTabOrder(self.ui.numberED, self.ui.dateED)
		self.setTabOrder(self.ui.dateED, self.ui.supplierCB)
		self.setTabOrder(self.ui.supplierCB, self.ui.cbCondiciones)
		self.setTabOrder(self.ui.cbCondiciones, self.ui.productSelector)
		self.setTabOrder(self.ui.productSelector, self.ui.itemsTA)
		self.setTabOrder(self.ui.itemsTA, self.ui.subtotalED)
		self.setTabOrder(self.ui.subtotalED, self.ui.discountFactorED)
		self.setTabOrder(self.ui.discountFactorED, self.ui.discountED)
		self.setTabOrder(self.ui.discountED, self.ui.subtotal2ED)
		self.setTabOrder(self.ui.subtotal2ED, self.ui.taxFactorED)
		self.setTabOrder(self.ui.taxFactorED, self.ui.taxED)
		self.setTabOrder(self.ui.taxED, self.ui.tax2FactorED)
		self.setTabOrder(self.ui.tax2FactorED, self.ui.tax2ED)
		self.setTabOrder(self.ui.tax2ED, self.ui.totalED)
		self.setTabOrder(self.ui.totalED, self.ui.chAjustes)
		self.setTabOrder(self.ui.chAjustes, self.ui.saveBU)
		self.setTabOrder(self.ui.saveBU, self.ui.cancelBU)

		## POSSET

		self.__rangoPrecioActual = 1

		self.state_reset()

		self.useServer_set(0)

		self.app.log2sys ( 'info', "    purchases view  CaptureView.__init__() - END" )


	def clear(self):
		# print("    purchases view    CaptureView.clear()")

		view.CaptureView.clear(self)

		self.state_set(self.cnt.BUSY)

		if self.task is self.cnt.EDIT:
			self.ui.orderCB.hide()
			self.ui.orderED.show()
		else:
			self.ui.orderCB.show()
			self.ui.orderED.hide()
			self.ui.orderCB.setCurrentIndex(-1, initialToo=True)

		# self.taxMode = self.txSTRIPPED

		self.tipo = None

		self.ui.itemsTA.clear()

		self.ui.documentKindLA.current_setByData(self.cnt.defaultDocumentKind(reference='formalize')['code'], initialToo=True)

		self.ui.numberED.clear()
		self.ui.numberED.setExternalValidation(True, u"")

		self.ui.supplierCB.setCurrentIndex(-1, initialToo=True)
		self.ui.cbCondiciones.setCurrentIndex(-1, initialToo=True)

		# self.ui.cbOrigen.setCurrentIndex(0)

		self.ui.productSelector.clear()

		# self.ui.cbLinea.setCurrentIndex(-1)

		self.ui.subtotalED.clear()
		self.ui.discountFactorED.clear()
		self.ui.discountED.clear()
		self.ui.subtotal2ED.clear()

		self.ui.taxLA.setText(self.app.generalTax['name'])
		self.ui.taxFactorED.setValue(self.app.generalTax['value'])
		self.ui.taxED.setValue(Decimal('0'), initialToo=True)

		# self.ui.tax2FactorED.clear()
		self.ui.tax2FactorED.setValue(Decimal('0'), initialToo=True)
		# self.ui.tax2ED.clear()
		self.ui.tax2ED.setValue(Decimal('0'), initialToo=True)

		self.taxes_hide()
		self.taxes_show()

		self.ui.totalED.clear()

		self.ui.textTotalLA.clear()

		## Payment
		# self.ui.paymentFR.clear()

		self.ui.cbTipoAjuste.setCurrentIndex(-1)
		self.ui.cbTipoDocumentoAjuste.setCurrentIndex(-1)
		self.ui.edFolioAjuste.clear()
		self.ui.fechaAjuste.setDate(QtCore.QDate().currentDate())
		self.ui.edMontoAjuste.clear()

		self.initialDocument = None

		self.state_reset()

		# print("    purchases view    CaptureView.clear() - END")


	def modified_data(self):
		""" Regresa una estructura de datos (dict) que representa los documentos
		que contienen los widgets de la vista """

		self.app.log2sys ( 'info', "    purchases view      CaptureView.modified_data()" )

		view.CaptureView.modified_data(self)

		"""No se modifica el proceso, sólo los documentos"""

		messages = u""

		# process = self.cnt.process_new()

		documents = []

		document = {}

		#! No ha quedado el tax2

		total = self.ui.totalED.value()

		if self.taxMode == self.txMERGED:

			taxFactor = 1 + self.ui.taxFactorED.value() / 100

			subtotal = self.ui.subtotalED.value() / taxFactor

			discount = self.ui.discountFactorED.value() / taxFactor

			tax = total * ( 1 - 1 / taxFactor )

			if self.ui.tax2FactorED.isVisible():

				tax2Factor = 1 + self.ui.tax2FactorED.value() / 100

				tax2 = subtotal * ( 1 - 1 / tax2Factor )

		elif self.taxMode == self.txSTRIPPED:

			subtotal = self.ui.subtotalED.value()
			discount = self.ui.discountFactorED.value()
			tax = self.ui.taxED.value()
			tax2 = self.ui.tax2ED.value()

		# if self.ui.kindSE.isModified() or self.task is self.cnt.ADD:
			# process.kind_set(self.ui.kindSE.currentData())

		if self.ui.orderCB.isModified() and "No hay" not in self.ui.orderCB.currentText():
			orderId = self.ui.orderCB.currentData()
			document['relation'] = orderId

		if self.ui.documentKindLA.isModified() or self.task is self.cnt.ADD:
			document['kind'] = {'code':self.ui.documentKindLA.currentData()}
			if not self.task is self.cnt.ADD:
				messages += u"Se cambió el tipo de documento\n"

		if self.ui.numberED.isModified() or self.task is self.cnt.ADD:
			document['number'] = unicode(self.ui.numberED.text())
			if self.ui.numberED.isModified():
				messages += u"Se cambió el folio\n"

		if self.ui.dateED.isModified() or self.task is self.cnt.ADD:
			document['date'] = self.ui.dateED.dateTime().toPyDateTime()

			messages += u"Se cambió la fecha\n"

		if self.ui.supplierCB.isModified() or self.task is self.cnt.ADD:
			document['rol_id'] = self.ui.supplierCB.currentData()
			messages += u"Se cambió el proveedor\n"

		if self.ui.cbCondiciones.isModified() or self.task is self.cnt.ADD:
			if self.ui.cbCondiciones.currentData():
				document['reference'] = "%s" % self.ui.cbCondiciones.currentData()
				messages += u"Se cambiaron las condiciones\n"

		if self.ui.subtotalED.isModified() or self.task is self.cnt.ADD:
			# document['subtotal'] = self.ui.subtotalED.value()
			document['subtotal'] = subtotal
			messages += u"Se cambió el subtotal\n"

		if self.ui.discountED.isModified() or self.task is self.cnt.ADD:
			# document['discount'] = self.ui.discountED.value()
			document['discount'] = discount
			messages += u"Se cambió el descuento\n"

		if self.ui.discountFactorED.isModified() or self.task is self.cnt.ADD:
			document['discountpercent'] = self.ui.discountFactorED.value()
			messages += u"Se cambió el descuento\n"

		if self.ui.taxED.isModified() or self.task is self.cnt.ADD:
			# document['tax'] = self.ui.taxED.value()
			document['tax'] = tax
			messages += u"Se cambió el impuesto\n"

		if self.ui.taxFactorED.isModified() or self.task is self.cnt.ADD:
			document['taxpercent'] = self.ui.taxFactorED.value()
			messages += u"Se cambió el impuesto\n"

		if (self.ui.tax2ED.isVisible() and self.ui.tax2ED.isModified()) or self.task is self.cnt.ADD:
			document['tax2'] = self.ui.tax2ED.value()
			messages += u"Se cambió el impuesto 2\n"

		if (self.ui.tax2FactorED.isVisible() and self.ui.tax2FactorED.isModified()) or self.task is self.cnt.ADD:
			document['tax2percent'] = self.ui.tax2FactorED.value()
			messages += u"Se cambió el impuesto 2\n"

		if self.task is self.cnt.ADD and not document['tax2'] and not document['tax2percent']:
			document.pop('tax2')
			document.pop('tax2percent')

		if self.ui.totalED.isModified() or self.task is self.cnt.ADD:
			document['total'] = total
			messages += u"Se cambió el total\n"

		## ~~~ PARTIDAS ~~~~~~
		# items = self.ui.itemsTA.modifiedData()
		# if items:
			# document['items'] = items
			# messages += self.ui.itemsTA.modificationMessages

		if self.task is self.cnt.ADD or self.ui.itemsTA.isModified():
			items = []
			for item in self.document.items:

				#! Cleaning item data for pushing (should remove when item pushing
				#! is made by the instance itself)

				data_ = item.data

				data_.pop('aception_code', None)
				data_.pop('aception_name', None)

				items.append(data_)

			document['items'] = items

		## ~~~ Status del documento ~~~~~~

		payments_total = self.ui.paymentsBox.total()

		if payments_total == total:
			status_expected = 'closed'
		else:
			status_expected = 'open'

		if self.document.status != status_expected:
			document['status'] = status_expected

		if document:

			if self.document.id:

				document['id'] = self.document.id

			# if self.task is self.cnt.EDIT:
				# doc = [x for x in self.initial['documents'] if x['kind_code'] in [self.cnt.documentKind_factura['code'], self.cnt.documentKind_remision['code']]][0]
				# document['id'] = doc['id']


			if self.attributes:

				document['attributes'] = self.attributes

			documents.append(document)
			# process.document_add(**document)

		## ~~~ Obtención de datos de pago modificados ~~~~~~
		## !! Los PAGOS se disfrazan de registro de documento
		## Los PAGOS son registro de documento

		try:
			payments_modified = self.ui.paymentsBox.modified_data()

			if payments_modified:

				# documents.extend(payments_modified)

				for payment in payments_modified:

					documents.append(payment)
					# process.document_add(payment)

			# paymentsIsModified = self.ui.paymentsBox.isModified()

			"""
			payments = []
			for index in range(self.ui.paymentsBox.ui.itemsLY.count()):

				payment = self.ui.paymentsBox.ui.itemsLY.itemAt(index).widget()

				paymentData = self.ui.paymentFR.modified_data(index)
				if paymentData:
					## ~~~ Existen datos de pago modificados ~~~
					#! Deberían obtienerse datos validados de paymentFR
					## Checar validez
					if 'total' not in paymentData or paymentData['total'] != Decimal('0.00'):
						if 'id' not in paymentData.keys():
							paymentData['rol_id'] = self.ui.supplierCB.currentData()
							paymentData['status'] = u'closed'

						if 'id' not in paymentData.keys() or len(paymentData.keys())==1:
							paymentData['relation'] = self.initialDocumentId

						payments.append(paymentData)

						messages += u"%s\n" % self.ui.paymentFR.modificationMessages(index)

			# if self.ui.paymentFR.ui.itemsLY.count() != self.ui.paymentFR.initialCount:
				# pass
				#! Check payment count modified
			"""
		except:
			print ("""\n    purchases view    CaptureView.modified_data() - payments\n
				payments_modified:{}""".format(payments_modified))
			raise

		# if documents:
			# process['documents'] = documents

		# if process:

			# if self.initial:
				# if type(self.initial) == dict:
					# process.id_set(self.initial['id'])
				# else:
					# process.id_set(self.initial.id)

		self.modificationMessages = messages.rstrip("\n")

		self.app.log2sys ( 'info', "    purchases view      CaptureView.modified_data() - END" )

		return documents


	def set_data(self, document):
		"""Fills data widgets with document's attributes"""
		self.app.log2sys ( 'info', "    purchases view  CaptureView.set_data()" )

		try:
			document.data
		except:
			print ("    purchases view CaptureView.set_data() - ", self.document.data)
			print ("    purchases view CaptureView.set_data() - ", document)
			raise Fault("    purchases view CaptureView.set_data()", "purchase document attribute must not be empty")

		eMessage = ""

		try:
			view.CaptureView.set_data(self, document)
		except:
			eMessage += "Could not set data to ancestor\n"

		## Document Kind
		try:
			self.documentKind_set(document.kind['code'], initialToo=True)
		except Exception as e:
			self.app.log2sys ( 'error', "    purchases view  CaptureView.set_data()\n        document.kind:{}".format(document.kind) )
			eMessage += "Could not set data to document kind\n"

		self.state_set(self.cnt.BUSY)

		## Pedido
		kindPedido = self.cnt.attribute(category='documentKind', name=u'order', cast_=u'purchase')

		print(kindPedido)
		print(document.process.documents)

		print(document.process.documents[0].data)

		print(document.process.documents[0].kind)


		orderZero = [x for x in document.process.documents if x.kind['code'] == kindPedido['code']]
		if orderZero:
			order = orderZero[0]
			self.ui.orderCB.setCurrentText(order.number)

		## GoodKind
		try:
			self.ui.kindSE.setCurrentData(document.process.kind['code'], initialToo=True)
			self.kind_update()
		except Exception as e:
			eMessage += "Could not set good kind\n"

		## Document Series
		try:
			self.ui.serieED.setText("%s" % document.serie, initialToo=True)
		except Exception as e:
			eMessage += "Could not set document series\n"

		## Document Number
		try:
			self.ui.numberED.setText("%s" % document.number, initialToo=True)
		except:
			## A facturas que no traen folio se les asigna uno
			## No cuenta como error
			self.ui.numberED.setText("{}".format(document.date.strftime("%Y%m%d")))
			self.document.number_set(self.ui.numberED.text())

		try:
			self.ui.dateED.setDate(QtCore.QDate().fromString(document.date.strftime("%d%m%Y"), "ddMMyyyy"), initialToo=True)
		except Exception as e:
			eMessage += "Could not set document date\n"

		## Supplier
		try:
			if document.state_is_stROL_CURRENT:

				if self.ui.supplierCB.findData(document.rol['id']) < 0:

					self.ui.supplierCB.addItem("%s %s" % (document.rol['person']['name'], document.rol['person']['name2']), document.rol['id'])
					self.ui.supplierCB.setItemData(self.ui.supplierCB.count()-1, document.rol['person']['rfc'], QtCore.Qt.UserRole+1)
					self.ui.supplierCB.setItemData(self.ui.supplierCB.count()-1, document.rol, self.ui.supplierCB.FULLDATA)

				self.ui.supplierCB.setCurrentData(document.rol['id'], initialToo=True)

				self.ui.productSelector.dealer_set(document.rol)
				self.ui.itemsTA.origin_set(document.rol['id'])
		except Exception as e:
			eMessage += "    Could not set document rol\n        {}".format(e)
			print(document.state_is_stROL_CURRENT)


		## ~~~~  ITEMS  ~~~~
		try:
			self.ui.itemsTA.set_data(document.items)
		except:
			self.app.log2sys ( 'error', "    Could not set document items\n        document.items: {}".format(document.items) )

		try:
			self.ui.subtotalED.setValue(document.subtotal, initialToo=True)
		except:
			eMessage += "    Could not set document subtotal\n"

		try:
			if document.discounts:
				discount = document.discounts[0]
				self.ui.discountED.setValue(discount['amount'], initialToo=True)
				self.ui.discountFactorED.setValue(discount['factor'], initialToo=True)
				#! Why is this?
				self.ui.itemsTA.generalDiscount = discount['factor']

				self.ui.subtotal2ED.setValue(document.subtotal - discount['amount'], initialToo=True)
			else:
				self.ui.discountFactorED.setValue(Decimal('0'), initialToo=True)
				self.ui.subtotal2ED.setValue(document.subtotal, initialToo=True)
		except:
			eMessage += "    Could not set document discounts\n"

		try:
			if 'general' in document.taxes:
				self.ui.taxLA.setText(document.taxes['general']['name'])
				self.ui.taxED.setValue(document.taxes['general']['amount'], initialToo=True)
				self.ui.taxFactorED.setValue(document.taxes['general']['factor'], initialToo=True)

			if 'special' in document.taxes:
				self.ui.tax2LA.setText(document.taxes['special']['name'])
				self.ui.tax2ED.setValue(document.taxes['special']['amount'], initialToo=True)
				self.ui.tax2FactorED.setValue(document.taxes['special']['factor'], initialToo=True)
				self.ui.tax2LA.show()
				self.ui.tax2ED.show()
				self.ui.tax2FactorED.show()
			else:
				self.ui.tax2LA.hide()
				self.ui.tax2ED.hide()
				self.ui.tax2FactorED.hide()
		except:
			eMessage += "    Could not set document taxes\n"

		try:
			self.ui.totalED.setValue(document.total, initialToo=True)
		except:
			eMessage += "    Could not set document total\n"

		try:
			self.ui.textTotalLA.setText("Son %s" % utilities.moneyToText(Decimal(str(document.total))))
		except:
			eMessage += "    Could not set document cantidad con letra\n"

		## Payment
		try:
			if document.relations:
				payments = [x for x in document.process.documents if x.id in document.relations]
			else:
				payments = []

			if payments:
				self.ui.paymentFR.show()

			self.ui.paymentFR.initialCount = len(payments)

			for index, payment in enumerate(payments):
				'''
				self.ui.paymentFR.add()
				self.ui.paymentFR.setData(index, payment)

				if self.ui.paymentFR.isValid(index):
					self.ui.paymentFR.addTO.show()
				'''
				self.ui.paymentsBox.add(payment)

		except:
			eMessage += "    Could not set process payments\n"

		self.state_reset()

		self.ui.paymentFR.update()

		self.update_status()

		## SUPPLIER DATA
		try:
			if document.rol and not document.state_is_stROL_CURRENT:

				result = QtGui.QMessageBox.warning(self, u"Empresa Básica - Captura de Compra", u"El proveedor {} no existe en el sistema\n\n¿Quieres darlo de alta?".format(document.rol['person']['name']), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)

				if result == QtGui.QMessageBox.Yes:

					personsPackages = [x for x in self.app.packages['maintenance'].controllers if x.cast == 'person' ]

					suppliersPackage = [x for x in personsPackages if x.subCast[1] == 'supplier' ][0]

					'''
					## Set return point
					self.app.addToStack( [
						[ self.document.rol_set, [ 'method', suppliersPackage.master.captureView.saved ] ],
						[ self.set_data, [ 'data', self.document ] ],
						[ self.mst.form_show, [ 'no argument' , '' ], 'x' ]
						] )
					'''

					self.mst.imports_pending_set()

					suppliersPackage.master.addPerson(document.rol)

					suppliersPackage.master.form_show()
		except:
			eMessage += "    Could not process inexistent supplier\n"

		if eMessage:
			self.app.log2sys ( 'error', eMessage )
			raise Fault("    purchases.CaptureView.set_data()", eMessage)

		self.app.log2sys ( 'info', "    purchases view  CaptureView.set_data() - END" )


	def update_date(self):
		# print("    purchase view CaptureView.update_date()")

		if self.ui.dateED.isModified():
			self._isModified = self._isModified | 2 ** self.ui.dateED.bit
		else:
			self._isModified = self._isModified & ( ~ 2 ** self.ui.dateED.bit )

		view.CaptureView.update_date(self)

		# print("    purchase view CaptureView.update_date() - END")


	def update_discount(self):
		# print("    purchases view     CaptureView.update_discount()")

		if self.document.discounts:
			self.document.discounts[0]['amount'] = self.ui.discountED.value()
		else:
			self.document.discount_add(self.ui.discountED.value(), self.ui.discountFactorED.value())

		subtotal = self.ui.subtotalED.value()

		descuento = self.ui.discountED.value()

		subtotal2 = subtotal - descuento

		if self.taxMode == self.txMERGED:
			tax = Decimal("0.00")
		else:
			if self.ui.taxFactorED.value():
				tax = subtotal2 * self.ui.taxFactorED.value() / Decimal('100')
			else:
				tax = Decimal("0.00")

		total = subtotal2 + tax

		self.ui.subtotalED.setValue(subtotal)

		self.document.subtotal_set(subtotal)

		self.ui.discountED.setValue(descuento)

		if descuento:
			self.document.discounts_set([{'amount': descuento, 'factor': Decimal('0.00')}])

		self.ui.subtotal2ED.setValue(subtotal2)

		self.ui.taxED.setValue(tax)

		if 'general' in self.document.taxes:
			self.document.taxes['general']['amount'] = self.ui.taxED.value()

		self.ui.totalED.setValue(total)

		self.document.total_set(total)

		if total:
			self.ui.textTotalLA.setText("Son %s" % utilities.moneyToText(self.ui.totalED.value()))

		if self.ui.discountED.isModified():
			self._isModified = self._isModified | 2 ** self.ui.discountED.bit
		else:
			self._isModified = self._isModified & ( ~ 2 ** self.ui.discountED.bit )

		self.update_status()

		# print("    purchases view     CaptureView.update_discount() - END")


	def update_discountFactor(self):

		subtotal = self.ui.subtotalED.value()

		discountFactor = self.ui.discountFactorED.value()

		descuento = subtotal * discountFactor

		self.ui.discountED.setValue(descuento)

		subtotal2 = subtotal - descuento

		if self.taxMode == self.txMERGED:
			tax = Decimal("0.00")
		else:
			if self.ui.taxFactorED.value():
				tax = subtotal2 * self.ui.taxFactorED.value() / Decimal('100')
			else:
				tax = Decimal("0.00")

		total = subtotal2 + tax

		self.ui.subtotalED.setValue(subtotal)

		self.document.subtotal_set(subtotal)

		self.ui.discountED.setValue(descuento)

		if descuento:
			self.document.discounts_set([{'amount': descuento, 'factor': Decimal('0.00')}])

		self.ui.subtotal2ED.setValue(subtotal2)

		self.ui.taxED.setValue(tax)

		if 'general' in self.document.taxes:
			self.document.taxes['general']['amount'] = self.ui.taxED.value()

		self.ui.totalED.setValue(total)

		self.document.total_set(total)

		if total:
			self.ui.textTotalLA.setText("Son %s" % utilities.moneyToText(self.ui.totalED.value()))

		if self.ui.discountFactorED.isModified():
			self._isModified = self._isModified | 2 ** self.ui.discountFactorED.bit
		else:
			self._isModified = self._isModified & ( ~ 2 ** self.ui.discountFactorED.bit )

		self.update_status()


	def documentKind_update(self):
		self.app.log2sys ( 'info', "    purchases view  CaptureView.documentKind_update()" )

		self.ui.documentKindLA.roll()

		# if eval("{}".format(self.ui.documentKindLA.currentData().toString()))['value'] ==  u'fiscal':
		if eval("{}".format(self.ui.documentKindLA.currentData()))['value'] ==  u'fiscal':
			self.ui.selectorCliente.setRfcObligatorio(True)
			self.taxMode = self.txSTRIPPED
			# self.ui.taxFactorED.setValue(self.app.generalTax.quantize(Decimal('0')))

		else:
			self.ui.selectorCliente.setRfcObligatorio(False)
			self.taxMode = self.txMERGED
			# self.ui.taxFactorED.setValue(Decimal('0'))

		self.ui.itemsTA.update()

		self.ui.itemsTA.redraw()

		self.ui.numberED.setText(self.cnt.documentNumber("%s %s" % (self.ui.documentKindLA.currentText().lower(), u'compra')))

		self.document.number_set(self.ui.numberED.text())

		if self.ui.documentKindLA.isModified() or self.task is self.cnt.ADD:
			self._isModified = self._isModified | 2 ** self.ui.documentKindLA.bit
		else:
			self._isModified = self._isModified & ( ~ 2 ** self.ui.documentKindLA.bit )

		self.update_status()

		self.app.log2sys ( 'info', "    purchases view  CaptureView.documentKind_update() -END" )

	def editt(self, purchase, documentId=None):
		# print("""\npurchases.CaptureView.edit()""")

		## Mode setting
		self.task = self.EDIT
		self.ui.itemsTA.task = self.ui.itemsTA.EDIT

		## Widget Creation and clearing
		self.menu = QtGui.QMenu(self)

		self.clear()

		## Widget abilitation
		#~ self.ui.frameCaptura.setEnabled(True)
		self.ui.numberED.setEnabled(False)
		# self.ui.edCodigoProducto.setEnabled(False)
		# self.ui.edNombreProducto.setEnabled(False)
		# self.ui.cbLinea.setEnabled(False)

		self.ui.productSelector.setEnabled(False)

		self.mst.setInnerStatus('hidden')

		## Data setting
		# self.app.master.informacion = u"Para capturar partidas debe localizar el producto, por medio de su código o de su nombre"
		# self.ui.titulo.setText(QtGui.QApplication.translate(u"Empresa Básica", u"Modificación de Compra", None, QtGui.QApplication.UnicodeUTF8))
		self.ui.titulo.setText(u"Modificación de Compra")

		self.set_data(purchase, documentId)

		## Focus setting

		## Status updating
		self.update_status()

		self.show()


	def fechaFocused(self):
		self.ui.dateED.setVisible(False)
		self.ui.dateED.setVisible(True)
		self.update_status()


	def import_(self):
		# print("        purchases.CaptureView.import_()")

		#! Sends local document for resetting and filling, Why?
		#! Could just receive a new instance and set it

		self.cnt.import_(self.document)

		#! document is new, it cannot be stCURRENT, must be stCHANGED,
		#! can be stBAD if data has errors

		## Process rol state
		if not self.document.state_is_stROL_CURRENT:

			result = QtGui.QMessageBox.warning(self, u"Empresa Básica - Modificación de Compra", u"El proveedor {} no existe en el sistema\n\n¿Quieres darlo de alta?".format(self.document.rol['person']['name']), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)

			if result == QtGui.QMessageBox.Yes:

				personsPackages = [ x for x in self.app.packages['maintenance'].controllers if x.cast == 'person' ]

				suppliersPackage = [ x for x in personsPackages if x.subCast[1] == 'supplier' ][0]

				## Set return point
				self.app.addToStack([
					[ self.document.rol_set, [ 'method', suppliersPackage.master.captureView.saved ] ],
					[ self.set_data, [ 'data', self.document ] ],
					[ self.mst.form_show, [ 'no argument' , '' ], 'x' ]
					])

				suppliersPackage.master.addPerson(self.document.rol)

				suppliersPackage.master.form_show()

				self.supplier_pending_set()

		else:

			## Validate existence

			existent = self.cnt.documents_pull(rol_id=self.document.rol['id'], number=self.document.number)

			if existent:
				QtGui.QMessageBox.critical(self, self.app.name, u"El documento No.{} de {}{} ya existe en el sistema.\n\nNo se puede agregar de nuevo".format(self.document.number, self.document.rol['person']['name'], self.document.rol['person']['name2']), QtGui.QMessageBox.Ok)

			else:
				self.set_data(self.document)

		# print("        purchases.CaptureView.import_() - END")


	def init(self, *args, **kwds):
		self.app.log2sys ( 'info', "    purchases view  CaptureView.init()" )

		view.CaptureView.init(self, *args, **kwds)

		self.attributes = None

		self.state_set(self.cnt.BUSY)

		self.suppliers_update()

		## Purchase kinds
		purchaseKinds = self.cnt.processKinds_pull(cast_=self.cnt.cast)

		self.ui.kindSE.setData([x['name'] for x in purchaseKinds], [x['code'] for x in purchaseKinds])

		self.ui.kindSE.setCurrentData(self.cnt.processKinds_pull('default')['code'])

		self.ui.addSupplierBU.setToolTip(u'Presiona para agregar un Proveedor')
		self.orders_reset()
		self.loadPaymentConditions()

		self.load_documentKinds('formalize')

		self.adjustDocumentKinds_reset()

		self.documentKind_set(self.cnt.defaultDocumentKind(reference='formalize')['code'])

		self.state_reset()

		self.ui.productSelector.init()

		# self.clear()
		# self.impuestoGeneralFactor = (self.app.generalTax + Decimal('100')) / Decimal('100')

		self.ui.itemsTA.init()

		self.payments_show()

		# self.payment_new()
		# self.payment.init()

		self.set_data(self.document)

		self.app.log2sys ( 'info', "    purchases view  CaptureView.init() - END" )


	def isValid(self):
		# print("""    purchases.CaptureView.isValid()""")
		isValid = True
		messages = ""

		# documentKind is valid implicity

		try:
			if self.ui.numberED.isEmpty():
				isValid = False
				messages += u"Falta el folio.\n"
			elif not self.ui.numberED.isValid():
				isValid = False
				messages += u"%s\n" % self.ui.numberED.message()

			if not self.ui.dateED.text():
				isValid = False
				messages += u"Falta la fecha.\n"

			if self.ui.supplierCB.currentIndex() <= 0:
				isValid = False
				messages += u"Debe seleccionar un proveedor.\n"

			partidasValidas = self.ui.itemsTA.isValid()
			if not partidasValidas:
				isValid = False
				messages += self.ui.itemsTA.validityMessages

			if not self.ui.subtotalED.isValid():
				isValid = False
				messages += u"Subtotal fuera de rango\.n"

			if not self.ui.discountFactorED.isValid():
				isValid = False
				messages += u"Porcentaje de descuento no válido.\n"

			if not self.ui.discountED.isValid():
				isValid = False
				messages += u"Descuento fuera de rango.\n"

			if not self.ui.taxFactorED.isValid():
				isValid = False
				messages += u"Porcentaje de impuesto no válido.\n"

			if not self.ui.taxED.isValid():
				isValid = False
				messages += u"Impuesto fuera de rango.\n"

			if not self.ui.totalED.isValid():
				isValid = False
				messages += u"Total fuera de rango.\n"

			if not self.ui.paymentsBox.isValid():
				isValid = False
				messages += self.ui.paymentsBox.messages

			"""
			for index in range(self.ui.paymentsBox.ui.itemsLY.count()):

				layoutItem = self.ui.paymentsBox.ui.itemsLY.itemAt(index)

				if not layoutItem.widget().isValid():


					# messages += u"%s\n" % self.ui.paymentFR.validityMessages(index)
					messages += u"Payment {} is not valid\n".format(index+1)
			"""

			if not self.ui.cbCondiciones.currentIndex() > -1:
				messages += u"No ha seleccionado condiciones de pago.\n"


			# if self.ui.framePago2.isVisible():
				# if self.ui.cbCuenta.currentIndex() == -1:
					# isValid = False
					# self.mensajes += u"Debe seleccionar una cuenta\n"

				#~ if not self.ui.edNumeroCheque.isValid:
					#~ isValid = False
					#~ self.mensajes += u"%s\n" % self.ui.edNumero.message()

				# if self.ui.edMontoPago.value() == Decimal("0"):
					# isValid = False
					# self.mensajes += u"Falta el Monto del pago\n"
				# else:
					# if not self.ui.edMontoPago.isValid:
						# isValid = False
						# self.mensajes += u"El monto del pago no es válido\n"

			self.validityMessages = messages.rstrip("\n")

		except:
			print (4441, sys.exc_info())
			print (4442, messages)

		# print("""    purchases.CaptureView.isValid() - END""")

		return isValid


	def kind_update(self):
		# print("purchases.CaptureView.kind_update()")
		if self.state is self.cnt.IDLE:
			current = self.ui.kindSE.currentData()
			# self.suppliers_set()
			self.suppliers_
		# print("purchases.CaptureView.kind_update() - END")


	def adjustDocumentKinds_reset(self):
		# print("""    purchases.CaptureView.adjustDocumentKinds_reset()""")

		self.ui.cbTipoDocumentoAjuste.clear()
		kinds = self.cnt.documentKinds_pull(referenceLIKE=u'ajustes')
		for kind in kinds:
			self.ui.cbTipoDocumentoAjuste.addItem("%s" % kind['value'], kind['code'])

		# print("""    purchases.CaptureView.adjustDocumentKinds_reset() - END""")


	# def loadLines(self, **filtros):
		# """ Filtra por Marca """
		# lines = self.cnt.productLines(**filtros)
		# self.ui.cbLinea.clear()
		# self.ui.cbLinea.addItem("", -1)
		# for line in lines:
			# self.ui.cbLinea.addItem(line['name'], line['id'])


	def loadPaymentConditions(self):
		"""purchases.CaptureView.loadPaymentConditions()"""
		self.ui.cbCondiciones.clear()
		conditions = self.cnt.paymentConditions()
		for condition in conditions:
			self.ui.cbCondiciones.addItem(condition['name'], condition['code'])
		self.ui.cbCondiciones.setCurrentIndex(-1)


	def number_validate(self):
		"""purchases.CaptureView.number_validate()"""

		if self.task is self.cnt.ADD:

			if self.ui.supplierCB.currentData() is None:
				self.ui.serieED.setExternalValidation(False, u"Se requiere proveedor para validar folio")
				self.ui.numberED.setExternalValidation(False, u"Se requiere proveedor para validar folio")

			elif self.cnt.process(number=unicode(self.ui.numberED.text()), rol_id=self.ui.supplierCB.currentData(), kind={'code':self.ui.documentKindLA.currentData()}):
				self.ui.numberED.setExternalValidation(False, u"El folio ya existe para este Proveedor")

			else:
				self.ui.numberED.setExternalValidation(True, u"")

				self.document.number_set(self.ui.numberED.text())

			if self.ui.serieED.isModified():
				self._isModified = self._isModified | 2 ** self.ui.serieED.bit
			else:
				self._isModified = self._isModified & ( ~ 2 ** self.ui.serieED.bit )

			if self.ui.numberED.isModified():
				self._isModified = self._isModified | 2 ** self.ui.numberED.bit
			else:
				self._isModified = self._isModified & ( ~ 2 ** self.ui.numberED.bit )


			self.update_status()


	def order_selected(self, index):
		"""purchases.CaptureView.order_selected()"""
		if index != -1:
			if not "No hay" in self.ui.orderCB.currentText():
				# order = app.model.getOrder(id=self.ui.orderCB.itemData(index).toInt()[0])
				# order = self.ui.orderCB.fullData[self.ui.orderCB.itemData(self.ui.orderCB.currentIndex()).toInt()[0]]
				# orderProcess = eval('{}'.format(self.ui.orderCB.currentData(1001)))
				# document = [x for x in orderProcess['documents'] if x['kind']['code'] == 12513][0]

				orderProcess = self.ui.orderCB.currentData(1001)

				document = [x for x in orderProcess.documents if x.kind['code'] == 12513][0]

				if self.ui.itemsTA.rowCount() == 0:

					self.cnt.items_pull(document)

					self.orderData_set(document)

					self.update_status()

				# self.initial = orderProcess
				self.initialDocument = document


	def orderData_set(self, documento):
		""" Receives a purchase process with an order document to
			capture the correspondent invoice or receipt document
		"""
		# print("""        purchases.CaptureView.orderData_set()""")

		process = {}
		process['id'] = documento.process.id
		process['kind'] = documento.process.kind

		document = {}
		document['date'] = documento.date
		document['total'] = documento.total
		document['subtotal'] = documento.subtotal
		document['discounts'] = documento.discounts
		document['taxes'] = documento.taxes
		document['rol'] = documento.rol
		document['kind'] = self.app.model.attribute_get(category='documentKind', name='Invoice', cast_='purchase')
		document['status'] = 'open'

		items = []
		for item_ in documento.items:
			item = {}
			item['status'] = item_.status
			item['product'] = item_.product
			item['price'] = item_.price
			item['cost'] = item_.cost
			item['quantity'] = item_.quantity
			items.append(item)

		document['items'] = items

		process['documents'] = [document]

		process = self.cnt.process_new(**process)

		self.set_data(process.documents[0])

		# self.state_set(self.cnt.BUSY)

		# print("""        purchases.CaptureView.orderData_set() - END""")


	def orders_reset(self, rol_id=None):
		"""
			Loads processes that contain not closed order document(s).
			If a rol is selected, limits search to it.
		"""
		# oldLevel = self.app.stdoutLog.level
		# self.app.stdoutLog.setLevel(logging.INFO)
		self.app.log2sys ( 'info', "    purchase view  CaptureView.orders_reset()" )

		self.ui.orderED.hide()

		currentDataBackup = self.ui.orderCB.currentData()

		self.ui.orderCB.clear()

		orders = []

		if self.document.rol:

			try:
				if self.document.rol['id']:
					orders = self.cnt.orders_load(**{'document status':['open', 'pending', 'delivered', 'received'], 'rol_id':self.document.rol['id']})
				else:
					orders = self.cnt.orders_load(**{'document status':['open', 'pending', 'delivered', 'received']})

			except:
				## Se asume que no existe el proveedor
				self.app.log2sys ( 'error', "    purchase view CaptureView.orders_reset()\n        Error al cargar pedidos para {}\n        {}\n        {}".format(self.document.rol['person']['name'], sys.exc_info(), self.document.rol) )

		if orders:

			orders.reverse()

			for fullDataIndex, order in enumerate(orders):

				# document = [x for x in order.documents if x.kind['code'] == 12513]

				# if document:
					# document = document[0]

					self.ui.orderCB.addItem("{}".format(order.number), order.id)
					# self.ui.orderCB.setItemData(fullDataIndex, repr(order), 1001)
					self.ui.orderCB.setItemData(fullDataIndex, order, 1001)

		else:
			self.ui.orderCB.addItem("No hay pedidos pendientes", -1)

		self.ui.orderCB.setCurrentData(currentDataBackup)

		self.app.log2sys ( 'info', "    purchase view  CaptureView.orders_reset() - END" )
		# self.app.stdoutLog.setLevel(oldLevel)


	def origenChanged(self, index):
		f=h
		origen = self.cnt.rol(id=self.ui.cbOrigen.currentData())

		if origen['id'] == self.app.holder['id']:
			self.ui.laNombre.setText(u" &Nombre LOCAL de artículo")
		else:
			self.ui.laNombre.setText(u" &Nombre de artículo de %s %s" % (origen['person']['name'], origen['person']['name2']))

		if len(self.ui.edNombreProducto.text()) < 2:
			self.ui.edNombreProducto.completer().model().clear()
		else:
			self.nombreProductoEditado(self.ui.edNombreProducto.text()[:2])


	def origin_update(self):
		"""purchases.CaptureView.origin_update()"""
		# self.ui.itemsTA.origin_set(self.ui.productSelector.origin())
		pass


	def partidaCapturada(self):
		self.ui.itemsTA.clearSelection()

		self.ui.productSelector.ui.nameED.setFocus()


	def productAdded(self, product):
		# print("""        purchases.CaptureView.productAdded()""")

		if self.waitsForProduct:
			try:
				aception = [ x for x in product['aceptions'] if x['rol_id'] == self.ui.itemsTA.origin()['id'] ][0]
			except IndexError:
				self.app.log2sys ( 'error', "        purchases.CaptureView.productAdded()\n            origin: {}\n            product: {}".format(self.ui.itemsTA.origin(), product) )
				raise
			else:

				kwds = {}

				if aception['code'] == '---':

					kwds['name'] = aception['name']

				else:

					kwds['code'] = aception['code']

				indexes = self.ui.itemsTA.rows_find(**kwds)

				if len(indexes) == 1:

					rowIndex = indexes[0]

					codeItem = self.ui.itemsTA.item(rowIndex, 0)

					itemInstance = codeItem.data(self.ui.itemsTA.INSTANCE)

					itemInstance.product_set(product)

					self.ui.itemsTA.setDatosRenglon(rowIndex, itemInstance)

				else:

					print ("No hay equivalente o hay más de uno")

				self.update_status()

		# print("""        purchases.CaptureView.productAdded() - END""")


	@property
	def rangoPrecioActual(self):
		return self.__rangoPrecioActual


	def reset(self):
		# print("""        purchases.CaptureView.reset()""")
		f=j
		view.CaptureView.reset(self)

		self.state_set(self.cnt.BUSY)

		self.ui.itemsTA.reset()

		if self.task is self.cnt.EDIT:
			self.ui.orderCB.hide()
			self.ui.orderED.show()
		else:
			self.ui.orderCB.show()
			self.ui.orderED.hide()
			self.ui.orderCB.setCurrentIndex(-1, initialToo=True)

		self.taxMode = self.txSTRIPPED

		self.tipo = None

		# self.ui.itemsTA.reset()
		self.ui.documentKindLA.current_setByData(self.cnt.defaultDocumentKind( reference='formalize')['code'], initialToo=True)

		self.ui.numberED.clear()
		self.ui.numberED.setExternalValidation(True, u"")

		self.ui.supplierCB.setCurrentIndex(-1, initialToo=True)
		self.ui.cbCondiciones.setCurrentIndex(-1, initialToo=True)

		# self.ui.cbOrigen.setCurrentIndex(0)

		self.ui.productSelector.clear()

		# self.ui.cbLinea.setCurrentIndex(-1)

		self.ui.subtotalED.clear()
		self.ui.discountFactorED.clear()
		self.ui.discountED.clear()
		self.ui.subtotal2ED.clear()

		self.ui.taxBU.setText(self.app.generalTax['name'])
		self.ui.taxFactorED.setValue(self.app.generalTax['value'])
		self.ui.taxED.setValue(Decimal('0'), initialToo=True)
		self.document.tax_set(Decimal('0.00'))

		# self.ui.tax2FactorED.clear()
		self.ui.tax2FactorED.setValue(Decimal('0'), initialToo=True)
		# self.ui.tax2ED.clear()
		self.ui.tax2ED.setValue(Decimal('0'), initialToo=True)

		self.taxes_hide()
		self.taxes_show()

		self.ui.totalED.clear()

		self.ui.textTotallA.clear()

		## Payment
		self.ui.paymentFR.clear()

		self.ui.cbTipoAjuste.setCurrentIndex(-1)
		self.ui.cbTipoDocumentoAjuste.setCurrentIndex(-1)
		self.ui.edFolioAjuste.clear()
		self.ui.fechaAjuste.setDate(QtCore.QDate().currentDate())
		self.ui.edMontoAjuste.clear()

		self.initialDocument = None

		self.state_reset()

		# print("""        purchases.CaptureView.reset() - END""")


	def save(self):

		#~ oldLevel = self.app.stdoutLog.level
		#~ self.app.stdoutLog.setLevel(logging.INFO)
		self.app.log2sys ( 'info', "    purchases view  CaptureView.save()" )

		## Si el proceso ya existe
		if self.document.process.id:

			modified_documents = self.modified_data()

			for document in modified_documents:

				## Si el documento ya existe
				if self.document.id:

					document['processId'] = self.document.process.id


			# for document in self.document.process.documents:

				# Processes only new documents (with no id)
				# if not document.id:
					# Asumed valid

					# self.document.status_set('open')    #! This doesn't push

					# document.relation_add(self.document.id)

					# document.status_set('closed')
					# status = document.push()

					# If document is payment
					# if document.kind['code'] in [14517, 14519]:

						# if document.total >= self.document.total:
							# self.document.status_set('closed')
							# status = self.document.push()

				# else:
					# print (204, self.modified_data())
					## process_modified = self.modified_data()
					# documents_modified = self.modified_data()

					# for document in documents_modified:

						# documentInstance = Document(process, document)

						# document.push()

					# status = self.document.push()



		## Si es proceso nuevo
		else:
			self.document.status_set('open')

			self.document.process.push()

			if self.ui.orderCB.currentIndex() != -1:

				self.mst.eventRouter.emit(QtCore.SIGNAL('ordersChanged()'))

		self.mst.eventRouter.emit(QtCore.SIGNAL('productsChanged()'))
		self.mst.eventRouter.emit(QtCore.SIGNAL('purchasesChanged()'))

		if False:
			self.orders_reset()

		self.hide()
		self.emit(QtCore.SIGNAL('captureViewClosed()'))

		self.app.log2sys ( 'info', "    purchases view  CaptureView.save() - END" )
		#~ self.app.stdoutLog.setLevel(oldLevel)


	def showed(self):
		if self.ui.supplierCB.currentIndex() <= 0:
			self.cnt.information_set(u"""Para capturar partidas debe localizar el producto, por medio de su código o de su nombre\n\n""")  # lint:ok
		else:
			self.cnt.information_set(u"""Si no aparece el producto que desea, tal vez no existan los datos para el proveedor seleccionado.""")  # lint:ok


	def update_status(self, args=None):
		# print("    purchases view    CaptureView.update_status()")

		view.CaptureView.update_status(self, args)

		if self.state is self.cnt.IDLE:

			if self.ui.supplierCB.currentIndex() == -1:
				self.ui.captureFR.setEnabled(False)
				self.ui.captureFR.setToolTip(u"Selecciona un proveedor para activar la captura de productos")
			else:
				self.ui.captureFR.setEnabled(True)
				self.ui.captureFR.setToolTip(u"")

		# print("    purchases view    CaptureView.update_status() - END")


	def supplier_add(self):
		# print("purchases.CaptureView.supplier_add() - empty")
		f=j
		pass


	def supplier_added(self, supplier):

		if self.supplier_pending:

			self.ui.supplierCB.setCurrentData(supplier['id'], initialToo=True)


	@property
	def supplier_pending(self):
		self._supplier_pending
	def supplier_pending_set(self, value=True):
		self._supplier_pending = value


	def supplier_update(self, index):
		# print("""    purchases.CaptureView.supplier_update()""")

		if self.state is self.cnt.IDLE:

			if index != -1:

				rol = eval("{}".format(self.ui.supplierCB.currentData(self.ui.supplierCB.FULLDATA)))

				self.orders_reset(rol_id=rol['id'])

				oldFocused = self.focusWidget()
				self.number_validate()
				if oldFocused:
					oldFocused.setFocus()

				self.ui.productSelector.dealer_set(rol)
				self.ui.itemsTA.origin_set(rol['id'])

				self.document.rol_set(rol)

				if self.ui.supplierCB.isModified():
					self._isModified = self._isModified | 2 ** self.ui.supplierCB.bit
				else:
					self._isModified = self._isModified & ( ~ 2 ** self.ui.supplierCB.bit )


				# self.ui.subtotalED.setValue(self.ui.itemsTA.subtotal())
				# self.update_total()

		# print("""    purchases.CaptureView.supplier_update() - END""")


	def suppliers_update(self, goodKinds=None):
		# print("    purchases.CaptureView.suppliers_update()")

		self.state_set(self.cnt.BUSY)

		if goodKinds:
			suppliers = [x for x in self.mst.suppliers if goodKinds == goodKinds]
		else:
			suppliers = self.mst.suppliers

		oldCurrentData = self.ui.supplierCB.currentData()

		self.ui.supplierCB.clear()

		self.ui.supplierCB.addItem(u"", self.app.holder['id'])

		self.ui.supplierCB.setItemData(0, self.app.holder, self.ui.supplierCB.FULLDATA)

		if suppliers:
			for supplierIndex, supplier in enumerate(suppliers):
				self.ui.supplierCB.addItem("%s %s" % (supplier['person']['name'], supplier['person']['name2']), supplier['id'])
				self.ui.supplierCB.setItemData(supplierIndex+1, supplier['person']['rfc'], QtCore.Qt.UserRole+1)
				self.ui.supplierCB.setItemData(supplierIndex+1, supplier, self.ui.supplierCB.FULLDATA)

		else:
			self.ui.supplierCB.setToolTip("No hay proveedores capturados")

		self.ui.supplierCB.setCurrentData(oldCurrentData)

		self.state_reset()

		# print("    purchases.CaptureView.suppliers_update() - END")


	def set_task(self, value):
		# print("    purchases view    CaptureView.set_task()")

		self._task = value
		self.ui.itemsTA.task = value

		self.state_set(self.cnt.BUSY)
		self.taxMode = self.txSTRIPPED

		self.ui.titulo.setText(QtGui.QApplication.translate("Empresa Básica", "Compra nueva", None, QtGui.QApplication.UnicodeUTF8))
		# self.clear()

		try:
			if self.ui.documentKindLA.currentData == 12515:
				self.ui.numberED.setText(self.cnt.documentNumber('remisión compra'.decode('utf8')))
			else:
				self.ui.numberED.setText('{}'.format(self.cnt.documentNumber('invoice')))
			self.ui.numberED.setEnabled(True)

			self.document.number_set(self.ui.numberED.text())
		except:
			print ("""    ==== Error @ purchases.CaptureView.set_data()""")
			print ("""        Could not set process payments\n""")
			raise

		self.ui.dateED.setDate(QtCore.QDate().currentDate())
		self.document.date_set(self.ui.dateED.dateTime().toPyDateTime())

		self.ui.productSelector.setEnabled(True)

		## Data setting
		self.cnt.information_set(u"Para capturar partidas debe localizar el producto, por medio de su código o de su nombre")

		self.ui.chAjustes.setChecked(False)

		# print("    purchases view    CaptureView.set_task() - END")

		# if process:
			# self.initial = process
			# self.initialDocumentId = None

			# orderDocument = [ x for x in process['documents'] if x['kind']['code'] == 12513][0]

			# self.ui.supplierCB.setCurrentData(orderDocument['rol']['id'], initialToo=True)
			# self.ui.itemsTA.origin_set(orderDocument['rol'])

			# self.orderData_set(orderDocument)

		self.state_reset()

		## Focus setting
		self.ui.supplierCB.setFocus()

		## Status updating
		self.update_status()

		self.show()

		# print("""    purchases.CaptureView.set_task() - END""")


	def update_tax(self):
		total = self.ui.subtotalED.value() - self.ui.discountED.value() + self.ui.taxED.value()

		if 'general' in self.document.taxes:
			self.document.taxes['general']['amount'] = self.ui.taxED.value()

		self.ui.totalED.setValue(total)
		self.document.total_set(total)
		self.totalEdited()

	def update_taxFactor(self):
		# print("""    purchases.CaptureView.update_taxFactor()""")
		if 'general' in self.document.taxes:
			self.document.taxes['general']['factor'] = self.ui.taxFactorED.value()
		else:
			self.document.tax_add('general', {'name':'iva', 'factor':self.ui.taxFactorED.value(), 'amount':self.ui.taxED.value()})

		self.update_total()

		# print("""    purchases.CaptureView.update_taxFactor() - END""")


	def taxes_hide(self):
		# for taxIndex in range(self.taxes_count):
		self.ui.taxLA.hide()
		self.ui.taxED.hide()
		self.ui.taxFactorED.hide()
		self.ui.tax2ED.hide()
		self.ui.tax2FactorED.hide()
		pass


	def taxes_show(self):
		self.ui.taxLA.show()
		self.ui.taxED.show()
		self.ui.taxFactorED.show()
		if self.ui.tax2FactorED.value():
			self.ui.tax2ED.show()
			self.ui.tax2FactorED.show()
		pass


	def toggleAjustes(self, state):
		if state == QtCore.Qt.Checked:
			# valor = u"1"
			if not self.ui.edMontoAjuste.text():
				self.ui.edMontoAjuste.setValue(self.ui.totalED.value())
			self.ui.frAjustes.show()
			self.update_status()
		else:
			# valor = u""
			self.ui.frAjustes.hide()
			self.update_status()


	def update_total(self):
		# print("    purchases view CaptureView.update_total()")

		if self.state is self.cnt.IDLE:

			# subtotal = self.ui.subtotalED.value()
			subtotal = self.ui.itemsTA.total

			if self.ui.discountFactorED.value():
				descuento = subtotal * self.ui.discountFactorED.value() / Decimal("100")
			else:
				descuento = Decimal("0.00")

			subtotal2 = subtotal - descuento

			if self.taxMode == self.txMERGED:
				self.ui.taxED.setText('')  # No aplica el despliegue de impuesto
				total = subtotal2
			else:
				if self.ui.taxFactorED.value():
					tax = subtotal2 * self.ui.taxFactorED.value() / Decimal("100")
				else:
					tax = Decimal("0.00")

				self.ui.taxED.setValue(tax)
				if 'general' in self.document.taxes:
					self.document.taxes['general']['amount'] = self.ui.taxED.value()

				total = subtotal2 + tax

			self.ui.subtotalED.setValue(subtotal)
			self.document.subtotal_set(subtotal)

			self.ui.discountED.setValue(descuento)
			if descuento:
				self.document.discount_add(descuento)

			self.ui.subtotal2ED.setValue(subtotal2)
			self.ui.totalED.setValue(total)
			self.document.total_set(total)

			if total:
				self.ui.textTotalLA.setText("Son %s" % utilities.moneyToText(Decimal(str(self.ui.totalED.value()))))

			#~ self.payment.setImporte(self.ui.totalED.value())

			if self.ui.totalED.isModified():
				self._isModified = self._isModified | 2 ** self.ui.totalED.bit
			else:
				self._isModified = self._isModified & ( ~ 2 ** self.ui.totalED.bit )

			self.update_status()

		# print("    purchases view CaptureView.update_total() - END")


	def totalEdited(self, text=None):
		self.ui.textTotalLA.setText(" Son %s" % utilities.moneyToText(self.ui.totalED.value()))
		self.update_status()

	def ui_set(self):
		self.ui = capture_ui.Ui_Form()
		self.ui.setupUi(self)

	# _waitsForProduct = False
	# def waitsForProduct(self):
		# return self._waitsForProduct
	# def waitsForProduct_set(self, value):
		# self._waitsForProduct = value


class Details(view.Details):

	# @property
	# def state(self):
		# return self._state[-1]
	# def state_set(self, value):
		# self._state.append(value)
	# def state_reset(self):
		# self._state.pop()

	def __init__(self, *args, **kwds):


		# self.mst = args[0]
		# self.cnt = self.mst.cnt

		view.Details.__init__(self, *args)

		self.ui = details_ui.Ui_Form()
		self.ui.setupUi(self)




		# self.connect(self.ui.toImprimir, QtCore.SIGNAL("clicked()"), self.imprimir)










		# self.connect(self, QtCore.SIGNAL("doubleClicked()"), self.close)
		self.connect(self.mst.eventRouter, QtCore.SIGNAL('comprasChanged()'), self.update)


		# self._state = [self.cnt.IDLE]


	def clear(self):
		"""purchases.view.Details().clear()"""
		for rowIndex in range(1, self.ui.codeLY.count()):
			widget = self.ui.codeLY.takeAt(1).widget()
			widget.close()
			widget = self.ui.nameLY.takeAt(1).widget()
			widget.close()
			widget = self.ui.clasificationLY.takeAt(1).widget()
			widget.close()
			widget = self.ui.quantityLY.takeAt(1).widget()
			widget.close()
			widget = self.ui.priceLY.takeAt(1).widget()
			widget.close()
			widget = self.ui.importLY.takeAt(1).widget()
			widget.close()

		self.ui.paymentTextLA.setText("")


	def setData(self, document):
		self.app.log2sys ( 'info', "    purchases view          Details.setData()" )

		self.data = document

		document.items_set(self.cnt.documentItems(document_id=document.id))

		self.clear()

		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)

		self.ui.laFolio.setText("%s" % document.number)
		self.ui.laFecha.setText(document.date.strftime("%d %b %Y"))

		rol = self.cnt.origin(id=document.rol['id'])

		self.ui.laOrigen.setText("%s %s" % (rol['person']['name'], rol['person']['name2']))
		# self.ui.laOrigen.setFont(font)

		self.ui.laSubtotal.setText("%.2f" % document.subtotal)
		if document.discounts:
			self.ui.laDescuento.setText("%.2f" % document.discounts[0]['amount'])

		self.ui.laImpuesto.setText("{}".format(document.taxes['general']['amount']))

		self.ui.laTotal.setText("%.2f" % document.total)
		self.ui.laTotal.setFont(font)

		font.setPointSize(8)

		font2 = QtGui.QFont()
		font2.setPointSize(9)
		font2.setBold(True)

		for rowIndex, item in enumerate(document.items):
			# try:
			print(123234, rowIndex, item.product)

			# aception = self.cnt.aception(product_id=item['product']['id'], rol_id=rol['id'])
			aception = [x for x in item.product['aceptions'] if x['rol_id'] == rol['id']][0]

			tableItem = QtGui.QLabel("%s " % aception['code'])
			tableItem.setFont(font2)
			self.ui.codeLY.addWidget(tableItem)

			tableItem = QtGui.QLabel("%s " % aception['name'])
			tableItem.setFont(font)
			self.ui.nameLY.addWidget(tableItem)

			tableItem = QtGui.QLabel("%s " % item.product['lines'][0]['name'])
			tableItem.setFont(font2)
			self.ui.clasificationLY.addWidget(tableItem)

			tableItem = QtGui.QLabel("%s" % item.quantity)
			tableItem.setFont(font)
			tableItem.setAlignment(QtCore.Qt.AlignCenter)
			self.ui.quantityLY.addWidget(tableItem)

			tableItem = QtGui.QLabel(" %.2f" % item.price)
			tableItem.setFont(font)
			tableItem.setAlignment(QtCore.Qt.AlignRight)
			self.ui.priceLY.addWidget(tableItem)

			tableItem = QtGui.QLabel(" %.2f" % (item.quantity * item.price))
			tableItem.setFont(font2)
			tableItem.setAlignment(QtCore.Qt.AlignRight)
			self.ui.importLY.addWidget(tableItem)

		## Paymnt
		self.ui.framePago.show()

		text = ''

		kindCheque = self.cnt.attribute(category='documentKind', name=u'cheque')

		checks = [x for x in document.process.documents if x.kind['code'] == kindCheque['code']]

		for check in checks:
			text += "Cheque  %s   %s   %s    %8.2f \n" % (check.date.strftime("%d-%b-%Y"), check.reference, check.number, check.total)

		self.ui.paymentTextLA.setText(text)

		"""
#        payment = app.model.getDocumento(proceso_id=compra['proceso_id'], operacion_tipo='pago')
		documentPagoZero = [x for x in purchase['documents'] if x['kind_code'] in [app.model.getAttribute(category='documentKind', name='efectivo')['code'], app.model.getAttribute(category='documentKind', name='cheque')['code']]]
		# operacionPagoZero = [x for x in compra.operaciones if x.tipo==u'pago']
		if documentPagoZero:

				if documentPagoZero[0]['kind_code'] == app.model.getAttribute(category='documentKind', name=u'efectivo')['code']:
					self.ui.paymentTextLA.setText("Efectivo  %s   %8.2f  Cambio %8.2f" % (documentPagoZero[0]['date'].strftime("%d-%b-%Y"), documentPagoZero[0]['total'], documentPagoZero[0]['subtotal']))
				elif documentoPago.tipo.name == app.model.getAttribute(category='documentKind', name=u'cheque')['id']:
					self.ui.paymentTextLA.setText("Cheque  %s   %s   %s    %8.2f" % (documentPagoZero[0]['date'].strftime("%d-%b-%Y"), documentPagoZero[0]['reference'], documentPagoZero[0]['number'], documentPagoZero[0]['total']))
			# else:
				# self.ui.paymentTextLA.setText("En efectivo  $ %s" % payment.monto)

				self.ui.framePago.show()
		else:
				self.ui.framePago.hide()
		"""

		self.setCursor(QtCore.Qt.ArrowCursor)

		self.app.log2sys ( 'info', "    purchases view          Details.setData() - END" )


class Splitter(QtGui.QSplitter):

	def __init__(self, *args):
		self.orientation = args[0]
		QtGui.QSplitter.__init__(self, *args)

	def createHandle(self):
		return Handle(self.orientation, self)



class Handle(QtGui.QSplitterHandle):

	def __init__(self, *args):
		QtGui.QSplitterHandle.__init__(self, *args)

	def mouseDoubleClickEvent(self, event):
		self.emit(QtCore.SIGNAL("handlePressed"))



class Model(QtCore.QAbstractListModel):

	def __init__(self, *args):
		QtCore.QAbstractListModel.__init__(self, *args)
		self.__data = []


	def clear(self):
		# self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount())
		self.__data = []
		self.reset()
		# self.endRemoveRows()


	def data(self, index, role=QtCore.Qt.DisplayRole):
		if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
			return self.__data[index.row()][index.column()]
		elif role == QtCore.Qt.TextAlignmentRole:
			# if index.column() == self.COL_QUANTITY:
				# return int(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
			# if index.column() in [self.COL_PRICE, self.COL_AMOUNT]:
				# return int(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
			return int(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
		elif role == 1001:
			return self.__data[index.row()][1]
		elif role == 1002:
			return self.__data[index.row()][2]
		elif role == 1003:
			return self.__data[index.row()][3]
		elif role == 1004:
			return self.__data[index.row()][4]
		else:
			return

	def insertRow(self, row, parent=QtCore.QModelIndex()):
		self.__data.insert(row, [u"", u""])
		return True


	def rowCount(self, parent=QtCore.QModelIndex()):
		return len(self.__data)


	def setData(self, row, value, role=QtCore.Qt.DisplayRole):
		""" No se usa la porquería de modelIndex """
		if row >= len(self.__data):
			self.__data.append([None, None, None, None, None])

		if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
			self.__data[row][0] = value
		elif role == 1001:
			self.__data[row][1] = value
		elif role == 1002:
			self.__data[row][2] = value
		elif role == 1003:
			self.__data[row][3] = value
		elif role == 1004:
			self.__data[row][4] = value
		else:
			print ("puaj")
		return True


class Fault(Exception):

	 def __init__(self, method, error):
		 self.method = method
		 self.error = error

	 def __str__(self):
		 return '{}\n    {}'.format(self.method, self.error)


## Se tiene instalada la capacidad de modificacion de acepción, pero
## se deshabilitó por fines de simplicidad.

class OptionsFR(QtGui.QFrame):

	@property
	def state(self):
		return self._state[-1]
	def state_set(self, value):
		self._state.append(value)
	def state_reset(self):
		self._state.pop()

	def __init__(self, *args, **kwds):

		self.mst = kwds.pop('mst', None)
		self.cnt = self.mst.cnt
		self.app = self.mst.cnt.app

		QtGui.QFrame.__init__(self, *args, **kwds)

		self._state = [self.cnt.IDLE]

		self.state_set(self.cnt.BUSY)

		layoutZoom = self.app.master.layoutZoom

		font = QtGui.QFont()
		font.setPointSize(10 * layoutZoom)
		font.setWeight(75)
		font.setBold(True)

		# self.setStyleSheet("""#frVentas{
			# border-style: solid;
			# border-width: 1px;
			# border-radius: 9px;
			# border-bottom-color: #A0A0A0;
			# border-right-color: #A0A0A0;
			# border-left-color: #FFFFFF;
			# border-top-color: #FFFFFF;
			# background-color: #F0F0D0;
			# }""")

		self.ui = tools_ui.Ui_Frame()
		self.ui.setupUi(self)


	def init(self):
		"""            OptionsFR.init()"""

		self.state_set(self.cnt.BUSY)

		# self.ui.periodoSD.setData([x['name'] for x in statuss], [x['code'] for x in statuss])

		lastSync = self.app.model.getAttribute(category='system', name='lastSync', cast_=self.cnt.cast)

		print ( lastSync )

		self.ui.lastExecutionDateLA.setText ( lastSync['value'] )

		self.state_reset()

		"""            OptionsFR.init() - END"""


if __name__ == "__main__":
	print ("Test routine not implemented for purchases.view")





"""
  ~~~~  Changelog  ~~~~

	2014.04.23        Manager.cbProveedor changed maxVisible items from 10 to 15
					CaptureView. Fixed update_total() calls


  ~~~~  BEHAVIOUR  ~~~~
	Data Layout :   Defines if tax and discount data will we shown at
					table or at sum data.
		- dataLayout
		- [dlXXX*] : dlSUMMARY = 0, dlEXPLICIT = 100
		- default = dlSUMMARY

  ~~~~~~  Technicality  ~~~~~~

	Each process (object) displayed in the manager, may have hooked a capture view and a details
	view.
	Besides, the master can have one process that will be used for adding new processes to the
	database, it will have a capture view hooked, and should not have a details view, as they are
	for displaying valid (complete) data objects.
	When a manager requests a process add, if the corresponding process object in the master does
	not exist, one is created, with its capture corresponding view and the view is displayed.

"""
