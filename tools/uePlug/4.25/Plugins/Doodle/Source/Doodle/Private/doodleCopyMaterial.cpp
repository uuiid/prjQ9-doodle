#include "doodleCopyMaterial.h"

#include "Editor/ContentBrowser/Public/ContentBrowserModule.h"
#include "Editor/ContentBrowser/Public/IContentBrowserSingleton.h"
#include "EditorAssetLibrary.h"

#include "GeometryCache.h"
#include "Materials/MaterialInterface.h"
#include "Materials/Material.h"

//批量导入
#include "AlembicImporterModule.h"
#include "AssetToolsModule.h"
#include "IAssetTools.h"
#include "DesktopPlatformModule.h"
#include "AlembicImportFactory.h"
#include "AbcImporter.h"
#include "AbcImportSettings.h"
#include "AssetImportTask.h"
#include "ObjectTools.h"

//重命名资产
#include "EditorAssetLibrary.h"
//#include "doodleAbcFactory.h"

void DoodleCopyMat::Construct(const FArguments& Arg)
{
    //这个是ue界面的创建方法

    ChildSlot[
        SNew(SHorizontalBox)
            + SHorizontalBox::Slot( )
            .AutoWidth( )
            .HAlign(HAlign_Left)
            .Padding(FMargin(1.f, 1.f))
            [
                SNew(SButton)//创建按钮
                .OnClicked(this, &DoodleCopyMat::getSelect)//添加回调函数
            [
                SNew(STextBlock).Text(FText::FromString("Get Select Obj"))//按钮中的字符
            ]
            ]
        + SHorizontalBox::Slot( )
            .AutoWidth( )
            .HAlign(HAlign_Left)
            .Padding(FMargin(1.f, 1.f))
            [
                SNew(SButton)//创建按钮
                .OnClicked(this, &DoodleCopyMat::CopyMateral)//添加回调函数
            [
                SNew(STextBlock).Text(FText::FromString("copy To obj"))//按钮中的字符
            ]
            ]
        + SHorizontalBox::Slot( )
            .AutoWidth( )
            .HAlign(HAlign_Left)
            .Padding(FMargin(1.f, 1.f))
            [
                SNew(SButton)
                .OnClicked(this, &DoodleCopyMat::BathImport)
            [
                SNew(STextBlock).Text(FText::FromString("bath import"))
            ]
            ]
        + SHorizontalBox::Slot( )
            .AutoWidth()
            .HAlign(HAlign_Left)
            .Padding(FMargin(1.f,1.f))
            [
                SNew(SButton)
                .OnClicked(this, &DoodleCopyMat::BathReameAss)[
                    SNew(STextBlock).Text(FText::FromString("bath rename"))
                ]
            ]
    ];
}

void DoodleCopyMat::AddReferencedObjects(FReferenceCollector& collector)
{
    //collector.AddReferencedObjects()
}

