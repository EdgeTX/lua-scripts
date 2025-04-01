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

local serialize = loadScript(dir .. "tableser.lua")();

widget.ui = nil;

local settings = {}
local controllersOnline = 0;

local function switchCallback(controller, switch, on)
    print("switchCB:", controller, switch, on);
    for i, c in pairs(settings.controller) do
        if (c.id == controller) then
            local s = c.switches[switch];
            if ((s ~= nil) and (s > 0)) then
                setVirtualSwitch(s, on);        
            end
        end
    end
end
local function propCallback(controller, prop, value)
    print("propCB:", controller, prop, value);
    for i, c in pairs(settings.controller) do
        if (c.id == controller) then
            local p = c.props[prop];
            if (p ~= nil) then
                setVirtualInput(p, (value - 1024));
            end
        end
    end
end

local function prop8Callback(controller, prop, value)
    print("prop8CB:", controller, prop, value);
    for i, c in pairs(settings.controller) do
        if (c.id == controller) then
            local p = c.props[prop];
            if (p ~= nil) then
                setVirtualInput(p, (value - 128) * 8);
            end
        end
    end
end

local function activateVSwitches()
    for ci, c in pairs(settings.controller) do
        for si, s in pairs(c.switches) do
            activateVirtualSwitch(s, true);        
        end        
    end
end

local function activateVInputs()
    for ci, c in pairs(settings.controller) do
        for pi, p in pairs(c.props) do
            activateVirtualInput(p, true);        
        end        
    end
end

local settingsVersion = 9;
local function resetSettings() 
    print("resetSettings");
    settings.version = settingsVersion;
    settings.controller = { 
        { id = 0, name = "Intern", switches = {1, 2, 3, 4, 5},  props = {} },
        { id = 1, name = "Pult",   switches = {17, 18, 
                                                19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
                                                33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48
                                            }, props = {1, 2, 3, 4} }
    };
    activateVSwitches();
    activateVInputs();
end
resetSettings();

local function isValidSettingsTable(t) 
    if (t.version ~= nil) then
        if (t.version == settingsVersion) then
            return true;
        end
    end
    return false;
end

local settingsFilename = nil;

local function updateFilename()
    local fname = dir .. model.getInfo().name .. ".lua";
    if (fname ~= settingsFilename) then
        settingsFilename = fname;
        return true;
    end
    return false;
end
updateFilename();

local function askClose()
    lvgl.confirm({title = "Exit", message = "Really exit?", confirm = (function() serialize.save(settings, settingsFilename); lvgl.exitFullScreen(); end),})
end

local function createSwitchDisplay(c)
    local swlines = {};
    local xoffset = 20
    local rw = (LCD_W - 2 * xoffset) / 16;
    local rh = rw;

    for row = 1, 4 do
        for col = 1, 16 do
            local swn = (row - 1) * 16 + col;
            local filled = false;
            for i, sw in pairs(c.switches) do
                if (sw == swn) then
                    filled = true;
                    break;
                end
            end                   
            swlines[#swlines+1] = {type = "rectangle", x = xoffset + (col - 1) * rw, y = (row - 1) * rh, w = rw / 2, h = rh / 2, filled = filled,
                                   color = (function() 
                                    if (filled) then
                                        if (getVirtualSwitch(swn)) then 
                                            return COLOR_THEME_WARNING; 
                                        else 
                                            return COLOR_THEME_SECONDARY1; 
                                        end; 
                                    else
                                        return COLOR_THEME_SECONDARY2;
                                    end
                                end),
                                  };
        end 
    end
    local sd = {type = "box", flexFlow = lvgl.FLOW_COLUMN, children = {
        {type = "label", text = "Switches"},
        {type = "box", children = swlines}
    }
    };
    return sd;
end

