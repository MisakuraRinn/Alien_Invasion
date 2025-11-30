#coding=GBK
import pygame
import os, sys

def resource_path(relative_path):
    """同样的资源路径处理函数，兼容打包。"""
    if hasattr(sys, '_MEIPASS'):   # PyInstaller 打包后的临时目录
        base = sys._MEIPASS
    else:
        base = os.path.dirname(__file__)
    return os.path.join(base, relative_path)

from pygame.sprite import Sprite

class Ship(Sprite):
  """管理玩家飞船的类。"""

  def __init__(self,ai_game):
    super().__init__()
    self.screen=ai_game.screen
    self.screen_rect=ai_game.screen.get_rect()
    self.settings=ai_game.settings

    # 载入飞船图片并设置 rect
    self.image=pygame.image.load(resource_path(r"images/ship.bmp"))
    self.rect=self.image.get_rect()
    # 初始位置：底部中央
    self.rect.midbottom=self.screen_rect.midbottom

    # 移动标志（布尔值）
    self.moving_right=False
    self.moving_left=False

  def blitme(self):
    """在指定位置绘制飞船。"""
    self.screen.blit(self.image,self.rect)

  def update(self):
    """根据移动标志调整飞船位置，不允许飞出屏幕。"""
    if self.moving_left and self.rect.left>0:
      self.rect.x-=self.settings.ship_speed
    if self.moving_right and self.rect.right<self.screen_rect.right:
      self.rect.x+=self.settings.ship_speed

  def center_ship(self):
    """将飞船重新放到底部中央（用于死亡后重置）。"""
    self.rect.midbottom=self.screen_rect.midbottom
    # 使用 float 记录精确横坐标（如有需要）
    self.x=float(self.rect.x)
