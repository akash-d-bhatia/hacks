-- Zoom Capture (Akash - Nov 2023)
-- Simple script to bind a hot key that allows one to take a screen shot of the active Zoom window and save the image
-- To use, just put this in your init.lua file for Hammerspoon: local ZoomCapture  = require('ZoomCapture')

local hotkey = require "hs.hotkey"
local timer = require "hs.timer"

-- Function to capture a screenshot of a Zoom window
function captureZoomWindow()
    -- Find all open windows
    local allWindows = hs.window.allWindows()
    
    -- Iterate over all windows to find a Zoom window
    for _, win in pairs(allWindows) do
        if win:application():name() == "zoom.us" then
            print("Zoom Window found!")
            win:maximize()
            
              win:focus()
              -- Get the frame of the Zoom window
              local zoomFrame = win:frame()
              local timestamp = os.date("%Y%m%d_%H%M%S")
              -- Construct the filename using the timestamp
              local filename = string.format("~/Downloads/zoomSreenShots/zoomShot_%s.png", timestamp)
                
              
              -- Construct the screencapture command
              -- The -R flag specifies the region to capture: x,y,width,height
              local command = string.format(
                  'screencapture -R%d,%d,%d,%d %s',
                  zoomFrame.x, zoomFrame.y, zoomFrame.w, zoomFrame.h,
                  filename
              )
              
              -- Execute the command
              hs.execute(command)
              
              -- Exit the function after capturing the screenshot
              return
              
        end
    end
    
    print('No Zoom window found')
end

-- Bind the keyboard shortcut
-- This binds the function to the keys "ctrl+alt+cmd+Z"
hotkey.bind({"ctrl", "alt", "cmd"}, "Z", captureZoomWindow)
--End Zoom Capture
