#coding=GBK
import pygame
class Ship:
  #管理飞船
  def __init__(self,ai_game):
    self.screen=ai_game.screen
    self.screen_rect=ai_game.screen.get_rect()
    self.settings=ai_game.settings
    self.image=pygame.image.load("./images/ship.bmp")
    self.rect=self.image.get_rect()
    self.rect.midbottom=self.screen_rect.midbottom
    self.moving_right=False
    self.moving_left=False
  def blitme(self):
    self.screen.blit(self.image,self.rect)
  def update(self):
    if self.moving_right and self.rect.right<self.screen_rect.right:
      self.rect.x+=self.settings.ship_speed
    if self.moving_left and self.rect.left>0:
      self.rect.x-=self.settings.ship_speed