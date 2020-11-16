// Fill out your copyright notice in the Description page of Project Settings.


#include "doodleAbcFactory.h"

#include "AbcImportSettings.h"
#include "GeometryCache.h"
#include "AbcImporter.h"
#include "AssetImportTask.h"
#include "AbcImportLogger.h"
#include "AbcAssetImportData.h"

UdoodleAbcFactory::UdoodleAbcFactory( ) {
    bCreateNew = false;
    bEditAfterNew = true;
    SupportedClass = nullptr;

    bEditorImport = true;
    bText = false;
    bShowOption = false;

    Formats.Add(TEXT("abc;Alembic"));
    ImportPriority = 0.f;
}


void UdoodleAbcFactory::PostInitProperties( )
{
    Super::PostInitProperties( );
    importSetting = UAbcImportSettings::Get( );
}

FText UdoodleAbcFactory::GetDisplayName( ) const
{
    return NSLOCTEXT("doodle", "doodleAbc", "Alembic");
}

bool UdoodleAbcFactory::DoesSupportClass(UClass* Class)
{
    return (Class == UGeometryCache::StaticClass( ));
}

bool UdoodleAbcFactory::FactoryCanImport(const FString& FileName)
{
    //����Ϊʲô����ôһ��������Ҳ��֪��
    const FString suff = FPaths::GetExtension(FileName);

    return (FPaths::GetExtension(FileName) == TEXT("abc"));
}

UObject* UdoodleAbcFactory::FactoryCreateFile(UClass* InClass, UObject* InParent, FName InName, EObjectFlags Flags, const FString& Filename, const TCHAR* Parms, FFeedbackContext* Warn, bool& bOutOperationCanceled)
{
    GEditor->GetEditorSubsystem<UImportSubsystem>( )->BroadcastAssetPreImport(this, InClass, InParent, InName, TEXT("doodle_abc"));
    FAbcImporter Import;
    EAbcImportError errorCode = Import.OpenAbcFileForImport(Filename);

    importSetting->bReimport = false;

    AdditionalImportedObjects.Empty( );

    if (errorCode != AbcImportError_NoError)
    {
        GEditor->GetEditorSubsystem<UImportSubsystem>( )->BroadcastAssetPostImport(this, nullptr);
        return nullptr;
    }
    importSetting->SamplingSettings.FrameStart = 1001;
    importSetting->SamplingSettings.FrameEnd = Import.GetEndFrameIndex( );
    bOutOperationCanceled = false;

    UAbcImportSettings* scriptedStting = AssetImportTask ? Cast<UAbcImportSettings>(AssetImportTask->Options) : nullptr;
    if (scriptedStting)
    {
        importSetting = scriptedStting;
    }
    //�����־
    const FString PageName = "Importing " + InName.ToString( ) + ".abc";

    TArray<UObject*> ResultAssets;
    if (!bOutOperationCanceled)
    {
        GEditor->GetEditorSubsystem<UImportSubsystem>( )->BroadcastAssetPreImport(this, InClass, InParent, InName, TEXT("ABC"));
        
        int32 NumThreads = 1;
        if (FPlatformProcess::SupportsMultithreading( ))
        {
            NumThreads = FPlatformMisc::NumberOfCores( );
        }
        //�����ļ�
        errorCode = Import.ImportTrackData(NumThreads, importSetting);

        if (errorCode != AbcImportError_NoError)
        {
            GEditor->GetEditorSubsystem<UImportSubsystem>( )->BroadcastAssetPostImport(this, nullptr);
            FAbcImportLogger::OutputMessages(PageName);
            return nullptr;
        }
        else
        {//���뼸�λ���
            if (importSetting->ImportType == EAlembicImportType::GeometryCache)
            {
                UObject* GeometryCache = ImportGeometryCache(Import, InParent, Flags);
                if (GeometryCache)
                {
                    ResultAssets.Add(GeometryCache);
                }
            }
        }

        AdditionalImportedObjects.Reserve(ResultAssets.Num( ));
        for (UObject* obj : ResultAssets)
        {
            if (obj)
            {
                GEditor->GetEditorSubsystem<UImportSubsystem>( )->BroadcastAssetPostImport(this, obj);
                obj->MarkPackageDirty( );
                obj->PostEditChange( );
                AdditionalImportedObjects.Add(obj);
            }
        }

        FAbcImportLogger::OutputMessages(PageName);
    }
    //ȷ�ϸ���;
    UObject* OutParent = (ResultAssets.Num( ) > 0 && InParent != ResultAssets[0]->GetOutermost( )) ? ResultAssets[0]->GetOutermost( ) : InParent;
    return (ResultAssets.Num( ) > 0) ? OutParent : nullptr;
}

