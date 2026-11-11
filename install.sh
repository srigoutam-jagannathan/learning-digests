#!/bin/bash
# Installs the Sunday 18:00 schedule for build_week.py. Run once: bash install.sh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
LABEL="com.learning-digests.weekly"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
mkdir -p "$DIR/logs" "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array><string>/usr/bin/caffeinate</string><string>-is</string><string>/usr/bin/python3</string><string>$DIR/build_week.py</string></array>
  <key>WorkingDirectory</key><string>$DIR</string>
  <key>StartCalendarInterval</key>
  <dict><key>Weekday</key><integer>0</integer><key>Hour</key><integer>18</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>$DIR/logs/build.log</string>
  <key>StandardErrorPath</key><string>$DIR/logs/build.log</string>
  <key>EnvironmentVariables</key>
  <dict><key>PATH</key><string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string></dict>
</dict></plist>
PL
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "Scheduled: every Sunday at 18:00. Log: $DIR/logs/build.log"
echo "Run it now with: launchctl kickstart gui/$(id -u)/$LABEL"
