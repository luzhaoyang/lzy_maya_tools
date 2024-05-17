import pymel.core as pm


def limitInfluence(skin,num=4,mode='toParent'):
    '''
    mode:
        'toParent'
        'average'
        'toMax'
    '''

    skin =pm.PyNode(skin)
    inf_list = skin.getInfluence()
    inf_index_list  = skin.lw.get(mi=1)
    #vtxs = pm.ls(sl=1,fl=1)
    skin.wl.get(mi=1)
    info = {}

    for vtx_i in skin.wl.get(mi=1):    
        jnt_list = skin.wl[vtx_i].w.get(mi=1)
        w_list = list(skin.wl[vtx_i].w.get())
        
        if not jnt_list:
            continue
        exr = len(jnt_list) -num
        if exr:
            for i in range(exr):
                _k = w_list.index(min(w_list))
                jnt = inf_list[inf_index_list.index(jnt_list[w_list.index(min(w_list))])]
                
                if mode == 'average':
                    sw =  w_list[_k]/(len(w_list)-1)
                    w_list[_k] = 0
                    jnt_list.remove(jnt_list[_k])
                    w_list.remove(w_list[_k])
                    
                    for iw,ww in enumerate(w_list):
                        w_list[iw] = ww+sw
                elif mode == 'toMax':
                    mi = w_list.index(max(w_list))
                    w_list[mi] += w_list[_k]
                    w_list[_k] = 0
                    jnt_list.remove(jnt_list[_k])
                    w_list.remove(w_list[_k])

                else :
                    if jnt.getParent().name() == 'DeformationSystem':
                        sw =  w_list[_k]/(len(w_list)-1)
                        w_list[_k] = 0
                        jnt_list.remove(jnt_list[_k])
                        w_list.remove(w_list[_k])
                        
                        for iw,ww in enumerate(w_list):
                            w_list[iw] = ww+sw
                        
                    else:    
                        pi = inf_index_list[inf_list.index(jnt.getParent())]
                        if pi in jnt_list:
                            k = jnt_list.index(pi)
                            w_list[k] += w_list[_k]
                            w_list[_k] = 0
                            jnt_list.remove(jnt_list[_k])
                            w_list.remove(w_list[_k])
                        else:
                            sw =  w_list[_k]/(len(w_list)-1)
                            w_list[_k] = 0
                            jnt_list.remove(jnt_list[_k])
                            w_list.remove(w_list[_k])
                            
                            for iw,ww in enumerate(w_list):
                                w_list[iw] = ww+sw
                
                info[vtx_i] = dict(zip(jnt_list,w_list))
                    
    for vi,wl in info.items():
        print(vi)
        for ji in skin.wl[vi].w.get(mi=1):
            if ji not in wl.keys():
                skin.wl[vi].w[ji].set(0)
            else:
                skin.wl[vi].w[ji].set(wl[ji])


def run():
    sel = pm.filterExpand(pm.ls(sl=1), sm=12)
    for s in sel :
        skins = pm.listHistory(s,type='skinCluster')
        if skins :
            skin = skins[0]
            limitInfluence(skin,num=4,mode='average')