import pygame as pg;
import sounddevice as sd
import soundfile as sf
import numpy as np
import threading

class StreamedAudio:
    def __init__(self, filename):
        self.file = sf.SoundFile(filename)
        self.samplerate = self.file.samplerate
        self.channels = self.file.channels
        self.lock = threading.Lock()
        self.frames_total = len(self.file)

    def seek(self, frame):
        with self.lock:
            self.file.seek(int(frame))

    def tell(self):
        with self.lock:
            return self.file.tell()

    def read_block(self, blocksize):
        with self.lock:
            data = self.file.read(blocksize, dtype='float32', always_2d=True)
            if len(data) < blocksize:
                self.file.seek(0)
                remaining = blocksize - len(data)
                data = np.vstack([data, self.file.read(remaining, dtype='float32', always_2d=True)])
            return data

class musicPlayer:
    def __init__(self,audio1,audio2=None):
        self.BLOCKSIZE = 1024
        self.VOLUME_A = 1.0
        self.VOLUME_B = 1.0

        self.paused = False
        
        self.stream_a = StreamedAudio(audio1);
        if audio2 != None:
            self.stream_b = StreamedAudio(audio2);
        else:
            self.stream_b = StreamedAudio(audio1);

        assert self.stream_a.samplerate == self.stream_b.samplerate
        assert self.stream_a.channels == self.stream_b.channels
        
        self.stream = sd.OutputStream(
            samplerate=self.stream_a.samplerate,
            channels=self.stream_a.channels,
            blocksize=self.BLOCKSIZE,
            callback=self.audio_callback
        )
        self.stream.start()

    def audio_callback(self,outdata, frames, time, status):
        if self.paused:
            outdata[:] = np.zeros((frames, self.stream_a.channels), dtype='float32')
        else:
            block_a = self.stream_a.read_block(frames)
            block_b = self.stream_b.read_block(frames)
            mixed = self.VOLUME_A * block_a + self.VOLUME_B * block_b
            outdata[:] = mixed;