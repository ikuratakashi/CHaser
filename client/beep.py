import sys
#sys.path.append('./lib')
sys.path.append('lib')
import numpy as np # type: ignore
import sounddevice as sd # type: ignore
import time

# beep
class clsBeep:
    """
    beep音のクラス
    """    
    # サンプリングレート
    sample_rate = 44100

    # 音の周波数（Hz）と持続時間（秒）のペア
    SE_PIPO = "SE_PIPO"
    SE_KEYINPUT = "SE_KEYINPUT"
    SE_OK = "SE_OK"
    SE_NG = "SE_NG"
    notes = {   
                SE_PIPO:
                [
                    (2000, 0.15),  # 高音（2000 Hz）0.1秒（「ぴ」）
                    (1000, 0.25)   # 高音（1000 Hz）0.1秒（「っ」）
                ],
                SE_OK:
                [
                    (1500, 0.01)    # 低音（500 Hz）0.1秒（「」）
                ],
                SE_NG:
                [
                    (500, 0.01)    # 低音（500 Hz）0.1秒（「」）
                ]
    }
    
    def generate_tone(self,frequency, duration, sample_rate):
        """
        各音の信号を生成
        """
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        signal = 0.5 * np.sin(2 * np.pi * frequency * t)
        return signal

    def generate_sequence(self,notes, sample_rate):
        """
        シーケンスを生成
        """
        sequence = np.concatenate([self.generate_tone(frequency, duration, sample_rate) for frequency, duration in notes])
        return sequence
    
    def CreateSound(self,pKey):
        """
        音を作る
        """
        # 音を生成
        return self.generate_sequence(self.notes[pKey], self.sample_rate)

    def SoundStart(self,pSound,pIsWait:bool = False):
        """
        再生
        """
        # 音を再生
        sd.play(pSound, self.sample_rate)
        # 再生が終わるのを待つ
        if pIsWait:
            sd.wait()
            time.sleep(0.3)       

input("エンターを押すと音が鳴ります")
beep = clsBeep()
se = beep.CreateSound(clsBeep.SE_PIPO)
beep.SoundStart(se,True)
