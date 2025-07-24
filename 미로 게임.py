import streamlit as st

# 미로맵: #은 벽, ' '은 길, E는 도착점
maze = [
    ['#', '#', '#', '#', '#', '#', '#'],
    ['#', ' ', ' ', ' ', '#', 'E', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', ' ', ' ', '#'],
    ['#', 'P', '#', '#', '#', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#'],
]

# 플레이어 위치 찾기
def find_player(maze):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'P':
                return i, j
    return None, None

# 플레이어 위치 업데이트
def move_player(maze, direction):
    x, y = find_player(maze)
    dx, dy = 0, 0
    if direction == '상':
        dx = -1
    elif direction == '하':
        dx = 1
    elif direction == '좌':
        dy = -1
    elif direction == '우':
        dy = 1

    nx, ny = x + dx, y + dy
    if maze[nx][ny] != '#':
        if maze[nx][ny] == 'E':
            st.success("도착했다! 축하해!")
            return maze, True
        maze[x][y] = ' '
        maze[nx][ny] = 'P'
    return maze, False

if 'maze' not in st.session_state:
    st.session_state.maze = maze
    st.session_state.finished = False

st.title("간단한 미로 게임")

if st.session_state.finished:
    st.write("게임이 끝났어요! 새로고침해서 다시 해보세요.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("상"):
            st.session_state.maze, st.session_state.finished = move_player(st.session_state.maze, '상')
    with col2:
        if st.button("좌"):
            st.session_state.maze, st.session_state.finished = move_player(st.session_state.maze, '좌')
        if st.button("우"):
            st.session_state.maze, st.session_state.finished = move_player(st.session_state.maze, '우')
    with col3:
        if st.button("하"):
            st.session_state.maze, st.session_state.finished = move_player(st.session_state.maze, '하')

    # 미로 출력
    maze_str = '\n'.join([''.join(row) for row in st.session_state.maze])
    st.text(maze_str)
