import pysrt
from pydub import AudioSegment
import os
from phonemizer import phonemize

# Path to .srt file
subs = pysrt.open('/content/CreateVoiceDatasetsOnColab/makeDataset/tools/audio.srt')

# path to .wav file
audio = AudioSegment.from_wav('/content/CreateVoiceDatasetsOnColab/makeDataset/tools/audio.wav')

output_dir = '/content/CreateVoiceDatasetsOnColab/makeDataset/tools/segmentedAudio'  # path to where you want the segmented audio to go
bad_audio_dir = '/content/CreateVoiceDatasetsOnColab/makeDataset/tools/badAudio' # path to where you want the bad audio to go

os.makedirs(output_dir, exist_ok=True)
os.makedirs(bad_audio_dir, exist_ok=True)

# Check if there is a saved state
try:
   with open('last_index.txt', 'r') as f:
       last_index = int(f.read())
except FileNotFoundError:
   last_index = 0

with open('/content/CreateVoiceDatasetsOnColab/makeDataset/tools/output.txt', 'w') as out_file, open('phonemized_audio.srt', 'w') as phonemized_file: 

   for i, sub in enumerate(subs[last_index:]):

       start_time = (sub.start.minutes * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
       end_time = (sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds

       audio_segment = audio[start_time:end_time]

       duration = len(audio_segment)

       filename = f'segment_{i}.wav'
       if 1000 <= duration <= 11600: # This part throws out audio segments under 1 second and over 11.6 seconds
           audio_segment.export(os.path.join(output_dir, filename), format='wav')
           out_file.write(f'{filename}|{sub.text}|1\n')
       else:
           audio_segment.export(os.path.join(bad_audio_dir, filename), format='wav')

       phonemized_text = phonemize(sub.text, language='es')
       phonemized_file.write(f'{i}\n{str(sub.start)} --> {str(sub.end)}\n{phonemized_text}\n\n')

       # Save the current index
       with open('last_index.txt', 'w') as f:
           f.write(str(i))
