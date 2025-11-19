#code=GBK
import sys
import pygame
from settings import Settings
from ship import Ship
class AlienInvasion:
  """管理游戏资源和行为"""
  def __init__(self):
    pygame.init()
    self.clock=pygame.time.Clock()
    self.settings=Settings()
    
    self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    self.ship=Ship(self)
    # self.bg_color=(2)
  def run_game(self):
    """开始游戏的主循环"""  
    while True:
      # 监听事件
      self._check_events()
      self.screen.fill(self.settings.bg_color)
      self.ship.blitme()
      pygame.display.flip()
      self.clock.tick(60)
  def _check_events():
    pass
if __name__=="__main__":
  ai=AlienInvasion()
  ai.run_game()
