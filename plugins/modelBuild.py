__author__      =   "HarshaRani"
__credits__     =   ["Upi Lab"]
__license__     =   "GPL3"
__version__     =   "1.0.0"
__maintainer__  =   "HarshaRani"
__email__       =   "hrani@ncbs.res.in"
__status__      =   "Development"
__updated__     =   "Apr 11 2018"

import moose
from kkitQGraphics import * 
from kkitOrdinateUtil import *
from kkitUtil import *
import PyQt5
from setsolver import *

def updateCompartmentSize(qGraCompt):
    #childBoundingRect = qGraCompt.childrenBoundingRect()
    childBoundingRect = calculateChildBoundingRect(qGraCompt)
    comptBoundingRect = qGraCompt.boundingRect()
    rectcompt = comptBoundingRect.united(childBoundingRect)
    comptPen = qGraCompt.pen()
    comptWidth =  1
    comptPen.setWidth(comptWidth)
    qGraCompt.setPen(comptPen)
    if not comptBoundingRect.contains(childBoundingRect):
        qGraCompt.setRect(rectcompt.x()-comptWidth,rectcompt.y()-comptWidth,rectcompt.width()+(comptWidth*2),rectcompt.height()+(comptWidth*2))
    
# def checkCreate(string,num,itemAt,qGraCompt,modelRoot,scene,pos,posf,view,qGIMob):
def checkCreate(scene,view,modelpath,mobj,string,ret_string,num,event_pos,layoutPt):
    # The variable 'compt' will be empty when dropping cubeMesh,cyclMesh, but rest it shd be
    # compartment
    # if modelpath.find('/',1) > -1:
    #     modelRoot = modelpath[0:modelpath.find('/',1)]
    # else:
    #     modelRoot = modelpath
    if moose.exists(modelpath+'/info'):
        mType = moose.Annotator((moose.element(modelpath+'/info'))).modeltype
    itemAtView = view.sceneContainerPt.itemAt(view.mapToScene(event_pos),QtGui.QTransform())
    pos = view.mapToScene(event_pos)
    modelpath = moose.element(modelpath)
    if num:
        string_num = ret_string+str(num)
    else:
        string_num = ret_string
    if string == "CubeMesh" or string == "CylMesh":
        if string == "CylMesh":
            mobj = moose.CylMesh(modelpath.path+'/'+string_num)
        else:    
            mobj = moose.CubeMesh(modelpath.path+'/'+string_num)
        
        mobj.volume = 1e-15
        mesh = moose.element(mobj.path+'/mesh')
        qGItem = ComptItem(scene,pos.toPoint().x(),pos.toPoint().y(),100,100,mobj)
        qGItem.setPen(QtGui.QPen(QtGui.QColor(66,66,66,100), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        view.sceneContainerPt.addItem(qGItem)
        #qGItem.cmptEmitter.connect(qGItem.cmptEmitter,QtCore.SIGNAL("qgtextPositionChange(PyQt_PyObject)"),layoutPt.positionChange1)
        #qGItem.cmptEmitter.connect(qGItem.cmptEmitter,QtCore.SIGNAL("qgtextItemSelectedChange(PyQt_PyObject)"),layoutPt.objectEditSlot)
        compartment = qGItem
        layoutPt.qGraCompt[mobj]= qGItem
        #self.view.dropped.connect(self.pictureDropped)
        #view.dropped.emit(mobj)
        #self.dropped.emit(mobj)
        #view.emit(QtCore.SIGNAL("dropped"),mobj)
        #view.dropped.emit(mobj)
        #qGItem.cmptEmitter.dropped(mobj)
        #qGItem.cmptEmitter.qgdropped.connect(layoutPt.objectEditSlot)#.emit(mobj)
        #view.dropped.cmptEmitter(layoutPt.objectEditSlot)
        #view.emit.dropped(mobj)
        compt = layoutPt.qGraCompt[moose.element(mobj)]
        #updateCompartmentSize(compt)
        #setupItem(modelpath.path,layoutPt.srcdesConnection)
        #view.emit.resizeEvent()
        view.fitInView(view.sceneContainerPt.itemsBoundingRect().x()-10,view.sceneContainerPt.itemsBoundingRect().y()-10,view.sceneContainerPt.itemsBoundingRect().width()+20,view.sceneContainerPt.itemsBoundingRect().height()+20,Qt.IgnoreAspectRatio)
    elif string == "Pool" or string == "BufPool":
        #getting pos with respect to compartment otherwise if compartment is moved then pos would be wrong
        posWrtComp = (itemAtView.mapFromScene(pos)).toPoint()
        if string == "Pool":
            poolObj = moose.Pool(mobj.path+'/'+string_num)
        else:
            poolObj = moose.BufPool(mobj.path+'/'+string_num)    
        
        poolinfo = moose.Annotator(poolObj.path+'/info')
        #Compartment's one Pool object is picked to get the font size
        
        qGItem = PoolItem(poolObj,itemAtView)
        layoutPt.mooseId_GObj[poolObj] = qGItem
        posWrtComp = (itemAtView.mapFromScene(pos)).toPoint()
        bgcolor = getRandColor()
        qGItem.setDisplayProperties(posWrtComp.x(),posWrtComp.y(),QtGui.QColor('green'),bgcolor)
        poolinfo.color = str(bgcolor.getRgb())
        #view.emit(QtCore.SIGNAL("dropped"),poolObj)
        view.dropped.emit(poolObj)
        setupItem(modelpath.path,layoutPt.srcdesConnection)
        layoutPt.drawLine_arrow(False)
        x,y = roundoff(qGItem.scenePos(),layoutPt)
        poolinfo.x = x
        poolinfo.y = y
        
        #Dropping is on compartment then update Compart size
        if mobj.isA("ChemCompt"):
            compt = layoutPt.qGraCompt[moose.element(mobj)]
            updateCompartmentSize(compt)
        
    elif  string == "Reac":
        posWrtComp = (itemAtView.mapFromScene(pos)).toPoint()
        reacObj = moose.Reac(mobj.path+'/'+string_num)
        reacinfo = moose.Annotator(reacObj.path+'/info')
        qGItem = ReacItem(reacObj,itemAtView)
        qGItem.setDisplayProperties(posWrtComp.x(),posWrtComp.y(),"white", "white")
        #if mType == "new_kkit":
        # reacinfo.x = posWrtComp.x()
        # reacinfo.y = posWrtComp.y()
        layoutPt.mooseId_GObj[reacObj] = qGItem
        #view.emit(QtCore.SIGNAL("dropped"),reacObj)
        view.dropped.emit(reacObj)
        
        setupItem(modelpath.path,layoutPt.srcdesConnection)
        layoutPt.drawLine_arrow(False)
        #Dropping is on compartment then update Compart size
        if isinstance(mobj,moose.ChemCompt):
            compt = layoutPt.qGraCompt[moose.element(mobj)]
            updateCompartmentSize(compt)
        x,y = roundoff(qGItem.scenePos(),layoutPt)
        reacinfo.x = x
        reacinfo.y = y
        
    elif  string == "StimulusTable":
        posWrtComp = (itemAtView.mapFromScene(pos)).toPoint()
        tabObj = moose.StimulusTable(mobj.path+'/'+string_num)
        tabinfo = moose.Annotator(tabObj.path+'/info')
        qGItem = TableItem(tabObj,itemAtView)
        qGItem.setDisplayProperties(posWrtComp.x(),posWrtComp.y(),QtGui.QColor('white'),QtGui.QColor('white'))
        #if mType == "new_kkit":
        #tabinfo.x = posWrtComp.x()
        #tabinfo.y = posWrtComp.y()
        layoutPt.mooseId_GObj[tabObj] = qGItem
        #view.emit(QtCore.SIGNAL("dropped"),tabObj)
        view.dropped.emit(tabObj)
        
        setupItem(modelpath.path,layoutPt.srcdesConnection)
        layoutPt.drawLine_arrow(False)
        #Dropping is on compartment then update Compart size
        if isinstance(mobj,moose.ChemCompt):
            compt = layoutPt.qGraCompt[moose.element(mobj)]
            updateCompartmentSize(compt)
        x,y = roundoff(qGItem.scenePos(),layoutPt)
        tabinfo.x = x
        tabinfo.y = y
        
    elif string == "Function":
        posWrtComp = (itemAtView.mapFromScene(pos)).toPoint()
        funcObj = moose.Function(mobj.path+'/'+string_num)
        funcinfo = moose.Annotator(funcObj.path+'/info')
        #moose.connect( funcObj, 'valueOut', mobj ,'setN' )
        poolclass = ["ZombieBufPool","BufPool"]
        comptclass = ["CubeMesh","cyclMesh"]

        if mobj.className in poolclass:
            funcParent = layoutPt.mooseId_GObj[element(mobj.path)]
        elif mobj.className in comptclass:
            funcParent = layoutPt.qGraCompt[moose.element(mobj)]
            posWrtComp = funcParent.mapFromScene(pos).toPoint()
            #posWrtComp = (itemAtView.mapFromScene(pos)).toPoint()
        elif mobj.className in "Neutral":
            funcParent = layoutPt.qGraGrp[element(mobj)]

        qGItem = FuncItem(funcObj,funcParent)
        qGItem.setDisplayProperties(posWrtComp.x(),posWrtComp.y(),QtGui.QColor('red'),QtGui.QColor('green'))
        layoutPt.mooseId_GObj[funcObj] = qGItem
        #if mType == "new_kkit":
        #funcinfo.x = posWrtComp.x()
        #funcinfo.y = posWrtComp.y()
        #view.emit(QtCore.SIGNAL("dropped"),funcObj)
        view.dropped.emit(funcObj)
        
        setupItem(modelpath.path,layoutPt.srcdesConnection)
        layoutPt.drawLine_arrow(False)
        #Dropping is on compartment then update Compart size
        mooseCmpt = findCompartment(mobj)
        if isinstance(mooseCmpt,moose.ChemCompt):
            compt = layoutPt.qGraCompt[moose.element(mooseCmpt)]
            updateCompartmentSize(compt)
        x,y = roundoff(qGItem.scenePos(),layoutPt)
        funcinfo.x = x
        funcinfo.y = y
        
    elif  string == "Enz" or string == "MMenz":
        #If 2 enz has same pool parent, then pos of the 2nd enz shd be displaced by some position, need to check how to deal with it
        posWrtComp = pos
        enzPool = layoutPt.mooseId_GObj[mobj]
        if ((mobj.parent).className == "Enz"):
            QtWidgets.QMessageBox.information(None,'Drop Not possible','\'{newString}\' has to have Pool as its parent and not Enzyme Complex'.format(newString =string),QtWidgets.QMessageBox.Ok)
            createdObj= None
        else:
            enzparent = findCompartment(mobj)
            parentcompt = layoutPt.qGraCompt[enzparent]
        if string == "Enz":
            enzObj = moose.Enz(moose.element(mobj).path+'/'+string_num)
            enzinfo = moose.Annotator(enzObj.path+'/info')
            moose.connect( enzObj, 'enz', mobj, 'reac' )
            qGItem = EnzItem(enzObj,parentcompt)
            layoutPt.mooseId_GObj[enzObj] = qGItem
            posWrtComp = pos
            bgcolor = getRandColor()
            qGItem.setDisplayProperties(posWrtComp.x(),posWrtComp.y()-40,QtGui.QColor('green'),bgcolor)
            x,y = roundoff(qGItem.scenePos(),layoutPt)
            enzinfo.x = x
            enzinfo.y = y
            enzinfo.color = str(bgcolor.name())
            enzinfo.textColor = str(QtGui.QColor('green').name())
            #if mType == "new_kkit":
            #enzinfo.x = posWrtComp.x()
            #enzinfo.y = posWrtComp.y()
        
            #enzinfo.color = str(bgcolor.name())
            e = moose.Annotator(enzinfo)
            #e.x = posWrtComp.x()
            #e.y = posWrtComp.y()
            Enz_cplx = enzObj.path+'/'+string_num+'_cplx';
            cplxItem = moose.Pool(Enz_cplx)
            cplxinfo = moose.Annotator(cplxItem.path+'/info')
            qGEnz = layoutPt.mooseId_GObj[enzObj]
            qGItem = CplxItem(cplxItem,qGEnz)
            layoutPt.mooseId_GObj[cplxItem] = qGItem
            enzboundingRect = qGEnz.boundingRect()
            moose.connect( enzObj, 'cplx', cplxItem, 'reac' )
            qGItem.setDisplayProperties(enzboundingRect.height()/2,enzboundingRect.height()-40,QtGui.QColor('white'),QtGui.QColor('white'))
            #cplxinfo.x = enzboundingRect.height()/2
            #cplxinfo.y = enzboundingRect.height()-60
            #view.emit(QtCore.SIGNAL("dropped"),enzObj)
            view.dropped.emit(enzObj)
        else:
            enzObj = moose.MMenz(mobj.path+'/'+string_num)
            enzinfo = moose.Annotator(enzObj.path+'/info')
            moose.connect(mobj,"nOut",enzObj,"enzDest")
            qGItem = MMEnzItem(enzObj,parentcompt)
            posWrtComp = pos
            bgcolor = getRandColor()
            qGItem.setDisplayProperties(posWrtComp.x(),posWrtComp.y()-30,QtGui.QColor('green'),bgcolor)
            #enzinfo.x = posWrtComp.x()
            #enzinfo.y = posWrtComp.y()
            enzinfo.color = str(bgcolor.name())
            layoutPt.mooseId_GObj[enzObj] = qGItem
            #view.emit(QtCore.SIGNAL("dropped"),enzObj)
            view.dropped.emit(enzObj)
            x,y = roundoff(qGItem.scenePos(),layoutPt)
            enzinfo.x = x
            enzinfo.y = y
        setupItem(modelpath.path,layoutPt.srcdesConnection)
        layoutPt.drawLine_arrow(False)

        #Dropping is on compartment then update Compart size
        if isinstance(enzparent,moose.ChemCompt):
            updateCompartmentSize(parentcompt)
    if view.iconScale != 1:
        view.updateScale(view.iconScale)
    
def createObj(scene,view,modelpath,string,pos,layoutPt):
    event_pos = pos
    num = 0
    ret_string = " "
    pos = view.mapToScene(event_pos)
    itemAt = view.sceneContainerPt.itemAt(pos,QtGui.QTransform())
    #itemAt(event.scenePos(), QtGui.QTransform())
    chemMesh = moose.wildcardFind(modelpath+'/##[ISA=ChemCompt]')
    deleteSolver(modelpath)
    mobj = ""

    if itemAt != None:
        pos = itemAtView = view.mapToScene(event_pos)
        itemAtView = view.sceneContainerPt.itemAt(view.mapToScene(event_pos),QtGui.QTransform())
        #itemAtView = view.sceneContainerPt.itemAt(view.mapToScene(event_pos))
        itemClass = type(itemAtView).__name__
        if ( itemClass == 'QGraphicsRectItem'):
            mobj = itemAtView.parentItem().mobj
        elif(itemClass == 'QGraphicsSvgItem'):
            mobj = itemAtView.parent().mobj
        else:
            mobj = itemAtView.mobj
    if string == "CubeMesh" or string == "CylMesh":
        ret_string,num = findUniqId(moose.element(modelpath),"Compartment",0)
        comptexist = moose.wildcardFind(modelpath+'/##[ISA=ChemCompt]')
        if not len(comptexist):
            if itemAt != None:
                QtWidgets.QMessageBox.information(None,'Drop Not possible','\'{newString}\' currently single compartment model building is allowed'.format(newString =string),QtWidgets.QMessageBox.Ok)
                return
            else:
                mobj = moose.element(modelpath)

        else:
            QtWidgets.QMessageBox.information(None,'Drop Not possible','\'{newString}\' currently single compartment model building is allowed'.format(newString =string),QtWidgets.QMessageBox.Ok)
            return
    
    elif string == "Pool" or string == "BufPool" or string == "Reac" or string == "StimulusTable":
        if itemAt == None:
            QtWidgets.QMessageBox.information(None,'Drop Not possible','\'{newString}\' has to have compartment as its parent'.format(newString =string),QtWidgets.QMessageBox.Ok)
            return
        else:
            #mobj = findCompartmentX(mobj)
            mobj = findGroup_compt(mobj)
            ret_string,num = findUniqId(mobj,string,num)

    elif string == "Function":
        #mobj = findCompartment(mobj)
        ret_string,num = findUniqId(mobj,string,num)
        '''
        if itemAt != None:
            if ((mobj).className != "BufPool"):    
                QtWidgets.QMessageBox.information(None,'Drop Not possible','\'{newString}\' has to have BufPool as its parent'.format(newString =string),QtWidgets.QMessageBox.Ok)
                return
            else:
                ret_string,num = findUniqId(mobj,string,num)
        else:
            QtWidgets.QMessageBox.information(None,'Drop Not possible','\'{newString}\' has to have BufPool as its parent'.format(newString =string),QtWidgets.QMessageBox.Ok)
            return
        '''
    elif string == "Enz" or string == "MMenz":
        if itemAt != None:
            if ((mobj).className != "Pool" and (mobj).className != "BufPool"):    
                QtWidgets.QMessageBox.information(None,'Drop Not possible','\'{newString}\' has to have Pool as its parent'.format(newString =string),QtWidgets.QMessageBox.Ok)
                return
            else:
                ret_string,num = findUniqId(mobj,string,num)
        else:
            QtWidgets.QMessageBox.information(None,'Drop Not possible','\'{newString}\' has to have Pool as its parent'.format(newString =string),QtWidgets.QMessageBox.Ok)
            return

    if ret_string != " ":
        checkCreate(scene,view,modelpath,mobj,string,ret_string,num,event_pos,layoutPt)
        
def roundoff(scenePos,layoutPt):
    xtest = scenePos.x()//layoutPt.defaultScenewidth
    xroundoff = round(xtest,1)

    ytest = scenePos.y()//layoutPt.defaultSceneheight
    yroundoff = round(ytest,1)
    
    return(xroundoff,yroundoff)

def findUniqId(mobj,string,num):
    if num == 0:
        path = mobj.path+'/'+string;
    else:
        path = mobj.path+'/'+string+str(num);
    if not moose.exists(path):
        return(string,num)
    else:
        num +=1;
        return(findUniqId(mobj,string,num))

def findCompartment2(elem):
    element = moose.element(elem)
    if element.path == '/':
        return element
    if element.isA['ChemCompt']:
        return element
    return findCompartment(element.parent)

def findCompartment1(mooseObj):
    if mooseObj.path == '/':
        return None
    elif element.isA['ChemCompt']:
        return (mooseObj)
    else:
        return findCompartment(moose.element(mooseObj.parent))
