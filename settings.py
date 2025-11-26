#coding=GBK
class Settings:
  def __init__(self):
    self.screen_width=1200
    self.screen_height=800
    self.bg_color=(230,230,230)
    
    #飞船速度
    self.ship_speed=10
    
    #子弹设置
    self.bullet_speed=15.0
    self.bullet_width=3000
    self.bullet_height=15
    self.bullet_color=(60,60,60)
    self.bullet_allowed=100
    
    #外星人设置
    self.alien_speed=1.0
    self.fleet_drop_speed=10
    
    #1为向右运动，-1为向左运动
    self.fleet_direction=1