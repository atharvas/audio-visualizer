import pyaudio
import numpy as np

class Microphone:
    def __init__(self, FORMAT, CHANNELS, RATE, FRAMES_PER_BUFFER, DEVICE_ID):
        self.format = FORMAT
        self.channels = CHANNELS
        self.rate = RATE
        self.chunk = FRAMES_PER_BUFFER
        self.controller = pyaudio.PyAudio()
        self.scanInputDevices()
        self.stream = self.controller.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      frames_per_buffer=self.chunk,
                                      input_device_index=DEVICE_ID,
                                      input=True)

        

    def scanInputDevices(self):
        info = self.controller.get_host_api_info_by_index(0)
        print("SCANNING DEVICES:")
        for i in range(0, info.get('deviceCount')):
                if (self.controller.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    dev_id = i
                    device_dict = self.controller.get_device_info_by_host_api_device_index(0, i)
                    name = device_dict['name']
                    n_channels = device_dict['maxInputChannels']
                    sampling_rate = device_dict['defaultSampleRate']
                    print(f"input Device found with id: {dev_id}, name: {name}, n_channels: {n_channels}, sampling_rate: {sampling_rate}") 


    def sampleInput(self):
        # print("latency:", self.stream.get_input_latency())
        raw_data = self.stream.read(num_frames=self.chunk, exception_on_overflow=False)
        return np.fromstring(raw_data, dtype=np.int16).astype(np.float32)
                        
    def destroy(self):
        print("Deactivating Microphone...")
        self.stream.stop_stream()
        self.stream.close()
        self.controller.terminate()
