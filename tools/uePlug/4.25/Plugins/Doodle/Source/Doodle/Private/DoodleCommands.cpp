// Copyright Epic Games, Inc. All Rights Reserved.

#include "DoodleCommands.h"

#define LOCTEXT_NAMESPACE "FDoodleModule"

void FDoodleCommands::RegisterCommands()
{
	UI_COMMAND(OpenPluginWindow, "Doodle", "Bring up Doodle window", EUserInterfaceActionType::Button, FInputGesture());
}

#undef LOCTEXT_NAMESPACE
