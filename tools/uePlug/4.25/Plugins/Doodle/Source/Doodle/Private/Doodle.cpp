// Copyright Epic Games, Inc. All Rights Reserved.

#include "Doodle.h"
#include "DoodleStyle.h"
#include "DoodleCommands.h"
#include "LevelEditor.h"
#include "Widgets/Docking/SDockTab.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/Text/STextBlock.h"
#include "ToolMenus.h"

static const FName DoodleTabName("Doodle");

#define LOCTEXT_NAMESPACE "FDoodleModule"

void FDoodleModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
	
	FDoodleStyle::Initialize();
	FDoodleStyle::ReloadTextures();

	FDoodleCommands::Register();
	
	PluginCommands = MakeShareable(new FUICommandList);

	PluginCommands->MapAction(
		FDoodleCommands::Get().OpenPluginWindow,
		FExecuteAction::CreateRaw(this, &FDoodleModule::PluginButtonClicked),
		FCanExecuteAction());

	UToolMenus::RegisterStartupCallback(FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FDoodleModule::RegisterMenus));
	
	FGlobalTabmanager::Get()->RegisterNomadTabSpawner(DoodleTabName, FOnSpawnTab::CreateRaw(this, &FDoodleModule::OnSpawnPluginTab))
		.SetDisplayName(LOCTEXT("FDoodleTabTitle", "Doodle"))
		.SetMenuType(ETabSpawnerMenuType::Hidden);
}

void FDoodleModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.

	UToolMenus::UnRegisterStartupCallback(this);

	UToolMenus::UnregisterOwner(this);

	FDoodleStyle::Shutdown();

	FDoodleCommands::Unregister();

	FGlobalTabmanager::Get()->UnregisterNomadTabSpawner(DoodleTabName);
}

TSharedRef<SDockTab> FDoodleModule::OnSpawnPluginTab(const FSpawnTabArgs& SpawnTabArgs)
{
	FText WidgetText = FText::Format(
		LOCTEXT("WindowWidgetText", "Add code to {0} in {1} to override this window's contents"),
		FText::FromString(TEXT("FDoodleModule::OnSpawnPluginTab")),
		FText::FromString(TEXT("Doodle.cpp"))
		);

	return SNew(SDockTab)
		.TabRole(ETabRole::NomadTab)
		[
			// Put your tab content here!
			SNew(SBox)
			.HAlign(HAlign_Center)
			.VAlign(VAlign_Center)
			[
				SNew(STextBlock)
				.Text(WidgetText)
			]
		];
}

void FDoodleModule::PluginButtonClicked()
{
	FGlobalTabmanager::Get()->InvokeTab(DoodleTabName);
}

void FDoodleModule::RegisterMenus()
{
	// Owner will be used for cleanup in call to UToolMenus::UnregisterOwner
	FToolMenuOwnerScoped OwnerScoped(this);

	{
		UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Window");
		{
			FToolMenuSection& Section = Menu->FindOrAddSection("WindowLayout");
			Section.AddMenuEntryWithCommandList(FDoodleCommands::Get().OpenPluginWindow, PluginCommands);
		}
	}

	{
		UToolMenu* ToolbarMenu = UToolMenus::Get()->ExtendMenu("LevelEditor.LevelEditorToolBar");
		{
			FToolMenuSection& Section = ToolbarMenu->FindOrAddSection("Settings");
			{
				FToolMenuEntry& Entry = Section.AddEntry(FToolMenuEntry::InitToolBarButton(FDoodleCommands::Get().OpenPluginWindow));
				Entry.SetCommandList(PluginCommands);
			}
		}
	}
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FDoodleModule, Doodle)