#coding=GBK

import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
  """管理游戏资源和行为"""
  def __init__(self):
    pygame.init()
    self.clock=pygame.time.Clock()
    self.settings=Settings()
    self.bullet=pygame.sprite.Group()
    
    self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
    # self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    # self.settings.screen_width=self.screen.get_rect().width
    # self.settings.screen_height=self.screen.get_rect().height
    pygame.display.set_caption("Alien Invasion")
    self.ship=Ship(self)
    # self.bg_color=(2)
  def run_game(self):
    """开始游戏的主循环"""  
    while True:
      # 监听事件
      self._check_events()
      self.ship.update()
      self.bullet.update()
      self._update_screen()
      self.clock.tick(60)
  def _check_events(self):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        sys.exit()
      elif event.type==pygame.KEYDOWN:
        self._check_keydown_events(event)
      elif event.type==pygame.KEYUP:
        self._check_keyup_events(event)
  def _update_screen(self):
    self.screen.fill(self.settings.bg_color)
    self.ship.blitme()
    pygame.display.flip()
  def _fire_bullet(self):
    new_bullet=Bullet(self)
    self.bullet.add(new_bullet)
  def _check_keydown_events(self,event):
    """响应按下"""
    if event.key ==pygame.K_RIGHT:
      self.ship.moving_right=True
    if event.key==pygame.K_LEFT:
      self.ship.moving_left=True
    if event.key==pygame.K_q:
      sys.exit()
    if event.key==pygame.K_SPACE:
      self._fire_bullet()
      
  def _check_keyup_events(self,event):
    if event.key==pygame.K_RIGHT:
      self.ship.moving_right=False
    if event.key==pygame.K_LEFT:
      self.ship.moving_left=False

if __name__=="__main__":
  ai=AlienInvasion()
  ai.run_game()
