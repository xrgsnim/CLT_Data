import numpy as np
# 초기 설정
# wmin = min(data)
# wmax = max(data)
# intv = 8
# interval = (wmax - wmin) // intv
# grade = [0, wmin]
# level = []

# # 구간 경계 생성
# for i in range(2, intv + 1):
#     grade.append(grade[i - 1] + interval)
# grade.append(wmax)

# # 각 데이터의 구간 레벨 결정
# for i in range(n):
#     for j in range(len(grade)):
#         if data[i] < grade[j]:
#             level.append(j - 1)
#             break
#         elif data[i] == grade[j]:
#             level.append(j)
#             break
# print(f"level = {level}")
# 결과가 낮은 레벨부터 정렬되어 있어야 하므로 정렬
# level.sort()

def place_containers_diagonally(levels, row, col):
    # 2차원 배열 초기화
    # bay = [[0] * col for _ in range(row)]
    grid = np.zeros((row, col))
    sorted_levels = sorted(levels)
    
    
    # 각 대각선에 대해 처리
    index = 0  # levels 리스트에서 사용할 인덱스
    for k in range(row + col - 1):
        if k < row:
            start_row = row - 1 - k
            start_col = 0
        else:
            start_row = 0
            start_col = k - row + 1
        
        # 대각선을 따라 값 할당
        i, j = start_row, start_col
        while i < row and j < col:
            if index < len(sorted_levels):
                grid[i][j] = sorted_levels[index]
                index += 1
            i += 1
            j += 1

    return grid

# # 함수 호출 및 결과 출력
# row, col = 5, 6
# bay = place_containers_diagonally(level, row, col)

# # 결과 출력
# for line in bay:
#     print(" ".join(map(str, line)))