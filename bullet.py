#coding=GBK
import math
import random
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
  """子弹"""
  def __init__(self,ai_game):
    super().__init__()
    self.screen=ai_game.screen
    self.settings=ai_game.settings
    self.color=self.settings.bullet_color
    self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
    self.rect.midtop=ai_game.ship.rect.midtop
    self.health=ai_game.gun.current_gun['bullet_can_through_aliens_number']
    self.bullet_can_rebound_number=ai_game.gun.current_gun['bullet_can_rebound_number']
    #是否是弹片
    self.is_piece=False
    
    #二元组，用来计算子弹速度，模长小于1
    
    if ai_game.ship.moving_right and not ai_game.ship.moving_left:
      # print("shoot right")
      self.current_mid_directX=0.3
    elif ai_game.ship.moving_left and not ai_game.ship.moving_right:
      # print("shoot left")
      self.current_mid_directX=-0.3
    else :self.current_mid_directX=0
    self.bullet_max_directX=ai_game.gun.current_gun['bullet_max_directX']
    self.current_max_directX=min(self.current_mid_directX+self.bullet_max_directX,1)
    self.current_min_directX=max(self.current_mid_directX-self.bullet_max_directX,-1)
    # print(f"mxdirx{self.current_max_directX}")
    # print(f"midirx{self.current_min_directX}")
    
    self.directX=random.uniform(self.current_min_directX,self.current_max_directX)
    self.directY=math.sqrt(1-self.directX*self.directX)
    #子弹位置
    self.y=float(self.rect.y)
    self.x=float(self.rect.x)
    
  def update(self):
    self.y-=self.settings.bullet_speed*self.directY
    self.x+=self.settings.bullet_speed*self.directX
    self.rect.y=self.y
    self.rect.x=self.x
  def draw_bullet(self):
    pygame.draw.rect(self.screen,self.color,self.rect)