import math
import wave


def toreadable(s):
	s = s.hex()
	s = s[-4:]
	t = bin(int(s, 16))
	t = t[2:]
	if t[0] == '1' and len(t) ==16:
		negative = True
		s2 = ""
		for ch in t:
			if ch == '0':
				s2 += '1'
			else:
				s2 += '0'
		s2 = bin(int(s2,2) +1)
		s2 = s2[2:]
	else:
		negative = False
		s2 = t
	if len(s2) == 16:
		s2 = s2[1:]
	i = 0
	n=len(s2)-1
	for ch in s2:
		i+=int(ch)*(2**n)
		n-=1
	if negative:
		i*=-1
	return i


def distortion(x,of):
	framelist = getFile(x)
	#print("distortion")
	maxAmp = 32000
	minAmp = -32000
	for i in range(len(framelist)):
		if framelist[i] >= 0:
			framelist[i] = min(framelist[i], maxAmp)
		else:
			framelist[i] = max(framelist[i], minAmp)
	makeFile(framelist, x, of)

def tremelo(inf,of):
	framelist = getFile(inf)
	CYCLERATE = 14
	FRAMES_PER_SECOND = 44100
	CYCLE = 2*math.pi
	#Function has frequency of 10hz, deviding fps by cycle rate, find cycle legnth
	frames_per_cycle = FRAMES_PER_SECOND/CYCLERATE
	#jump is distance that should be jumped between each sin value
	jump = CYCLE/frames_per_cycle
	x = jump
	#constants to avoid overflow
	maxVal = 32767
	minVal = -32767
	for i in range(len(framelist)):
		if framelist[i] > 6000 or framelist[i]< -6000:
			factor = 1
		else:
			factor = 1 * .0005*math.sin(x)
		frame = int(framelist[i] * factor)
		if framelist[i]>0:
			framelist[i] = min(maxVal, frame)
		else:
			framelist[i] = max(minVal, frame)
		x+=jump
	makeFile(framelist, inf, of)

def vibrato(framelist):
	CYCLERATE = 14
	FRAMES_PER_SECOND = 44100
	CYCLE = 2*math.pi
	#Function has frequency of 10hz, deviding fps by cycle rate, find cycle legnth
	frames_per_cycle = FRAMES_PER_SECOND/CYCLERATE
	#jump is distance that should be jumped between each sin value
	jump = CYCLE/frames_per_cycle
	x = jump
	#constants to avoid overflow
	maxVal = 32767
	minVal = -32767

def boost(x, of):
	framelist = getFile(x)
	maxVal = 32767
	minVal = -32767
	for frame in framelist:
		if frame >= 0:
			frame = min(maxVal, frame*1.3)
		else:
			frame = max(minVal, frame*1.3)
	x = str(x)
	makeFile(framelist, x, of)

def delay(x):
	framelist = getFile(x)
	maxVal = 32767
	minVal = -32767
	delayLength = .5
	Frames_PER_SECOND = 44100
	delayFrames = int(FRAMES_PER_SECOND*delayLength)
	deminish = .5
	for i in range(len(framelist)-delayFrames):
		framelist[i+delayFrames] += int(framelist[i]*deminish)
		framelist[i] = min(maxVal, framelist[i])
		framelist[i] = max(minVal, framelist[i])
	makeFile(framelist, x)
'''
def pitch(framelist)
	wr = wave.open(file, 'r')
	par = list(wr.getparams())
	par[3] = 0  # The number of samples will be set by writeframes.
	par = tuple(par)
	reverbed = [];
	fr = 5
	sz = wr.getframerate()//fr  # Read and process 1/fr second at a time.
 	# A larger number for fr means less reverb.
	c = int(wr.getnframes()/sz)  # count of the whole file
	shift = 0//fr  # shifting 100 Hz
	for num in range(c):
		da = np.frombuffer(wr.readframes(sz), dtype=np.int16)
		left, right = da[0::2], da[1::2]  # left and right channel
		lf, rf = np.fft.rfft(left), np.fft.rfft(right)
		lf, rf = np.roll(lf, shift), np.roll(rf, shift)
		lf[0:shift], rf[0:shift] = 0, 0
		nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
		ns = np.column_stack((nl, nr)

'''


def getFile(x):
	w = wave.open('instance/static/'+ x ,'r')
	frameList = []
	#print("FIle opened")
	numFrames = w.getnframes()
	#print(numFrames)
	for i in range(0,numFrames):
		frame = w.readframes(1)
		if frame.hex() == '':
			break
		#print(frame, end="\t")
		frame = toreadable(frame)
		#print(frame)
		frameList.append(frame)

	w.close()
	return frameList


def makeFile(frameList, x, of):
	print(x)
	w = wave.open('instance/static/'+ x ,'r')
	y = wave.open("instance/static/" +of, 'wb')
	y.setnchannels(w.getnchannels())
	y.setsampwidth(w.getsampwidth())
	y.setframerate(w.getframerate())
	for f in frameList:
		s = f.to_bytes(4,byteorder='big', signed=True)
		y.writeframes(s)
	w.close()
	y.close()
	return


#distortion('8805.wav')