FReply DoodleCopyMat::getSelect( )
{
    /*
    获得文件管理器中的骨架网格物体的选择
    这是一个按钮的回调参数
    */

    //获得文件管理器的模块(或者类?)
    FContentBrowserModule& contentBrowserModle = FModuleManager::Get( ).LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
    TArray<FAssetData> selectedAss;
    contentBrowserModle.Get( ).GetSelectedAssets(selectedAss);
    for (int i = 0; i < selectedAss.Num( ); i++)
    {
        // 测试选中物体是否是骨骼物体
        if (selectedAss[i].GetClass( )->IsChildOf<USkeletalMesh>( ))
        {
            //如果是骨骼物体就可以复制材质了
            UE_LOG(LogTemp, Log, TEXT("确认骨骼物体 %s"), *(selectedAss[i].GetFullName( )));

            UObject* skinObj = selectedAss[i].ToSoftObjectPath( ).TryLoad( );
            // assLoad.LoadAsset(selectedAss[i].GetFullName( ));
            //将加载的类转换为skeletalMesh类并进行储存
            if (skinObj) {
                copySoureSkinObj = Cast<USkeletalMesh>(skinObj);
                UE_LOG(LogTemp, Log, TEXT("%s"), *(copySoureSkinObj->GetPathName( )));
            }
            //TArray<FSkeletalMaterial> SoureMat = copySoureSkinObj->Materials;
            //for (int m = 0; m < SoureMat.Num( ); m++)
            //{
            //    SoureMat[m].MaterialInterface->GetPathName( );
            //    UE_LOG(LogTemp, Log, TEXT("%s"), *(SoureMat[m].MaterialInterface->GetPathName( )));
            //}
            //
            //if (UClass *cl = loadObj->GetClass())
            //{
            //    if (UProperty *mproperty = cl->FindPropertyByName("materials"))
            //    {
            //        mproperty.
            //        UE_LOG(LogTemp, Log, TEXT("%s"), *(mproperty->GetName()));
            //    }
            //}
            //selectedAss[i].ToSoftObjectPath( ).TryLoad()
            //TFieldIterator<UProperty> iter(loadObj);
            //USkeletalMeshComponent test;
            //test.getmaterial
            //test.SetMaterial( );
            //UStaticMeshComponent test2;
            //test2.SetMaterial( );
        }//测试是否是几何缓存物体
        else if (selectedAss[i].GetClass( ) == UGeometryCache::StaticClass( )) {
            //如果是骨骼物体就可以复制材质了
            UE_LOG(LogTemp, Log, TEXT("确认几何缓存  %s"), *(selectedAss[i].GetFullName( )));
            UObject* cacheObj = selectedAss[i].ToSoftObjectPath( ).TryLoad( );
            if (cacheObj) {
                copySoureGeoCache = cacheObj;
                //*(cacheObj->GetFullName( )
                UE_LOG(LogTemp, Log, TEXT("%s"), *(cacheObj->GetFullName( )));
            }
        }
        //bool is =selectedAss[i].GetClass( )->IsChildOf<USkeletalMesh>( );
        //UE_LOG(LogTemp, Log, TEXT("%s"), *(FString::FromInt(is)));
        //selectedAss[i].GetFullName( )
    }
    return FReply::Handled( );
}

FReply DoodleCopyMat::CopyMateral( )
{
    FContentBrowserModule& contentBrowserModle = FModuleManager::Get( ).LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
    TArray<FAssetData> selectedAss;
    contentBrowserModle.Get( ).GetSelectedAssets(selectedAss);
    for (int i = 0; i < selectedAss.Num( ); i++)
    {
        UObject* loadObj = selectedAss[i].ToSoftObjectPath( ).TryLoad( );// assLoad.LoadAsset(selectedAss[i].GetFullName( ));

        // 测试选中物体是否是骨骼物体
        if (selectedAss[i].GetClass( )->IsChildOf<USkeletalMesh>( ))
        {
            //如果是骨骼物体就可以复制材质了
            UE_LOG(LogTemp, Log, TEXT("开始复制材质 %s"), *(selectedAss[i].GetFullName( )));

            USkeletalMesh* copyTrange = Cast<USkeletalMesh>(loadObj);

            UE_LOG(LogTemp, Log, TEXT("确认并加载为几何物体 %s"), *(copyTrange->GetPathName( )));
            TArray<FSkeletalMaterial> trangeMat = copyTrange->Materials;
            if (copySoureSkinObj)
                for (int m = 0; m < trangeMat.Num( ); m++) {
                    trangeMat[m] = copySoureSkinObj->Materials[m];
                    UE_LOG(LogTemp, Log, TEXT("%s"), *(trangeMat[m].MaterialInterface->GetPathName( )));
                    //材质插槽命名
                }
            copyTrange->Materials = trangeMat;

        }//如果是几何缓存就复制几何缓存
        else if (selectedAss[i].GetClass( ) == UGeometryCache::StaticClass( )) {
            UE_LOG(LogTemp, Log, TEXT("开始复制材质 %s"), *(selectedAss[i].GetFullName( )));

            UGeometryCache* copyTrange = Cast<UGeometryCache>(loadObj);
            TArray<UMaterialInterface*> trange = copyTrange->Materials;

            if (copySoureGeoCache) {
                auto soure = Cast<UGeometryCache>(copySoureGeoCache);
                for (int m = 0; m < trange.Num( ); m++)
                {
                    trange[m] = soure->Materials[m];
                    UE_LOG(LogTemp, Log, TEXT("%s"), *(trange[m]->GetPathName( )));
                }
            }
            copyTrange->Materials = trange;
        }
    }
    return FReply::Handled( );
}

