
bb = 20
bd = 4

gate_n_per_line = 13

gate_width = 50
gate_height = 52

# 706
init_win_width = bb * 2 + gate_n_per_line * gate_width + 4 * bd
init_win_height = 275

plt_win_x = init_win_width
plt_win_y = bb
plt_win_width = 500
plt_win_height = lambda size: cir_frame_height(size) + bb + wid_frame_height

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
