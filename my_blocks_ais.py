import numpy as np
import math as m
import pygame as py
import random as rand
from sys import exit
																																																					
py.init()

#________________________________

def text(t,c,p,s):
	font=py.font.Font(None,s)
	text=font.render(t,True,c)
	sc.blit(text,p)


class creature(py.sprite.Sprite):
	def __init__(self,pos,mass,isnew):
		super().__init__()
		self.radius=10
		self.img=surf01
		self.img2=surf03
		self.img1=surf02
		self.rect=self.img.get_rect(center=pos)
		self.mask=py.mask.from_surface(self.img)
		
		
		self.pos=pos
		self.velocity=[0,0]
		self.acceleration=[0,0]
		self.mass=mass
		self.kinetic_friction=0.5
		self.static_friction=0.6
		self.gravity=100
		self.force=[0,0]
		
		self.angle=rand.randint(0,359)
		self.anglea=0
		self.speed_limit=rand.randint(50,100)
		self.view_range=rand.randint(15,25)
		
		self.sprt=[]
		
		self.istokill=False
		
		
		self.a=np.zeros([3+2])
		self.w=np.array([]).reshape(0,4)
		self.inp=3
		self.out=2
		self.bias=0
		if isnew:
			for _ in range(4):
				self.mutate_w()
		
		self.score=0
		self.hp=100
		self.hunger=100
		
		self.boo1=True
		self.sprt2=0
		self.iscoll=False
		self.mass1=self.mass
		self.imgg=py.transform.scale(self.img,(round(self.mass*35),round(self.mass*35)))
		self.where_food=None
	def update(self):
		global leadscore
		if self.score>leadscore:
			leadscore=self.score
		self.angle+=360 if (self.angle<0) else (-360 if (self.angle>=360) else 0)
		if self.hunger>100:
			self.hunger=100
			self.hp+=0.1
		if self.hunger>0:
			self.hunger-=0.2*30/fps
		if self.hunger<=0:
			self.hp-=0.2*30/fps
		if self.hp<=0:
			self.kill()
			global diedcount
			diedcount+=1
		if self.mass>1:
			self.mass=1
		if self.hunger>0 and self.mass!=self.mass1:
			self.image=py.transform.scale(self.img,(round(self.mass*35),round(self.mass*35)))
			self.imgg=self.image
		elif self.hunger<=0:
			if round(self.hp)/4%2==0:
				self.image=py.transform.scale(self.img2,(round(self.mass*35),round(self.mass*35)))
			else:
				self.image=py.transform.scale(self.img,(round(self.mass*35),round(self.mass*35)))
			self.mass+=0.00001
		else:
			self.image=self.imgg
		self.image=py.transform.rotate(self.image,-self.angle)
		self.rect=self.image.get_rect(center=np.add(self.pos,offset))
		self.mask=py.mask.from_surface(self.image)
		
		self.circoll=py.sprite.collide_circle_ratio(self.view_range)
		self.coll=py.sprite.spritecollide(self,food_group,False,collided=self.circoll)
		if len(self.coll)>0:
			self.pts=[]
			self.daa=0
			if self.sprt2!=0:
				self.coll=[self.sprt2]
			for sprite in self.coll:
				self.da2=(pangle(sprite.pos,self.pos)*180/m.pi-180)-(self.angle-180)
				if abs(self.da2)<90 and sprite.alive():
					self.pts.append(sprite.rect.center)
					self.daa=self.da2/45
					self.sprt2=sprite
					self.daa1=0
					self.where_food=None
					break
				else:
					if self.where_food==None:
						self.where_food=food_group.sprites()[rand.randint(0,len(food_group)-1)].pos
					self.sprt2=0
					self.daa1=((pangle(self.where_food,self.pos)*180/m.pi-180)-(self.angle-180))
					
#			if len(self.pts)>0:
#				for p in self.pts:
#					py.draw.line(sc,(255,0,255),self.rect.center,p,5)
		else:
			self.daa=0
			self.daa1=0
			self.where_food=None
		
	#	py.draw.circle(sc,(0,255,0),(self.rect.centerx+100*self.daa,self.rect.centery),10)
		
		self.collide=py.sprite.spritecollide(self,crea_group,False)
		if len(self.collide)>0:
			self.sprt1=[]
			for sprite in self.collide:
				if self.sprt.count(sprite):
					self.boo=False
					self.sprt1.append(sprite)
				else:
					self.boo=True
					self.sprt1=[]
				if (py.sprite.collide_mask(self,sprite)!=None and sprite!=self) and self.boo:
					self.da=pangle(self.pos,sprite.pos)*180/m.pi
					self.da1=pangle(self.pos,py.sprite.collide_mask(self,sprite))*180/m.pi
					self.dv=(self.velocity[0]-v2a(np.multiply(a2v([sprite.velocity[0],sprite.angle]),[m.cos(self.da*m.pi/180),m.sin(self.da*m.pi/180)]))[0])*self.mass
					sprite.force=np.add(sprite.force,[abs(self.dv),(180+self.da)])
					self.dr=np.subtract(py.sprite.collide_mask(self,sprite),self.pos)
					sprite.anglea+=self.dv*m.sin(((self.da-180)-(self.da1-180))*m.pi/180)/2-self.anglea
					self.sprt1.append(sprite)
					sprite.iscoll=True

			self.sprt=[]
			self.sprt=self.sprt1
			
		self.proceed([self.daa,self.daa1,2])
		if (abs(self.velocity[0])<=self.speed_limit and self.iscoll==False) and abs(self.anglea)<5:
			self.force=[self.output[0]*5*self.mass*25/fps,self.angle]
		else:
			self.iscoll=False
		if abs(self.anglea)<5:
			self.angle+=self.output[1]*5*25/fps
			
