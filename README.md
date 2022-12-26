# Lua-scripts

The goal for this repo is to have a central place to share example Lua scripts, host any 'new' scripts, and to document where to find Lua scripts that already exist, as well as any tips or tricks related to getting started with them.

Games and other fun Lua scripts are listed [seperately here](/games.md).

List of Lua-scripts:
## [ExpressLRS](https://www.expresslrs.org/3.0/quick-start/transmitters/lua-howto/)
LUA configurator for ExpressLRS hardware<br/>
<a href="https://www.expresslrs.org/3.0/quick-start/transmitters/lua-howto/">
    <img src="https://www.expresslrs.org/3.0/assets/images/lua3.jpg" width="250">>
    <img src="https://www.expresslrs.org/3.0/assets/images/lua/config-bw.png" width="250">
</a>

### [ExpressLRS Telemetry Widget](https://github.com/ExpressLRS/ElrsTelemWidget) 
Display ExpressLRS LinkStats telemetry as well as common Betaflight and iNav flight controller telemetry.
<a href="https://github.com/ExpressLRS/ElrsTelemWidget"> 
    <img src="https://raw.githubusercontent.com/ExpressLRS/ElrsTelemWidget/main/docs/images/screen-2-1.png" width="250">
</a>

## [Yaapu telemetry widget](https://github.com/yaapu/FrskyTelemetryScript)
ArduPilot LUA telemetry script for color and B&W. For color screen radios, use [Yaapu's development branch](https://github.com/yaapu/FrskyTelemetryScript/tree/dev) instead, which has EdgeTX color fixes (these are expected to be available from 1.9.6 release of Yaapu LUA telemetry widget).<br/>
<a href="https://user-images.githubusercontent.com/30294218/135524984-f732af4a-490b-4ce2-b4dc-9c8bfe1f6d4c.png" target="_blank" title="Click for larger version"><img src="https://user-images.githubusercontent.com/30294218/135524984-f732af4a-490b-4ce2-b4dc-9c8bfe1f6d4c.png" width="250"></a>
<img src="https://raw.githubusercontent.com/yaapu/FrskyTelemetryScript/master/TARANIS/IMAGES/x9d.png" width="212"></a>
<img src="https://raw.githubusercontent.com/yaapu/FrskyTelemetryScript/master/TARANIS/IMAGES/x7.png" width="128"></a>

## [Yaapu Horus Mapping Widget for iNAV/Betaflight](https://github.com/yaapu/HorusMappingWidget)
Offline GPS Mapping Widget for Horus and T16 radios. It supports Ardupilot, iNAV, Betaflight, Crossfire and whatever FC or firmware that can send GPS info to OpenTX.
<br/>Presently use [rotorman's fork](https://github.com/rotorman/HorusMappingWidget/tree/etx-colors/HORUS/SOURCES/SRC) instead, which has EdgeTX color fixes.
<br/><img src="https://user-images.githubusercontent.com/30294218/76712734-946a6500-671b-11ea-9fbc-6c779cf4d0b5.png" width="250"></a>

## [GPS widget](https://github.com/moschotto/OpenTX_GPS_Telemetry)
GPS Telemetry Widget (B&W & Color). Shows total distance traveled, distance from home, as well as both home and last seen telemetry positions. Also logs to file, and has a log viewer so you don't have to worry about losing the coordinates if you turn the transmitter off.</br>
<a href="https://github.com/moschotto/OpenTX_GPS_Telemetry">
    <img src="https://raw.githubusercontent.com/moschotto/OpenTX_GPS_Telemetry/main/media/description.png" width="250">
    <img src="https://github.com/moschotto/OpenTX_GPS_Telemetry/blob/main/media/x9_GPS_screen.PNG" width="350">
</a>

## [GPS Plus Code, Home Arrow and AvgBatt widgets](https://github.com/kristjanbjarni/opentx-widgets)
Collection of Colorlcd & B&W widgets. 
For colorlcd includes GPS lat/long and Google Plus code widget, Home direction/distance widget, and average battery voltage widget.
For B&W includes GPS Telemetry screen, and Home distance telemetry screen.</br>
<a href="https://github.com/kristjanbjarni/opentx-widgets">
    <img src="https://github.com/kristjanbjarni/opentx-widgets/blob/main/docs/images/GPS.png" width="250">
    <img src="https://github.com/kristjanbjarni/opentx-widgets/raw/main/docs/images/AvgBatt.png" width="250">
    <img src="https://github.com/kristjanbjarni/opentx-widgets/raw/main/docs/images/home_taranis.png" width="250">
</a>

## [Switch2 widget](https://repository.justfly.solutions/index.php?view=product&id=115:switch-config)
Widget that shows switch positions with customisable icons. Shows all switches with different icons for every switch position.</br>
Links: [JustFly](https://repository.justfly.solutions/index.php?view=product&id=115:switch-config), [RCGroups](https://www.rcgroups.com/forums/showpost.php?p=50176699&postcount=4012)

<a href="https://www.rcgroups.com/forums/showpost.php?p=47009445&postcount=3793">
    <img src="https://static.rcgroups.net/forums/attachments/5/9/3/7/9/7/a14905909-20-screenshot_tx16s_21-04-25_20-19-54.png" width="250">
    <img src="https://static.rcgroups.net/forums/attachments/5/9/3/7/9/7/a14905913-151-screenshot_tx16s_21-04-25_20-19-25.png" width="250">
</a>

## [Multi Protocol Module](https://github.com/pascallanger/DIY-Multiprotocol-TX-Module/tree/master/Lua_scripts)
Scripts to complement the Multi Protocol Module, such as allowing you to configure certain aspects of the module, automacitally name channels, do DSM forward programming, as well as other protocol specific tasks.</br>
<a href="https://github.com/pascallanger/DIY-Multiprotocol-TX-Module/tree/master/Lua_scripts">
    <img src="https://camo.githubusercontent.com/dfaff56a2701fde5d8b70af711536a7f59234ab0dc600f8f7a67661ff6cef215/68747470733a2f2f696d672e796f75747562652e636f6d2f76692f6c47794356326b707148552f302e6a7067" width="250">
    <img src="https://camo.githubusercontent.com/d1197777b39f854c1c87a3a3220f03ea750bf095b49b90c61fe0ede65a124d80/68747470733a2f2f696d672e796f75747562652e636f6d2f76692f4c353861795875657779412f302e6a7067" width="250">
    <img src="https://camo.githubusercontent.com/86dd3c9e3976aa9224378573bdddd163db07b062964a925399fff2e41eba154a/68747470733a2f2f696d672e796f75747562652e636f6d2f76692f736a49614477356a396e452f302e6a7067" width="250">
</a>

## [Betaflight LUA Script](https://github.com/betaflight/betaflight-tx-lua-scripts)
The Betaflight LUA script allows you to change flight controller settings on your radio, such as PID, rates, VTX channels and power, and many more.<br/>
<a href="https://github.com/betaflight/betaflight-tx-lua-scripts">
    <img src="https://oscarliang.com/ctt/uploads/2021/07/betaflight-lua-script-config-home-menu-screen-options.jpg" width="250">
</a>

## [INAV Lua Telemetry Flight Status](https://github.com/iNavFlight/OpenTX-Telemetry-Widget)
Shows you telementry and flight status information. Supports radios with color and black and white screens.<br/>
<a href="https://github.com/iNavFlight/OpenTX-Telemetry-Widget">
    <img  src="https://github.com/teckel12/LuaTelemetry/blob/master/assets/iNavHorus.png" width="250">
    <img src="https://github.com/teckel12/LuaTelemetry/blob/master/assets/iNavQX7.png" width="128">
</a>

## [FM2M ToolBox](http://fm2m.jimb40.com/ToolBox.html)
Feature rich FM2M ToolBox is LUA App focusing on BetaFlight users. Provides dashboard with telemetry overview for all major RC Links,  custom alerts , VTx info and much more. Supports radios with color and black and white screens.<br/>
<a href="http://fm2m.jimb40.com/ToolBox.html">
    <img src="http://fm2m.jimb40.com/pub/FM2M_ToolBox073_db.png" width="250">
    <img src="http://fm2m.jimb40.com/pub/FM2M_ToolBox073_cfg.png" width="250">
    <img src="http://fm2m.jimb40.com/pub/FM2M_ToolBox073_vtx.png" width="250">
</a>

## [FM2M Widgets Pack](http://fm2m.jimb40.com/download.html)
Enhanced Model, Timer, Channels and Analog Clock widgets.<br/>
<a href="http://fm2m.jimb40.com/download.html">
    <img src="http://fm2m.jimb40.com/assets/images/fm2m-widget-pack-155327-480x272.png" width="250">
    <img src="http://fm2m.jimb40.com/assets/images/fm2m-widget-pack-132700-480x272.png" width="250">
    <img src="http://fm2m.jimb40.com/assets/images/fm2m-widget-pack-155436-480x272.png" width="250">
    <br/>
    <img src="http://fm2m.jimb40.com/assets/images/fm2m-widget-clock-22-00-9-480x272.png" width="250">
</a>

## [TBS Agent Lite](https://www.team-blacksheep.com/products/prod:agentx)
LUA configurator for numerous TBS products. Use this instead of Crossfire lua.<br/>
<a href="https://www.team-blacksheep.com/products/prod:agentx">
    <img src="https://www.team-blacksheep.com/img/gallery/conIkNCQ.jpg" width="250">
    <img src="https://www.team-blacksheep.com/img/gallery/scressen-2022-02-23-181848.jpg" width="250">
</a>

## [Show It All](https://rc-soar.com/opentx/lua/showitall/index.htm)
ShowItAll displays various information in a single pane.<br/>
<a href="https://rc-soar.com/opentx/lua/showitall/index.htm">
    <img src="https://rc-soar.com/opentx/lua/showitall/sia.png" width="250">
</a>

## [vu fullscreen image viewer widget for big screens](https://www.schleth.com/fpv/vu-a-simple-image-viewer-for-edgetx-radios-with-big-screens-2113.html)
View fullscreen images with layout information or photos, cycle through them and have quick access to your favourite one.<br/>
<a href="https://www.schleth.com/fpv/vu-a-simple-image-viewer-for-edgetx-radios-with-big-screens-2113.html">
    <img src="https://www.schleth.com/wp-content/uploads/vu-screen1.jpg"  width="250">
    <img src="https://www.schleth.com/wp-content/uploads/diagram.jpg"  width="250">
    <img src="https://www.schleth.com/wp-content/uploads/vu_license.jpg"  width="250">
    <img src="https://www.schleth.com/wp-content/uploads/vu-screen2.jpg"  width="250">
</a>

## [EdgeTX Goodies](https://github.com/MadMonkey87/EdgeTX-Goodies)
Some widgets, themes and other scripts for EdgeTX<br/>
<a href="https://github.com/MadMonkey87/EdgeTX-Goodies">
    <img src="https://github.com/MadMonkey87/EdgeTX-Goodies/blob/main/SCREENSHOTS/screenshot_tx16s_22-08-02_18-49-59.png"  width="250">
    <img src="https://github.com/MadMonkey87/EdgeTX-Goodies/blob/main/SCREENSHOTS/screenshot_tx16s_22-08-02_18-52-08.png"  width="250">
    <img src="https://github.com/MadMonkey87/EdgeTX-Goodies/blob/main/SCREENSHOTS/screenshot_tx16s_22-08-07_10-35-43.png"  width="250">
    <img src="https://github.com/MadMonkey87/EdgeTX-Goodies/blob/main/SCREENSHOTS/screenshot_tx16s_22-08-09_19-54-00.png"  width="250">
</a>

## [EdgeTx Log Viewer](https://github.com/offer-shmuely/edgetx-x10-scripts/wiki/LogViewer)
The **_LogViewer_** read and present up to 4 columns from a log file.<br/>

<a href="https://github.com/offer-shmuely/edgetx-x10-scripts/wiki/LogViewer"> 
    <img src="https://user-images.githubusercontent.com/7026911/193412100-5cdb3b51-1e33-4eaa-94cd-6ca07aede43b.gif" width="400">
</a>

###### Selecting files & columns
<a href="https://github.com/offer-shmuely/edgetx-x10-scripts/wiki/LogViewer"> 
    <img src="https://user-images.githubusercontent.com/7026911/193409667-75e314ab-06cb-4136-a18f-88647755c755.png" width="200">
    <img src="https://user-images.githubusercontent.com/7026911/193409686-4fff1c25-229a-419e-8a2a-e64e703a4fc2.png" width="200">
    <img src="https://user-images.githubusercontent.com/7026911/193409707-1020eebe-f2af-4d83-b0a9-a138aad4aca3.png" width="200">
    <img src="https://user-images.githubusercontent.com/7026911/193409719-bd1b2f27-ad19-452b-b042-bba85822a5c1.png" width="200">
</a>

## [Widget for Voltage and Current Telemetry](https://github.com/fdm225/mahRe2)
Displays various battery related data.<br/>
<a href="https://github.com/fdm225/mahRe2/blob/main/README.md">
    <img src="https://static.rcgroups.net/forums/attachments/6/4/3/0/2/9/a16811177-105-mAhRe2_full_screen.png" width="250">
    <img src="https://static.rcgroups.net/forums/attachments/6/4/3/0/2/9/a16811165-83-mAhRe2_quarter.png" width="250">
    <img src="https://static.rcgroups.net/forums/attachments/6/4/3/0/2/9/a16811163-82-mAhRe2_settings.png" width="250">
    <img src="https://static.rcgroups.net/forums/attachments/6/4/3/0/2/9/a16811169-236-mAhRe2_mAh_sensor.png" width="250">
</a>
