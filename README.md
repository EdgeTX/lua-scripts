# Lua-scripts

The goal for this repo is to have a central place to share example Lua scripts, host any 'new' scripts, and to document where to find Lua scripts that already exist, as well as any tips or tricks related to getting started with them.

Games and other fun Lua scripts are listed [seperately here](/games.md).

---

## ExpressLRS

### [ExpressLRS Configurator](https://www.expresslrs.org/3.0/quick-start/transmitters/lua-howto/)

LUA configurator for ExpressLRS hardware<br/>
<a href="https://www.expresslrs.org/3.0/quick-start/transmitters/lua-howto/">
<img src="https://www.expresslrs.org/assets/images/lua3.jpg" width="250">
<img src="https://www.expresslrs.org/assets/images/lua/config-bw.png" width="250">
</a>

<br/>

### [ExpressLRS Telemetry Widget (Betaflight & iNav)](https://github.com/ExpressLRS/ElrsTelemWidget)

Display ExpressLRS LinkStats telemetry as well as common Betaflight and iNav flight controller telemetry.<br/>
<a href="https://github.com/ExpressLRS/ElrsTelemWidget">
<img src="https://raw.githubusercontent.com/ExpressLRS/ElrsTelemWidget/main/docs/images/screen-2-1.png" width="250">
</a>

<br/>

## [ExpressLRS RF Telemetry Widget (for fixed wing/heli)](https://github.com/offer-shmuely/edgetx-x10-widgets/wiki/els_rf)

- Display **_RF Only_** telemetry for Planes/Heli/Glider (i.e. line of site)
- Display rf-rate / link-quality / power / rssi1 / rssi2
- Display **min & max** indicator
- **Post flight summary** (auto-detection end-of-flight)

<a href="https://github.com/offer-shmuely/edgetx-x10-widgets/wiki/els_rf"> 
    <img src="https://user-images.githubusercontent.com/7026911/257013252-cc7ac64c-2b1c-4bef-a3bb-2718fbf264ac.gif" width="400">
</a>

<br/>

## GPS

### [Yaapu telemetry widget](https://github.com/yaapu/FrskyTelemetryScript)

ArduPilot LUA telemetry script for color and B&W.<br/>
<a href="https://user-images.githubusercontent.com/30294218/198382377-cb48032f-ea5c-4f8d-aa12-f592c1e09358.png" target="_blank" title="Click for larger version"><img src="https://user-images.githubusercontent.com/30294218/198382377-cb48032f-ea5c-4f8d-aa12-f592c1e09358.png" width="250"></a>
<a href="https://user-images.githubusercontent.com/30294218/216000387-f330a204-b674-48ea-bdaf-64ec33871eb2.png" target="_blank" title="Click for larger version"><img src="https://user-images.githubusercontent.com/30294218/216000387-f330a204-b674-48ea-bdaf-64ec33871eb2.png" width="150"></a>
<a href="https://user-images.githubusercontent.com/30294218/215983189-06106fe8-b0d8-47f5-8e3f-e8d2472028ee.png" target="_blank" title="Click for larger version"><img src="https://user-images.githubusercontent.com/30294218/215983189-06106fe8-b0d8-47f5-8e3f-e8d2472028ee.png" width="212"></a>
<a href="https://user-images.githubusercontent.com/30294218/215983214-b11f53a6-90f4-40ba-a29d-90a58cf6f1ff.png" target="_blank" title="Click for larger version"><img src="https://user-images.githubusercontent.com/30294218/215983214-b11f53a6-90f4-40ba-a29d-90a58cf6f1ff.png" width="128"></a>

<br/>

### [Yaapu Horus Mapping Widget](https://github.com/yaapu/HorusMappingWidget)

Offline GPS Mapping Widget for Horus and T16 radios. It supports Ardupilot, iNAV, Betaflight, Crossfire and whatever FC or firmware that can send GPS info to EdgeTX.<br/>
<a href="https://user-images.githubusercontent.com/30294218/76712734-946a6500-671b-11ea-9fbc-6c779cf4d0b5.png" target="_blank" title="Click for larger version"><img src="https://user-images.githubusercontent.com/30294218/76712734-946a6500-671b-11ea-9fbc-6c779cf4d0b5.png" width="250"></a>

<br/>

### [GPS widget](https://github.com/moschotto/OpenTX_GPS_Telemetry)

