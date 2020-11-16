// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Factories/Factory.h"
#include "EditorReimportHandler.h"

#include "doodleAbcFactory.generated.h"

class FAbcImporter;
class UAbcImportSettings;
class FAbcImporter;
class UGeometryCache;
class UAbcAssetImportData;

class SAlembicImportOptions;

/**
 * �Զ���abc�ļ�����
 */

UCLASS()
class DOODLE_API UdoodleAbcFactory : public UFactory, public FReimportHandler
{
	GENERATED_BODY()
public:

	UdoodleAbcFactory( );

	UPROPERTY( )
	UAbcImportSettings* importSetting;
	
	UPROPERTY( )
	bool bShowOption;

	//��ʼ uobj�ӿ�
	void PostInitProperties( );
	//�����ӿ�

	//��ʼ ufactory �ӿ� 
	virtual FText GetDisplayName( ) const override;
	virtual bool DoesSupportClass(UClass * Class)override;
	//virtual UClass* ResolveSupportedClass( ) override;
	virtual bool FactoryCanImport(const FString& FileName) override;
	virtual UObject * FactoryCreateFile(UClass* InClass, UObject* InParent, FName InName, EObjectFlags Flags, const FString& Filename, const TCHAR* Parms, FFeedbackContext* Warn, bool& bOutOperationCanceled) override;
	//�����ӿ�

	//��ʼ���µ���ӿ�
	virtual bool CanReimport(UObject* Obj, TArray<FString>& OutFilenames) override;
	virtual void SetReimportPaths(UObject* Obj, const TArray<FString>& NewReimportPaths) override;
	virtual EReimportResult::Type Reimport(UObject* Obj) override;

	void ShowImportOptionsWindow(TSharedPtr<SAlembicImportOptions>& Options, FString FilePath, const FAbcImporter& Importer);

	virtual int32 GetPriority( ) const override;
	//�������µ���ӿ�

	/// <summary>
	/// ����Ϊ���λ���
	/// </summary>
	/// <param name="Importer">import��ʵ��</param>
	/// <param name="InParent">���λ���ĸ����ʲ�</param>
	/// <param name="Flags">Ϊ���λ��洴���ı�־</param>
	/// <returns></returns>
	UObject* ImportGeometryCache(FAbcImporter& Importer, UObject* InParent, EObjectFlags Flags);

	EReimportResult::Type ReimportGeometryCache(UGeometryCache* Cache);

	void PopulateOptionsWithImportData(UAbcAssetImportData* ImportData);

};
