import streamlit as st

# 미로맵: #은 벽, ' '은 길, E는 도착점, P는 플레이어 위치
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
    if direction == 'w':  # 상
        dx = -1
    elif direction == 's':  # 하
        dx = 1
    elif direction == 'a':  # 좌
        dy = -1
    elif direction == 'd':  # 우
        dy = 1
    else:
        return maze, False  # 방향키가 아니면 움직이지 않음

    nx, ny = x + dx, y + dy
    if maze[nx][ny] != '#':  # 벽이 아니면 이동 가능
        if maze[nx][ny] == 'E':  # 도착점 도달
            st.success("🎉 도착했다! 축하해! 🎉")
            return maze, True
        maze[x][y] = ' '       # 이전 위치는 빈칸으로
        maze[nx][ny] = 'P'     # 새 위치에 플레이어 표시
    return maze, False

if 'maze' not in st.session_state:
    st.session_state.maze = maze
    st.session_state.finished = False

st.title("간단한 미로 게임 (WASD로 이동)")

st.markdown("""
### 게임 설명  
- **P**: 플레이어 위치  
- **#**: 벽 (지나갈 수 없음)  
- **E**: 도착 지점  
- 키보드로 **W(상), A(좌), S(하), D(우)** 입력 후 엔터를 눌러 이동  
- 도착 지점에 가면 게임 클리어!  
- 입력칸에 방향키 대신 다른 글자나 아무것도 입력하지 말고 정확히 W, A, S, D 만 입력해 주세요.  
""")

if st.session_state.finished:
    st.write("게임이 끝났어요! 새로고침(F5)해서 다시 시작하세요.")
else:
    move = st.text_input("이동할 방향을 입력하세요 (W, A, S, D):").lower()
    if move:
        st.session_state.maze, st.session_state.finished = move_player(st.session_state.maze, move)

    maze_str = '\n'.join([''.join(row) for row in st.session_state.maze])
    st.text(maze_str)
