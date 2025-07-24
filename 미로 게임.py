import streamlit as st

# 미로맵: #은 벽, ' '은 길, E는 출구, P는 플레이어 위치
maze = [
    ['#', '#', '#', '#', '#', '#', '#'],
    ['#', ' ', ' ', ' ', '#', 'E', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', ' ', ' ', '#'],
    ['#', 'P', '#', '#', '#', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#'],
]

def find_player(maze):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'P':
                return i, j
    return None, None

def move_player(maze, direction):
    x, y = find_player(maze)
    dx, dy = 0, 0
    if direction == 'up':
        dx = -1
    elif direction == 'down':
        dx = 1
    elif direction == 'left':
        dy = -1
    elif direction == 'right':
        dy = 1
    else:
        return maze, False

    nx, ny = x + dx, y + dy
    if maze[nx][ny] != '#':
        if maze[nx][ny] == 'E':
            st.success("🎉 도착했다! 축하해! 🎉")
            return maze, True
        maze[x][y] = ' '
        maze[nx][ny] = 'P'
    return maze, False

if 'maze' not in st.session_state:
    st.session_state.maze = maze
    st.session_state.finished = False

st.title("미로 게임 (버튼 옆 배치)")

st.markdown("""
### 게임 설명  
- **P**: 출발 위치 (플레이어)  
- **E**: 출구 (도착점)  
- **#**: 벽 (지나갈 수 없음)  
- 빈 칸: 이동 가능한 길  
- 오른쪽 버튼으로 방향을 선택해 이동하세요!  
- 출구에 도착하면 게임 클리어!  
""")

col_maze, col_buttons = st.columns([3,1])

with col_maze:
    maze_str = '\n'.join([''.join(row) for row in st.session_state.maze])
    st.text(maze_str)

with col_buttons:
    if st.session_state.finished:
        st.write("게임이 끝났어요! 새로고침(F5)해서 다시 시작하세요.")
    else:
        if st.button("위"):
            st.session_state.maze, st.session_state.finished = move_player(st.session_state.maze, 'up')
        if st.button("아래"):
            st.session_state.maze, st.session_state.finished = move_player(st.session_state.maze, 'down')
        if st.button("왼쪽"):
            st.session_state.maze, st.session_state.finished = move_player(st.session_state.maze, 'left')
        if st.button("오른쪽"):
            st.session_state.maze, st.session_state.finished = move_player(st.session_state.maze, 'right')
