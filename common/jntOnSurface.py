import maya.cmds as cmds
import pymel.core as pm
#createPointOnSurfaceLoc('nurbsPlane1',parameterU=.3,parameterV=.3,parent=None,name='aa')


class JntOnSurface():
            
    def show(self):
        if cmds.window("createJointOnSurface", q = 1, ex = 1):
            cmds.deleteUI("createJointOnSurface", window = 1) 
        window = cmds.window("createJointOnSurface",title="createJointOnSurface", s = 1,wh = [200,100])
        cmds.columnLayout( adjustableColumn=True )
        cmds.text(label = "U && V count:                                                                            ")
        cmds.text(l =  "", h = 4)
        cmds.columnLayout(adjustableColumn=1)
        self.UcountTFG = cmds.intFieldGrp("UcountTFG", label = "U count:", v1 = 5, columnWidth2 =[70, 70])
        cmds.text(l =  "", h = 4)
        self.VcountTFG = cmds.intFieldGrp("VcountTFG", label = "V count:", v1 = 1, columnWidth2 =[70, 70])
        cmds.text(l =  "", h = 4)
        
        cmds.button( h = 50, l = "Create!!!", c = lambda *arg:self.create(), bgc = [0.675, 0.663, 0.843])
        
        cmds.text(l =  "", h = 4)
        cmds.text('select jnt and surface ',h=20)
        cmds.button( h = 50, l = "Pin sel to surface", c = lambda *arg:self.pinSelTosurface(), bgc = [0.675, 0.663, 0.843])
        cmds.text('select follicle ',h=20)
        cmds.button( h =30, l = "keeepLenSetting!!!", c = lambda *arg:self.keeepLenSetting(), bgc = [0.60, 0.8, 0.80])
        cmds.setParent("..");
        
        cmds.setParent( '..' )
        cmds.showWindow( window )

    def createJointOnSurface(self,type='joint', Ucount=5, Vcount=5):
        selectObj = cmds.ls(sl=True)
        for i in selectObj:
            allFollicNUL = cmds.createNode('transform',n=(i+'FollicNUL'))
            allTypeNUL = cmds.createNode('transform',n=(i+type+'NUL'))
            surfaceShape = cmds.listRelatives(selectObj,s=True)
            for u in range(Ucount):
                for v in range(Vcount):
                    parameterU = 0.5
                    parameterV = 0.5
                    if Ucount > 1:
                        parameterU = float(u)/(Ucount-1)
                    if Vcount > 1:
                        parameterV = float(v)/(Vcount-1.0)
                    u = str(u)
                    v = str(v)
                    print('U_V',u,v)
                    #FollicleShapeTransform = cmds.createNode('transform', n=(i+'_'+u+'_'+v+'_Follicle'))
                    #FollicleShape = cmds.createNode('follicle',n=(i+'_'+u+'_'+v+'_FollicleShape'),p=FollicleShapeTransform)
                    #cmds.connectAttr((surfaceShape[0]+'.worldMatrix'), (FollicleShapeTransform+'.inputWorldMatrix'))
                    #cmds.connectAttr((surfaceShape[0]+'.local'), (FollicleShapeTransform+'.inputSurface'))
                    #cmds.connectAttr((FollicleShape+'.outTranslate'), (FollicleShapeTransform+'.translate'))
                    #cmds.connectAttr((FollicleShape+'.outRotate'), (FollicleShapeTransform+'.rotate'))
                    #cmds.setAttr(FollicleShape+'.parameterU',parameterU)
                    #cmds.setAttr(FollicleShape+'.parameterV',parameterV)
                    #cmds.parent(FollicleShapeTransform,allFollicNUL)
                    
                    FollicleShapeTransform = self.createPointOnSurfaceLoc(i,parameterU=parameterU,parameterV=parameterV,parent=allFollicNUL,name=(i+'_'+u+'_'+v+'_loc'))
                    
                    typeObj = cmds.createNode(type,n=(i+'_'+u+'_'+v+'_'+type))
                    #objRo = cmds.xform(FollicleShapeTransform, q = True, ro = True, ws = 1)
                    objTr = cmds.xform(FollicleShapeTransform, q = True, m = True, )
                    #cmds.xform(typeObj, ro = objRo)
                    cmds.xform(typeObj, m = objTr)
                    
                    #pm.matchTransform(typeObj,FollicleShapeTransform)
                    cmds.parent(typeObj,allTypeNUL)
                    cmds.parentConstraint(FollicleShapeTransform, typeObj,mo=1)

    def keeepLenSetting(self, follicle=None,sampleSur='',sur='',par=''):
            sel = pm.ls(sl=True)
            if not sel:
                print ('ple select folli')
                #return
            pm.select(cl=1)
            if follicle:
                sel = follicle
            print (sel)
            uvs = []
            pps = []
            jnts = []
            for j,s in enumerate(sel) :
                uv = (s.parameterU.get(),s.parameterV.get())
                p = pm.xform(s,q=1,t=1,ws=1)
                uvs.append(uv)
                pps.append(p)
                jnt = pm.joint(p=p,n='{}_{}_chain_jnt'.format(s,j))
                if j !=0:
                    #joint -e -zso -oj xyz -sao yup joint2;
                    pm.joint(jnts[j-1],e=1,zso=1,oj='xyz',sao='yup')
                jnts.append(jnt)
            
            if not sur:
                #sur = sel[0].getShape().inputSurface.inputs()[0]
                posi = sel[0].parameterU.outputs()[0]
                sur = posi.inputSurface.inputs()[0]
            else:
                sur = pm.PyNode(sur).getShape()
                
            if not sampleSur:
                sampleSur = sur

            #crv = cmds.curve( d=3, p=pps ,n=sur+'_crv')
            crv = pm.duplicateCurve("{}.v[0.5]".format(sampleSur), ch=1, rn=0, local=0,n=sur+'_crv' )[0]
            ikHandel = cmds.ikHandle( sj=jnts[0].name(), ee=jnts[-1].name(),c=crv, sol='ikSplineSolver',ccv=False, pcv= False,n='{}_{}_chain_ikHandel'.format(s,j))
            print (ikHandel)

            for i,jnt in enumerate(jnts):
                loc = pm.createNode('locator',p=jnt,n='{}_{}_loc'.format(jnt,i))
                loc.v.set(0)
                
                cpos = pm.createNode('closestPointOnSurface',n='{}_{}_cpos'.format(jnt,i))
                loc.worldPosition >> cpos.inPosition
                sur.worldSpace >> cpos.inputSurface
                cpos.parameterU >> sel[jnts.index(jnt)].parameterU
            grp = pm.createNode('transform',n='{}_keeepLenSetting_grp'.format(sur.name()),p=par)
            grp.v.set(0)
            pm.parent(ikHandel[0],jnts[0],crv,grp)
            return jnts,crv,ikHandel,grp
                    
    def pinSelTosurface(self):
        sel = pm.ls(sl=1)
        if len(sel) <2 or sel[-1].getShape().nodeType() !='nurbsSurface':
            return 'select nothing'
        
        shape = sel[-1].getShape()
        allFollicNUL = pm.createNode('transform',n=(sel[-1]+'_loc_grp'))
        scaleNUl = pm.createNode('transform',n=(sel[-1]+'_scale_nul'))
        cpos = pm.createNode('closestPointOnSurface',n='TEMP_cpos')
        #loc.worldPosition >> cpos.inPosition
        shape.worldSpace >> cpos.inputSurface
        for i,jnt in enumerate(sel[0:-1]):

                pos = pm.xform(jnt,q=1,ws=1,t=1)
                cpos.inPosition.set(pos)
                parameterU = cpos.parameterU.get()
                parameterV = cpos.parameterV.get()
                
                loc = self.createPointOnSurfaceLoc(sel[-1],parameterU=parameterU,parameterV=parameterV,
                                                    parent=allFollicNUL,name=('{}_{}_loc'.format(sel[-1],i)))
                
                scaleNUl.s >> pm.PyNode(loc).s
                nul =  pm.createNode('transform',name='{}_{}_nul'.format(sel[-1],i),p=loc)
                pm.parentConstraint(nul,jnt,mo=1)
                pm.scaleConstraint(nul,jnt,mo=1)
        
        pm.delete(cpos)
        
        
    def pinJntsTosurface(self,jnt_list=None,surface=None):
        sel = jnt_list
        
        shape = pm.PyNode(surface).getShape()
        allFollicNUL = pm.createNode('transform',n=(sel[-1]+'_loc_grp'))
        scaleNUl = pm.createNode('transform',n=(sel[-1]+'_scale_nul'))
        cpos = pm.createNode('closestPointOnSurface',n='TEMP_cpos')
        #loc.worldPosition >> cpos.inPosition
        shape.worldSpace >> cpos.inputSurface
        for i,jnt in enumerate(sel):

                pos = pm.xform(jnt,q=1,ws=1,t=1)
                cpos.inPosition.set(pos)
                parameterU = cpos.parameterU.get()
                parameterV = cpos.parameterV.get()
                
                loc = self.createPointOnSurfaceLoc(sel[-1],parameterU=parameterU,parameterV=parameterV,
                                                    parent=allFollicNUL,name=('{}_{}_loc'.format(sel[-1],i)))
                
                scaleNUl.s >> pm.PyNode(loc).s
                nul =  pm.createNode('transform',name='{}_{}_nul'.format(sel[-1],i),p=loc)
                pm.parentConstraint(nul,jnt,mo=1)
                pm.scaleConstraint(nul,jnt,mo=1)
        
        pm.delete(cpos)
    
    
    def createPointOnSurfaceLoc(self,sur,parameterU=0,parameterV=0,parent=None,name=None):
            sur = pm.PyNode(sur)
            surfaceShape = sur.getShape()

            u = str(parameterU)
            v = str(parameterV)

            locator = pm.createNode('transform', n=name,p=parent)
            locShape = pm.createNode('locator', n=name+'Shape',p=locator)

            pointOnSurfaceInfo = pm.createNode('pointOnSurfaceInfo',n=name+'_pointOnSurfaceInfo')
            fourByFourMatrix = pm.createNode('fourByFourMatrix',n=name+'_fourByFourMatrix')
            decomposeMatrix = pm.createNode('decomposeMatrix',n=name+'_decomposeMatrix')

            #pointOnSurfaceInfo.parameterU.set(parameterU)
            #pointOnSurfaceInfo.parameterV.set(parameterV)
            
            pm.addAttr(locator,ln='parameterU',k=1)
            pm.addAttr(locator,ln='parameterV',k=1)
            
            locator.parameterU.set(parameterU)
            locator.parameterV.set(parameterV)

            locator.v.set(0)
            locator.rotateAxis.set(180,0,90)

            locator.parameterU >> pointOnSurfaceInfo.parameterU
            locator.parameterV >> pointOnSurfaceInfo.parameterV

            surfaceShape.worldSpace >> pointOnSurfaceInfo.inputSurface
            
            pointOnSurfaceInfo.normalX >> fourByFourMatrix.in00
            pointOnSurfaceInfo.normalY >> fourByFourMatrix.in01
            pointOnSurfaceInfo.normalZ >> fourByFourMatrix.in02
            
            pointOnSurfaceInfo.tangentUx >> fourByFourMatrix.in10
            pointOnSurfaceInfo.tangentUy >> fourByFourMatrix.in11
            pointOnSurfaceInfo.tangentUz >> fourByFourMatrix.in12
            
            pointOnSurfaceInfo.tangentVx >> fourByFourMatrix.in20
            pointOnSurfaceInfo.tangentVy >> fourByFourMatrix.in21
            pointOnSurfaceInfo.tangentVz >> fourByFourMatrix.in22

            pointOnSurfaceInfo.positionX >> fourByFourMatrix.in30
            pointOnSurfaceInfo.positionY >> fourByFourMatrix.in31
            pointOnSurfaceInfo.positionZ >> fourByFourMatrix.in32

            fourByFourMatrix.output >> decomposeMatrix.inputMatrix

            decomposeMatrix.outputTranslate >> locator.translate
            decomposeMatrix.outputRotate >> locator.rotate

            
            return locator.name()
    
    def create(self):
        Ucount = int(cmds.intFieldGrp("UcountTFG", q = True, v1 = True))
        Vcount = int(cmds.intFieldGrp("VcountTFG", q = True, v1 = True))
        self.createJointOnSurface('joint', Ucount, Vcount)
    


UI = JntOnSurface()
UI.show()