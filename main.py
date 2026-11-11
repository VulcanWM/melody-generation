import pretty_midi
import json
import random

NOTES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

def create_markov_chain(n_gram=2, major_file_path="major_markov_chain.json", minor_file_path="minor_markov_chain.json"):
    markov_chain_major = {

    }

    markov_chain_minor = {

    }

    for page_number in range(1, 910):
        file_number = str(page_number).zfill(3)

        midi_data = pretty_midi.PrettyMIDI(f"POP909/{file_number}/{file_number}.mid")
        number_of_keys = 0
        with open(f"POP909/{file_number}/key_audio.txt") as f:
            number_of_keys = len(f.readlines())

        if number_of_keys == 1:
            key_file = open(f"POP909/{file_number}/key_audio.txt")
            key = key_file.read().replace("\n", "").split("	")[-1]
            key_tone = key.split(":")[0]
            tonality = key.split(":")[1]
            shift = NOTES.index(key_tone)

            for instrument in midi_data.instruments:
                if instrument.name == "MELODY":
                    number_of_notes = len(instrument.notes)
                    for i in range(0, number_of_notes-(n_gram-1)):
                        key_notes = instrument.notes[i:i+n_gram-1]
                        markov_key_arr = []
                        for note in key_notes:
                            markov_key_arr.append(str((note.pitch - shift) % 12))
                        markov_key = " ".join(markov_key_arr)
                        markov_value = str((instrument.notes[i+n_gram-1].pitch - shift) % 12)
                        if tonality == "maj":
                            if markov_key in markov_chain_major:
                                if markov_value in markov_chain_major[markov_key]:
                                    markov_chain_major[markov_key][markov_value] += 1
                                else:
                                    markov_chain_major[markov_key][markov_value] = 1
                            else:
                                markov_chain_major[markov_key] = {}
                                markov_chain_major[markov_key][markov_value] = 1
                        else:
                            if markov_key in markov_chain_minor:
                                if markov_value in markov_chain_minor[markov_key]:
                                    markov_chain_minor[markov_key][markov_value] += 1
                                else:
                                    markov_chain_minor[markov_key][markov_value] = 1
                            else:
                                markov_chain_minor[markov_key] = {}
                                markov_chain_minor[markov_key][markov_value] = 1
    json.dump(markov_chain_major, open(major_file_path, 'w'))
    json.dump(markov_chain_minor, open(minor_file_path, 'w'))

    return markov_chain_major, markov_chain_minor


print(create_markov_chain(3))