GPS Telemetry Widget (B&W & Color). Shows total distance traveled, distance from home, as well as both home and last seen telemetry positions. Also logs to file, and has a log viewer so you don't have to worry about losing the coordinates if you turn the transmitter off.</br>
<a href="https://github.com/moschotto/OpenTX_GPS_Telemetry">
<img src="https://raw.githubusercontent.com/moschotto/OpenTX_GPS_Telemetry/main/media/description.png" width="250">
<img src="https://github.com/moschotto/OpenTX_GPS_Telemetry/raw/main/media/x9_GPS_screen.PNG" width="350">
</a>

<br/>

### [GPS Plus Code, Home Arrow and AvgBatt widgets](https://github.com/kristjanbjarni/opentx-widgets)

Collection of Colorlcd & B&W widgets.
For colorlcd includes GPS lat/long and Google Plus code widget, Home direction/distance widget, and average battery voltage widget.
For B&W includes GPS Telemetry screen, and Home distance telemetry screen.</br>
<a href="https://github.com/kristjanbjarni/opentx-widgets">
<img src="https://github.com/kristjanbjarni/opentx-widgets/raw/main/docs/images/GPS.png" width="250">
<img src="https://github.com/kristjanbjarni/opentx-widgets/raw/main/docs/images/AvgBatt.png" width="250">
<img src="https://github.com/kristjanbjarni/opentx-widgets/raw/main/docs/images/home_taranis.png" width="250">
</a>

<br/>

## Telemetery & Flight Controllers

### [Betaflight Setup](https://github.com/betaflight/betaflight-tx-lua-scripts)

The Betaflight LUA script allows you to change flight controller settings on your radio, such as PID, rates, VTX channels and power, and many more.<br/>
<a href="https://github.com/betaflight/betaflight-tx-lua-scripts">
<img src="https://oscarliang.com/ctt/uploads/2021/07/betaflight-lua-script-config-home-menu-screen-options.jpg" width="250">
</a>

<br/>

### [INAV Telemetry Flight Status](https://github.com/iNavFlight/OpenTX-Telemetry-Widget)

Shows you telementry and flight status information. Supports radios with color and black and white screens.<br/>
<a href="https://github.com/iNavFlight/OpenTX-Telemetry-Widget">
<img  src="https://github.com/teckel12/LuaTelemetry/raw/master/assets/iNavHorus.png" width="250">
<img src="https://github.com/teckel12/LuaTelemetry/raw/master/assets/iNavQX7.png" width="128">
</a>

<br/>

### [FM2M ToolBox](https://fm2m.online/toolbox-edgetx/)

Feature rich FM2M ToolBox is LUA App focusing on BetaFlight users. Provides dashboard with telemetry overview for all major RC Links, custom alerts , VTx info, GPS and much more. Supports radios with color and black and white screens.<br/>
<a href="https://fm2m.online/toolbox-edgetx/">
<img src="https://download.fm2m.online/remote/edgetx-lua-scripts/fm2m-toolbox-090-color-db.png" width="250">
<img src="https://download.fm2m.online/remote/edgetx-lua-scripts/fm2m-toolbox-090-color-vtx.png" width="250">
<img src="https://download.fm2m.online/remote/edgetx-lua-scripts/fm2m-toolbox-090-color-armstop.png" width="250">
<img src="https://download.fm2m.online/remote/edgetx-lua-scripts/fm2m-toolbox-090-color-gps.png" width="250">
<img src="https://download.fm2m.online/remote/edgetx-lua-scripts/fm2m-toolbox-090-color-sticks.png" width="250">
<img src="https://download.fm2m.online/remote/edgetx-lua-scripts/fm2m-toolbox-090-bw-db.png" width="250">
<img src="https://download.fm2m.online/remote/edgetx-lua-scripts/fm2m-toolbox-090-bw-vtx.png" width="250">
<img src="https://download.fm2m.online/remote/edgetx-lua-scripts/fm2m-toolbox-090-bw-armstop.png" width="250">
<img src="https://download.fm2m.online/remote/edgetx-lua-scripts/fm2m-toolbox-090-bw-dbgps.png" width="250">
<img src="https://download.fm2m.online/remote/edgetx-lua-scripts/fm2m-toolbox-090-bw-sticks.png" width="250">
</a>

<br/>

### [FM2M Digital Clock](https://fm2m.online/digital-clock-edgetx/)

