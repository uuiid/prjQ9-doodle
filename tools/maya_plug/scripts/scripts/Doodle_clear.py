import maya.cmds



class clearAndUpload(object):
    def __init__(self):
        pass
    def clearScane(self):
        un_know_plugs = maya.cmds.unknownPlugin(query=True,list=True)
        for un_plug in un_know_plugs:
            maya.cmds.unknownPlugin(un_plug,remove=True)
        
        plugs = maya.cmds.pluginInfo( query=True, listPlugins=True )
        for plug in plugs:
            maya.cmds.pluginInfo(plug, edit=True, writeRequires=False)