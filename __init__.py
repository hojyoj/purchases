# -*- coding: utf-8 -*-

 ##############################################
 ##                                            ##
 ##              Purchases package              ##
 ##                                             ##
 ##                                             ##
 ##              from Basiq Series              ##
 ##           by Críptidos Digitales            ##
 ##                 GPL (c)2008                 ##
  ##                                            ##
    ##############################################

"""
"""

from __future__ import print_function

__version__ = "0.1.1"       ## Go to end for change log

import sys
import os
import copy

import logging

from decimal import Decimal
import datetime

from PyQt4 import QtCore, QtGui

import spynner

import processes

import view
import model

stOK = 0


class Controller(processes.Controller):

    _cast = 'purchase'      # Process kind
    _title = u"Compras"
    
    
    def __init__(self, *args, **kwds):
        # print("""    purchases.Controller.__init__()""")
        
        kwds['role'] = 'purchase'
        
        processes.Controller.__init__(self, *args, **kwds)

        self.initOrder = 3
        self.displayOrder = 2

        self.model = model.Model(self.app.model)

        if self.capture_mode is 1:
            self.master = view.Master(self.owner.master, cnt=self)

        # print("""    purchases.Controller.__init__() - END""")


    @property
    def activePriceRules(self):
        return self._activePriceRules


    def init(self):
        # print("""    purchases.Controller.init()""")

        self.documentKind_efectivo = self.documentKinds_pull(name=u'efectivo')[0]
        self.documentKind_cheque = self.documentKinds_pull(name=u'cheque')[0]

        self.documentKind_factura = self.documentKinds_pull(name=u'invoice', reference='formalize', cast_=self.cast)[0]
        self.documentKind_remision = self.documentKinds_pull(name=u'receipt', reference='formalize', cast_=self.cast)[0]
        
        self._activePriceRules = self.app.model.getActivePriceRules()
        
        self._purchase_documentKind_default = self.defaultDocumentKind(reference='order')

        # print("""    purchases.Controller.init() - END""")


    def make_captureView(self, document, task):
        # print("        purchases Controller.make_captureView()")
        
        captureView = view.CaptureView(master=self.master, document=document, task=task)
        self.connect(captureView, QtCore.SIGNAL("captureViewClosed()"), self.master.manager_update)
        self.master.ui.outerSplitter.insertWidget(1, captureView)
        
        # print("        purchases Controller.make_captureView() - END")

        return captureView
        

    def documents_pull(self, **kwds):
        documents = self.app.model.getDocuments(**kwds)
        return documents

    def import_(self, document_):
        # print("""\n    purchases.Controller.import_()""")
        
        filename = unicode(QtGui.QFileDialog.getOpenFileName(self.master, u"Empresa Básica - Selecciona el arhivo XML de la Factura", '/', "Facturas (*.xml)"))
        
        if filename:
            
            self.master.setCursor(QtCore.Qt.WaitCursor)
            
            self.app.model.attribute_set(category='system', name='path', cast_='purchase', value=filename)

            document, status, messages = self.app.packages['cfd'].parse(filename)
            
            # if 'subTotal' in document:
                # document['subtotal'] = document.pop('subTotal')
            ''' 
            if 'discount' in document:
                discounts = []
                discount = {}
                discount['amount'] = document.pop('discount')
                factor = document.pop('discountpercent', None)
                if factor is None:
                    factor = ( discount['amount'] / document['subtotal'] * Decimal('100')).quantize(Decimal('1'))
                discount['factor'] = factor
                
                discounts.append(discount)
                document['discounts'] = discounts
            
            
            if 'tax' in document:
                taxes = {}
                
                tax = {}
                tax['amount'] = Decimal(document.pop('tax', '0'))
                tax['factor'] = Decimal(document.pop('taxpercent', '0'))
                tax['name'] = document.pop('taxname', "")
                if tax['amount'] > Decimal('0'):
                    if tax['factor'] < Decimal('0'):
                        tax_ = self.cnt.tax_pull(name=tax['name'])
                        tax['factor'] = tax_['value']
                
                taxes['general'] = tax
                
                document['taxes'] = taxes
                
            if 'items' in document:
                for item in document['items']:
                    print ('++++', item)
                    if document['rol_id'] is None:
                        product = None
                        
                    else:
                        if 'aception_code' in item:
                            product = self.product_get(code=item['aception_code'], rol_id=document['rol_id'])
                            print ('----1', product)
                    
                        if not product:
                            product = self.product_get(name=item['aception_name'], rol_id=document['rol_id'])
                            print ('----2', product)
                        
                    if product:
                        item['product'] = product
            '''
            
            if 'rol' in document:
                
                person = {}
                if 'name' in document['rol']:
                    person['name'] = document['rol'].pop('name')
                    person['rfc'] = document['rol'].pop('rfc')
                    person['curp'] = document['rol'].pop('curp')
                    person['birthdate'] = document['rol'].pop('birthdate')
                    person['name2'] = document['rol'].pop('name2')
                    person['id'] = document['rol'].pop('person_id')
                if person:
                    document['rol']['person'] = person
        
            document_.reset()
            
            document_.kind_set( {'code':document['kind']['code'], 'name':document['kind']['name']} )
            
            document_.set_data(document)
        
            
            self.master.setCursor(QtCore.Qt.ArrowCursor)

        # print("""    purchases.Controller.import_() - END""")



    def cfdis_save(self, xmlFile):
        """ Saves xml files if not existent
        """
        self.app.stdoutLog.info("    purchases Controller.cfdis_save()")
        
        exists = False
        found = False

        path = self.app.model.attribute_get(name='storage_path', cast_='cfd')['value']

        ##    Search date and uid in filename

        date = parsed['date'].date()
        
        self.app.stdoutLog.info("    purchases Controller.cfdis_save() - END")
        
        """
                    sat = [x for x in parsed['attributes'] if x['name'] == 'SAT'][0]
                    uuid = sat['value']
                    
                    print ( 'Searching {}__{}'.format(date.strftime("%Y.%m.%d"), uuid.upper()[:8]) )
                    
                    print (9876876, os.listdir(path) )
                    
                    exists = not not [ x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x)) and '{}__{}'.format(date.strftime("%Y.%m.%d"), uuid.upper()[:8]) in x ]
                    
                    if not exists:
                        
                        ##    Search uuid in content of not formatted filenames
                        
                        filesNotFormated = [ x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x)) and ( '{}{}{}{}'.format(x[4], x[7], x[10:12], x[20:22]) != '..____' or ( '{}{}{}{}'.format(x[4], x[7], x[10:12], x[20:22]) == '..____' and x[12:20] != x[12:20].upper() ) ) ]
                        
                        print ( 'Searching {}'.format(uuid.upper()) )
                        
                        print ( filesNotFormated )
                        
                        index = 0
                        while not found and index < len(filesNotFormated):
                            
                            found = uuid.upper() in open( os.path.join(path, filesNotFormated[index]) ).read().upper()
                            
                            index += 1
                        
                        alias = parsed['rol']['person']['alias']
                        
                        if not found:
                            
                            ##    Save file with formatted name
                        
                            filename = "{}__{}__{}.xml".format(date.strftime("%Y.%m.%d"), uuid.upper()[:8], alias)
                            
                            sat['reference'] = filename
                            
                            try:
                                file = open(os.path.join(path, filename), 'w')
                            except:
                                error += self.erNoAccessToFile
                            else:
                                try:
                                    file.write(cfdi_xml)
                                    self.app.emit_signal("import_message(QString)", "Data succesfully written to {}".format(filename))
                                    print ("Data succesfully written to {}".format(filename))
                                except:
                                    # error += self.erWriteFailed
                                    self.app.emit_signal("import_message(QString)", "Could not write to {}".format(filename))
                                    print ("Write failed")
                                file.close()
                                    
                        elif found:
                        
                            filename_old = os.path.join( path, filesNotFormated[index-1] )
                            
                            filename = filesNotFormated[index-1]
                            if '{}{}'.format(filename[4], filename[7]) == '..':
                                filename = filename[12:]
                            index_ = filename.find('__') + 2
                            if index_ > 1:
                                filename = filename[index_:]
                            
                            print ( 44453, path)
                            print ( 44454, filename )
                            print ( 44455, filename_old )
                            
                            filename_new = os.path.join( path, "{}__{}__{}__{}".format( date.strftime("%Y.%m.%d"), uuid.upper()[:8], alias, filename) )
                            
                            print ( 44456, filename_new )
                            
                            os.rename( filename_old, filename_new )
                            
                            if os.path.isfile(filename_old.replace('.xml', '.pdf')):
                                
                                os.rename( filename_old.replace('.xml', '.pdf'), filename_new.replace('.xml', '.pdf') )
                            
                            #! Missing    sat['reference'] = filename_new
                    """
        

    def newCfdis_pull(self):
        """ Returns a list of Document instances not captured in the system
            from preset date range (last 15 days)
        """
        
        # oldLevel = self.app.stdoutLog.level
        # self.app.stdoutLog.setLevel(logging.INFO)
        self.app.stdoutLog.info("    purchases   Controller.newCfdis_pull()")

        cfdis = self.app.packages['cfd'].cfdis_download()

        documents = []

        for cfdi in cfdis:
            
            cfdi.pop('tipo', None)
            
            documentX = self.create_process(document_=cfdi)
            
            if documentX.kind == None:
            
                documentX.kind = self.defaultDocumentKind(reference='formalize')
            
            documents.append(documentX)
        
        documents_new = []

        for document in documents:
            
            if not document.number:
                ## Facturas que no traen folio
                document.number_set("{}".format(document.date.strftime("%Y%m%d"))) 
            
            status = "already processed"
            
            if document.state_is_stROL_CURRENT:
                existent = self.documents_pull(rol_id=document.rol['id'], number=document.number)
            else:
                existent = False

            if not existent:
                documents_new.append( document )                
                self.app.stdoutLog.info(">>>> {} Must process {}".format(documents.index(document), document.data))
            else :
                self.app.stdoutLog.info(">>>> {}".format(documents.index(document)))
        
        self.app.stdoutLog.info("    purchases   Controller.newCfdis_pull() - END")
        # self.app.stdoutLog.setLevel(oldLevel)
    
        return documents_new


    def orders_load(self, **kwds):
        self.app.stdoutLog.info("    purchases Controller.orders_load()")
        
        kwds['document kind_code'] = 12513
        
        dbProcesses = self.app.model.getProcesses(**kwds)
        
        documents = []
        for index, dbProcess in enumerate(dbProcesses):
            for document in dbProcess['documents']:
                if 'discount' in document:
                    document['discounts'] = [{'amount':document['discount'], 'factor':document['discountpercent']}]
            
            # Se asume un sólo documento tipo pedido
            order = [ x for x in self.create_process(dbProcess).process.documents if x.kind['code'] == 12513][0]
            
            documents.append(order)
        
        self.app.stdoutLog.info("    purchases Controller.orders_load() - END")
        
        return documents

    # def payment_documentKind(self, name):
        # kwds = {'category':'documentKind', 'name':name, 'cast_':'payment'}
        # return self.app.model.getAttribute(**kwds)

    # def paymentKinds(self):
        # return self.app.model.getAttributes(category='documentKind', cast_LIKE='payment')

    def productsCount(self):
        return self.app.model.getProductsCount()

    def pullData(self, xml):
        """ Receives string
        """
        
        if 'cfd' in self.app.packages:
            document = self.app['cfd'].parseFromText(xml)
        else:
            print ('cfd package missing, cannot parse purchase document')




    def process(self, **kwds):
        return self.model.getPurchase(**kwds)




    def process_save(self, **data):
        # oldLevel = self.app.stdoutLog.level
        # self.app.stdoutLog.setLevel(logging.INFO)
        self.app.stdoutLog.info("    purchases Controller.process_save()")
        
        #! status 0 asumes success
        
        try:
            ## Get order id for posterior status update to received
            orderId = data.pop('orderId', None)
        except:
            print (""">>> Error @ purchases.Controller.processs_save()""")
            print ("""    Could not process orderId\n""")
            raise


        if 'id' not in data:
            if 'kind' not in data:
                f=g
                data['kind'] = {'name':u'Mercancía'}
        
        ## Keep original documents for transaction apply
        # documentsTmp = copy.deepcopy(data['documents'][:])
        
        
        self.app.model.startTransaction()

        try:
            process = self.app.model.setProcess(**data)
        except:
            print ("ERROR @ purchases.model.process_save():: self.app.model.setProcess()")
            print (data)
            print (sys.exc_info())
            
            self.app.model.rollback()
        
        try:
            ## Update order status
            if orderId:
                self.app.model.setDocument(id=orderId, status='received')
        except:
            print ("ERROR @ purchases.model.setPurchase():: self.app.model.setDocument()")
            print (orderId)
            print (sys.exc_info())
            
            self.app.model.rollback()
        
        # try:
            # Update Product data (prices and aceptions may change)
            # for document in [x for x in [x for x in documentsTmp if 'kind' in x.keys()] if x['kind']['code'] in [12515, 12517]]:        # remisión, factura
                # self.app.model.transaction_apply(u'Mercancía', document)
        # except:
            # print ("ERROR @ purchases.model.setPurchase():: self.app.model.transaction_apply()")
            # print (document)
            # print (sys.exc_info())
            # self.app.model.rollback()
        
        self.app.model.endTransaction()
            
        self.app.stdoutLog.info("    purchases Controller.process_save() - END")
        # self.app.stdoutLog.setLevel(oldLevel)
        
        return process


    def product_get(self, **filters):
        product = self.app.model.product_full_pull(**filters)
        return product
        
        
    # def setPurchase(self, **kwds):
        # return self.model.setPurchase(**kwds)


    def purchasesCount(self):
        return self.model.count('processes', kind_code=12113)


    def origin(self, **kwds):
        return self.app.model.rol_full_pull(**kwds)

    def suppliers(self, **kwds):
        kwds['kind'] = 'supplier'
        if 'goodKinds' in kwds:
            kwds['goodKinds'] = kwds['goodKinds'].replace(u'Mercancía', 'goods')
            kwds['goodKinds'] = kwds['goodKinds'].replace(u'Equipamiento', 'supplies')
            kwds['goodKinds'] = kwds['goodKinds'].replace(u'Gasto', 'services')
    
        return self.app.model.rols_full_pull(order='name', **kwds)

    def tax_pull(self, **kwds):
        kwds['category'] = 'tax'
        kwds['cast_'] = 'system'
        tax = self.app.model.getAttribute(**kwds)
        return tax
        
    def taxes(self):
        taxes = self.app.model.getAttributes(category=u'tax')
        return taxes

    
    # def translate(self, text, plural=False):
        # if plural:
            # return u"{}".format(self.app.translate(None, text, '', QtCore.QCoreApplication.UnicodeUTF8, 2))
        # else:
            # return u"{}".format(self.app.translate(None, text, '', QtCore.QCoreApplication.UnicodeUTF8, 1))



