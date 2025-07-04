
from collisionbody import CollisionBody, CollisionSide, get_broadphase
from pygame import Vector2, Rect, Color
import pygame
import engine as engine
from sprite import Sprite
from tileset import Tileset
from tilemap import Tilemap
from mario import Mario, COYOTE_TIME_MAX, DeadMario, PowerupState
import mario
from utils import clamp, floorvec
from math import ceil, floor
from goomba import Goomba
from green_koopa import GreenKoopa
from green_koopa_shell import GreenKoopaShell
from paratroopa import Paratroopa
import green_koopa_shell
import red_koopa_shell
from red_koopa_shell import RedKoopaShell
from red_koopa import RedKoopa
import main_game as main_game

class World:
    def draw(self):
        self.tilemap.draw()
        self.draw_enemies()
        self.draw_mario()
        self.draw_powerups()
        self.draw_misc()
    
    def update(self):
        self.update_powerups()
        self.update_enemies()
        self.update_misc()
        self.update_mario()
    
    def draw_powerups(self):
        for mushroom in self.mushrooms:
            mushroom.draw()
        for flower in self.fire_flowers:
            flower.draw()
    
    def draw_mario(self):
        if self.mario.alive:
            self.mario.draw()
        if self.dead_mario:
            self.dead_mario.draw()
    
    def draw_misc(self):
        for fireball in self.fireballs:
            fireball.draw()
    
    def draw_enemies(self):
        for goomba in self.goombas:
            goomba.draw()
        for koopa in self.green_koopas:
            koopa.draw()
        for shell in self.green_koopa_shells:
            shell.draw()
        for koopa in self.red_koopas:
            koopa.draw()
        for shell in self.red_koopa_shells:
            shell.draw()
        for paratroopa in self.paratroopas:
            paratroopa.draw()
    
    def update_misc(self):
        for fireball in self.fireballs:
            fireball.update()
    
    def update_mario(self):
        pos = floorvec(self.tilemap.translate(Vector2(self.mario.body.position.x, self.mario.body.position.y + self.mario.sprite.size.y)))
        if pos.y >= self.tilemap.size[1]:
            self.kill_mario()
        
        if self.mario.alive:
            self.mario.update()
        else:
            if self.dead_mario.reset_flag == 1:
                engine.instance.gamestate_manager.set_state(main_game.MainGame())
            
            self.dead_mario.update()

    def damage_mario(self):
        if self.mario.lock_state:
            return
        if self.mario.powerup_state == PowerupState.Small:
            self.kill_mario()
        else:
            self.mario.change_powerup_state(PowerupState.Small)

    def kill_mario(self):
        if not self.mario.alive or self.mario.lock_state:
            return
        
        self.dead_mario = DeadMario(self.mario.body.position)
        self.mario.alive = False
    
    def update_powerups(self):
        for flower in self.fire_flowers:
            if flower.delete_flag == 1:
                self.fire_flowers.remove(flower)
                continue
            
            flower.update()
            
            if not self.mario.alive or self.mario.lock_state:
                continue
            
            side = self.mario.body.get_collision_side(flower.body)
            if side != CollisionSide.Null and not self.mario.lock_state:
                if self.mario.powerup_state == PowerupState.Small:
                    self.mario.change_powerup_state(PowerupState.Normal)
                else:
                    self.mario.change_powerup_state(PowerupState.Fire)
                flower.delete_flag = 1
        for mushroom in self.mushrooms:
            if mushroom.delete_flag == 1:
                self.mushrooms.remove(mushroom)
                continue
                
            mushroom.update()
            
            if not self.mario.alive or self.mario.lock_state:
                continue
            
            side = self.mario.body.get_collision_side(mushroom.body)
            if side != CollisionSide.Null and not self.mario.lock_state:
                self.mario.change_powerup_state(PowerupState.Normal)
                mushroom.delete_flag = 1
            
    
    def update_enemies(self):
        for goomba in self.goombas:
            if goomba.delete_flag == 1:
                self.goombas.remove(goomba)
                continue
            
            goomba.update()
            
            if not self.mario.alive or not goomba.alive or self.mario.invincibility_frames > 0 or self.mario.lock_state:
                continue
            
            side = self.mario.body.get_collision_side(goomba.body)
            if side == CollisionSide.Bottom:
                self.mario.body.velocity.y = -3.5
                goomba.stomp()
            elif side != CollisionSide.Null:
                self.damage_mario()
      
        for koopa in self.red_koopas:
            if koopa.delete_flag == 1:
                self.red_koopas.remove(koopa)
                continue
            
            koopa.update()
            
            if self.mario.alive == False or self.mario.invincibility_frames > 0 or self.mario.lock_state:
                continue
            
            side = self.mario.body.get_collision_side(koopa.body)
            if side == CollisionSide.Bottom:
                self.mario.body.velocity.y = -3
                self.red_koopas.remove(koopa)
                
                shell = RedKoopaShell(self.tilemap)
                shell.body.position = koopa.body.position
                shell.direction = 0
                shell.wakeup_direction = koopa.direction
                shell.can_wakeup = True
                shell.time_since_reset = 0
                shell.time_of_reset = pygame.time.get_ticks()
                self.red_koopa_shells.append(shell)
            elif side != CollisionSide.Null:
                self.damage_mario()
        
        for koopa in self.green_koopas:
            if koopa.delete_flag == 1:
                self.green_koopas.remove(koopa)
                continue
            
            koopa.update()
            
            if self.mario.alive == False or self.mario.invincibility_frames > 0 or self.mario.lock_state:
                continue
            
            side = self.mario.body.get_collision_side(koopa.body)
            if side == CollisionSide.Bottom:
                self.mario.body.velocity.y = -3
                self.green_koopas.remove(koopa)
                
                shell = GreenKoopaShell(self.tilemap)
                shell.body.position = koopa.body.position
                shell.direction = 0
                shell.wakeup_direction = koopa.direction
                shell.can_wakeup = True
                shell.time_since_reset = 0
                shell.time_of_reset = pygame.time.get_ticks()
                self.green_koopa_shells.append(shell)
            elif side != CollisionSide.Null:
                self.damage_mario()
        
        for paratroopa in self.paratroopas:
            if paratroopa.delete_flag == 1:
                self.paratroopas.remove(paratroopa)
                continue
            
            paratroopa.update()
            
            if self.mario.alive == False or self.mario.invincibility_frames > 0 or self.mario.lock_state:
                continue
            
            side = self.mario.body.get_collision_side(paratroopa.body)
            if side != CollisionSide.Null:
                if side == CollisionSide.Bottom:
                    self.mario.body.velocity.y = -3.5
                    
                    self.paratroopas.remove(paratroopa)
                    
                    koopa = GreenKoopa(self.tilemap)
                    koopa.body.position = paratroopa.body.position
                    koopa.direction = paratroopa.direction
                    
                    self.green_koopas.append(koopa)
                    koopa.update()
                else:
                    self.damage_mario()
        
        for shell in self.red_koopa_shells:
            if shell.delete_flag == 1:
                self.red_koopa_shells.remove(shell)
                continue
            
            shell.update()
            
            if shell.time_since_reset > red_koopa_shell.WAKEUP_TIME and shell.direction == 0 and shell.can_wakeup:
                
                self.red_koopa_shells.remove(shell)
                
                koopa = RedKoopa(self.tilemap)
                koopa.body.position = shell.body.position
                koopa.direction = shell.wakeup_direction
                self.red_koopas.append(koopa)
                koopa.update()
                
                continue
            
            enemies = self.get_all_enemies()
            enemies.remove(shell)
            for enemy in enemies:
                if not enemy.alive:
                    continue
                
                side = shell.body.get_collision_side(enemy.body)
                if side != CollisionSide.Null:
                    kill_op = getattr(enemy, "kill", None)
                    if callable(kill_op):
                        kill_op()
            
            
            if self.mario.alive == False or self.mario.invincibility_frames > 0 or self.mario.lock_state:
                continue
            
            side = self.mario.body.get_collision_side(shell.body)
            if side != CollisionSide.Null:
                if side == CollisionSide.Bottom:
                    self.mario.body.velocity.y = -3.5
                    if shell.direction == 0:
                        shell.can_wakeup = False
                        shell.direction = self.mario.direction
                        shell.time_since_reset = 0
                        shell.time_of_reset = 0
                        self.mario.body.solve_collision(shell.body, side)
                    else:
                        shell.direction = 0
                        shell.can_wakeup = True
                        shell.time_of_reset = pygame.time.get_ticks()
                        shell.time_since_reset = 0
                else:    
                    if shell.direction == 0:
                        shell.can_wakeup = False
                        shell.direction = self.mario.direction
                        shell.time_since_reset = 0
                        shell.time_of_reset = 0
                        self.mario.body.solve_collision(shell.body, side)
                    else:
                        self.damage_mario()
                        pass
        
        for shell in self.green_koopa_shells:
            if shell.delete_flag == 1:
                self.green_koopa_shells.remove(shell)
                continue
            
            shell.update()
            
            if shell.time_since_reset > green_koopa_shell.WAKEUP_TIME and shell.direction == 0 and shell.can_wakeup:
                
                self.green_koopa_shells.remove(shell)
                
                koopa = GreenKoopa(self.tilemap)
                koopa.body.position = shell.body.position
                koopa.direction = shell.wakeup_direction
                self.green_koopas.append(koopa)
                koopa.update()
                
                continue
            
            enemies = self.get_all_enemies()
            enemies.remove(shell)
            for enemy in enemies:
                if not enemy.alive:
                    continue
                
                side = shell.body.get_collision_side(enemy.body)
                if side != CollisionSide.Null:
                    kill_op = getattr(enemy, "kill", None)
                    if callable(kill_op):
                        kill_op()
            
            
            if self.mario.alive == False or self.mario.invincibility_frames > 0 or self.mario.lock_state:
                continue
            
            side = self.mario.body.get_collision_side(shell.body)
            if side != CollisionSide.Null:
                if side == CollisionSide.Bottom:
                    self.mario.body.velocity.y = -3
                    if shell.direction == 0:
                        shell.can_wakeup = False
                        shell.direction = self.mario.direction
                        shell.time_since_reset = 0
                        shell.time_of_reset = 0
                        self.mario.body.solve_collision(shell.body, side)
                    else:
                        shell.direction = 0
                        shell.can_wakeup = True
                        shell.time_of_reset = pygame.time.get_ticks()
                        shell.time_since_reset = 0
                else:    
                    if shell.direction == 0:
                        shell.can_wakeup = False
                        shell.direction = self.mario.direction
                        shell.time_since_reset = 0
                        shell.time_of_reset = 0
                        self.mario.body.solve_collision(shell.body, side)
                    else:
                        self.damage_mario()
                        pass
    
    def get_all_enemies(self) -> list:
        return self.goombas + self.green_koopas + self.green_koopa_shells + self.red_koopas + self.red_koopa_shells + self.paratroopas
    
    def __init__(self):
        self.mario = None
        self.dead_mario = None
        self.goombas = []
        self.green_koopas = []
        self.green_koopa_shells = []
        self.red_koopas = []
        self.red_koopa_shells = []
        self.paratroopas = []
        self.dead_marios = []
        self.pipes = []
        self.mushrooms = []
        self.fire_flowers = []
        self.fireballs = []
        self.tilemap = None
        self.tileset = None