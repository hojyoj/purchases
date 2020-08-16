# -*- coding: utf-8 -*-

 ##############################################
 ##                                            ##
 ##              Purchases package              ##
 ##                  Data Model                 ##
 ##                                             ##
 ##              from Basiq Series              ##
 ##           by Críptidos Digitales            ##
 ##                 GPL (c)2008                 ##
  ##                                            ##
	##############################################

"""
"""

from __future__ import print_function

import sys, copy

import datetime
from decimal import Decimal

# from basiq.baseModel import Model
import processes.model as processes


class Model(processes.Model):

	def __init__(self, *args, **kwds):
		self.model = args[0]

		processes.Model.__init__(self, *args, **kwds)


	def plug(self):
		# print "purchases.model.plug()"
		self.model.recalculatePriceOnPurchase = self.recalculatePriceOnPurchase


	def recalculatePriceOnPurchase(self):
		return not not self.model.getAttribute(category=u'system', name=u'recalcularPreciosAlComprar', cast_=u'purchase')['value']


	def getOrigins(self, **filters):
		origins = self.model.rols_full_pull(kind='origen')

		global __originCount
		__originCount = len(origins)

		return origins


	def getPurchase(self, **filters):
		command = """SELECT
			processes.id,
			processes.status,
			array_agg(docs.id) AS docs_id,
			array_agg(docs.kind_code) AS docs_kind_code,
			array_agg(docs.number) AS docs_number,
			array_agg(docs.date) AS docs_date,
			array_agg(docs.rol_id) AS docs_rol_id,
			array_agg(docs.subtotal) AS docs_subtotal,
			array_agg(docs.discount) AS docs_discount,
			array_agg(docs.discountpercent) AS docs_discountpercent,
			array_agg(docs.tax) AS docs_tax,
			array_agg(docs.taxpercent) AS docs_taxpercent,
			array_agg(docs.total) AS docs_total,
			array_agg(docs.status) AS docs_status,
			array_agg(docs.relation) AS docs_relation,
			array_agg(docs.reference) AS docs_reference
			FROM processes
			JOIN processes_documents AS link ON (processes.id=link.process_id)
			JOIN (SELECT * FROM documents ORDER BY date ASC) AS docs ON (link.document_id=docs.id)
			WHERE
			GROUP BY processes.id, processes.status
		"""

		if 'document_id' in filters.keys():
			filters['docs.id'] = filters.pop('document_id')

		if 'id' in filters.keys():
			filters['processes.id'] = filters.pop('id')

		if 'kind' in filters.keys():
			if 'code' in filters['kind']:
				filters['docs.kind_code'] = filters.pop('kind')['code']

		if 'number' in filters.keys():
			filters['docs.number'] = filters.pop('number')

		filtersText = ""
		for filter in filters.keys():
			if type(filters[filter]) in (str, datetime.datetime):
				filtersText += "%s='%s' AND " % (filter, filters[filter])
			elif type(filters[filter]) in (list,):
				temp = ("%s" % filters[filter]).replace("[", "(").replace("]",")")
				filtersText += "%s IN %s AND " % (filter, temp)
			else:
				try:
					if type(filters[filter]) in [unicode]:
						filtersText += "%s='%s' AND " % (filter, filters[filter])
					else:
						filtersText += "%s=%s AND " % (filter, filters[filter])
				except:
					filtersText += "%s=%s AND " % (filter, filters[filter])

		command = command.replace("WHERE", "WHERE %s " % filtersText.rstrip("AND "))

		cursor = self.model.execute(command, giveCursor=True)
		purchase = cursor.fetchone()
		cursor.close()

		if purchase:
			purchase['documents'] = [{
				'id':id,
				'kind'     :{'code':purchase['docs_kind_code'][index]},
				'number'   :purchase['docs_number'][index],
				'date'     :purchase['docs_date'][index],
				'rol_id'   :purchase['docs_rol_id'][index],
				'subtotal' :purchase['docs_subtotal'][index],
				'discount' :purchase['docs_discount'][index],
				'discountpercent':purchase['docs_discountpercent'][index],
				'tax'      :purchase['docs_tax'][index],
				'taxpercent':purchase['docs_taxpercent'][index],
				'total'    :purchase['docs_total'][index],
				'status'   :purchase['docs_status'][index],
				'relation' :purchase['docs_relation'][index],
				'reference':purchase['docs_reference'][index],
			} for index, id in enumerate(purchase['docs_id'])]

			purchase.pop('docs_id')
			purchase.pop('docs_kind_code')
			purchase.pop('docs_number')
			purchase.pop('docs_date')
			purchase.pop('docs_rol_id')
			purchase.pop('docs_subtotal')
			purchase.pop('docs_discount')
			purchase.pop('docs_discountpercent')
			purchase.pop('docs_tax')
			purchase.pop('docs_taxpercent')
			purchase.pop('docs_total')
			purchase.pop('docs_status')
			purchase.pop('docs_relation')
			purchase.pop('docs_reference')

		return purchase


	def updateProductData(self, document):
		# print "\n    purchases.model.updateProductData()"
		f=g
		# print document
		# print items

		#! Esta rutina existe tanien en el package documents, checar dónde debe quedar finalmente

		try:
		# if True:

			for item in document['items']:
				product = item.pop('product')
				# print product

				documentDiscountP = document['discount'] / document['subtotal'] * 100

				newCost = item['price'] * (100-item['discountf'])/100 * (100-documentDiscountP)/100

				newMeanCost = ( product['current'] * product['meancost'] + item['quantity'] * newCost ) / ( product['current'] + item['quantity'] ).quantize(Decimal('0.0001'))

				## Cost / Mean Cost deviation
				costDeviationP = ( newCost - newMeanCost ) / newCost * 100

				newCurrent = product['current'] + item['quantity']

				## Get Product data Modifications
				modifiedProduct = {}
				modifiedProduct['current'] = newCurrent

				if product['meancost'] != newMeanCost:
					modifiedProduct['meancost'] = newMeanCost

				## Get Product Price Modifications
				if self.recalculatePriceOnPurchase():
					# print "    Recalculating Price ..."

					priceDeviationMarginP = Decimal(self.model.getAttribute(category=u'system', name=u'margenDeCambio', cast_='product')['value'])
					sentido = self.model.getAttribute(category=u'system', name=u'sentidoDeCambio', cast_='product')['value']

					attributes = []

					for price in product['prices']:
						attribute = {}
						netMargin = ((100 + product['margin']) * (100 + Decimal(price['factor1'])) / 100 * (100 - Decimal(price['factor2'])) / 100) - 100
						## Apply cost deviation
						## Act on deviation bigger than 5%, newMeanCost = newCost - 5%
						if costDeviationP > Decimal('5'):
							newPrice = (newCost * Decimal('0.95')) * (100 + item['taxf']) / 100 * (100 + document['taxpercent']) / 100 * (100 + netMargin) / 100
						else:
							newPrice = newMeanCost * (100 + item['taxf']) / 100 * (100 + document['taxpercent']) / 100 * (100 + netMargin) / 100

						if sentido == u'+/-':
							if Decimal(price['value']) * (100 + priceDeviationMarginP) / 100 < newPrice < Decimal(price['value']) * (100 - priceDeviationMarginP) / 100:
								attribute['value'] = "%s" % newPrice
								# self.model.setProductAttribute(id=price['id'], value="%s" % newPrice)
						elif sentido == u'+':
							if newPrice > Decimal(price['value']) * (100 + priceDeviationMarginP) / 100:
								attribute['value'] = "%s" % newPrice
								# self.model.setProductAttribute(id=price['id'], value="%s" % newPrice)

						if attribute:
							attribute['id'] = price['id']
							attributes.append(attribute)

					if attributes:
						modifiedProduct['attributes'] = attributes

				## Get Aception modifications

				modifiedAception = {}
				aception = [x for x in product['aceptions'] if x['rol_id'] == document['rol_id']][0]

				# print 9998, aception
				# print 996, item

				if aception['cost'] != item['price']:
					modifiedAception['cost'] = item['price']

				if aception['individualdiscount'] != item['discountf']:
					modifiedAception['individualdiscount'] = item['discountf']

				if aception['generaldiscount'] != document['discountpercent']:
					modifiedAception['generaldiscount'] = document['discountpercent']

				if modifiedAception:
					modifiedAception['id'] = aception['id']
					# self.model.setAception(**modifiedAception)
					modifiedProduct['aceptions'] = [modifiedAception]

				# item['product'] = modifiedProduct

				if modifiedProduct:
					modifiedProduct['id'] = product['id']

					self.model.setProduct(**modifiedProduct)

		except:
			raise Exception("purchases.model.updateProductData()\n    {}".format(sys.exc_info()[1]))


	def getSuppliers(self):
		suppliers = self.model.rols_full_pull(kind='proveedor', order='name')

		global __supplierCount
		__supplierCount = len(suppliers)

		return suppliers


	def initDb(self):
		# print("""\n    purchases.model.initDb()""")

		processes.Model.initDb(self)

		try:
			version = int(self.model.getOne('attributes', code=12001)['value'])
		except:
			self.createDb()
			print ("    Initializing purchases data")
			version = 0

		"""
		12000-12999 Purchases ---------

		  000-  099     Process generals
		   01               databaseVersion
		   05               recalcularPreciosAlComprar
		   tegory='system', name='lastSync', cast_=self.cnt.cast)

		  100-  199     Process kinds
		   13               mercancía       -1       1
		   15               gasto           -1      -1
		   17               equipamiento    -1       0
		  200-  299     Rol kinds
		   13               purchaser
		   15               supplier

		  300-  499

		  500-  699     documentKind
		   13               order
		   15               receipt
		   17               invoice

		  700-  999     documentNumber
		   13               order
		   15               receipt
		   17               invoice
		"""

		if version < 3:

			employee = self.model.getOne('attributes', category=u'rolKind', name='employee')

			registros = [
				[12001, u'system', 		u'databaseVersion', u'0',  	u''],

				[12005, u'system',		u'recalcularPreciosAlComprar', u'0', u''],

				[12009, u'system', 		u'lastSync', 	u'',		u''],

				[12041, u'processFase', u'order',   	u'', 		u''],
				[12043, u'processFase', u'invoice', 	u'', 		u''],
				[12045, u'processFase', u'pay',     	u'', 		u''],
				[12047, u'processFase', u'cancel',  	u'', 		u''],

				[12113, u'processKind', u'Mercancía',    u'1',      u''],
				[12115, u'processKind', u'Gasto',        u'-1',     u''],
				[12117, u'processKind', u'Equipamiento', u'0',      u''],
				[12100, u'processKind', u'default',      u'12113',  u''],

				[12213, u'rolKind',     u'purchaser', 	employee['code'], u''],
				[12215, u'rolKind',     u'supplier',  	u'',      	u''],

				[12513, u'documentKind', u'Order',    	u'',        u'order'],
				[12515, u'documentKind', u'Receipt',  	u'',        u'formalize'],
				[12517, u'documentKind', u'Invoice',  	u'default', u'formalize'],

				[12713, u'documentNumber', u'', 		u'000',   	u'12513'],
				[12715, u'documentNumber', u'', 		u'000',   	u'12515'],
				[12717, u'documentNumber', u'', 		u'000',   	u'12517']
			]

			for registro in registros:
				data = {'code':registro[0], 'category':registro[1], 'name':registro[2], 'value':registro[3], 'reference':registro[4], 'cast_':'purchase'}
				self.model.set('attributes', **data)

			version = 3
			self.model.set('attributes', code=12001, value=version)
			print ("            Applied version {}".format(version))


		if version < 4:
			## This introduces a mayor change in the way general document
			## data is managed.
			## For purchases case general document data will still be
			## contained in range 12500-12999, only now instead of having
			## zones separated by attribute kind, there will be a small
			## range of continuos registers to each document kind.
			## Ranges will be selected so it won't interfere with
			## present setup.

			registros = [
				[12520, u'document', u'kind',   u'receipt', u'-1'],
				[12521, u'document', u'number', u'13861',   u'12520'],
				[12522, u'document', u'path',   u'',        u'12520'],

				[12540, u'document', u'kind',   u'invoice', u'-1'],
				[12541, u'document', u'number', u'0',       u'12540'],
				[12542, u'document', u'path',   u'',        u'12540'],

				[12560, u'document', u'kind',   u'order',   u'0'],
				[12561, u'document', u'number', u'040',     u'12560'],
				[12562, u'document', u'path',   u'choose D:/Dropbox/2.Nuevo Japon/proveedores',        u'12560']
			]

			for registro in registros:
				data = {'code':registro[0], 'category':registro[1], 'name':registro[2], 'value':registro[3], 'reference':registro[4], 'cast_':'purchase'}
				self.model.set('attributes', **data)

			version = 4
			self.model.set('attributes', code=12001, value=version)
			print ("            Applied version {}".format(version))


		if version > 4:
			print (u"        LA BASE DE DATOS DEL MÓDULO purchases ES UNA VERSION MÁS RECIENTE QUE LA REQUERIDA (3)\nTAL VEZ EL SISTEMA NO FUNCIONE ADECUADAMENTE")

		# print("""    purchases data initialized""")

		# print("""    purchases.model.initDb() - END""")


	# def createDb(self):
		# pass







	def elimina(**filtros):
		f=g
		registro = session().query(Documento).filter(Documento.documento_id==filtros['id']).one()
		session().delete(registro)
		session().commit()






if __name__ == "__main__":
	print ("Test routine not implemented for purchases.model")