FReply DoodleCopyMat::BathImport( )
{
    FlushRenderingCommands( );
    //auto fileName = OpenFileDialog("Bath import abc file", "", " abc file|*.abc;");
    //TScriptInterface<IAssetTools> test = UAssetToolsHelpers::GetAssetTools( );
    
    //IAssetTools& assetTools = FModuleManager::LoadModuleChecked<FAssetToolsModule>("AssetTools").Get( );
    
    //重命名资产
    UEditorAssetLibrary::RenameAsset("/Game/Developers/teXiao/Collections/NewMaterial", "/Game/Developers/teXiao/Collections/NewMaterial2");
    //auto arr_string = assetTools.ImportAssetsWithDialog(FString("/game/test"));
    
    //auto abc_import = NewObject<FAbcImporter>( );
    //auto import = FAbcImporter( );

    //auto errCore = import.OpenAbcFileForImport("D:/tmp/test.abc");

    //if (errCore != AbcImportError_NoError)
    //{
    //    GEditor->GetEditorSubsystem<UImportSubsystem>()->BroadcastAssetPreImport()
    //}
    
    //auto test = UAlembicImportFactory::StaticClass( );
    //auto test1 = test->GetDefaultObject( );









    //auto open_ex = UAssetToolsHelpers::GetAssetTools( );
    //auto arr_string = open_ex->ImportAssetsWithDialog(FString("/game/test"));
    //
    
    //auto & test = FModuleManager::LoadModuleChecked<UAlembicImportFactory>("AlembicImporter");

    //UAlembicImportFactory *abc_import_factory = &test;
    //UAlembicImportFactory::StaticClass( )->GetDefaultObject(); 
    //auto abc_import_factory = NewObject<UAlembicImportFactory>();


    // Get the list of valid factories
    //for (TObjectIterator<UClass> It; It; ++It)
    //{
    //    UClass* CurrentClass = (*It);
    //    if (CurrentClass->IsChildOf(UAlembicImportFactory::StaticClass( )) && !(CurrentClass->HasAnyClassFlags(CLASS_Abstract)))
    //    {
    //        //UAlembicImportFactory* Factory = Cast<UAlembicImportFactory>(CurrentClass->GetDefaultObject( ));
    //    }
    //}




    //auto abc_import_factory = Cast<UAlembicImportFactory>(UAlembicImportFactory::StaticClass( )->GetDefaultObject( ));

    //abc_import_factory->GetDefaultSubobjects

    //abc_import_factory->ImportSettings->ImportType = EAlembicImportType::GeometryCache;
    //abc_import_factory->ImportSettings->GeometryCacheSettings.bApplyConstantTopologyOptimizations = true;
    //abc_import_factory->ImportSettings->GeometryCacheSettings.CompressedPositionPrecision = 0.f;

    //abc_import_factory->ImportSettings->SamplingSettings.FrameStart = 1001;
    //abc_import_factory->ImportSettings->SamplingSettings.bSkipEmpty = true;
    //abc_import_factory->ImportSettings->SamplingSettings.FrameSteps = 25.f;

    //abc_import_factory->bShowOption = false;


    //UAssetImportTask* importTask = NewObject<UAssetImportTask>( );    
    //importTask->bAutomated = true;
    //importTask->bSave = true;

    //for (auto&& item : fileName) {
    //    UE_LOG(LogTemp, Log, TEXT("%s"), *item);
    //    //if (!abc_import_factory->FactoryCanImport(item)) {
    //    //    UE_LOG(LogTemp, Log, TEXT("无法导入 %s 文件"), *item);
    //    //    continue;
    //    //}

    //}

    return FReply::Handled( );
}

