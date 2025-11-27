#coding=GBK
import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
class AlienInvasion:
  """管理游戏资源和行为"""
  def __init__(self):
    pygame.init()
    self.clock=pygame.time.Clock()
    self.settings=Settings()
    self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
    self.game_active=False
    self.stats=GameStats(self)
    self.sb=Scoreboard(self)
    self.bullets=pygame.sprite.Group()
    self.aliens=pygame.sprite.Group()
    self.play_button=Button(self,"Play")
    self._create_fleet()
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
      # sys("cls")
      self._check_events()
      if self.game_active:
        self.ship.update()
        self._update_aliens()
        self._update_bullets()
        
      self._update_screen()
      self.clock.tick(60)
      # print(len(self.bullets))
  def _check_events(self):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        sys.exit()
      elif event.type==pygame.KEYDOWN:
        self._check_keydown_events(event)
      elif event.type==pygame.KEYUP:
        self._check_keyup_events(event)
      elif event.type==pygame.MOUSEBUTTONDOWN:
        mouse_pos=pygame.mouse.get_pos()
        self._check_play_button(mouse_pos)
  
  def _update_screen(self):
    self.screen.fill(self.settings.bg_color)
    self.aliens.draw(self.screen)
    self.ship.blitme()
    for bullet in self.bullets.sprites():
      bullet.draw_bullet()
    
    if not self.game_active:
      self.play_button.draw_button()
    
    self.sb.show_score()
    pygame.display.flip()
    
      
  def _update_bullets(self):
    self.bullets.update()
    for bullet in self.bullets.copy():
        if bullet.rect.bottom<=0:
          self.bullets.remove(bullet)
    self._check_bullet_alien_collisions()

  def _check_bullet_alien_collisions(self):
    """响应碰装"""
    collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,False,True)
    if collisions:
      for aliens in collisions.values():
        self.stats.score+=self.settings.alien_points*len(aliens)
      # self.stats.score+=self.settings.alien_points
      self.sb.prep_score()
      self.sb.check_high_score()
    if not self.aliens:
      # self.bullets.empty()
      self._create_fleet()
      self.stats.level+=1
      self.settings.increase_speed()
      self.sb.prep_level()
  
  def _check_aliens_bottom(self):
    for alien in self.aliens.sprites():
      if alien.rect.bottom>=self.settings.screen_height:
        print("到达边界")
        self._ship_hit()
        break
  
  def _update_aliens(self):
    """更新外星舰队中所有外星人的位置"""
    self._check_fleet_edges() 
    self.aliens.update()
    if pygame.sprite.spritecollideany(self.ship,self.aliens):
      self._ship_hit()
      # print("ship hit")
    self._check_aliens_bottom()
  
  def _ship_hit(self):
    """响应飞船和外星人的碰撞"""
    if self.stats.ships_left>0:
      self.stats.ships_left-=1
      self.sb.prep_ships()
      self.bullets.empty()
      self.aliens.empty()
      self._create_fleet()
      self.ship.center_ship()
      sleep(0.5)
    else :
      self.game_active=False
      pygame.mouse.set_visible(True)
  
  def _check_play_button(self,mouse_pos):
    button_clicked=self.play_button.rect.collidepoint(mouse_pos)
    if button_clicked and not self.game_active:
      self.stats.reset_stats()
      self.sb.prep_score()
      self.sb.prep_ships()
      self.sb.prep_level()
      self.game_active=True
      self.bullets.empty()
      self.aliens.empty()
      
      self._create_fleet()
      self.ship.center_ship()
      pygame.mouse.set_visible(False)
      
  def _fire_bullet(self):
    if len(self.bullets)<self.settings.bullet_allowed:
      new_bullet=Bullet(self)
      self.bullets.add(new_bullet)
  
  def _create_fleet(self):
    """创建一个外星舰队"""
    # self.aliens.add(alien)
    alien=Alien(self)
    alien_width,alien_height=alien.rect.size
    current_x,current_y=alien_width,alien_height
    while current_y <(self.settings.screen_height-3*alien_height):
      while current_x <(self.settings.screen_width-2*alien_width):
        # new_alien=Alien(self)
        # new_alien.x=current_x
        # new_alien.rect.x=current_x
        # new_alien.rect.y=current_y
        # self.aliens.add(new_alien)
        self._create_alien(current_x,current_y)
        current_x+=2*alien_width
      current_x=alien_width
      current_y+=2*alien_height
      print(current_y)
  
  def _create_alien(self,x_position,y_position):
    """创建一个外星人，并将其加入外星舰队"""
    new_alien=Alien(self)
    new_alien.x=x_position
    new_alien.rect.x=x_position
    new_alien.rect.y=y_position
    self.aliens.add(new_alien)
    
  def _check_fleet_edges(self):
    """在边缘的处理情况"""
    for alien in self.aliens.sprites():
      if alien.check_edges():
        self._change_fleet_direction()
        break
        
  def _change_fleet_direction(self):
    """将整个舰队下移，并改变方向"""
    for alien in self.aliens.sprites():
      alien.rect.y+=self.settings.fleet_drop_speed
    self.settings.fleet_direction*=-1
    
    
  def _check_keydown_events(self,event):
    """响应按下"""
    if event.key ==pygame.K_RIGHT:
      self.ship.moving_right=True
    if event.key==pygame.K_LEFT:
      self.ship.moving_left=True
    if event.key==pygame.K_q:
      print("exit")
      sys.exit()
    if event.key==pygame.K_SPACE and self.game_active:
      self._fire_bullet()
      
  def _check_keyup_events(self,event):
    if event.key==pygame.K_RIGHT:
      self.ship.moving_right=False
    if event.key==pygame.K_LEFT:
      self.ship.moving_left=False

if __name__=="__main__":
  ai=AlienInvasion()
  ai.run_game()