local function createPropDisplay(c)
    local plines = {};
    local xoffset = 20
    local rw = (LCD_W - 2 * xoffset) / 16;
    local rh = rw;
    for i = 1, 16 do
        local filled = false;
        for _, p in pairs(c.props) do
            if (p == i) then
                filled = true;
                break;
            end
        end                   
        plines[#plines+1] = {type = "rectangle", x = xoffset + (i - 1) * rw, y = 0, w = rw / 2, h = 2 * rh,
                             color = (function() if (filled) then return COLOR_THEME_SECONDARY1; else return COLOR_THEME_SECONDARY2; end; end)};    
        if (filled) then
            
            plines[#plines+1] = {type = "rectangle", 
                                 pos  = (function() local vscaled = rh * (getVirtualInput(i) + 1024) / 1024; return xoffset + (i - 1) * rw + 1, vscaled; end), 
                                 size = (function() local vscaled = rh * (getVirtualInput(i) + 1024) / 1024; return rw / 2 - 2, 2 * rh - vscaled; end), 
                                 filled = true, color = COLOR_THEME_SECONDARY1};
        end
    end
    local pd = {type = "box", flexFlow = lvgl.FLOW_COLUMN, children = {
        {type = "label", text = "Props"},
        {type = "box", children = plines}
    }};
    return pd;
end

local function createControllerDisplay(c)
    local cd = {type = "box", flexFlow = lvgl.FLOW_COLUMN, children = {
       createSwitchDisplay(c),
       {type = "hline", w = 100, h = 1},
       createPropDisplay(c)
       }
    };
    return cd;
end