if __name__ == "__main__":

    app = MyApp(sys.argv)
    app.setQuitOnLastWindowClosed(True)


    sys.exit(app.exec_())



"""
  ~~~~~~  Change log  ~~~~~~

        v0.1.1
    2014.07.29  Implementing Pull data from XML electronic document


    Al agregar una compra

    Si existe un proceso relacionado (por el folio de pedido), se agrega
        el documento de compra a ese proceso, si no existe se crea.

    Se actualiza el ultimoFolio de compra en los registros.

    Se consolida el inventario sumando las entradas al inventario
        existente

    Restricciones
        Los folios son únicos

    Restricciones configurables (Activadas por default)
        Un solo pedido por proceso
        Una solo compra por proceso
        Una sola compra por pedido


  ~~~~~~  NOTES  ~~~~~~
    
    USE CASE 1
    Las facturas de Telmex no traen folio, se generaliza y para las
    facturas que no traen folio, se usa la fecha como tal.
  

  =================================================
    Lógica para el manejo de acepciones [20 Abr 2010]

    La captura de acepciones evitará modificar datos ya existentes.

    Se llevarán dos registros de las acepciones capturadas, uno para las
        capturadas por acepción local, y otro para las capturadas por
        acepción de proveedor.

    Las partidas del documento guardan sólo las referencias a las
        acepciones del proveedor, no los textos, por lo que no se podrán
        utilizar acepciones temporales o por evento.

    Si un artículo no cuenta con una acepción del proveedor, la rutina
        de registro la creará a partir de los textos recibidos, esta es
        la única modificación que se podrá realizar.

    En los widgets de captura, la selección de un artículo se puede
        realizar mediante cualquier acepción registrada, cualquiera.

    Independientemente del origen que se haya seleccionado, se
        identifica el producto y se guardan los textos de la acepción
        local.

    En caso de que se haya seleccionado un proveedor para el documento,
        se busca la acepción para ese proveedor, si existe, se guarda, y
        es la que se muestra, si no existe, se guarda los textos de la
        acepción que se utilizó para identificar el artículo, y serán
        los que se usarán para crear la acepción para el proveedor
        seleccionado.

    #!
    Si no existe acepción para un artículo capturado, se deberá permitir
        la modificación de los textos, para que se cree la acepción con
        los textos adecuados.

"""