#		if self.force[0]<=self.static_friction*self.mass*self.gravity and self.velocity[0]==0:
#			self.force[0]=0
		if self.istokill:
			self.kill()
#		if self.force[0]>=2000:
#			self.image.fill('Red')
#			self.istokill=True
		if self.force[0]>0:
			self.acceleration=[self.force[0]/self.mass,self.force[1]]
			self.force=[0,0]
			self.acceleration1=a2v(self.acceleration)
			self.velocity1=a2v(self.velocity)
			self.velocity=v2a(np.add(self.velocity1,self.acceleration1))
		
		self.velocity=[self.velocity[0]+((-self.kinetic_friction*self.gravity/fps) if (self.velocity[0]+(-self.kinetic_friction*self.gravity/fps))>0 else -self.velocity[0]),self.velocity[1]]
		if self.anglea>0:
			self.anglea-=abs(self.anglea*self.kinetic_friction/fps) if (self.anglea-abs(self.anglea*self.kinetic_friction/fps)>0) else self.anglea
		else:
			self.anglea+=abs(self.anglea*self.kinetic_friction/fps) if (self.anglea+abs(self.anglea*self.kinetic_friction/fps)<0) else self.anglea
		self.angle+=self.anglea/fps
		
		self.pos=np.add(self.pos,np.divide(a2v(self.velocity),fps))
		
		self.mass1=self.mass
		
	def mutate_w(self):
		while m.comb(len(self.a),2)-m.comb(self.inp,2)-m.comb(self.out,2)!=len(self.w):
			self.ws=[]
			self.ws1=[]
			self.ws3=np.array([])
			self.boo=True
			for i in range(len(self.a)-self.out):
				if i>=self.inp:
					i+=self.out
				self.ws.append(i)
			self.r=self.ws[rand.randint(0,len(self.ws)-1)]
			for i,r in enumerate(self.w[:,0]):
				if self.r==r:
					self.ws1.append(self.w[i,1])
			for i in range(len(self.a)-self.inp):
				if self.r<self.inp:
					i+=self.inp
				else:
					i+=self.r+1
				if i>=len(self.a)+self.out:
					break
				if i>=len(self.a):
					i=i-len(self.a)+self.inp
				self.ws3=np.append(self.ws3,i)
			for i,p in enumerate(self.ws3):
				if self.ws1.count(p)>0:
					self.ws3=np.delete(self.ws3,np.where(self.ws3==p)[0])
			if len(self.ws3)>0:
				self.r1=self.ws3[rand.randint(0,len(self.ws3)-1)]
			else:
				self.boo=False
			if self.boo:
				self.w=np.vstack([self.w,[self.r,self.r1,rand.uniform(-2,2),1]])
				break
	def mutate_a(self):
		if len(self.w)>0:
			self.av=[]
			for i,r in enumerate(self.w[:,1]):
				for j in range(self.out):
					j+=self.inp
					if r==j and self.w[i,3]==1:
						self.av.append(i)
			if len(self.av)>0:
				self.r2=rand.randint(0,len(self.av)-1)
				self.r2=self.av[self.r2]
				self.p=self.w[self.r2,0]
				self.p1=self.w[self.r2,1]
				self.w[self.r2,3]=0
				self.w=np.vstack([self.w,[self.p,len(self.a),rand.uniform(-2,2),1]])
				self.w=np.vstack([self.w,[len(self.a),self.p1,rand.uniform(-2,2),1]])
				self.a=np.append(self.a,0)
	def proceed(self,input):
		if len(self.w)>1:
			self.a[:]=0
			self.a[:self.inp]=input
			for i in range(len(self.a)-self.inp):
				i+=self.inp+self.out
				if i>=len(self.a):
					i=i-len(self.a)+self.inp
				for j,r in enumerate(self.w[:,1]):
					if i==r:
						self.a[i]+=self.w[j,2]*self.a[int(self.w[j,0])]
				self.a[i]=tanh(self.a[i]-self.bias)
			self.output=self.a[self.inp:self.inp+self.out]
		else:
			self.output=np.zeros([self.out])
			
			
