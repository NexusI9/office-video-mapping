cls
@echo off
echo. 
tasklist | find /i "node.exe" && taskkill /im node.exe /F || echo.
echo.
echo Starting Redbox Mapping Manager server...
echo. 
echo (Si le serveur ne se lance pas automatiquement apres 10 secondes, appuyez sur ENTRER)
cd /D V:
node "V:\Design\RedBox Media\Mapping\MapManager\app"