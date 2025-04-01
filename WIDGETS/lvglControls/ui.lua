-- WM EdgeTx LUA 
-- Copyright (C) 2016 - 2025 Wilhelm Meier <wilhelm.wm.meier@googlemail.com>
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.
--

local zone, options, name, dir = ...
local widget = {}
widget.options = options;
widget.zone = zone;
widget.name = name;

local TYPE_BUTTON    = 1;
local TYPE_TOGGLE    = 2;
local TYPE_MOMENTARY = 3;

local serialize = loadScript(dir .. "tableser.lua")();

widget.ui = nil;

local hasVirtualInputs = (getVirtualSwitch ~= nil);

local function bool2int(b)
    if (b) then 
        return 1;
    end
    return 0;
end

local function int2bool(v)
    if (v > 0) then
        return true;
    end
    return false;
end

local settings = {};
local state = {};
local settingsFilename = dir .. model.getInfo().name .. "_" .. widget.options.Name .. ".lua";
local settingsVersion = 16;

local function getVSwitch(i)
    if (hasVirtualInputs) then
        return getVirtualSwitch(i);
    end
    return false;
end

local function setVSwitch(i, v)
    if (hasVirtualInputs) then
        setVirtualSwitch(i, v);
    end
end

local function setVInput(i, v)
    if (settings.sliders[i].useShm > 0) then
        setShmVar(settings.sliders[i].shm, v);
    else
        if (hasVirtualInputs) then
            setVirtualInput(settings.sliders[i].vin, v);
            state.values[i] = v;
        end    
    end
end

local function getVInput(i)
    if (settings.sliders[i].useShm > 0) then 
        return getShmVar(settings.sliders[i].shm); 
    else 
        return state.values[i]; 
    end;
end

local function activateVInput(i, b)
    if (hasVirtualInputs) then
        activateVirtualInput(settings.sliders[i].vin, b);        
    end
end

local function activateVSwitch(i, b)
    if (hasVirtualInputs) then
        activateVirtualSwitch(settings.buttons[i].vs, b);        
    end
end

local function buttonToggle(i)
    state.buttons[i] = not state.buttons[i]; 
    setVSwitch(settings.buttons[i].vs, state.buttons[i]); 
    if (state.buttons[i]) then 
        return 1; 
    end; 
    return 0; 
end

local function buttonSet(i, v)
    state.buttons[i] = v; 
    setVSwitch(settings.buttons[i].vs, state.buttons[i]); 
    if (state.buttons[i]) then 
        return 1; 
    end; 
    return 0; 
end

local function saveSettings() 
    serialize.save(settings, settingsFilename);
end

local function resetSlider(i)
    settings.sliders[i] = { name = "VS" .. i, shm = i, vin = i, 
                            useShm = bool2int(not hasVirtualInputs), 
                            width = (LCD_W - 20) / settings.numberOfSliders,
                            color = COLOR_THEME_SECONDARY3, textColor = COLOR_THEME_PRIMARY3, font = 0 };
    state.values[i] = 0;
end

local function resetButton(i) 
    settings.buttons[i] = { name = "Button" .. i, type = TYPE_BUTTON; width = (LCD_W - 20) / 4, vs = i,
    color = COLOR_THEME_SECONDARY3, textColor = COLOR_THEME_PRIMARY3, font = 0 };
    state.buttons[i] = getVSwitch(settings.buttons[i].vs);
end

local function resetSettings()
    settings.version = settingsVersion;
    settings.numberOfSliders = 6;
    settings.sliders = {};
    state.values = {};
    for i = 1, settings.numberOfSliders do
        resetSlider(i);
    end
    settings.numberOfButtons = 6;
    settings.buttons = {};
    state.buttons = {};
    for i = 1, settings.numberOfButtons do
        resetButton(i);
    end
    settings.momentaryButton_radius = 20;
end
resetSettings();

local function askClose()
    lvgl.confirm({title = "Exit", message = "Really exit?", confirm = (function() saveSettings(); lvgl.exitFullScreen(); end) })
end
  
