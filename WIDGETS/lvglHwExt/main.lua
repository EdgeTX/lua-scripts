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

-- todo: check for virtual controls

local name = "HwExt/L"
local longname = "HwExtension/L"

local hasVirtualInputs = (getVirtualSwitch ~= nil);

local function create(zone, options, dir)
    if (lvgl == nil) then
        return {zone = zone, options = options, name = name, 
                update = (function() end), background = (function() end), 
                refresh = (function() 
                    lcd.drawText(zone.x, zone.y, "Lvgl support required", COLOR_THEME_WARNING)
                end)};
    end
    if (dir == nil) then
        dir = "/WIDGETS/lvglHwExt/";
    end
    if (hasVirtualInputs) then
        return loadScript(dir .. "ui.lua")(zone, options, longname, dir);
    else 
        return {zone = zone, options = options, name = name, 
                update = (function() 
                    lvgl.clear();
                    lvgl.build({{type = "box", flexFlow = lvgl.FLOW_COLUMN, children = {
                                                {type = "label", text = "VControls support needed", w = zone.x, align = CENTER},
                                            }}});
                    end), 
                background = (function() end), 
                refresh = (function() end)};
    end    
end

local function refresh(widget, event, touchState)
    widget.refresh(event, touchState)
end

local function background(widget)
    widget.background();
end

local options = {}
  
local function update(widget, options)
    widget.options = options;
    widget.update();
end

return {
    useLvgl = true,
    name = name,
    create = create,
    refresh = refresh,
    background = background,
    options = options,
    update = update
}
