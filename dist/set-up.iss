[Setup]
AppName=ImageConverter
AppVersion=1.0
DefaultDirName={pf}\ImageConverter
OutputDir=.
OutputBaseFilename=ImageConverterInstaller
Compression=lzma2
SolidCompression=yes

[Files]
Source: "image-converter.exe"; DestDir: "{app}"

[Icons]
Name: "{commondesktop}\YourApp"; Filename: "{app}\image-converter.exe"

[Run]
Filename: "{app}\image-converter.exe"; Description: "{cm:LaunchProgram,ImageConverter}"; Flags: nowait postinstall skipifsilent
