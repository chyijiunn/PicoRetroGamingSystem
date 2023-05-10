from machine import Pin, I2C,PWM
from ssd1306 import SSD1306_I2C
from time import sleep,time
import _thread ,random,sys
def conway_main():
    start = time()
    generation = 0
    buzzer = PWM(Pin(12))
    buzzer.freq(500)
    i2c=I2C(0,sda=Pin(20), scl=Pin(21), freq=40000)
    oled = SSD1306_I2C(128, 64, i2c)
    buttonR = Pin(3, Pin.IN, Pin.PULL_UP)#press = 0 , unpress = 1
    buttonL = Pin(2, Pin.IN, Pin.PULL_UP)

    scale = 8 #128*64(X), scale:time = 2:44s , 4:9s , 8:2s , 16:1s
    WIDTH = 128/scale
    HEIGHT = 64/scale

    nextCells = {}
    for x in range(WIDTH):  
        for y in range(HEIGHT): 
            if random.randint(0, 1) == 0:
                nextCells[(x, y)] = 1
            else:
                nextCells[(x, y)] = 0
    while True:
        cells = nextCells.copy()
        for y in range(HEIGHT):
            for x in range(WIDTH):
                oled.fill_rect(scale*x,scale*y,scale*(x+1)-1,scale*(y+1)-1,nextCells[(x, y)])
                   
        for x in range(WIDTH):
            for y in range(HEIGHT):
                left = (x - 1)% WIDTH
                right = (x + 1)% WIDTH
                above = (y - 1)% HEIGHT
                below = (y + 1)% HEIGHT
      
                numNeighbors = 0
                if cells[(left, above)] == 1:
                    numNeighbors += 1
                if cells[(x, above)] == 1:
                    numNeighbors += 1  
                if cells[(right, above)] == 1:
                    numNeighbors += 1
                if cells[(left, y)] == 1:
                    numNeighbors += 1
                if cells[(right, y)] == 1:
                    numNeighbors += 1 
                if cells[(left, below)] == 1:
                    numNeighbors += 1
                if cells[(x, below)] == 1:
                    numNeighbors += 1
                if cells[(right, below)] == 1:
                    numNeighbors += 1
                # Conway's Game of Life rules:
                if cells[(x, y)] == 1 and (numNeighbors == 2 or numNeighbors == 3):
                    nextCells[(x, y)] = 1
                elif cells[(x, y)] == 0 and numNeighbors == 3:
                    nextCells[(x, y)] = 1
                else:
                    nextCells[(x, y)] = 0
        generation += 1
        oled.text(str(generation),55,0,1)
        oled.show()
    
if __name__ == "__main__":
    conway_main()
