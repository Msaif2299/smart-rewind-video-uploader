import pytest
from smartrewind.compressor import *
import os

TEST_ASSETS_FOLDER = "./smartrewind/tests/test_assets/"

GENERIC_CHAR_OP = {'mike': [[25366, 28366], [34866, 45200], [225800, 242566], [273399, 274399]], 'whitey': [[25366, 45200], [158966, 161966], [211533, 211533], [225800, 239066]], 'betty': [[48700, 49200], [70466, 78799], [88799, 97299], [180766, 181266]], 'paul': [[68466, 119399], [261400, 268399], [275399, 299699]], 'mr': [[74466, 119399]], 'tommy': [[125899, 128399], [186766, 189766], [210533, 223300], [252566, 267899], [278899, 299699]]}
GENERIC_SEGMENT_OP = [[0, 3033], [3033, 5233], [5233, 8133], [8133, 22633], [22633, 25100], [25100, 28633], [28633, 34666], [34666, 37900], [37900, 40100], [40100, 45466], [45466, 46733], [46733, 48300], [48300, 50633], [50633, 53433], [53433, 59100], [59100, 75666], [75666, 78866], [78866, 85200], [85200, 91866], [91866, 94200], [94200, 98300], [98300, 99500], [99500, 119533], [119533, 122166], [122166, 125766], [125766, 128666], [128666, 136933], [136933, 142700], [142700, 142833], [142833, 145900], [145900, 156866], [156866, 158966], [158966, 163200], [163200, 164766], [164766, 166266], [166266, 171066], [171066, 172566], [172566, 175066], [175066, 176900], [176900, 178100], [178100, 180633], [180633, 182100], [182100, 183500], [183500, 184933], [184933, 185766], [185766, 186733], [186733, 187600], [187600, 189266], [189266, 190066], [190066, 192133], [192133, 198633], [198633, 201466], [201466, 203833], [203833, 205766], [205766, 211466], [211466, 223700], [223700, 225700], [225700, 229700], [229700, 232000], [232000, 241533], [241533, 242900], [242900, 246600], [246600, 252333], [252333, 261033], [261033, 268800], [268800, 273000], [273000, 274900], [274900, 300000]]
GENERIC_COMBINED_COMPRESS_OP = {'CHAR': GENERIC_CHAR_OP, 'SEG': GENERIC_SEGMENT_OP}

@pytest.mark.parametrize("test_ip, expected_op", [
    ("results.txt", GENERIC_CHAR_OP),
    ("results_empty.txt", {}),
    ("results_missing_charname.txt", GENERIC_CHAR_OP),
    ("results_missing_timestamp.txt", GENERIC_CHAR_OP)
])
def test_extract_character_time_slots(test_ip, expected_op):
    assert(extract_character_time_slots(TEST_ASSETS_FOLDER+test_ip) == expected_op)

def test_extract_character_time_slots_illegal_filename():
    with pytest.raises(Exception):
        extract_character_time_slots("allthebest.txt")

@pytest.mark.parametrize("test_ip, expected_op", [
    ("results-segments.txt", GENERIC_SEGMENT_OP),
    ("results_empty.txt", []),
    ("results-segments_no_segments.txt", []),
    ("results-segments_no_total_duration.txt", [])
])
def test_extract_segment_time_slots(test_ip, expected_op):
    assert(extract_segment_timeslots(TEST_ASSETS_FOLDER+test_ip) == expected_op)

def test_extract_segment_time_slots_illegal_filename():
    with pytest.raises(Exception):
        extract_segment_timeslots("allthebest.txt")

@pytest.mark.parametrize("test_char_file, test_seg_file, expected_op", [
    ("results.txt", "results-segments.txt", GENERIC_COMBINED_COMPRESS_OP),
    ("results_empty.txt", "results-segments.txt", {'CHAR': {}, 'SEG': GENERIC_SEGMENT_OP}),
    ("results.txt", "results_empty.txt", {'CHAR': GENERIC_CHAR_OP, 'SEG': []}),
    ("results_empty.txt", "results_empty.txt", {'CHAR': {}, 'SEG': []})
])
def test_extract_time_slots(test_char_file, test_seg_file, expected_op):
    temp_store_file = TEST_ASSETS_FOLDER + "unit_test_results.txt"
    extract_timeslots(TEST_ASSETS_FOLDER + test_char_file, TEST_ASSETS_FOLDER + test_seg_file, temp_store_file)
    with open(temp_store_file, "r") as ftest:
        assert(expected_op == eval(ftest.read()))
    os.remove(temp_store_file)