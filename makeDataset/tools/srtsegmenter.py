import pysrt
from pydub import AudioSegment
import os
from phonemizer import phonemize

subs = pysrt.open('/content/CreateVoiceDatasetsOnColab/makeDataset/tools/audio.srt')
audio = AudioSegment.from_wav('/content/CreateVoiceDatasetsOnColab/makeDataset/tools/audio.wav')
output_dir = '/content/CreateVoiceDatasetsOnColab/makeDataset/tools/segmentedAudio'
bad_audio_dir = '/content/CreateVoiceDatasetsOnColab/makeDataset/tools/badAudio'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(bad_audio_dir, exist_ok=True)
output_file_path = '/content/CreateVoiceDatasetsOnColab/makeDataset/tools/output.txt'

# Leer las líneas de output.txt
try:
    with open(output_file_path, 'r') as out_file:
        lines = out_file.read().splitlines()
        # Filtrar líneas vacías o no válidas al final del archivo
        valid_lines = [line for line in reversed(lines) if line.strip() and '|' in line]
        if valid_lines:
            last_line = valid_lines[0]  # Última línea válida
            last_index = int(last_line.split('_')[1].split('.')[0]) + 1  # Obtener el índice del último segmento procesado y sumar 1
        else:
            last_index = 0  # Si no hay líneas válidas, comenzar desde cero
except FileNotFoundError:
    last_index = 0

# Continuar desde el último índice válido
with open(output_file_path, 'a') as out_file, open('phonemized_audio.srt', 'w') as phonemized_file:
    for i, sub in enumerate(subs[last_index:]):
        start_time = (sub.start.minutes * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
        end_time = (sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds
        audio_segment = audio[start_time:end_time]
        duration = len(audio_segment)
        print(f"Segment {i + last_index} - Start: {start_time}ms, End: {end_time}ms, Duration: {duration}ms")
        filename = f'segment_{i + last_index}.wav'
        if 1000 <= duration <= 11600:
            audio_segment.export(os.path.join(output_dir, filename), format='wav')
            out_file.write(f'{filename}|{sub.text}|1\n')
        else:
            audio_segment.export(os.path.join(bad_audio_dir, filename), format='wav')
        phonemized_text = phonemize(sub.text, language='es')
        print(f"Phonemized text for segment {i + last_index}: {phonemized_text}")
        phonemized_file.write(f'{i + last_index}\n{str(sub.start)} --> {str(sub.end)}\n{phonemized_text}\n\n')
