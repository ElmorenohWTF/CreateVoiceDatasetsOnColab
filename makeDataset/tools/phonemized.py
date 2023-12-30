from phonemizer import phonemize
import os

with open('/content/CreateVoiceDatasetsOnColab/makeDataset/tools/output.txt', 'r') as f: # Path to output.txt
    lines = f.readlines()

# Phonemize the transcriptions
phonemized_lines = []
for line in lines:
    filename, transcription, speaker = line.strip().split('|')
    phonemes = phonemize(transcription, language='es', backend='espeak')
    phonemized_lines.append((filename, f'{filename}|{phonemes}|{speaker}\n'))

# Sort
phonemized_lines.sort(key=lambda x: int(x[0].split('_')[1].split('.')[0]))

# Split training set and validation set
train_lines = phonemized_lines[:int(len(phonemized_lines) * 0.9)]
val_lines = phonemized_lines[int(len(phonemized_lines) * 0.9):]

with open('/content/CreateVoiceDatasetsOnColab/makeDataset/tools/train_list.txt', 'w') as f: # Path for train_list.txt in the training data folder
    for _, line in train_lines:
        f.write(line)

with open('/content/CreateVoiceDatasetsOnColab/makeDataset/tools/val_list.txt', 'w') as f:  # Path for val_list.txt in the training data folder
    for _, line in val_lines:
        f.write(line)
