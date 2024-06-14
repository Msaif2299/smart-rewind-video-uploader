from typing import Dict, List
THRESHOLD_IN_MS = 5000

def extract_character_time_slots(input_file: str) -> Dict:
    results = []
    with open(input_file, "r") as f:
        data = f.read()
        if data == "" or data is None:
            print(f"No data found in input file {input_file}, aborting character timeslot extraction...")
            return {}
        results = eval(data)
    analysis = {}
    for item in results:
        try:
            character = item['character']
        except KeyError:
            continue
        if character == 'unknown':
            continue
        if character not in analysis:
            analysis[character] = []
        try:
            analysis[character].append(item['timestamp'])
        except KeyError:
            continue
    for character in analysis:
        analysis[character] = sorted(analysis[character])
    slots = {}
    for character in analysis:
        timestamps = analysis[character]
        character_slots = []
        current_slot = [timestamps[0]]
        for idx, time in enumerate(timestamps[:-1]):
            if len(current_slot) == 2:
                character_slots.append(current_slot)
                current_slot = [time]
            if timestamps[idx+1]-time >= THRESHOLD_IN_MS:
                current_slot.append(time)
        if len(current_slot) == 1:
            current_slot.append(timestamps[-1])
            character_slots.append(current_slot)
        slots[character] = character_slots

    return slots

def extract_segment_timeslots(input_file: str) -> List[List[int]]:
    input_segments = []
    with open(input_file, "r") as f:
        data = f.read()
        if data == "" or data is None:
            print(f"No data found in input file {input_file}, aborting character segment extraction...")
            return []
        input_segments = eval(data)
    slots =  input_segments[0]["segments"]
    if len(slots) == 0:
        return []
    slots[0][0] = 0
    try:
        slots[-1][-1] = input_segments[0]["total_duration"]
    except KeyError:
        print(f"No total duration found in {input_file}, aborting segment extraction...")
        return []
    for idx, _ in enumerate(slots[:-1]):
        slots[idx][1] = slots[idx+1][0]
    return slots

def extract_timeslots(char_tracking_file, segment_file, output_file_path):
    char_slots = extract_character_time_slots(char_tracking_file)
    segment_slots = extract_segment_timeslots(segment_file)
    with open(output_file_path, "w") as f:
        metadata = {
            "CHAR": char_slots,
            "SEG": segment_slots
        }
        print(metadata, file=f)