bool UdoodleAbcFactory::CanReimport(UObject* Obj, TArray<FString>& OutFilenames)
{
    UAssetImportData* ImportData = nullptr;
    if (Obj->GetClass( ) == UGeometryCache::StaticClass( ))
    {
        UGeometryCache* Cache = Cast<UGeometryCache>(Obj);
        ImportData = Cache->AssetImportData;
    }
    if (ImportData)
    {
        if (FPaths::GetExtension(ImportData->GetFirstFilename( )) == TEXT("abc") || (Obj->GetClass( ) == UAnimSequence::StaticClass( ) && ImportData->GetFirstFilename( ).IsEmpty( )))
        {
            ImportData->ExtractFilenames(OutFilenames);
            return true;
        }
    }
    return false;
}

void UdoodleAbcFactory::SetReimportPaths(UObject* Obj, const TArray<FString>& NewReimportPaths)
{
    UGeometryCache* GeometryCache = Cast<UGeometryCache>(Obj);
    if (GeometryCache && GeometryCache->AssetImportData && ensure(NewReimportPaths.Num( ) == 1))
    {
        GeometryCache->AssetImportData->UpdateFilenameOnly(NewReimportPaths[0]);
    }
}

EReimportResult::Type UdoodleAbcFactory::Reimport(UObject* Obj)
{
    importSetting->bReimport = true;
    const FString PageName = "Reimporting " + Obj->GetName( ) + ".abc";
    if (Obj->GetClass( ) == UGeometryCache::StaticClass( ))
    {
        UGeometryCache* GeometryCache = Cast<UGeometryCache>(Obj);
        if (!GeometryCache)
        {
            return EReimportResult::Failed;
        }

        CurrentFilename = GeometryCache->AssetImportData->GetFirstFilename( );

        EReimportResult::Type Result = ReimportGeometryCache(GeometryCache);

        if (GeometryCache->GetOuter( ))
        {
            GeometryCache->GetOuter( )->MarkPackageDirty( );
        }
        else
        {
            GeometryCache->MarkPackageDirty( );
        }

        // Close possible open editors using this asset	
        GEditor->GetEditorSubsystem<UAssetEditorSubsystem>( )->CloseAllEditorsForAsset(GeometryCache);

        FAbcImportLogger::OutputMessages(PageName);
        return Result;
    }
    return EReimportResult::Failed;
}

void UdoodleAbcFactory::ShowImportOptionsWindow(TSharedPtr<SAlembicImportOptions>& Options, FString FilePath, const FAbcImporter& Importer)
{
    //// Window size computed from SAlembicImportOptions
    //const float WindowHeight = 500.f + FMath::Clamp(Importer.GetPolyMeshes( ).Num( ) * 16.f, 0.f, 250.f);

    //TSharedRef<SWindow> Window = SNew(SWindow)
    //    .Title(LOCTEXT("WindowTitle", "Alembic Cache Import Options"))
    //    .ClientSize(FVector2D(522.f, WindowHeight));

    //Window->SetContent
    //(
    //    SAssignNew(Options, SAlembicImportOptions).WidgetWindow(Window)
    //    .ImportSettings(ImportSettings)
    //    .WidgetWindow(Window)
    //    .PolyMeshes(Importer.GetPolyMeshes( ))
    //    .FullPath(FText::FromString(FilePath))
    //);

    //TSharedPtr<SWindow> ParentWindow;

    //if (FModuleManager::Get( ).IsModuleLoaded("MainFrame"))
    //{
    //    IMainFrameModule& MainFrame = FModuleManager::LoadModuleChecked<IMainFrameModule>("MainFrame");
    //    ParentWindow = MainFrame.GetParentWindow( );
    //}

    //FSlateApplication::Get( ).AddModalWindow(Window, ParentWindow, false);
}

int32 UdoodleAbcFactory::GetPriority( ) const
{
    return ImportPriority;
}

