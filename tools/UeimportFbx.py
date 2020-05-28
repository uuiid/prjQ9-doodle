import unreal
import json
import socket
import datetime


def _unreal_import_fbx_asset(input_path, destination_path, destination_name):
    """
    Import an FBX into Unreal Content Browser
    :param input_path: The fbx file to import
    :param destination_path: The Content Browser path where the asset will be placed
    :param destination_name: The asset name to use; if None, will use the filename without extension
    """
    tasks = []
    tasks.append(_generate_fbx_import_task(input_path, destination_path,
                                           destination_name, animations=True, automated=True))

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    first_imported_object = None

    for task in tasks:
        unreal.log("Import Task for: {}".format(task.filename))
        for object_path in task.imported_object_paths:
            unreal.log("Imported object: {}".format(object_path))
            if not first_imported_object:
                first_imported_object = object_path

    return first_imported_object


def _generate_fbx_import_task(filename, destination_path, destination_name=None, replace_existing=False,
                              automated=False, save=False, materials=False,
                              textures=False, as_skeletal=False, animations=False):
    """
    Create and configure an Unreal AssetImportTask
    :param filename: The fbx file to import
    :param destination_path: The Content Browser path where the asset will be placed
    :return the configured AssetImportTask
    """
    task = unreal.AssetImportTask()
    task.filename = filename
    task.destination_path = destination_path

    # By default, destination_name is the filename without the extension
    if destination_name is not None:
        task.destination_name = destination_name

    task.replace_existing = replace_existing
    task.automated = automated
    task.save = save

    task.options = unreal.FbxImportUI()
    task.options.import_materials = materials
    task.options.import_textures = textures
    task.options.import_as_skeletal = as_skeletal
    task.options.import_animations = animations
    # task.options.import_mesh = True
    # task.options.static_mesh_import_data.combine_meshes = True
    # task.options.

    task.options.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH
    if as_skeletal:
        task.options.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH

    return task


sover = socket.socket()
sover.bind(("127.0.0.1", 23335))
sover.listen(2)
new = datetime.datetime.now() + datetime.timedelta(minutes=30)
while True:
    if new < datetime.datetime.now():
        break
    cs, address = sover.accept()

    data = cs.recv(1024)
    if b"close" == data:
        break

    print(data)
    fbxmodle = json.loads(data.decode('utf-8'))
    print(fbxmodle)
    eps = fbxmodle["eps"]
    shot = fbxmodle["shot"]
    {}.items()
    game_path = "/Game/shot/Ep{:0>3d}/Sc{:0>4d}/Ren".format(eps, shot)
    for key, item in fbxmodle["content"].items():
        if key in ["camera"]:
            continue
        _unreal_import_fbx_asset(item[0], game_path, key)
    cs.close()

sover.close()
