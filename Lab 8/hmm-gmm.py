from python_speech_features import mfcc
from hmmlearn import hmm
import os
import joblib
import numpy as np
from scipy.io import wavfile # used in compute_mfcc

import pyaudio
import wave
CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()

def compute_mfcc(file):
    fs, audio = wavfile.read(file)
    mfcc_feat = mfcc(audio)
    return mfcc_feat

class Model():
    def __init__(self, CATEGORY=None, n_comp=4, n_mix = 3, cov_type='diag', n_iter=1000):
        super(Model, self).__init__()
        self.CATEGORY = CATEGORY
        self.category = len(CATEGORY)
        self.n_comp = n_comp
        self.n_mix = n_mix
        self.cov_type = cov_type
        self.n_iter = n_iter
        # 关键步骤，初始化models，返回特定参数的模型的列表
        self.models = []
        for k in range(self.category):
            model = hmm.GMMHMM(n_components=self.n_comp, n_mix = self.n_mix,
            covariance_type=self.cov_type, n_iter=self.n_iter)
            self.models.append(model)
            
    def train(self, wavdict=None, labeldict=None):
        for k in range(self.category):
            model = self.models[k]
            for x in wavdict:
                if labeldict[x] == self.CATEGORY[k]:
                    mfcc_feat = compute_mfcc(wavdict[x])
                    model.fit(mfcc_feat)
        
    def value(self, wavdict=None, labeldict=None):
        result = []
        for k in range(self.category):
            subre = []
            label = []
            model = self.models[k]
            for x in wavdict:
                mfcc_feat = compute_mfcc(wavdict[x])
                # 生成每个数据在当前模型下的得分情况
                re = model.score(mfcc_feat)
                subre.append(re)
                label.append(labeldict[x])
            result.append(subre)
        # 选取得分最高的种类
        result = np.vstack(result).argmax(axis=0)
        # 返回种类的类别标签
        result = [self.CATEGORY[label] for label in result]
        print('Result: ',result, '\n')
        print('Label :', label,  '\n')
        
        totalnum = len(label)
        correctnum = 0
        for i in range(totalnum):
            if result[i] == label[i]:
                correctnum += 1
        print('Correct Number', correctnum/totalnum)
        
    def controller(self):
        result = 0
        big_re = -10000000
        for k in range(self.category):
            subre = []
            label = []
            model = self.models[k]
            mfcc_feat = compute_mfcc('test.wav')
            # 生成每个数据在当前模型下的得分情况
            re = model.score(mfcc_feat)
            print(re)
            if(re > big_re):
                big_re = re
                result = k
                print(result)
        print('result',self.CATEGORY[result])

    def save(self, path="models.pkl"):
        joblib.dump(self.models, path)
    
    def load(self, path="models.pkl"):
        self.models = joblib.load(path)

def gen_wavlist(wavpath, mode):
    wavdict = {}
    labeldict = {}
    for (dirpath, _, filenames) in os.walk(wavpath):
        for filename in filenames:
            if filename.endswith('.wav'):
                filepath = os.sep.join([dirpath, filename])
                fileid = filename.strip('.wav')
                if mode in fileid:
                    wavdict[fileid] = filepath
                    # 获取文件的类别
                    label = (fileid.split(mode)[1]).split('_')[1]
                    labeldict[fileid] = label
    return wavdict, labeldict

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
channel = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN, GPIO.PUD_UP)

def record_test():
    stream=p.open(format=FORMAT,channels=CHANNELS,
                  rate=RATE,input=True,frames_per_buffer=CHUNK)
    filename = 'test.wav'
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    print("Recording wav:"+filename)
    while GPIO.input(channel) == 0:
        data=stream.read(CHUNK)
        wf.writeframes(data)
    print("Finished :b")
    wf.close()
    stream.stop_stream()
    stream.close()

if __name__ == "__main__":
    mode = 'test'
    CATEGORY = ['1', '2', '3', '4']
    if mode == 'train':
        wavdict, labeldict = gen_wavlist('train_data', 'train')
        models = Model(CATEGORY=CATEGORY)
        models.train(wavdict=wavdict, labeldict=labeldict)
        models.save()
    elif mode == 'test':
        CATEGORY = ['1', '2', '3', '4']
        models = Model(CATEGORY=CATEGORY)
        try:
            models.load()
            while True:
                if GPIO.input(channel) == 0:
                    record_test()
                    models.controller()
        except KeyboardInterrupt:
            p.terminate()
            GPIO.cleanup()
            pass