
bb = 20
bd = 4

gate_n_per_line = 17

gate_width = 50
gate_height = 52

win_width = 906
win_height = 600

# 858
cir_line_width = bd * 2 + gate_n_per_line * gate_width
# 60
cir_line_height = bd * 2 + gate_height

# 866
cir_frame_width = bd * 2 + cir_line_width
# 188
cir_frame_height = lambda lines_n: bd * 2 + cir_line_height * lines_n

wid_frame_height = 150
# 866
wid_frame_width = cir_frame_width

# 20
cir_x = bb
# 190
cir_y = bb * 2 + wid_frame_height
