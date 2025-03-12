# macOS Goodies

Apps:

- Alfred, launch on login
- Rectangle, launch on login
- iStat Menus, launch on login
- Firefox, pin to Dock
- Thunderbird, pin to Dock, click top-right button and change ui density and font size in the menu
- Visual Studio Code, pin to Dock
- WeChat, pin to Dock
- iTerm, pin to Dock
- Squirrel Rime
- 1Password
- Homebrew with TUNA Mirrors
- Nix home-manager, Setup trusted users: `echo "trusted-users = $USER" >> /etc/nix/nix.conf && sudo launchctl unload /Library/LaunchDaemons/org.nixos.nix-daemon.plist && sudo launchctl load /Library/LaunchDaemons/org.nixos.nix-daemon.plist`
- Rustup & Crates.io with TUNA Mirrors
- Windows App
- Tencent Meeting
- MikTeX

Configs:

- `defaults write -g ApplePressAndHoldEnabled -bool false` for press and hold
- Settings -> Control Center -> Battery -> Show in Control Center -> Disabled
- Settings -> Trackpad -> Look up & data detectors -> Tap with Three Fingers
- Settings -> Trackpad -> Tap to click -> Enabled
- Settings -> Accessibility -> Pointer Control -> Trackpad Options -> Use trackpad for dragging -> Enabled -> Dragging style -> Three Finger Drag
- Settings -> Keyboard -> Keyboard Shortcuts... -> Modifier Keys -> Caps Lock key -> Escape
- Settings -> Desktop & Dock -> Hot Corners... -> Bottom Right -> Lock Screen
- `sudo scutil --set HostName newhostname`
- Disk Utility -> Volume + -> Name: Data -> Add
