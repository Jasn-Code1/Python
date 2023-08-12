#pylint:disable=E1137
import pygame as py
import numpy as np
import sqlite3 as sq
from math import *
from sys import exit

py.init()

#__PYGAME_FUNCTIONS_AND_CLASSES__

def text(text,color,pos,size):
	font=py.font.Font(None,size)
	text=font.render(text,True,color)
	sc.blit(text,pos)

#__MATH_FUNCTION__

def lerp4(a,b,c,d,t):
	p=t/(2-t)
	q=(1-t)/(2-t)
	mat=[
	[1-t,-t,0,0],
	[1-t,t,0,2-t],
	[c*p,a*q,-t,-b],
	[d*p,b*q,1-t,-c]
	]
	return np.linalg.det(mat)

def lerp3v(p,t):
	a=p[0]
	b=p[1]
	c=p[2]
	d=p[3]
	x=lerp4(a[0],b[0],c[0],d[0],t)
	y=lerp4(a[1],b[1],c[1],d[1],t)
	return x,y

#__SETUP__

sc=py.display.set_mode((1450,670))
clock=py.time.Clock()

#__OTHERS__
off=100
mul=50
xoff=400
wi=300

p=[xoff,off+mul]
p1=[xoff,off+2*mul]
p2=[xoff,off+3*mul]
p3=[xoff,off+4*mul]
p4=[xoff,off+5*mul]
p5=[xoff,off+6*mul]
p6=[xoff,off+7*mul]
p7=[xoff,off+8*mul]
p8=[xoff,off+9*mul]
p9=[xoff,off+10*mul]
p10=[xoff,off+11*mul]
p11=[xoff,off+12*mul]
p12=[xoff,off+13*mul]
p13=[xoff,off+14*mul]
p14=[xoff,off+15*mul]
p15=[xoff,off+16*mul]
p16=[xoff,off+17*mul]
p17=[xoff,off+18*mul]
p18=[xoff,off+19*mul]
p19=[xoff,off+20*mul]
p20=[xoff,off+21*mul]
p21=[xoff,off+22*mul]
p22=[xoff,off+23*mul]
p23=[xoff,off+24*mul]
p24=[xoff,off+25*mul]

points_line=[]
points=[p,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23,p24]

rect=py.Rect(-100,-100,50,50)
ptc=None

anim=0

bool1=False

while 1:
	fps=clock.get_fps()
	if fps>60:
		fps=60
	if fps==0:
		fps=10**100
	event=py.event.get()
	for e in event:
		if e==py.QUIT:
			py.quit()
			exit()
		if e.type==py.FINGERDOWN:
			x=e.x*sc.get_width()
			y=e.y*sc.get_height()
			rect.center=(x,y)
		if e.type==py.FINGERMOTION:
			x=e.x*sc.get_width()
			y=e.y*sc.get_height()
			rect.center=(x,y)
		if e.type==py.FINGERUP:
			rect.center=(-100,-100)
			bool1=False
	
	if anim<360:
		anim+=10
	else:
		anim=0
	
	rad=anim*pi/180
	
	p=[xoff+7*wi/8*cos(rad),p[1]]
	p1=[xoff+wi*cos(rad+pi/6),p1[1]]
	p2=[xoff+wi*cos(rad+2*pi/6),p2[1]]
	p3=[xoff+7*wi/8*cos(rad+3*pi/6),p3[1]]
	p4=[xoff+wi*cos(rad+4*pi/6),p4[1]]
	p5=[xoff+wi*cos(rad+5*pi/6),p5[1]]
	p6=[xoff+7*wi/8*cos(rad+6*pi/6),p6[1]]
	p7=[xoff+wi*cos(rad+7*pi/6),p7[1]]
	p8=[xoff+wi*cos(rad+8*pi/6),p8[1]]
	p9=[xoff+7*wi/8*cos(rad+9*pi/6),p9[1]]
	p10=[xoff+wi*cos(rad+10*pi/6),p10[1]]
	p11=[xoff+wi*cos(rad+11*pi/6),p11[1]]
	p12=[xoff+7*wi/8*cos(rad),p12[1]]
	p13=[xoff+wi*cos(rad+pi/6),p13[1]]
	p14=[xoff+wi*cos(rad+2*pi/6),p14[1]]
	p15=[xoff+7*wi/8*cos(rad+3*pi/6),p15[1]]
	p16=[xoff+wi*cos(rad+4*pi/6),p16[1]]
	p17=[xoff+wi*cos(rad+5*pi/6),p17[1]]
	p18=[xoff+7*wi/8*cos(rad+6*pi/6),p18[1]]
	p19=[xoff+wi*cos(rad+7*pi/6),p19[1]]
	p20=[xoff+wi*cos(rad+8*pi/6),p20[1]]
	p21=[xoff+7*wi/8*cos(rad+9*pi/6),p21[1]]
	p22=[xoff+wi*cos(rad+10*pi/6),p22[1]]
	p23=[xoff+wi*cos(rad+11*pi/6),p23[1]]
	p24=[xoff+7*wi/8*cos(rad),p24[1]]
	
	points=[p,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23,p24]
	
	if rect.collidepoint((xoff-7*wi/8,off)):
		bool1=True
	if bool1:
		wi=8*(xoff-rect.centerx)/7
	
	sc.fill((0,0,0))
	
	py.draw.rect(sc,(255,0,0),rect)
	
	points_line.clear()
	if len(points_line)<=1:
		ran=21
		ra=ran-1
		for i in range(ran):
			t=i/ra
			points_line.append(lerp3v(points[:4],t))
		for i in range(ran):
			t=i/ra
			points_line.append(lerp3v(points[3:7],t))
		for i in range(ran):
			t=i/ra
			points_line.append(lerp3v(points[6:10],t))
		for i in range(ran):
			t=i/ra
			points_line.append(lerp3v(points[9:13],t))
		for i in range(ran):
			t=i/ra
			points_line.append(lerp3v(points[12:16],t))
		for i in range(ran):
			t=i/ra
			points_line.append(lerp3v(points[15:19],t))
		for i in range(ran):
			t=i/ra
			points_line.append(lerp3v(points[18:22],t))
		for i in range(ran):
			t=i/ra
			points_line.append(lerp3v(points[21:25],t))
	
#	py.draw.lines(sc,(255,0,0),False,points,3)
	py.draw.line(sc,(0,0,255),(xoff-7*wi/8,off),(xoff-7*wi/8,1350),5)
	
	if len(points_line)>1:
		py.draw.lines(sc,(0,255,0),False,points_line,5)
	
#	for point in points:
#		py.draw.circle(sc,(255,255,255),point,3)
	
	if fps!=10**100:
		text(str(round(fps)),(0,255,0),(10,10),30)
	py.display.update()
	clock.tick(60)