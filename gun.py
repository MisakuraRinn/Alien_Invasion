#coding=GBK
import pygame
class Gun:
  def __init__(self,ai_game):
    self.ai_game=ai_game
    self.settings=ai_game.settings
    self.stats=ai_game.stats
    self.sb=ai_game.sb
    self.initialize_dynamic_settings()
    self.weapons={
      'pistol':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':True,
        'max_ammo':12,
        'shoot_interval':0.5,
        'reload_interval':0.05,
        'bullet_max_directX':0.2,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        
        },
      'machineGun':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':False,
        'max_ammo':30,
        'shoot_interval':0.1,
        'reload_interval':0.05,
        'bullet_max_directX':0.1,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':2,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        },
      'shotGun':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':False,
        'max_ammo':5,
        'shoot_interval':1,
        'reload_interval':0.5,
        'bullet_max_directX':0.5,
        'number_of_bullets_in_one_fire':5,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        },
      'AssaultRifle':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':False,
        'max_ammo':5,
        'shoot_interval':1,
        'reload_interval':1,
        'bullet_max_directX':0.05,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':10,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        },
      'GrenadeLaucher':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'max_ammo':1,
        'shoot_interval':3,
        'reload_interval':3,
        'bullet_max_directX':0.1,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':100,
        'bullet_can_rebound_number':0
      }
    }
    for i in range(1,8):self.weapons["pistol"]['se_shot'].append(pygame.mixer.Sound(f"voices/pistol/Gun_Pistol_Shot{i}.ogg"))
    self.weapons["pistol"]['se_reload'].append(pygame.mixer.Sound("voices/pistol/Gun_Reload_Weapon07.ogg"))
    self.weapons["pistol"]['se_select'].append(pygame.mixer.Sound("voices/pistol/Gun_DrawSelect_Pistol3.ogg"))
    
    self.weapons["machineGun"]['se_shot'].append(pygame.mixer.Sound("voices/machineGun/K_MachineGun01.ogg"))
    self.weapons["machineGun"]['se_reload'].append(pygame.mixer.Sound("voices/machineGun/Gun_Reload_Weapon03.ogg"))
    self.weapons["machineGun"]['se_select'].append(pygame.mixer.Sound("voices/machineGun/Gun_DrawSelect_Weapon08.ogg"))
    
    for i in range(1,8):self.weapons["shotGun"]['se_shot'].append(pygame.mixer.Sound(f"voices/shotGun/Shotgun_Shot{i}.ogg"))
    self.weapons["shotGun"]['se_reload'].append(pygame.mixer.Sound("voices/shotGun/Gun_Reload_Weapon02.ogg"))
    self.weapons["shotGun"]['se_select'].append(pygame.mixer.Sound("voices/shotGun/Gun_DrawSelect_Weapon02.ogg"))
    
    for i in range(1,3):self.weapons["AssaultRifle"]['se_shot'].append(pygame.mixer.Sound(f"voices/AssaultRifle/Gun_AssaultRifle_PowerShot{i}.ogg"))
    self.weapons["AssaultRifle"]['se_reload'].append(pygame.mixer.Sound("voices/AssaultRifle/Gun_Reload_Weapon19.ogg"))
    self.weapons["AssaultRifle"]['se_select'].append(pygame.mixer.Sound("voices/AssaultRifle/Gun_DrawSelect_Weapon06.ogg"))
    
    for i in range(1,9):self.weapons["GrenadeLaucher"]['se_shot'].append(pygame.mixer.Sound(f"voices/GrenadeLaucher/GrenadeLauncher_Shot{i}.ogg"))
    self.weapons["GrenadeLaucher"]['se_reload'].append(pygame.mixer.Sound("voices/GrenadeLaucher/Gun_Reload_Weapon04.ogg"))
    self.weapons["GrenadeLaucher"]['se_select'].append(pygame.mixer.Sound("voices/GrenadeLaucher/Gun_DrawSelect_Weapon10.ogg"))
    print("ckp")
  def initialize_dynamic_settings(self):
    self.weapons={
      'pistol':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':True,
        'max_ammo':12,
        'shoot_interval':0.5,
        'reload_interval':0.05,
        'bullet_max_directX':0.2,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        
        },
      'machineGun':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':False,
        'max_ammo':30,
        'shoot_interval':0.1,
        'reload_interval':0.05,
        'bullet_max_directX':0.1,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':2,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        },
      'shotGun':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':False,
        'max_ammo':5,
        'shoot_interval':1,
        'reload_interval':0.5,
        'bullet_max_directX':0.5,
        'number_of_bullets_in_one_fire':5,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        },
      'AssaultRifle':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':False,
        'max_ammo':5,
        'shoot_interval':1,
        'reload_interval':1,
        'bullet_max_directX':0.05,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':20,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        },
      'GrenadeLaucher':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'max_ammo':3,
        'shoot_interval':1,
        'reload_interval':1,
        'bullet_max_directX':0.1,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':10,
        'bullet_can_rebound_number':3
      }
    }
    for i in range(1,8):self.weapons["pistol"]['se_shot'].append(pygame.mixer.Sound(f"voices/pistol/Gun_Pistol_Shot{i}.ogg"))
    self.weapons["pistol"]['se_reload'].append(pygame.mixer.Sound("voices/pistol/Gun_Reload_Weapon07.ogg"))
    self.weapons["pistol"]['se_select'].append(pygame.mixer.Sound("voices/pistol/Gun_DrawSelect_Pistol3.ogg"))
    
    self.weapons["machineGun"]['se_shot'].append(pygame.mixer.Sound("voices/machineGun/K_MachineGun01.ogg"))
    self.weapons["machineGun"]['se_reload'].append(pygame.mixer.Sound("voices/machineGun/Gun_Reload_Weapon03.ogg"))
    self.weapons["machineGun"]['se_select'].append(pygame.mixer.Sound("voices/machineGun/Gun_DrawSelect_Weapon08.ogg"))
    
    for i in range(1,8):self.weapons["shotGun"]['se_shot'].append(pygame.mixer.Sound(f"voices/shotGun/Shotgun_Shot{i}.ogg"))
    self.weapons["shotGun"]['se_reload'].append(pygame.mixer.Sound("voices/shotGun/Gun_Reload_Weapon02.ogg"))
    self.weapons["shotGun"]['se_select'].append(pygame.mixer.Sound("voices/shotGun/Gun_DrawSelect_Weapon02.ogg"))
    
    for i in range(1,3):self.weapons["AssaultRifle"]['se_shot'].append(pygame.mixer.Sound(f"voices/AssaultRifle/Gun_AssaultRifle_PowerShot{i}.ogg"))
    self.weapons["AssaultRifle"]['se_reload'].append(pygame.mixer.Sound("voices/AssaultRifle/Gun_Reload_Weapon19.ogg"))
    self.weapons["AssaultRifle"]['se_select'].append(pygame.mixer.Sound("voices/AssaultRifle/Gun_DrawSelect_Weapon06.ogg"))
    
    for i in range(1,9):self.weapons["GrenadeLaucher"]['se_shot'].append(pygame.mixer.Sound(f"voices/GrenadeLaucher/GrenadeLauncher_Shot{i}.ogg"))
    self.weapons["GrenadeLaucher"]['se_reload'].append(pygame.mixer.Sound("voices/GrenadeLaucher/Gun_Reload_Weapon04.ogg"))
    self.weapons["GrenadeLaucher"]['se_select'].append(pygame.mixer.Sound("voices/GrenadeLaucher/Gun_DrawSelect_Weapon10.ogg"))
    self.current_gun=self.weapons['pistol']
    
  def weapon_level_up(self,weapon,key,value):
    """升级武器，升级武器属性，升级数值"""
    self.weapons[weapon][key]+=value
  def change_weapon(self,weapon):
    # 播放换枪音效
    # print("play changeGUn")
    self.current_gun=self.weapons[weapon]
    self.ai_game.channel1.play(self.current_gun['se_select'][0])
    
    self.settings.ammo_left=0
    self.sb.prep_ammo()
    # self.