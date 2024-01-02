import pysrt
from pydub import AudioSegment
import os
from phonemizer import phonemize


subs = pysrt.open('/content/CreateVoiceDatasetsOnColab/makeDataset/tools/audio.srt') # Path to .srt file


audio = AudioSegment.from_wav('/content/CreateVoiceDatasetsOnColab/makeDataset/tools/audio.wav') # path to .wav file


output_dir = '/content/CreateVoiceDatasetsOnColab/makeDataset/tools/segmentedAudio'   # path to where you want the segmented audio to go
bad_audio_dir = '/content/CreateVoiceDatasetsOnColab/makeDataset/tools/badAudio'  # path to where you want the bad audio to go

os.makedirs(output_dir, exist_ok=True)
os.makedirs(bad_audio_dir, exist_ok=True)

output_file_path = '/content/CreateVoiceDatasetsOnColab/makeDataset/tools/output.txt'

# Comprobar si existe un estado guardado
try:
    with open(output_file_path, 'r') as out_file:
        lines = out_file.readlines()
        if lines:
            last_line = lines[-1].split('|')[0]  # Obtener la última línea procesada
            last_index = int(last_line.split('_')[1]) + 1  # Obtener el índice del último segmento procesado y sumar 1
        else:
            last_index = 0  # Si el archivo está vacío, comenzar desde cero
except FileNotFoundError:
    last_index = 0
   
                   # path to /output.txt
with open(output_file_path, 'a') as out_file, open('phonemized_audio.srt', 'w') as phonemized_file: 

    for i, sub in enumerate(subs):

        start_time = (sub.start.minutes * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
        end_time = (sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds

        audio_segment = audio[start_time:end_time]

        duration = len(audio_segment)

        print(f"Segment {i} - Start: {start_time}ms, End: {end_time}ms, Duration: {duration}ms")  # Print segment times and duration

        filename = f'segment_{i}.wav'
        if 1000 <= duration <= 11600: # This part throws out audio segments under 1 second and over 11.6 seconds
            audio_segment.export(os.path.join(output_dir, filename), format='wav')
            out_file.write(f'{filename}|{sub.text}|1\n')
        else:
            audio_segment.export(os.path.join(bad_audio_dir, filename), format='wav')


        phonemized_text = phonemize(sub.text, language='es')
        print(f"Phonemized text for segment {i}: {phonemized_text}")  # Print phonemized text

        phonemized_file.write(f'{i}\n{str(sub.start)} --> {str(sub.end)}\n{phonemized_text}\n\n')
