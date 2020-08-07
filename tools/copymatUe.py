import sys
import unreal

def copymat(strOld,strNew):
    myold = unreal.EditorAssetLibrary.load_asset(strOld)
    mymaterial = myold.get_editor_property("materials")
    mynew = unreal.EditorAssetLibrary.load_asset(strNew)
    mynew.set_editor_property("materials", mymaterial)


copymat(sys.argv[1],sys.argv[2])



'''
asset_name = unreal.EditableTextBox()
window = unreal.WindowStyle()(
    unreal.HorizontalBox()(
        asset_name
    )
)'''