from math import *
import numpy as np
import os
list=np.zeros([31,31])
a,a1=90,90
while 1:
	a-=2
	a1-=1/6
	a+=360 if (a<0) else (-360 if (a>=360) else 0)
	a1+=360 if (a1<0) else (-360 if (a>=360) else 0)
	list[:]=0
	for i in range(16):
		if a<=45 or a>=315:
			list[round(15-i*tan(a*pi/180))][(i+15)]=1
		elif a<=225 and a>=135:
			list[round(15+i*tan((a-180)*pi/180))][(15-i)]=1
		elif a>45 and a<135:
			list[(15-i)][round(15-i*tan((a-90)*pi/180))]=1
		elif a>225 and a<315:
			list[(15+i)][round(15+i*tan((a-270)*pi/180))]=1
		if i<=10:
			if a1<=45 or a1>=315:
				list[round(15-i*tan(a1*pi/180))][(i+15)]=1
			elif a1<=225 and a1>=135:
				list[round(15+i*tan((a1-180)*pi/180))][(15-i)]=1
			elif a1>45 and a1<135:
				list[(15-i)][round(15-i*tan((a1-90)*pi/180))]=1
			elif a1>225 and a1<315:
				list[(15+i)][round(15+i*tan((a1-270)*pi/180))]=1
	os.system('clear')
	for j in list:
		k=''
		for i in j:
			k+=(' ' if (str(int(i))=='0') else '$')+' '
		print(k)
	na=a-90 if (a>=90) else a+270
	na1=a1-90 if (a1>=90) else a1+270
	time=((12-ceil(na1/30) if (na1<=330) else 12),60-floor(na/6))
	print(f'Time = {0 if (time[0]<10) else ""}{time[0]}:{0 if (time[1]<10) else ""}{time[1]}')