Configurable EdgeTX widget that shows nifty Digital Clock.<br/>
<a href="https://fm2m.online/digital-clock-edgetx/">
<img src="https://download.fm2m.online/remote/edgetx-lua-scripts/fm2m-dclock-10-1.png" width="400">
<img src="https://download.fm2m.online/remote/edgetx-lua-scripts/fm2m-dclock-10-2.png" width="400">
</a>
<br/>

### [FM2M Widgets Pack](https://fm2m.online/addons-edgetx/#WPack)

Enhanced Model, Timer, Channels and Analog Clock widgets.<br/>
<a href="https://fm2m.online/addons-edgetx/#WPack">
<img src="https://download.fm2m.online/remote/edgetx-lua-scripts/fm2m-widgets-pack-021-promo.png" width="400">
</a>

<br/>

### [TBS Agent Lite](https://www.team-blacksheep.com/products/prod:agentx)

LUA configurator for numerous TBS products. Use this instead of Crossfire lua.

## Other

### [Show It All](https://rc-soar.com/opentx/lua/showitall/index.htm)

ShowItAll displays various information in a single pane.<br/>
<a href="https://rc-soar.com/opentx/lua/showitall/index.htm">
<img src="https://rc-soar.com/opentx/lua/showitall/sia.png" width="250">
</a>

<br/>

### [vu fullscreen image viewer widget for big screens](https://www.schleth.com/fpv/vu-a-simple-image-viewer-for-edgetx-radios-with-big-screens-2113.html)

View fullscreen images with layout information or photos, cycle through them and have quick access to your favourite one.<br/>
<a href="https://www.schleth.com/fpv/vu-a-simple-image-viewer-for-edgetx-radios-with-big-screens-2113.html">
<img src="https://www.schleth.com/wp-content/uploads/vu-screen1.jpg"  width="250">
<img src="https://www.schleth.com/wp-content/uploads/diagram.jpg"  width="250">
<img src="https://www.schleth.com/wp-content/uploads/vu_license.jpg"  width="250">
<img src="https://www.schleth.com/wp-content/uploads/vu-screen2.jpg"  width="250">
</a>

<br/>

### [EdgeTX Goodies](https://github.com/MadMonkey87/EdgeTX-Goodies)

Some widgets, themes and other scripts for EdgeTX<br/>
<a href="https://github.com/MadMonkey87/EdgeTX-Goodies">
<img src="https://github.com/MadMonkey87/EdgeTX-Goodies/raw/main/SCREENSHOTS/screenshot_tx16s_22-08-02_18-49-59.png"  width="250">
<img src="https://github.com/MadMonkey87/EdgeTX-Goodies/raw/main/SCREENSHOTS/screenshot_tx16s_22-08-02_18-52-08.png"  width="250">
<img src="https://github.com/MadMonkey87/EdgeTX-Goodies/raw/main/SCREENSHOTS/screenshot_tx16s_22-08-07_10-35-43.png"  width="250">
<img src="https://github.com/MadMonkey87/EdgeTX-Goodies/raw/main/SCREENSHOTS/screenshot_tx16s_22-08-09_19-54-00.png"  width="250">
</a>

<br/>

### [ImpExp](https://github.com/forbesmyester/EdgeTX-ImpExp)

Basic and slightly incomplete on-radio import / export functionality for EdgeTX. Can be used to move functions / logical switches / mixes etc between models.

<a href="https://github.com/forbesmyester/EdgeTX-ImpExp">
<img src="https://raw.githubusercontent.com/forbesmyester/EdgeTX-ImpExp/main/Screenshot.png" width="480">
</a>

### [Switch2 widget](https://repository.justfly.solutions/index.php?view=product&id=115:switch-config)

