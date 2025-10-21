# Dataview Plugin Interference Fix Script - Safe Backup + Comment main.js Replacement Lines
# Author: Obsidian Copilot | Ensure PowerShell Permissions Before Running

$vaultPath = "d:\OneDrive_RRXS\OneDrive\_RRXS_OBS"
$pluginFile = Join-Path $vaultPath ".obsidian\plugins\smart-connections\main.js"
$backupFile = "$pluginFile.backup"

# Check if file exists
if (-not (Test-Path $pluginFile)) {
    Write-Host "❌ File not found: $pluginFile" -ForegroundColor Red
    exit 1
}

# Step 1: Backup original file
Copy-Item $pluginFile $backupFile -Force
Write-Host "✅ Backup completed: $backupFile" -ForegroundColor Green

# Step 2: Read and modify content (comment the three if lines)
$content = Get-Content $pluginFile -Raw -Encoding UTF8

# Target pattern (same for lines 4881, 25845, 30060)
$pattern = 'if \(content\.includes\("```dataview"\)\) content = content\.replace\(/```dataview/g, "```\\dataview"\);'

$modified = $false
if ($content -match $pattern) {
    # Replace all occurrences with commented version
    $content = $content -replace $pattern, "// $&"  # $& is the full match
    $modified = $true
    Write-Host "✅ Commented Dataview replacement lines (all occurrences)" -ForegroundColor Green
}

# Extra handling: Comment line 35339 (dataview detection with some())
$extraPattern = 'if \(!opts\.calculating && raw\.split\("\n"\)\.some\(\(line\) => line\.startsWith\("```dataview"\)\)\) \{'
if ($content -match $extraPattern) {
    $content = $content -replace $extraPattern, "// $&"  # Comment the entire if
    $modified = $true
    Write-Host "✅ Commented extra detection line (line 35339)" -ForegroundColor Green
}

# Save modified content
Set-Content $pluginFile $content -Encoding UTF8
if ($modified) {
    Write-Host "✅ Modification completed: $pluginFile" -ForegroundColor Green
} else {
    Write-Host "⚠️ No matching lines found, plugin may be updated" -ForegroundColor Yellow
}

# Step 3: Next steps prompt
Write-Host "`n🚀 Fix completed! Please:" -ForegroundColor Cyan
Write-Host "1. Completely close and restart Obsidian" -ForegroundColor White
Write-Host "2. In Dataview settings, enable 'Enable JavaScript Queries'" -ForegroundColor White
Write-Host "3. Open a note, press Ctrl+E to switch to reading view and test Dataview" -ForegroundColor White
Write-Host "`nTo restore backup (if needed): Copy-Item '$backupFile' '$pluginFile' -Force" -ForegroundColor Yellow

Write-Host "`nTest example: In '所有AI对话索引.md', check if the search box renders." -ForegroundColor Cyanp