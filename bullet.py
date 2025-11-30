#coding=GBK
import math
import random
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
  """子弹类：管理单颗子弹的属性与运动。"""

  def __init__(self,ai_game):
    """在飞船当前位置创建一个向上飞行的子弹。"""
    super().__init__()
    self.screen=ai_game.screen
    self.settings=ai_game.settings
    self.color=self.settings.bullet_color

    # 使用一个矩形来表示子弹
    self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
    self.rect.midtop=ai_game.ship.rect.midtop

    # 子弹生命值 = 能穿透的外星人数
    self.health=ai_game.gun.current_gun['bullet_can_through_aliens_number']
    # 可反弹次数
    self.bullet_can_rebound_number=ai_game.gun.current_gun['bullet_can_rebound_number']
    # 是否是爆炸碎片（True 表示通过 _boom 生成）
    self.is_piece=False
    
    # 计算子弹方向向量（directX, directY），长度为 1
    # 根据飞船当前移动方向，为子弹加少量水平偏移
    if ai_game.ship.moving_right and not ai_game.ship.moving_left:
      # print("shoot right")
      self.current_mid_directX=0.3
    elif ai_game.ship.moving_left and not ai_game.ship.moving_right:
      # print("shoot left")
      self.current_mid_directX=-0.3
    else :
      self.current_mid_directX=0

    # 当前武器允许的最大散射角（在 X 方向上的投影范围）
    self.bullet_max_directX=ai_game.gun.current_gun['bullet_max_directX']
    self.current_max_directX=min(self.current_mid_directX+self.bullet_max_directX,1)
    self.current_min_directX=max(self.current_mid_directX-self.bullet_max_directX,-1)
    
    # 在 [min, max] 区间内随机一个水平分量 directX
    self.directX=random.uniform(self.current_min_directX,self.current_max_directX)
    # 根据直角三角形关系求得 directY，保证方向向量长度为 1
    self.directY=math.sqrt(1-self.directX*self.directX)

    # 使用 float 记录更精确的坐标
    self.y=float(self.rect.y)
    self.x=float(self.rect.x)
    
  def update(self):
    """根据 direction 和速度更新子弹位置。"""
    self.y-=self.settings.bullet_speed*self.directY
    self.x+=self.settings.bullet_speed*self.directX
    self.rect.y=self.y
    self.rect.x=self.x

  def draw_bullet(self):
    """在屏幕上绘制子弹（矩形）。"""
    pygame.draw.rect(self.screen,self.color,self.rect)