FReply DoodleCopyMat::BathReameAss( )
{
    FContentBrowserModule& contentBrowserModle = FModuleManager::Get( ).LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
    TArray<FAssetData> selectedAss;
    contentBrowserModle.Get( ).GetSelectedAssets(selectedAss);

    for (auto&& item : selectedAss) {
        UObject* loadObj = item.ToSoftObjectPath( ).TryLoad( );
        if (loadObj == nullptr) continue;
        if (!item.GetClass( )->IsChildOf<USkeletalMesh>( )) continue;
        //确认时骨骼物体
        USkeletalMesh* skinObj = Cast<USkeletalMesh>(loadObj);
        UE_LOG(LogTemp, Log, TEXT("确认并加载骨骼物体 %s"), *(skinObj->GetPathName( )));
        if (skinObj == nullptr) continue;
        for (auto& mat : skinObj->Materials)
        {
            if (mat.ImportedMaterialSlotName.IsValid( )) {
                
                if (mat.MaterialInterface->GetMaterial( ) != nullptr)
                {
                    mat.MaterialInterface->GetMaterial( )->bUsedWithGeometryCache = true;
                    UE_LOG(LogTemp, Log, TEXT("使材料支持集合缓存 %s"), *(mat.MaterialInterface->GetPathName( )));

                }
                UE_LOG(LogTemp, Log, TEXT("确认材质插槽名称 %s"), *(mat.ImportedMaterialSlotName.ToString( )));
                UEditorAssetLibrary::RenameAsset(mat.MaterialInterface->GetPathName( ),
                                                 mat.MaterialInterface->GetPathName( )
                                                 .Replace(
                                                    *(mat.MaterialInterface->GetName( )),
                                                    *(mat.ImportedMaterialSlotName.ToString( ))
                                                          )
                );
                //auto test = mat.MaterialInterface->GetPathName( )
                //    .Replace(*(mat.MaterialInterface->GetName( )),
                //             *(mat.ImportedMaterialSlotName.ToString( )));
                //FString left;
                //FString reag;
                //test.Split(".", &left, &reag);
                //UE_LOG(LogTemp, Log,
                //       TEXT("Test  %s  %s --> %s"),
                //       *(test),
                //       *(mat.MaterialInterface->GetName( )),
                //       *(mat.ImportedMaterialSlotName.ToString( )));
                UE_LOG(LogTemp, Log,
                       TEXT("重命名材质 路径 %s  %s --> %s"),
                       *(mat.MaterialInterface->GetPathName( )),
                       *(mat.MaterialInterface->GetName( )),
                       *(mat.ImportedMaterialSlotName.ToString( )));
            }
        }

    }

    return FReply::Handled();
}

TArray<FString> DoodleCopyMat::OpenFileDialog(const FString& DialogTitle, const FString& DefaultPath, const FString& FileTypes) {
    TArray<FString> OutFileNames;
    void* ParentWindowPtr = FSlateApplication::Get( ).GetActiveTopLevelWindow( )->GetNativeWindow( )->GetOSWindowHandle( );
    IDesktopPlatform* DesktopPlatform = FDesktopPlatformModule::Get( );
    if (DesktopPlatform)
    {
        uint32 SelectionFlag = 1; //A value of 0 represents single file selection while a value of 1 represents multiple file selection
        DesktopPlatform->OpenFileDialog(ParentWindowPtr, DialogTitle, DefaultPath, FString(""), FileTypes, SelectionFlag, OutFileNames);
    }
    return OutFileNames;
}