UObject* UdoodleAbcFactory::ImportGeometryCache(FAbcImporter& Importer, UObject* InParent, EObjectFlags Flags)
{
    // Flush commands before importing
    FlushRenderingCommands( );

    const uint32 NumMeshes = Importer.GetNumMeshTracks( );
    // Check if the alembic file contained any meshes
    if (NumMeshes > 0)
    {
        UGeometryCache* GeometryCache = Importer.ImportAsGeometryCache(InParent, Flags);

        if (!GeometryCache)
        {
            return nullptr;
        }

        // Setup asset import data
        if (!GeometryCache->AssetImportData || !GeometryCache->AssetImportData->IsA<UAbcAssetImportData>( ))
        {
            GeometryCache->AssetImportData = NewObject<UAbcAssetImportData>(GeometryCache);
        }
        GeometryCache->AssetImportData->Update(UFactory::CurrentFilename);
        UAbcAssetImportData* AssetImportData = Cast<UAbcAssetImportData>(GeometryCache->AssetImportData);
        if (AssetImportData)
        {
            Importer.UpdateAssetImportData(AssetImportData);
        }

        return GeometryCache;
    }
    else
    {
        // Not able to import a static mesh
        GEditor->GetEditorSubsystem<UImportSubsystem>( )->BroadcastAssetPostImport(this, nullptr);
        return nullptr;
    }
}

EReimportResult::Type UdoodleAbcFactory::ReimportGeometryCache(UGeometryCache* Cache)
{
    // Ensure that the file provided by the path exists
    if (IFileManager::Get( ).FileSize(*CurrentFilename) == INDEX_NONE)
    {
        return EReimportResult::Failed;
    }

    FAbcImporter Importer;
    EAbcImportError ErrorCode = Importer.OpenAbcFileForImport(CurrentFilename);

    if (ErrorCode != AbcImportError_NoError)
    {
        // Failed to read the file info, fail the re importing process 
        return EReimportResult::Failed;
    }
    
    importSetting->ImportType = EAlembicImportType::GeometryCache;
    importSetting->SamplingSettings.FrameStart = 0;
    importSetting->SamplingSettings.FrameEnd = Importer.GetEndFrameIndex( );

    if (Cache->AssetImportData && Cache->AssetImportData->IsA<UAbcAssetImportData>( ))
    {
        UAbcAssetImportData* ImportData = Cast<UAbcAssetImportData>(Cache->AssetImportData);
        PopulateOptionsWithImportData(ImportData);
        Importer.RetrieveAssetImportData(ImportData);
    }

    //if (bShowOption)
    //{
    //    TSharedPtr<SAlembicImportOptions> Options;
    //    ShowImportOptionsWindow(Options, CurrentFilename, Importer);

    //    if (!Options->ShouldImport( ))
    //    {
    //        return EReimportResult::Cancelled;
    //    }
    //}

    int32 NumThreads = 1;
    if (FPlatformProcess::SupportsMultithreading( ))
    {
        NumThreads = FPlatformMisc::NumberOfCores( );
    }

    // Import file	
    ErrorCode = Importer.ImportTrackData(NumThreads, importSetting);

    if (ErrorCode != AbcImportError_NoError)
    {
        // Failed to read the file info, fail the re importing process 
        return EReimportResult::Failed;
    }

    UGeometryCache* GeometryCache = Importer.ReimportAsGeometryCache(Cache);

    if (!GeometryCache)
    {
        return EReimportResult::Failed;
    }
    else
    {
        // Update file path/timestamp (Path could change if user has to browse for it manually)
        if (!GeometryCache->AssetImportData || !GeometryCache->AssetImportData->IsA<UAbcAssetImportData>( ))
        {
            GeometryCache->AssetImportData = NewObject<UAbcAssetImportData>(GeometryCache);
        }

        GeometryCache->AssetImportData->Update(CurrentFilename);
        UAbcAssetImportData* AssetImportData = Cast<UAbcAssetImportData>(GeometryCache->AssetImportData);
        if (AssetImportData)
        {
            Importer.UpdateAssetImportData(AssetImportData);
        }
    }

    return EReimportResult::Succeeded;
}

void UdoodleAbcFactory::PopulateOptionsWithImportData(UAbcAssetImportData* ImportData)
{
    importSetting->SamplingSettings = ImportData->SamplingSettings;
}


