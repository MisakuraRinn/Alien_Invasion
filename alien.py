#coding=GBK
import pygame
import random
import math
import os, sys

def resource_path(relative_path):
    """获取资源文件的绝对路径，兼容 PyInstaller 打包后的运行环境。
    
    当使用 PyInstaller 打包时，资源会被放在临时目录 _MEIPASS 下。
    """
    if hasattr(sys, '_MEIPASS'):   # PyInstaller 打包后的临时目录
        base = sys._MEIPASS
    else:
        base = os.path.dirname(__file__)
    return os.path.join(base, relative_path)

from pygame.sprite import Sprite

class Alien(Sprite):
  """表示单个外星人的类。"""

  def __init__(self,ai_game):
    """初始化外星人并设置其起始位置和生命值。"""
    super().__init__()
    self.screen=ai_game.screen
    
    # 使用位图图片作为外星人外观
    self.image=pygame.image.load(resource_path(r"images/alien.bmp"))
    self.rect=self.image.get_rect()

    # 外星人生命值随关卡变化，范围 [1+log2(level), level+3]
    self.health=random.randint(
      int(1+math.log2(ai_game.stats.level)),
      ai_game.stats.level+3
    )
    print(self.health)

    # 初始位置：先放在左上角附近，后续由 AlienInvasion 调整
    self.rect.x=self.rect.width
    self.rect.y=self.rect.height
    self.settings=ai_game.settings

    # 使用 float 保存精确位置
    self.x=float(self.rect.x)
    # self.y=float(self.rect.y)

  def update(self):
    """更新外星人位置：左右移动 + 少量向下“抖动”。"""
    # 横向移动：根据 fleet_direction 决定方向
    self.x+=self.settings.alien_speed *self.settings.fleet_direction
    # 轻微随机下落，增加不确定性
    self.rect.x=self.x
    self.rect.y+=random.randint(0,1)

  def check_edges(self):
    """如果外星人到达屏幕边缘，则返回 True，用于触发整群换向。"""
    screen_rect=self.screen.get_rect()
    return (self.rect.right>=screen_rect.right) or self.rect.left<=0
