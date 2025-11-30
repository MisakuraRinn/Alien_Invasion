#coding=GBK
import pygame
import random
import math
import os, sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):   # PyInstaller 打包后的临时目录
        base = sys._MEIPASS
    else:
        base = os.path.dirname(__file__)
    return os.path.join(base, relative_path)
from pygame.sprite import Sprite
class Alien(Sprite):
  """表示单个外星人的类"""
  def __init__(self,ai_game):
    super().__init__()
    self.screen=ai_game.screen
    
    self.image=pygame.image.load(resource_path(r"images/alien.bmp"))
    self.rect=self.image.get_rect()
    self.health=random.randint(int(1+math.log2(ai_game.stats.level)),ai_game.stats.level+3)
    print(self.health)
    self.rect.x=self.rect.width
    self.rect.y=self.rect.height
    self.settings=ai_game.settings
    self.x=float(self.rect.x)
    # self.y=float(self.rect.y)
  def update(self):
    """向右移动外星人"""
    self.x+=self.settings.alien_speed *self.settings.fleet_direction
    # self.y+=random.randint(0,1)
    self.rect.x=self.x
    self.rect.y+=random.randint(0,1)
  def check_edges(self):
    """位于边缘则返回true"""
    screen_rect=self.screen.get_rect()
    return (self.rect.right>=screen_rect.right) or self.rect.left<=0