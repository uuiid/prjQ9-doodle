#include "doodleCopyMaterial.h"

#include "Editor/ContentBrowser/Public/ContentBrowserModule.h"
#include "Editor/ContentBrowser/Public/IContentBrowserSingleton.h"
#include "EditorAssetLibrary.h"

void DoodleCopyMat::Construct(const FArguments & Arg)
{
    //这个是ue界面的创建方法

    ChildSlot[
        SNew(SHorizontalBox)
            +SHorizontalBox::Slot()
            .AutoWidth()
            .HAlign(HAlign_Left)
            .Padding(FMargin(1.f,1.f))
            [
                SNew(SButton)//创建按钮
                .OnClicked(this, &DoodleCopyMat::getSelect)//添加回调函数
                [
                    SNew(STextBlock).Text(FText::FromString("Get Select Obj"))//按钮中的字符
                ]
            ]
            +SHorizontalBox::Slot( )
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
            UE_LOG(LogTemp, Log, TEXT("%s"), *(selectedAss[i].GetFullName( )));
            
            UObject* skinObj = selectedAss[i].ToSoftObjectPath( ).TryLoad( );// assLoad.LoadAsset(selectedAss[i].GetFullName( ));
            //将加载的类转换为skeletalMesh类并进行储存
            copySoure = Cast<USkeletalMesh>(skinObj);
            UE_LOG(LogTemp, Log, TEXT("%s"), *(copySoure->GetPathName( )));
            //TArray<FSkeletalMaterial> SoureMat = copySoure->Materials;
            //for (int m = 0; m < SoureMat.Num( ); m++)
            //{
            //    SoureMat[m].MaterialInterface->GetPathName( );
            //    UE_LOG(LogTemp, Log, TEXT("%s"), *(SoureMat[m].MaterialInterface->GetPathName( )));
            //}

            //if (UClass *cl = skinObj->GetClass())
            //{
            //    if (UProperty *mproperty = cl->FindPropertyByName("materials"))
            //    {
            //        mproperty.
            //        UE_LOG(LogTemp, Log, TEXT("%s"), *(mproperty->GetName()));
            //    }
            //}
            //selectedAss[i].ToSoftObjectPath( ).TryLoad()
            //TFieldIterator<UProperty> iter(skinObj);
            //USkeletalMeshComponent test;
            //test.getmaterial
            //test.SetMaterial( );
            //UStaticMeshComponent test2;
            //test2.SetMaterial( );
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
        // 测试选中物体是否是骨骼物体
        if (selectedAss[i].GetClass( )->IsChildOf<USkeletalMesh>( ))
        {
            //如果是骨骼物体就可以复制材质了
            UE_LOG(LogTemp, Log, TEXT("%s"), *(selectedAss[i].GetFullName( )));

            UObject* skinObj = selectedAss[i].ToSoftObjectPath( ).TryLoad( );// assLoad.LoadAsset(selectedAss[i].GetFullName( ));
            USkeletalMesh *copyTrange = Cast<USkeletalMesh>(skinObj);
            UE_LOG(LogTemp, Log, TEXT("%s"), *(copyTrange->GetPathName( )));
            TArray<FSkeletalMaterial> trangeMat = copyTrange->Materials;
            if (copySoure)
            {
                for (int m = 0; m < trangeMat.Num(); m++)
                {
                    trangeMat[m] = copySoure->Materials[m];
                    UE_LOG(LogTemp, Log, TEXT("%s"), *(trangeMat[m].MaterialInterface->GetPathName( )));
                }                       
            }
            copyTrange->Materials = trangeMat;
        }
    }
    return FReply::Handled( );
}
