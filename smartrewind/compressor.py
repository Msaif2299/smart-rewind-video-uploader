THRESHOLD_IN_MS = 5000

def extract_character_time_slots(input_file):
    results = []
    with open(input_file, "r") as f:
        results = eval(f.read())
    analysis = {}
    for item in results:
        character = item['character']
        if character == 'unknown':
            continue
        if character not in analysis:
            analysis[character] = []
        analysis[character].append(item['timestamp'])
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

def extract_segment_timeslots(input_file_name):
    input_segments = []
    with open(input_file_name, "r") as f:
        input_segments = eval(f.read())
    slots =  input_segments[0]["segments"]
    slots[0][0] = 0
    slots[-1][-1] = input_segments[0]["total_duration"]
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