class food(py.sprite.Sprite):
		def __init__(self,img,pos):
			super().__init__()
			self.size=rand.randint(5,15)
			self.image=py.transform.scale(img,(self.size,self.size))
			self.mask=py.mask.from_surface(self.image)
			self.rect=self.image.get_rect(center=pos)
			self.pos=pos
		def update(self):
			self.rect=self.image.get_rect(center=np.add(self.pos,offset))
			self.col=py.sprite.spritecollide(self,crea_group,False)
			if len(self.col)>0:
				for sprite in self.col:
					if py.sprite.collide_mask(self,sprite):
						if sprite.mass<1:
							sprite.mass+=self.size/150
						sprite.hunger+=self.size*2
						sprite.hp+=self.size/2
						sprite.score+=1
						if sprite.mass>=0.9:
							if rand.random()<0.20:
								crea=creature((np.add(sprite.pos,a2v([50,180-sprite.angle]))),0.5,False)
								crea.w=sprite.w
								crea.a=sprite.a
								self.rand=rand.random()
								if self.rand<0.33:
									crea.mutate_w()
								elif self.rand>=0.33 and self.rand<0.66:
									crea.mutate_a()
								crea_group.add(crea)
						self.kill()

#________________________________


def lerp(a,b,t):
	return (1-t)*a+b*t
	
def tanh(x):
	return (pow(m.e,x)-pow(m.e,-x))/(pow(m.e,x)+pow(m.e,-x))

def pangle(p,p1):
	v=np.subtract(p,p1)
	c=m.sqrt(v[0]**2+v[1]**2)
	t=m.acos(v[0]/c)
	it=m.pi-t
	n=1 if v[1]<0 else 0
	res=t+2*it*n
	if np.isnan(res):
		res=0
	return res
	
def vangle(v):
	c=m.sqrt(v[0]**2+v[1]**2)
	t=m.acos(v[0]/c)
	it=m.pi-t
	n=1 if v[1]<0 else 0
	res=t+2*it*n
	if np.isnan(res):
		res=0
	return res
	
def a2v(adj_a):
	res=[adj_a[0]*m.cos(adj_a[1]*m.pi/180),adj_a[0]*m.sin(adj_a[1]*m.pi/180)]
	if np.isnan(res[0]):
		res[0]=0
	if np.isnan(res[1]):
		res[1]=0
	return res
	
def v2a(v):
	res=[m.sqrt(v[0]**2+v[1]**2),vangle(v)*180/m.pi]
	if np.isnan(res[0]):
		res[0]=0
	if np.isnan(res[1]):
		res[1]=0
	return res

def draw01(color):
	b=[0,0,0]
	c=color
	l=np.zeros([7,7,3],np.uint8)
	l[:]=[
	[b,b,b,b,b,b,b],
	[b,c,c,c,c,c,b],
	[b,c,b,c,b,c,b],
	[b,c,b,c,c,c,b],
	[b,c,b,c,b,c,b],
	[b,c,c,c,c,c,b],
	[b,b,b,b,b,b,b]
	]
	return py.image.frombuffer(l,[7,7],'RGB').convert_alpha()

def draw02(c):
	b=[0,0,0]
	l=np.zeros([5,5,3],np.uint8)
	l[:]=[
	[b,b,b,b,b],
	[b,c,c,c,b],
	[b,c,b,c,b],
	[b,c,c,c,b],
	[b,b,b,b,b]
	]
	return py.image.frombuffer(l,[5,5],'RGB').convert()

#________________________________


sc=py.display.set_mode((1450,670))
clock=py.time.Clock()


surf01=draw01([0,255,255])
surf02=draw02([127,0,255])
surf03=draw01([255,0,0])

crea_group=py.sprite.Group()
food_group=py.sprite.Group()

leadscore=0
diedcount=0

offset=[0,0]
counter=0

while 1:
	fps=clock.get_fps()
	if fps==0:
		fps=10*100
	elif fps>60:
		fps=60
	event=py.event.get()
	for e in event:
		if e==py.QUIT:
			py.quit()
			exit()
		if e.type==py.FINGERMOTION:
			x=e.x*sc.get_width()
			y=e.y*sc.get_height()
			dx=e.dx
			dy=e.dy
			offset[0]+=dx*1000
			offset[1]+=dy*1000
			
	sc.fill('Black')
	
	if len(food_group)<150:
		food_sprite=food(surf02,(rand.randint(-1200,1200),rand.randint(-1200,1200)))
		food_group.add(food_sprite)
	if len(crea_group)<5:
		crea=creature((rand.randint(-1000,1000),rand.randint(-1000,1000)),1,True)
		crea_group.add(crea)
	
	food_group.update()
	food_group.draw(sc)
	crea_group.update()
	crea_group.draw(sc)
	text(f'highscore: {leadscore}',(0,255,0),(200,10),30)
	text(f'starved to death: {diedcount}',(0,255,0),(600,10),30)
	
	text(f'population: {len(crea_group)}',(0,255,0),(400,10),30)
#	text(str(offset),(0,255,0),(100,200),30)
#	text(str(counter),(0,255,255),(50,200),40)

	if fps!=10*100:
		text(f'fps: {round(fps)}',(0,255,0),(10,10),30)
	py.display.update()
	clock.tick(60)