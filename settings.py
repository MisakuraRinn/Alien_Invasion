#coding=GBK
import math
class Settings:
  def __init__(self,ai_game):
    self.screen_width=800
    self.screen_height=1200
    self.bg_color=(230,230,230)
    self.ai_game=ai_game
    # self.sb=ai_game.sb
    self.ship_limit=3
    #子弹设置
    # self.bullet_speed=20
    self.bullet_width=3
    self.bullet_height=15
    self.bullet_color=(60,60,60)
    self.bullet_allowed=1000
    # self.bullet_max_angle=0
    #外星人设置
    # self.alien_speed=1
    self.fleet_drop_speed=10
    #1为向右运动，-1为向左运动
    self.fleet_direction=1
    
    #游戏节奏加快
    self.alien_max_speed=20
    self.speedup_scale=1.1
    self.score_scale=1.5
    self.initialize_dynamic_settings();
    
  
  def initialize_dynamic_settings(self):
    """初始化随游戏进行而变化的设置"""
    self.ship_speed=5
    self.bullet_speed=15
    self.alien_speed=1
    self.alien_points=50
    # self.alien_max_health=3
    self.fleet_direction=1
    self.ammo_left=0
    # self.max_ammo=5
    # self.shoot_interval=1
    # self.reload_interval=0.5
    # self.number_of_bullets_in_one_fire=1
    # self.bullet_can_through_aliens_number=False
    # self.bullet_can_expolode_number=False
    # 穿透这个要单独判断，有的子弹不能穿透，有的不能
    
  def increase_speed(self):
    """提高速度设置的值"""
    self.alien_speed=min(1+math.log2(self.ai_game.stats.level),15)
    self.alien_points=int(50+self.ai_game.stats.level)
  