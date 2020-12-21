import numpy as np
import wave
def pitch(inf, of):
	wr=wave.open("instance/static/" + inf, 'r')
	par = list(wr.getparams())
	par[3] = 0  # The number of samples will be set by writeframes.
	par = tuple(par)
	reverbed = []
	fr = 10
	sz = wr.getframerate()//fr  # Read and process 1/fr second at a time.
	# A larger number for fr means less reverb.
	c = int(wr.getnframes()/sz)  # count of the whole file
	print(c)
	shift = 500//fr  # shifting 100 Hz
	for num in range(c):
		da = np.frombuffer(wr.readframes(sz), dtype=np.int16)
		left, right = da[0::2], da[1::2]  # left and right channel
		try:
			lf, rf = np.fft.rfft(left), np.fft.rfft(right)
			lf, rf = np.roll(lf, shift), np.roll(rf, shift)
			lf[0:shift], rf[0:shift] = 0, 0
			nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
			ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
			reverbed.append(ns.tostring())
		except:
			1+1
	wr.close()
	x = wave.open("instance/static/"+of, 'wb')
	x.setnchannels(wr.getnchannels())
	x.setsampwidth(wr.getsampwidth())
	x.setframerate(wr.getframerate())
	for r in reverbed:(x.writeframes(r))


pitch("4656.wav", "6789.wav")
