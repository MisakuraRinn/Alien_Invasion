#coding=GBK
class Settings:
  def __init__(self):
    self.screen_width=1200
    self.screen_height=800
    self.bg_color=(230,230,230)
    
    #飞船速度
    self.ship_speed=5
    self.ship_limit=3
    #子弹设置
    self.bullet_speed=20
    self.bullet_width=3000
    self.bullet_height=15
    self.bullet_color=(60,60,60)
    self.bullet_allowed=100
    
    #外星人设置
    self.alien_speed=1
    self.fleet_drop_speed=10
  
    #1为向右运动，-1为向左运动
    self.fleet_direction=1
    
    #游戏节奏加快
    self.speedup_scale=1.1
    self.score_scale=1.5
    self.initialize_dynamic_settings();
    
    #计分设置
    self.alien_points=50
  
  def initialize_dynamic_settings(self):
    """初始化随游戏进行而变化的设置"""
    self.ship_speed=5
    self.bullet_speed=35
    self.alien_speed=1
    self.alien_points=50
    
    self.fleet_direction=1
  def increase_speed(self):
    """提高速度设置的值"""
    self.ship_speed*=self.speedup_scale
    # self.bullet_speed*=self.speedup_scale
    self.alien_speed*=self.speedup_scale
    self.alien_points=int(self.alien_points*self.score_scale)
  