Widget that shows switch positions with customisable icons. Shows all switches with different icons for every switch position.</br>
Links: [JustFly](https://repository.justfly.solutions/index.php?view=product&id=115:switch-config), [RCGroups](https://www.rcgroups.com/forums/showpost.php?p=50176699&postcount=4012)

<a href="https://www.rcgroups.com/forums/showpost.php?p=47009445&postcount=3793">
    <img src="https://static.rcgroups.net/forums/attachments/5/9/3/7/9/7/a14905909-20-screenshot_tx16s_21-04-25_20-19-54.png" width="250">
    <img src="https://static.rcgroups.net/forums/attachments/5/9/3/7/9/7/a14905913-151-screenshot_tx16s_21-04-25_20-19-25.png" width="250">
</a>
<br/>

### [Multi Protocol Module Tools](https://github.com/pascallanger/DIY-Multiprotocol-TX-Module/tree/master/Lua_scripts)

Scripts to complement the Multi Protocol Module, such as allowing you to configure certain aspects of the module, automacitally name channels, do DSM forward programming, as well as other protocol specific tasks.</br>
<a href="https://github.com/pascallanger/DIY-Multiprotocol-TX-Module/tree/master/Lua_scripts">
<img src="https://img.youtube.com/vi/lGyCV2kpqHU/0.jpg" width="250">
<img src="https://img.youtube.com/vi/L58ayXuewyA/0.jpg" width="250">
<img src="https://img.youtube.com/vi/81wd8NlF3Qw/0.jpg" width="250">
</a>
<br/>

### [Spektrum DSM Tools](https://github.com/frankiearzu/DSMTools)

Scripts to use with Spektrum Receivers. It has easy to install zip files versions of:

- DSM Forward Programming (In collaboration with Multi-Module)
- Spektrum Telemetry Scripts, Including TextGen for AVIAN ESC programming. Will become telemetry widgets in the future.
  - Smart RXs (AR631,AR637, etc)
  - Blade Heli helpers (AR636 based)
- Interim EdgeTX Firmware with latest (but tested) changes for Spektrum Sensors and TextGen (Official EdgeTx 2.8.1 + only Spektrum Telemetry changes). This change will be included in EdgeTx 2.9.0
  </br></br>
  <a href="https://github.com/frankiearzu/DSMTools">
  <img src="https://user-images.githubusercontent.com/32604366/230751340-dd118f36-1884-405b-b12b-81cba16c7321.png" width="250"/>
  <img src="https://user-images.githubusercontent.com/32604366/230751281-0c71ff4a-179f-41fd-9290-302a6e0fe821.png" width="250"/>
  <img src="https://user-images.githubusercontent.com/32604366/230751350-59070e75-afa3-439b-8902-bc7b3b901084.png" width="250"/>
  <img src="https://user-images.githubusercontent.com/32604366/230751370-b4e4355f-a3d2-4c44-aa1a-57861f1ff3da.png" width="250"/>
  <img src="https://user-images.githubusercontent.com/32604366/230123260-614f4e5e-9546-4439-9196-db885894083f.jpg" width="250"/>
  <br>
  <img src="https://user-images.githubusercontent.com/32604366/230751833-e92d3eae-2782-4009-a3dc-63ce893f2a38.png" width="250"/>
  <img src="https://user-images.githubusercontent.com/32604366/230751488-70b396b7-f08e-4152-a516-d355b3cf4001.png" width="250"/>
  </a>

<br/>

### [Log Viewer](https://github.com/offer-shmuely/edgetx-x10-scripts/wiki/LogViewer)

Nice presentation of log file on the field<br>
no computer needed for logs anymore.

<a href="https://github.com/offer-shmuely/edgetx-x10-scripts/wiki/LogViewer"> 
    <img src="https://user-images.githubusercontent.com/7026911/193412100-5cdb3b51-1e33-4eaa-94cd-6ca07aede43b.gif" width="480">
</a>

**Selecting files & columns**

<a href="https://github.com/offer-shmuely/edgetx-x10-scripts/wiki/LogViewer"> 
    <img src="https://user-images.githubusercontent.com/7026911/193409667-75e314ab-06cb-4136-a18f-88647755c755.png" width="200">
    <img src="https://user-images.githubusercontent.com/7026911/193409686-4fff1c25-229a-419e-8a2a-e64e703a4fc2.png" width="200">
    <img src="https://user-images.githubusercontent.com/7026911/193409707-1020eebe-f2af-4d83-b0a9-a138aad4aca3.png" width="200">
    <img src="https://user-images.githubusercontent.com/7026911/193409719-bd1b2f27-ad19-452b-b042-bba85822a5c1.png" width="200">
</a>

### [Log Viewer (BW only)](https://github.com/nikbg3/EdgeTXLogViewerBW)

Simple EdgeTX LUA script for BW radios to read logs files on the display. Rotary wheel is used to change the read value. Back is used to switch between modes. i.e., changing columns, rows or files.

<a href="https://github.com/nikbg3/EdgeTXLogViewerBW">
<img src="https://github.com/user-attachments/assets/43b69333-3dcc-4186-a3e8-68544e4cb3fc">
</a>

### [FlyLog](https://github.com/JohnnyCarvi/flylog_edgetx)

This script logs the arming and disarming events of your model, along with date/time and the model name and creates an CSV Log. Really Simple.

<a href="https://github.com/JohnnyCarvi/flylog_edgetx">
  <img src="https://raw.githubusercontent.com/JohnnyCarvi/flylog_edgetx/refs/heads/main/screenshots/1_special_functions_tab.png" width="250">
  <img src="https://github.com/JohnnyCarvi/flylog_edgetx/blob/main/screenshots/2_special_functions.png?raw=true" width="250">
</a>

### [Widget for Voltage and Current Telemetry](https://github.com/fdm225/mahRe2)

Displays various battery related data.<br/>
<a href="https://github.com/fdm225/mahRe2/raw/main/README.md">
  <img src="https://static.rcgroups.net/forums/attachments/6/4/3/0/2/9/a16811177-105-mAhRe2_full_screen.png" width="250">
  <img src="https://static.rcgroups.net/forums/attachments/6/4/3/0/2/9/a16811165-83-mAhRe2_quarter.png" width="250">
  <img src="https://static.rcgroups.net/forums/attachments/6/4/3/0/2/9/a16811163-82-mAhRe2_settings.png" width="250">
  <img src="https://static.rcgroups.net/forums/attachments/6/4/3/0/2/9/a16811169-236-mAhRe2_mAh_sensor.png" width="250">
</a>

### [Quad Telemetry Dashboard (BW only)](https://github.com/mvaldesshc/advanced-edgetx-dashboard)

LUA-based dashboard (only for black-and-white display radios).<br/>
<a href="https://github.com/mvaldesshc/advanced-edgetx-dashboard">
  <!-- <img src="https://i.postimg.cc/Jz1CdwTG/opentx-quad-telemetry.gif"> -->
</a>

<br/>

### [TSwitch Widget](https://github.com/Ziege-One/TSwitch)

Widget for color screen radios that allows touch buttons via logical switches (in German).<br/>
<a href="https://github.com/Ziege-One/TSwitch">
  <img src="https://raw.githubusercontent.com/Ziege-One/TSwitch/main/docs/fullscreen.png" width="250">
  <img src="https://raw.githubusercontent.com/Ziege-One/TSwitch/main/docs/widget_status.png" width="250">
</a>

### [Lap Timer](https://github.com/RadioMasterRC/EdgeTX-LapTimer)

Advanced lap timer script using as little controls as possible. It stores race and lap data for analysis back at the computer.<br/>
<a href="https://github.com/RadioMasterRC/EdgeTX-LapTimer">
  <img src="https://github.com/RadioMasterRC/EdgeTX-LapTimer/raw/master/ScreenShot/screen-1.bmp" height="128px"/>
  <img src="https://github.com/RadioMasterRC/EdgeTX-LapTimer/raw/master/ScreenShot/screen-2.bmp" height="128px"/>
  <img src="https://github.com/RadioMasterRC/EdgeTX-LapTimer/raw/master/ScreenShot/screen-3.bmp" height="128px"/>
  <br>
  <br>
  <img src="https://github.com/RadioMasterRC/EdgeTX-LapTimer/raw/master/ScreenShot/screen-4.bmp" height="128px"/>
  <img src="https://github.com/RadioMasterRC/EdgeTX-LapTimer/raw/master/ScreenShot/screen-5.bmp" height="128px"/>
  <img src="https://github.com/RadioMasterRC/EdgeTX-LapTimer/raw/master/ScreenShot/screen-6.bmp" height="128px"/>
</a>

### [F3A Caller](https://github.com/jrwieland/F3A)

Caller for practicing F3A pattern - Updated to 2024 Season<br/>
<a href="https://github.com/jrwieland/F3A">
  <img src="https://github.com/jrwieland/F3A/raw/main/Screenshots/p-21.png">
  <img src="https://github.com/jrwieland/F3A/raw/main/Screenshots/f25.png">
</a>

### [TaraniTunes](https://github.com/jrwieland/TaraniTunes-v4.x)

Enhanced music player for OpenTX & EdgeTX radios Multiple Playlists allow you to listen to your music while flying Your RC<br/>
<a href="https://github.com/jrwieland/TaraniTunes-v4.x">
<img src="https://github.com/jrwieland/TaraniTunes-v4.x/raw/master/Color%20Screen%20Widget/Screenshots3/Features.png" width="500">
<br>
<img src="https://github.com/jrwieland/TaraniTunes-v4.x/raw/master/Color%20Screen%20Widget/Screenshots3/Colorscreen.PNG" width="300">
<img src="https://github.com/jrwieland/TaraniTunes-v4.x/raw/master/Screenshots/TaraniTunesQX7.PNG" width="300">
<img src="https://github.com/jrwieland/TaraniTunes-v4.x/raw/master/Screenshots/Customize.PNG" width="300">
</a>

### [GPS QR Code generator](https://github.com/alufers/edgetx-gps-qrcode)

Generates a QR code of last GPS coordinates received (for black-and-white screen radios)<br/>
<a href="https://github.com/alufers/edgetx-gps-qrcode">
<img src="https://raw.githubusercontent.com/alufers/edgetx-gps-qrcode/master/docs/sim-screenshot.png" width="500">
<br>
<img src="https://raw.githubusercontent.com/alufers/edgetx-gps-qrcode/master/docs/x9dp-screenshot.png" width="500">
</a>

### [Battery Percentage and mAh Used](https://github.com/jrwieland/Battery-mAh)

Widget to display the levels of Lipo/HV-Lipo battery with mAh used based on battery voltage from 'Cels' sensor (FLVSS)<br/>
<a href="https://github.com/jrwieland/Battery-mAh">
<img src="https://github.com/jrwieland/Battery-mAh/raw/main/Screenshots/4_2lipo.png" width="400">
<img src="https://github.com/jrwieland/Battery-mAh/raw/main/Screenshots/4_35lipo.png" width="400">  
</a>

### [TxBatTele](https://github.com/derelict/TxBatTele)

Battery and Telemetry Monitoring LUA Widget which tries to rely as less as possible on radio settings (Everything is defined in the Script). So no need for "manual" Logical Switches or Custom Functions.

<a href="https://github.com/derelict/TxBatTele">
<img src="https://github.com/derelict/TxBatTele/raw/main/screenshots/demovid.gif">
</a>

### [SwitchOverview](https://github.com/druckgott/getswitchesWdgets/)

A simple widget to display switches which are configured in special function and have a PLAY_TRACK behind.

<a href="https://github.com/druckgott/getswitchesWdgets">
<img src="https://github.com/druckgott/getswitchesWdgets/raw/main/doc/img/example1.png">
</a>

### [GPS Viewer](https://github.com/ktaliaferro/gps-viewer)

Plot logged flight telemetry data on a map of your airfield.

<a href="https://github.com/ktaliaferro/gps-viewer">
<img src="https://github.com/ktaliaferro/gps-viewer/raw/master/images/screenshot_points.png">
</a>

### [GPS Logger (BW only)](https://github.com/poweredjj/gpslog)

Log each flight GPS coordinates to a separate GPX file.

<a href="https://github.com/poweredjj/gpslog">
<img src="https://github.com/poweredjj/gpslog/raw/main/screenshot.png"  width="300">
</a>



<br/><br/><br/>

## [Rotorflight Dashboard widget (for Heli flights)](https://github.com/offer-shmuely/rf2-touch-suite-edgeTx/wiki/widget-%E2%80%90-rf2_dash2)

* part of the rf2-touch-suite for edgexTx
* design for [rotorflight2](https://www.rotorflight.org/)
* the widget have 3 types of views

<img src="https://github.com/user-attachments/assets/7a98c153-4e23-4344-b4e4-c2acba6d116c" width="60">

<br>
dashboard type 1 

<a href="https://github.com/offer-shmuely/rf2-touch-suite-edgeTx/wiki/widget-%E2%80%90-rf2_dash2"> 
    <img src="https://github.com/user-attachments/assets/9b95d285-7881-4286-883a-ad68321e9f7f" width="550">
</a>

<br>
dashboard type 2

<a href="https://github.com/offer-shmuely/rf2-touch-suite-edgeTx/wiki/widget-%E2%80%90-rf2_dash2"> 
    <img src="https://github.com/user-attachments/assets/6c051557-f94b-432d-bda1-fcacb36c9c0d" width="550">
</a>

<br>
dashboard style 3

<a href="https://github.com/offer-shmuely/rf2-touch-suite-edgeTx/wiki/widget-%E2%80%90-rf2_dash2"> 
    <img src="https://github.com/user-attachments/assets/d2bcee9d-e5be-42a0-b2cc-868a900c5040" width="550">
</a>



<br/><br/><br/>



