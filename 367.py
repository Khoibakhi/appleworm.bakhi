import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Apple Worm Clone", page_icon="🐍", layout="centered")
st.title("🍎 Apple Worm - Streamlit Edition 🐍")

# Kích thước bản đồ (Lưới)
GRID_ROWS = 10
GRID_COLS = 15

# Khởi tạo trạng thái game ban đầu
if 'worm' not in st.session_state:
    st.session_state.worm = [(7, 2), (7, 1)]  # Đầu sâu ở (7,2), thân ở (7,1)
    st.session_state.direction = "RIGHT"
    st.session_state.apple = (5, 6)
    st.session_state.portal = (3, 12)
    st.session_state.game_over = False
    st.session_state.win = False

# Các khối tường cố định làm địa hình giống trong ảnh
WALLS = [
    (8,0), (8,1), (8,2), (8,3), (8,4), (8,5), (8,6), (8,7), (8,8), (8,9), (8,10), (8,11),
    (7,11), (6,11), (5,11), (4,11), (3,11), (3,12), (3,13), (4,13), (5,13), (6,13), (7,13), (8,13), (8,14),
    (2,3), (3,3), (4,3), (4,4), (4,5), (4,6), (4,7), (3,7), (2,7)
]

def reset_game():
    st.session_state.worm = [(7, 2), (7, 1)]
    st.session_state.direction = "RIGHT"
    st.session_state.game_over = False
    st.session_state.win = False

def move_worm(dr, dc, dir_name):
    if st.session_state.game_over or st.session_state.win:
        return
        
    st.session_state.direction = dir_name
    head_r, head_c = st.session_state.worm[0]
    new_head = (head_r + dr, head_c + dc)

    # 1. Kiểm tra va chạm biên hoặc va chạm tường/chướng ngại vật
    if (new_head[0] < 0 or new_head[0] >= GRID_ROWS or 
        new_head[1] < 0 or new_head[1] >= GRID_COLS or 
        new_head in WALLS or new_head in st.session_state.worm[:-1]):
        st.session_state.game_over = True
        return

    # 2. Xử lý di chuyển đầu sâu
    st.session_state.worm.insert(0, new_head)

    # 3. Kiểm tra ăn Táo
    if new_head == st.session_state.apple:
        st.session_state.apple = (-1, -1) # Biến mất quả táo
    else:
        st.session_state.worm.pop()

    # 4. Kiểm tra về Cổng Đích
    if new_head == st.session_state.portal:
        st.session_state.win = True

# Giao diện điều khiển nút bấm
st.write("Sử dụng các nút bên dưới để điều khiển chú sâu:")
col1, col2, col3 = st.columns([1,2,1])

with col2:
    if st.button("⬆️ Lên", use_container_width=True): move_worm(-1, 0, "UP")

col_left, col_space, col_right = st.columns([1,2,1])
with col_left:
    if st.button("⬅️ Trái", use_container_width=True): move_worm(0, -1, "LEFT")
with col_right:
    if st.button("➡️ Phải", use_container_width=True): move_worm(0, 1, "RIGHT")

with col2:
    if st.button("⬇️ Xuống", use_container_width=True): move_worm(1, 0, "DOWN")

# Trạng thái kết thúc game
if st.session_state.game_over:
    st.error("💥 Bạn đã va chạm và thua cuộc!")
    if st.button("Chơi lại", key="reset_over"): reset_game()
elif st.session_state.win:
    st.success("🎉 Xuất sắc! Chú sâu đã chui vào hố an toàn!")
    if st.button("Chơi lại", key="reset_win"): reset_game()

# Vẽ màn hình Game
game_grid = ""
for r in range(GRID_ROWS):
    row_str = ""
    for c in range(GRID_COLS):
        pos = (r, c)
        if pos == st.session_state.worm[0]:
            row_str += "👀" if st.session_state.direction in ["RIGHT", "UP"] else "🦧"
        elif pos in st.session_state.worm:
            row_str += "🟩"
        elif pos == st.session_state.apple:
            row_str += "🍎"
        elif pos == st.session_state.portal:
            row_str += "🕳️"
        elif pos in WALLS:
            row_str += "🟫"
        else:
            row_str += "⬜"
    game_grid += row_str + "\n"

st.text(game_grid)
st.info("Ký hiệu: 🟩 Thân sâu | 👀 Đầu sâu | 🍎 Quả táo | 🟫 Đất/Tường | 🕳️ Cổng đích")
