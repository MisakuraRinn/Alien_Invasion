#coding=GBK
import pygame.font

class Button:
  """为游戏创建按钮的类，目前用于 Play 按钮。"""

  def __init__(self,ai_game,msg):
    """初始化按钮的属性。
    
    参数：
        ai_game: AlienInvasion 实例，用于获取 screen
        msg: 按钮上显示的文本
    """
    self.screen=ai_game.screen
    self.screen_rect=self.screen.get_rect()
    
    # 设置按钮的尺寸和其他属性
    self.width,self.height=200,50
    self.button_color=(0,135,0)
    self.texat_color=(255,255,255)
    self.font=pygame.font.SysFont(None,48)
    
    # 创建按钮的 rect 对象，并使其居中
    self.rect=pygame.Rect(0,0,self.width,self.height)
    self.rect.center=self.screen_rect.center
    
    # 预渲染按钮文字图像
    self._prep_msg(msg)

  def _prep_msg(self,msg):
    """将 msg 渲染为图像，并让其在按钮上居中。"""
    self.msg_image=self.font.render(
      msg,True,self.texat_color,self.button_color)
    self.msg_image_rect=self.msg_image.get_rect()
    self.msg_image_rect.center=self.rect.center

  def draw_button(self):
    """在屏幕上绘制按钮及文字。"""
    # 先绘制按钮矩形
    self.screen.fill(self.button_color,self.rect)
    # 再绘制文字图像
    self.screen.blit(self.msg_image,self.msg_image_rect)