local function createSlider(i)    
    return { type = "box", flexFlow = lvgl.FLOW_COLUMN, w = settings.sliders[i].width, children = {
            { type = "label", text = settings.sliders[i].name, color = settings.sliders[i].textColor, font = settings.sliders[i].font},
            { type = "verticalSlider", min = -1024, max = 1024, h = 180,
                get = (function() return getVInput(i); end),
                set = (function(v) setVInput(i, v); end),
                color = settings.sliders[i].color
            },
            { type = "label", text = (function() return math.floor(getVInput(i) / 10.24 + 0.5) .. "%"; end)}
            }
        };
end

local function createSliders() 
    local children = {};
    for i = 1, settings.numberOfSliders do
        children[#children+1] = createSlider(i);
        if (i < settings.numberOfSliders) then
            children[#children+1] = {type = "vline", h = 100, w = 1};
        end
    end
    return children;
end

local function createButton(i)
    if (settings.buttons[i].type == TYPE_BUTTON) then
        return {type = "button", text = settings.buttons[i].name, w = settings.buttons[i].width,
            color = settings.buttons[i].color, textColor = settings.buttons[i].textColor, font = settings.buttons[i].font,
            checked = state.buttons[i],
            press = (function() return buttonToggle(i); end),
        };
    elseif (settings.buttons[i].type == TYPE_MOMENTARY) then
        return { type = "momentaryButton", text = settings.buttons[i].name, 
        w = settings.buttons[i].width, 
        cornerRadius = settings.momentaryButton_radius,
        color = settings.buttons[i].color, textColor = settings.buttons[i].textColor, font = settings.buttons[i].font,
        press = (function() buttonSet(i, true); end),
        release = (function() buttonSet(i, false); end)
    }
    elseif (settings.buttons[i].type == TYPE_TOGGLE) then
        return {type = "box", flexFlow = lvgl.FLOW_ROW, children = {
               {type = "label", text = settings.buttons[i].name, w = settings.buttons[i].width / 2,
                                color = settings.buttons[i].textColor, font = settings.buttons[i].font},
               {type = "toggle", get = (function() if (state.buttons[i]) then return 1; else return 0; end; end), 
                                 set = (function(v) if (v > 0) then buttonSet(i, true); else buttonSet(i, false); end; end), 
                                 w = settings.buttons[i].width / 2, color = settings.buttons[i].color }
        }};
    end
end

local function createButtons(row)
    local children = {};
    local i1 = (row - 1) * 4 + 1;
    local i2 = math.min(row * 4, settings.numberOfButtons);
    for i = i1, i2 do
        children[#children+1] = createButton(i);
    end
    return children;
end

local function createButtonRow(r)
    return {type = "box", flexFlow = lvgl.FLOW_ROW, children = createButtons(r)};
end

local function createButtons()
    local children = {};
    if (hasVirtualInputs) then
        local rows = math.floor(settings.numberOfButtons / 4 + 0.9);
        for i = 1, rows do
            children[i] = createButtonRow(i);
        end            
    end
    return children;
end

local function createControls()
    local children = {};
    children[#children+1] = {type = "box", flexFlow = lvgl.FLOW_ROW, children = createSliders()};
    children[#children+1] = {type = "hline", w = 100, h = 1};
    if (hasVirtualInputs) then
        children[#children+1] = {type = "box", flexFlow = lvgl.FLOW_COLUMN, children = createButtons()};
        children[#children+1] = {type = "hline", w = 100, h = 1};            
    end
    children[#children+1] = {type = "box", flexFlow = lvgl.FLOW_ROW, children = {
        {type = "button", text = "Settings", press = widget.settingsPage },
        {type = "button", text = "Global", press = widget.globalsPage }
    }};
    return children;
end

function widget.controlPage()
    lvgl.clear();
    local page = lvgl.page({
        title = widget.name,
        subtitle = "Controls - " .. widget.options.Name,
        back = askClose,
    });
    local uit = {
        {type = "box", flexFlow = lvgl.FLOW_COLUMN, children = createControls();}
    };
    widget.ui = page:build(uit);
end

local function createSetting(i)
    local w = widget.zone.w / 6;
    local wmin = math.min(30, w);
    local wmax = math.max(widget.zone.w / 2, w);
    return { type = "box", flexFlow = lvgl.FLOW_ROW, children = {
            {type = "label", text = "Name: "},
            {type = "textEdit", value = settings.sliders[i].name, set = (function(v) settings.sliders[i].name = v; end), w = 100},
            {type = "label", text = "Width: "},
            {type = "numberEdit", min = wmin , max = wmax, w = 60, get = (function() return settings.sliders[i].width; end), set = (function(v) settings.sliders[i].width = v; end) }, 
            { type = "label", text = " Color:" },
            { type = "color", get = (function() return settings.sliders[i].color; end),
                              set = (function(v) settings.sliders[i].color = v; end) },
            { type = "label", text = " TextColor:" },
            { type = "color", get = (function() return settings.sliders[i].textColor; end),
                              set = (function(v) settings.sliders[i].textColor = v; end) },                                     
            { type = "label", text = " Font:" },
            { type = "font", get = (function() return settings.sliders[i].font; end),
                            set = (function(v) settings.sliders[i].font = v; end) },                                     
            { type = "label", text = " UseShm:" },
            { type = "toggle", 
                               get = (function() return int2bool(settings.sliders[i].useShm); end),
                               set = (function(v) settings.sliders[i].useShm = bool2int(v); end),
                               active = (function() return hasVirtualInputs; end)},
            {type = "label", text = "ShmV: "},
            {type = "numberEdit", min = 1 , max = 16, w = 60, 
                    active = (function() return int2bool(settings.sliders[i].useShm); end),
                    get = (function() return settings.sliders[i].shm; end), 
                    set = (function(v) settings.sliders[i].shm = v; end) },                             
            {type = "label", text = "Vin: "},
            {type = "numberEdit", min = 1 , max = 16, w = 60, 
                    active = (function() return not int2bool(settings.sliders[i].useShm); end),
                    get = (function() return settings.sliders[i].vin; end), 
                    set = (function(v) settings.sliders[i].vin = v; end) },                             
        }
    }
end

local function createButtonSetting(i)
    local w = widget.zone.w / 6;
    local wmin = math.min(30, w);
    local wmax = math.max(widget.zone.w / 2, w);
    return { type = "box", flexFlow = lvgl.FLOW_ROW, children = {
            {type = "label", text = "Name: "},
            {type = "textEdit", value = settings.buttons[i].name, set = (function(v) settings.buttons[i].name = v; end), w = 100},
            {type = "label", text = " Type:" },
            {type = "choice", title = "Type", values = {"Button", "Toggle", "Momentary"}, get = (function() return settings.buttons[i].type; end), set = (function(t) settings.buttons[i].type = t; end) }, 
            {type = "label", text = "Width: "},
            {type = "numberEdit", min = wmin , max = wmax, w = 60, get = (function() return settings.buttons[i].width; end), set = (function(v) settings.buttons[i].width = v; end) }, 
            { type = "label", text = " Color:" },
            { type = "color", get = (function() return settings.buttons[i].color; end),
                              set = (function(v) settings.buttons[i].color = v; end) },
            { type = "label", text = " TextColor:" },
            { type = "color", get = (function() return settings.buttons[i].textColor; end),
                              set = (function(v) settings.buttons[i].textColor = v; end) },                                     
            { type = "label", text = " Font:" },
            { type = "font", get = (function() return settings.buttons[i].font; end),
                            set = (function(v) settings.buttons[i].font = v; end) },                                     
            {type = "label", text = "VS: "},
            {type = "numberEdit", min = 1 , max = 64, w = 60, 
                    get = (function() return settings.buttons[i].vs; end), 
                    set = (function(v) settings.buttons[i].vs = v; end) },                             
        }
    }
end

local function createSettings()
    local children = {};
    for i = 1, settings.numberOfSliders do
        children[#children+1] = createSetting(i);        
    end
    if (hasVirtualInputs) then
        children[#children+1] = {type = "hline", w = 100, h = 1};
        for i = 1, settings.numberOfButtons do
            children[#children+1] = createButtonSetting(i);        
        end            
    end
    children[#children+1] = {type = "hline", w = 100, h = 1};
    children[#children+1] = {type = "box", flexFlow = lvgl.FLOW_ROW, children = {
        {type = "button", text = "Controls", press = (function() saveSettings(); widget.controlPage(); end)},
        {type = "button", text = "Global", press = (function() saveSettings(); widget.globalsPage(); end)}
    }};
    return children;
end

function widget.settingsPage()
    lvgl.clear();
    local page = lvgl.page({
        title = widget.name,
        subtitle = "Settings - " .. widget.options.Name,
        back = (function() askClose(); end),
    });
    local uit = {
        {type = "box", flexFlow = lvgl.FLOW_COLUMN, children = createSettings() }
    };
    widget.ui = page:build(uit);
end

function widget.globalsPage() 
    lvgl.clear();
    local page = lvgl.page({
        title = widget.name,
        subtitle = "Global - " .. widget.options.Name,
        back = (function() askClose(); end),
    });
    local uit = {
        {type = "box", flexFlow = lvgl.FLOW_COLUMN, w = widget.zone.w, children = {
            {type = "box", flexFlow = lvgl.FLOW_ROW, children = {
                {type = "label", text = "Number of Sliders: "},
                {type = "numberEdit", min = 1, max = 8, w = 40, 
                        get = (function() return settings.numberOfSliders; end), 
                        set = (function(v) 
                            for i = 1, settings.numberOfSliders do
                                activateVInput(settings.sliders[i].vin, false);
                                settings.sliders[i] = nil;
                            end
                            settings.numberOfSliders = v;
                            for i = 1, settings.numberOfSliders do
                                resetSlider(i);
                                activateVInput(settings.sliders[i].vin, true);
                                settings.sliders[i].width = widget.zone.w / settings.numberOfSliders;
                            end
                        end) } 
                }
            },
            {type = "box", flexFlow = lvgl.FLOW_ROW, children = {
                {type = "label", text = "Number of buttons: "},
                {type = "numberEdit", min = 1, max = 64, w = 40, 
                        get = (function() return settings.numberOfButtons; end), 
                        set = (function(v) 
                            for i = 1, settings.numberOfButtons do
                                activateVSwitch(settings.buttons[i].vs, false);
                                settings.buttons[i] = nil;
                            end
                            settings.numberOfButtons = v;
                            for i = 1, settings.numberOfButtons do
                                resetButton(i);
                                activateVSwitch(settings.buttons[i].vs, true);
                            end
                        end),
                        active = (function() return hasVirtualInputs; end)} 
                }
            },
            {type = "box", flexFlow = lvgl.FLOW_ROW, children = {
                {type = "label", text = "Radius momentary Button: "},
                {type = "numberEdit", min = 10, max = 30, w = 40, get = (function() return settings.momentaryButton_radius; end), set = (function(v) settings.momentaryButton_radius = v; end) } 
            }},
            {type = "button", text = "Reset all Settings", press = (function() resetSettings() end)},
            {type = "hline", w = 100, h = 1},
            {type = "box", flexFlow = lvgl.FLOW_ROW, children = {
                {type = "button", text = "Controls", press = (function() saveSettings(); widget.controlPage(); end) },
                {type = "button", text = "Settings", press = (function() saveSettings(); widget.settingsPage(); end) }
            }}
            }
        }
    };
    widget.ui = page:build(uit);
end

function widget.widgetPage()
    lvgl.clear();
    widget.ui = lvgl.build({
        { type = "box", flexFlow = lvgl.FLOW_COLUMN, children = {
            { type = "label", text = widget.name, w = widget.zone.x, align = CENTER},
            { type = "label", text = widget.options.Name, w = widget.zone.x, align = CENTER },
        }
        }
    });
end

local function isValidSettingsTable(t) 
    if (t.version ~= nil) then
        if (t.version == settingsVersion) then
            return true;
        end
    end
    return false;
end

local initialized = false;
function widget.update()
    if (not initialized) then
        local st = serialize.load(settingsFilename);
        if (st ~= nil) then
            if (isValidSettingsTable(st)) then
                settings = st;
            else
                resetSettings();
            end
        else
            resetSettings();
        end
        for i = 1, settings.numberOfSliders do
            state.values[i] = 0;
            activateVInput(i, true);
        end
        for i = 1, settings.numberOfButtons do
            activateVSwitch(i, true);
        end
        initialized = true;
    end
    if lvgl.isFullScreen() then
        widget.controlPage();
    else
        widget.widgetPage();
    end
    saveSettings();
end

function widget.background()
end

local function fullScreenRefresh()
end

function widget.refresh(event, touchState)
    if lvgl == nil then
        lcd.drawText(widget.zone.x, widget.zone.y, "Lvgl support required", COLOR_THEME_WARNING)
    end
    if (lvgl.isFullScreen()) then
        fullScreenRefresh();
    end
    widget.background();
end

return widget;
