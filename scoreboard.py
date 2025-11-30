#coding=GBK
import pygame.font
from pygame.sprite import Group
from ship import Ship
from bullet import Bullet

class Scoreboard:
  """显示得分信息以及生命、子弹等 UI 的类。"""

  def __init__(self,ai_game):
    """初始化显示得分涉及的各种属性。"""
    self.ai_game=ai_game
    self.screen=ai_game.screen
    self.screen_rect=self.screen.get_rect()
    self.settings=ai_game.settings
    self.stats=ai_game.stats
    
    # 文本颜色和字体
    self.text_color=(30,30,30)
    self.font=pygame.font.SysFont(None,48)
    
    # 预渲染各类信息，避免每帧重复创建字体对象
    self.prep_score()
    self.prep_high_score()
    self.prep_level()
    self.prep_ships()
    self.prep_ammo()

  def prep_score(self):
    """将当前得分渲染为图像。"""  
    # 分数取 10 的倍数，格式化为带逗号的字符串
    rounded_score=round(self.stats.score,-1)
    score_str=f"{rounded_score:,}"
    self.score_image=self.font.render(
      score_str,True,self.text_color,self.settings.bg_color)
    
    # 显示位置：右上角
    self.score_rect=self.score_image.get_rect()
    self.score_rect.right=self.screen_rect.right-20
    self.score_rect.top=20

  def prep_high_score(self):
    """将最高分渲染为图像。"""
    high_score=round(self.stats.high_score,-1)
    high_score_str=f"{high_score:,}"
    self.high_score_image=self.font.render(
      high_score_str,True,self.text_color,self.settings.bg_color)

    # 显示在窗口中上方居中位置
    self.high_score_rect=self.high_score_image.get_rect()
    self.high_score_rect.centerx=self.screen_rect.centerx
    self.high_score_rect.top=self.score_rect.top

  def prep_level(self):
    """将当前关卡渲染为图像，显示在得分下方。"""
    level_str=str(self.stats.level)
    self.level_image=self.font.render(
      level_str,True,self.text_color,self.settings.bg_color)
    self.level_rect=self.level_image.get_rect()
    # 右对齐，放在 score 下面
    self.level_rect.right=self.score_rect.right
    self.level_rect.top=self.score_rect.bottom+10

  def prep_ammo(self):
    """根据当前剩余弹药数量，绘制在左上角的子弹 UI。"""
    self.ammo_left=Group()
    # 利用 Bullet 精灵本身作为“子弹图标”
    for ammo_number in range(self.settings.ammo_left):
      ammo=Bullet(self.ai_game)
      # 这里只用 rect 来表示 UI，不影响真正的子弹逻辑
      ammo.rect.x=10+ammo_number*(ammo.rect.width+3)
      ammo.rect.y=80
      self.ammo_left.add(ammo)
    
  def prep_ships(self):
    """根据剩余生命数，在左上角显示小飞船图标。"""
    self.ships=Group()
    for ship_number in range(self.stats.ships_left):
      # 创建一个小号 ship 当作图标
      ship=Ship(self.ai_game)
      ship.rect.x=10+ship_number*ship.rect.width
      ship.rect.y=10
      self.ships.add(ship)

  def show_score(self):
    """在屏幕上绘制所有与得分/状态相关的图像。"""
    self.screen.blit(self.high_score_image,self.high_score_rect)
    self.screen.blit(self.score_image,self.score_rect)
    self.screen.blit(self.level_image,self.level_rect)
    # 生命图标
    self.ships.draw(self.screen)
    # 剩余弹药 UI（用 Bullet 图标绘制）
    for bullet in self.ammo_left.sprites():
      bullet.draw_bullet()
    # self.ammo_left.draw_bullet()  # 这里使用手动调用 draw_bullet

  def check_high_score(self):
    """检查是否生成了新的最高分，如果有则更新显示。"""
    if self.stats.score>self.stats.high_score:
      self.stats.high_score=self.stats.score
      self.prep_high_score()
