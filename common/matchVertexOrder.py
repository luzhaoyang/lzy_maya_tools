

import maya.mel as mel
import pymel.core as pm

import maya.api.OpenMaya as om
import maya.cmds as cmds

def getClosestVertex(mayaMesh,pos=[0,0,0]):
    mVector = om.MVector(pos)#using MVector type to represent position
    selectionList = om.MSelectionList()
    selectionList.add(mayaMesh)
    dPath= selectionList.getDagPath(0)
    mMesh=om.MFnMesh(dPath)
    ID = mMesh.getClosestPoint(om.MPoint(mVector),space=om.MSpace.kObject)[1] #getting closest face ID
    list=cmds.ls( cmds.polyListComponentConversion (mayaMesh+'.f['+str(ID)+']',ff=True,tv=True),flatten=True)#face's vertices list
    #setting vertex [0] as the closest one
    d=mVector-om.MVector(cmds.xform(list[0],t=True,os=True,q=True))
    smallestDist2=d.x*d.x+d.y*d.y+d.z*d.z #using distance squared to compare distance
    closest=list[0]
    #iterating from vertex [1]
    for i in range(1,len(list)) :
        d=mVector-om.MVector(cmds.xform(list[i],t=True,os=True,q=True))
        d2=d.x*d.x+d.y*d.y+d.z*d.z
        if d2<smallestDist2:
            smallestDist2=d2
            closest=list[i]      
    return closest


def matchVertexOrder():
    '''
    first select a face of sample mesh, 
    '''
    
    #cmds.selectPref(tso=True)
    sel = pm.ls(orderedSelection=1)

    if len(sel) < 2 :
        return 
    
    
    index = sel[0].getVertices()
    
    sam = ['{}.vtx[{}]'.format(sel[0]._node.name(),x) for x in index[:3]]
    
    for s in sel[1:]:
        mayaMesh = s.name()

        tar = []
        for sa in sam:
            v = pm.PyNode(sa).getPosition()
            pos = [v[0],v[1],v[2]]
            tar.append(getClosestVertex(mayaMesh,pos))
        
        print sam,tar
        #meshRemap pPlaneShape2.vtx[2] pPlaneShape2.vtx[3] pPlaneShape2.vtx[1] pPlaneShape1.vtx[0] pPlaneShape1.vtx[2] pPlaneShape1.vtx[3];

        mel_cmd = 'meshRemap {} {} {} {} {} {};'.format(sam[0],sam[1],sam[2],tar[0],tar[1],tar[2])
        mel.eval(mel_cmd)
        
matchVertexOrder()       