local function createDisplay() 
    local children = {};
    for i, c in pairs(settings.controller) do
        children[#children+1] = {type = "label", text = "Controller@" .. c.id .. ": " .. c.name};
        children[#children+1] = createControllerDisplay(c);           
        children[#children+1] = {type = "hline", w = LCD_W - 10, h = 3};
    end
    children[#children+1] = {type = "hline", w = 100, h = 1};
    children[#children+1] = {type = "box", flexFlow = lvgl.FLOW_ROW, children = {
        {type = "button", text = "Settings", press = widget.settingsPage },
    }};
    return children;
end

function widget.displayPage()
    lvgl.clear();
    local page = lvgl.page({
        title = widget.name,
        subtitle = "Display",
        back = askClose,
    });
    local uit = {{type = "box", flexFlow = lvgl.FLOW_COLUMN, flexPad = lvgl.PAD_LARGE, children = createDisplay(); }};
    widget.ui = page:build(uit);
end

local function addController()
    local maxid = 0;
    for i, c in pairs(settings.controller) do
        if (c and (c.id > maxid)) then
            maxid = c.id;
        end
    end
    settings.controller[#settings.controller+1] = {id = maxid + 1, name = "", switches = {}, props = {}};
    widget.settingsPage();
end

local function deleteController(c)
    for i, cx in pairs(settings.controller) do
        if (cx == c) then
            table.remove(settings.controller, i);
            break;
        end
    end
    widget.settingsPage();
end

local function controllerSetting(c)
    local cs = {type = "box", flexFlow = lvgl.FLOW_ROW, children = {
        {type = "label", text = "Name"},
        {type = "textEdit", value = c.name, set = (function(v) c.name = v; end), w = 100},
        {type = "label", text = "ID"},
        {type = "numberEdit", min = 0, max = 7, get = (function() return c.id; end), set = (function(v) c.id = v; end),  w = 30 },
        {type = "button", text = "Delete", press = (function() deleteController(c); end)}
    }};
    return cs;
end

local function controllerSettings()
    local cs = {};
    cs[#cs+1] = {type = "label", text = "Controller:"};
    for i, c in pairs(settings.controller) do
        cs[#cs+1] = controllerSetting(c);            
    end
    cs[#cs+1] = {type = "hline", w = 100, h = 1};
    cs[#cs+1] = {type = "button", text = "Add Controller", press = addController };
    return cs;
end

local function deleteSwitchMapping(controller, inp)  
    controller.switches[inp] = 0;
end

local function switchMapping(controller, iswitch, vswitch)
    local sm = {type = "box", flexFlow = lvgl.FLOW_ROW, flexPad = lvgl.PAD_LARGE, children = {
        {type = "label", text = "Controller:"},
        {type = "label", text = controller.name},
        {type = "label", text = "In-Switch:"},
        {type = "numberEdit", get = (function() return iswitch; end), active = (function() return false; end), w = 50 },
        {type = "label", text = "Out-Switch:"},
        {type = "numberEdit", min = 1, max = 64, get = (function() return controller.switches[iswitch]; end), set = (function(v) controller.switches[iswitch] = v; end),  w = 50 },
        {type = "button", text = "Delete", press = (function() deleteSwitchMapping(controller, iswitch); widget.settingsPage(); end)}
    }};
    return sm;
end

local function deletePropMapping(controller, inp)  
    controller.props[inp] = 0;
end

local function propMapping(controller, iprop, vprop)
    local sm = {type = "box", flexFlow = lvgl.FLOW_ROW, flexPad = lvgl.PAD_LARGE, children = {
        {type = "label", text = "Controller:"},
        {type = "label", text = controller.name},
        {type = "label", text = "In-Prop:"},
        {type = "numberEdit", get = (function() return iprop; end), active = (function() return false; end), w = 50 },
        {type = "label", text = "Out-Prop:"},
        {type = "numberEdit", min = 1, max = 16, get = (function() return controller.props[iprop]; end), set = (function(v) controller.props[iprop] = v; end),  w = 50 },
        {type = "button", text = "Delete", press = (function() deletePropMapping(controller, iprop); widget.settingsPage(); end)}
    }};
    return sm;
end

local function addPropMapping(item)
    local c = settings.controller[item.controller];
    c.props[item.inprop] = item.outprop;
end

local addPropMappingItem = { controller = 1; inprop = 1; outprop = 1;};
local function addPropMappingDialog()
    local width = 200;
    local col2x = 100;
    local dg = lvgl.dialog({title="Add Prop-Mapping", flexFlow=lvgl.FLOW_COLUMN, w = width });
    local item = addPropMappingItem;
    local cnames = {};
    for _, c in pairs(settings.controller) do
        cnames[#cnames+1] = c.name;
    end
    local uit = {
        {type = "setting", title = "Controller", children = {
            {type = "choice", title = "Controller", x = col2x, values = cnames, 
             get = (function() return item.controller; end), set = (function(v) item.controller = v; end)};
        }},
        {type = "setting", title = "In-Prop", children = {
            {type = "numberEdit", x = col2x, min = 1, max = 16, 
             get = (function() return item.inprop; end), set = (function(v) item.inprop = v; end),  w = 50 },    
        }},      
        {type = "setting", title = "Out-Prop", children = {
            {type = "numberEdit", x = col2x, min = 1, max = 16, 
            get = (function() return item.outprop; end), set = (function(v) item.outprop = v; end),  w = 50 },    
        }},      
        {type = "hline", w = width / 2, h = 1},
        {type = "box", flexFlow=lvgl.FLOW_ROW, children = {
            {type = "button", text = "Add", press = (function() addPropMapping(item); dg:close(); widget.settingsPage(); end)},
            {type = "button", text = "Cancel", press = (function() dg:close(); end)}
        }}
    };
    dg:build(uit);
end

local function addSwitchMapping(item)
    local c = settings.controller[item.controller];
    c.switches[item.insw] = item.outsw;
end

local addSwitchMappingItem = { controller = 1; insw = 1; outsw = 1;};
local function addSwitchMappingDialog()
    local width = 200;
    local col2x = 100;
    local dg = lvgl.dialog({title="Add Switch-Mapping", flexFlow=lvgl.FLOW_COLUMN, w = width });
    local item = addSwitchMappingItem;
    local cnames = {};
    for _, c in pairs(settings.controller) do
        cnames[#cnames+1] = c.name;
    end
    local uit = {
        {type = "setting", title = "Controller", children = {
            {type = "choice", title = "Controller", x = col2x, values = cnames, 
             get = (function() return item.controller; end), set = (function(v) item.controller = v; end)};
        }},
        {type = "setting", title = "In-Switch", children = {
            {type = "numberEdit", x = col2x, min = 1, max = 64, 
             get = (function() return item.insw; end), set = (function(v) item.insw = v; end),  w = 50 },    
        }},      
        {type = "setting", title = "Out-Switch", children = {
            {type = "numberEdit", x = col2x, min = 1, max = 64, 
            get = (function() return item.outsw; end), set = (function(v) item.outsw = v; end),  w = 50 },    
        }},      
        {type = "hline", w = width / 2, h = 1},
        {type = "box", flexFlow=lvgl.FLOW_ROW, children = {
            {type = "button", text = "Add", press = (function() addSwitchMapping(item); dg:close(); widget.settingsPage(); end)},
            {type = "button", text = "Cancel", press = (function() dg:close(); end)}
        }}
    };
    dg:build(uit);
end

local function switchMappings()
    local sm = {};
    for ci, c in pairs(settings.controller) do
        for si, s in pairs(c.switches) do
            if (s > 0) then
                sm[#sm+1] = switchMapping(c, si, s);                
            end
        end
        sm[#sm+1] = {type = "hline", w = 100, h = 1};
    end
    sm[#sm+1] = {type = "button", text = "Add Switch-Mapping", press = addSwitchMappingDialog };
    return sm;
end

local function propMappings()
    local sm = {};
    for ci, c in pairs(settings.controller) do
        for si, s in pairs(c.props) do
            if (s > 0) then
                sm[#sm+1] = propMapping(c, si, s);                
            end
        end
        sm[#sm+1] = {type = "hline", w = 100, h = 1};
    end
   sm[#sm+1] = {type = "button", text = "Add Prop-Mapping", press = addPropMappingDialog };
return sm;
end


local function createSettings() 
    local children = {};
    children[#children+1] = {type = "box", flexFlow = lvgl.FLOW_COLUMN, children = controllerSettings()};
    children[#children+1] = {type = "hline", w = LCD_W - 10, h = 3};
    children[#children+1] = {type = "box", flexFlow = lvgl.FLOW_COLUMN, children = switchMappings()};
    children[#children+1] = {type = "hline", w = LCD_W - 10, h = 3};
    children[#children+1] = {type = "box", flexFlow = lvgl.FLOW_COLUMN, children = propMappings()};
    children[#children+1] = {type = "hline", w = LCD_W - 10, h = 3};
    children[#children+1] = {type = "button", text = "Display", press = widget.displayPage };
    return children;
end

function widget.settingsPage()
    lvgl.clear();
    local page = lvgl.page({
        title = widget.name,
        subtitle = "Settings",
        back = askClose,
    });
    local uit = { {
            type = "box",
            flexFlow = lvgl.FLOW_COLUMN,
            flexPad = lvgl.PAD_LARGE,
            children = createSettings();
         }
    };
    widget.ui = page:build(uit);
end

function widget.widgetPage()
    lvgl.clear();
    widget.ui = lvgl.build({
        { type = "box", flexFlow = lvgl.FLOW_COLUMN, children = {
            { type = "label", text = widget.name, w = widget.zone.x, align = CENTER},
            { type = "label", text = (function() return #settings.controller .. "/" .. controllersOnline; end), w = widget.zone.x, align = CENTER },
        }
        }
    });
end

local initialized = false;
function widget.update()
    local changed = updateFilename();
    if ((not initialized) or changed) then
        setSerialBaudrate(115200);
        local st = serialize.load(settingsFilename);
        if (st ~= nil) then
            if (isValidSettingsTable(st)) then
                settings = st;
            else
                resetSettings();
                changed = true;
            end
        else
            resetSettings();
            changed = true;
        end
        initialized = true;
    end
    if (lvgl.isFullScreen() or lvgl.isAppMode()) then
        widget.displayPage();
    else
        widget.widgetPage();
    end
    if (changed) then
        serialize.save(settings, settingsFilename);        
    end
end

local fsm = loadScript(dir .. "proto.lua")(switchCallback, propCallback, prop8Callback);

function widget.background()
    fsm.process();
end

local function fullScreenRefresh()
end

function widget.refresh(event, touchState)
    if (lvgl.isFullScreen()) then
        fullScreenRefresh();
    end
    widget.background();
end

return widget;
