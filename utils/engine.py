import threading
import pygame
from pygame import draw, display, image, event, mixer, font, transform
import time
import sys
import os


class GameItem:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.alive = True
        self.sprites = []
    
    def texture(self,renderer, image, position, size):
        rect = pygame.Rect(
            position[0], position[1], size[0], size[1])
        surf = transform.scale(image, (size[0], size[1]))
        renderer.blit(surf, rect)

    def text(self,renderer,value,position,size,color = (0,0,0),center=True):
        tFont = font.Font("../font/default.ttf", size) 
        text = tFont.render(value, True, color)
        
        textRect = text.get_rect()
        if center:
            textRect.center = (position[0], position[1])
        else:
            textRect.top = position[1]
            textRect.left = position[0]

        renderer.blit(text, textRect)

    def update(self, delta, events) -> None:
        pass

    def draw(self, delta, render) -> None:
        pass

class GameController:
    def __init__(self):
        pass
    
    def update(self,delta,items):
        pass

class GameMain:

    def __init__(self,size,title):
        self.gameItems = []
        self.gameControllers = []
        self.threads = []
        self.active = True
        
        pygame.init()
        mixer.init()

        self.renderer = display.set_mode(size)
        display.set_caption(title)

        self.threads.append(threading.Thread(target=self.update))
        self.threads.append(threading.Thread(target=self.draw))

    def add_item(self,item):
        self.gameItems.append(item)

    def add_controller(self,controller):
        self.gameControllers.append(controller)


    def run(self,enableThread = True):
        if enableThread:
            for thread in self.threads:
                thread.start()
        else:
            last_time = float(time.time())
            current_time = 0
            while self.active:
                events = event.get()
                for evt in events:
                    if evt.type == pygame.QUIT:
                        self.active = False
                        pygame.quit()
                        sys.exit()
                
                current_time = float(time.time())
                deltatime = (current_time - last_time)
                last_time = current_time

                for controller in self.gameControllers:
                    self.gameItems = controller.update(deltatime, self.gameItems).copy()

                index = 0
                for item in self.gameItems:
                    if not item.alive:
                        self.gameItems.remove(index)
                    else:
                        item.update(deltatime, events)
                        index+=1

                self.renderer.fill((0, 0, 0))
            
                for item in self.gameItems:
                    item.draw(deltatime,self.renderer)

                display.flip()
       

    def update(self):
        last_time = 0
        current_time = 0

        while self.active:
            events = event.get()
            for evt in events:
                if evt.type == pygame.QUIT:
                    self.active = False

            current_time = float(time.time())
            deltatime = (current_time - last_time)
            last_time = current_time

            for controller in self.gameControllers:
                self.gameItems = controller.update(deltatime, self.gameItems).copy()

            index = 0
            for item in self.gameItems:
                if not item.alive:
                    self.gameItems.remove(index)
                else:
                    item.update(deltatime, events)
                    index+=1

    def draw(self):
        last_time = 0
        current_time = 0
        
        while self.active:

            current_time = float(time.time())
            deltatime = (current_time - last_time)
            last_time = current_time

            self.renderer.fill((0, 0, 0))
            
            for item in self.gameItems:
                item.draw(deltatime,self.renderer)

            display.flip()
