'''
app["name"]="I2C Scan"
app["id"]="i2c_scan"
app["icon"]="0000000000000000000011010000000000000000000000000001111010000000000111101000000000011110101100000001111010111000000111101001110000011110100011100001111010000110000000000000011000001101000001100000000000001110000000000001110000111111010110000001111010110000"
'''
import random
import quantum_os
from quantum_os.display import *

class App:
    def setup(self, display):
        self.known_addresses = {
            "0D": "PicoVision GPU",
            "20": "Keyboard GPIO Expander"
        }
        self.cols = "0123456789ABCDEF"
        self.rows = "01234567"
    
        self.display = display
        self.display.set_pen(BG_COLOR)
        self.cursor = {"x": 0, "y": 0}
        w, h = display.get_bounds()
        display.rectangle(0, 0, w, h)
        
        self.devices = {}

        
        for device in quantum_os.get_internal_i2c().scan():
            addr = f'{device:02X}'
            
            if addr in self.known_addresses:
                name = self.known_addresses[addr]
            else:
                name = "Unknown Device"
                
            device = {
              "addr": addr,
              "name": name,
              "x": self.cols.find(addr[1]),
              "y": self.rows.find(addr[0])
            }
            
            
            self.devices[f'{device["x"]}x{device["y"]}'] = device


    def run(self):        
        while True:
            
            if self.cursor["x"] < 0:
                self.cursor["x"] = 15
            if self.cursor["x"] > 15:
                self.cursor["x"] = 0
                
            if self.cursor["y"] < 0:
                self.cursor["y"] = 7
            if self.cursor["y"] > 7:
                self.cursor["y"] = 0
                
            self.display.set_pen(BG_COLOR)
            w, h = self.display.get_bounds()
            self.display.rectangle(0, 0, w, h)
            self.display.set_pen(TEXT_COLOR)
            
            y_offset = 26
            x_offset = 36
            
            for col_index, col in enumerate(self.cols):
                self.display.text(col, 400-x_offset-((col_index+1)*20), 240-y_offset, -1, 1, 180)
                
            #f'{device:x}'
            #print()
            selected_device = "No Device selected."
            for row_index, row in enumerate(self.rows):
                y = 240-y_offset-((row_index+1)*16)
                self.display.set_pen(TEXT_COLOR)
                self.display.text(row, 400-x_offset, y, -1, 1, 180)
                for col_index in range(1, 17):
                    table_x = col_index-1
                    table_y = row_index
                    pos = f'{table_x}x{table_y}'
                    text = "--"
                    
                    x = 400-x_offset-(col_index*20)
                    
                    is_cursor = self.cursor["x"] == table_x and self.cursor["y"] == table_y
                    
                    if is_cursor:
                        self.display.set_pen(CURSOR_COLOR)
                        self.display.rectangle(x-12, y-8, 16, 11)
                    
                    if pos in self.devices:
                        text = self.devices[pos]["addr"]
                        self.display.set_pen(TEXT_COLOR)
                        if is_cursor:
                            selected_device = f'Device: {self.devices[pos]["name"]}'
                        if not is_cursor:
                            self.display.rectangle(x-12, y-8, 16, 11)
                            self.display.set_pen(CURSOR_COLOR)
                    else:
                        self.display.set_pen(TEXT_COLOR)
                        
                    self.display.text(text, x, y, -1, 1, 180)
                    
            self.display.line(400-x_offset, 240-y_offset-144, x_offset, 240-y_offset-144)
            self.display.text(selected_device, 400-x_offset, 240-y_offset-152, -1, 1, 180)
            
            yield quantum_os.INTENT_FLIP_BUFFER
            while True:
                yield quantum_os.INTENT_NO_OP
                
                # keys = quantum_os.kbd.get_keys([
                #     quantum_os.keycode.ENTER,
                #     quantum_os.keycode.LEFT_ARROW,
                #     quantum_os.keycode.RIGHT_ARROW,
                #     quantum_os.keycode.UP_ARROW,
                #     quantum_os.keycode.DOWN_ARROW,
                #     quantum_os.keycode.Q
                # ])

                # if keys[quantum_os.keycode.RIGHT_ARROW]:
                #     self.cursor["x"] += 1
                #     break

                # if keys[quantum_os.keycode.LEFT_ARROW]:
                #     self.cursor["x"] -= 1
                #     break
                
                # if keys[quantum_os.keycode.DOWN_ARROW]:
                #     self.cursor["y"] += 1
                #     break

                # if keys[quantum_os.keycode.UP_ARROW]:
                #     self.cursor["y"] -= 1
                #     break
                    
                # if keys[quantum_os.keycode.Q]:
                #     yield quantum_os.INTENT_KILL_APP
                
  
        
    def cleanup(self):
        pass


if __name__ == '__main__':
    quantum_os.boot(App)