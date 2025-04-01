local widget, state = ... 

local function encode()
    if (widget.options.ShmEncoding > 0) then
        local e = bit32.lshift(widget.options.Address, 8);
        for i, b in ipairs(state.buttons) do
            if (b.value > 0) then
                e = bit32.bor(e, bit32.lshift(1, (i - 1)));
            end
        end
        setShmVar(widget.options.ShmVar, e);
    end 
end

return {encode = encode}


