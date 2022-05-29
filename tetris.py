import math
import pygame
from random import randint
import tetromino

# an instance of the Tetris game: trường hợp game Tetris
class Tetris:
    def __init__(self, grid_width, grid_height, cell_width):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_width = cell_width
        # whether or not the game has been lost yet: game thua hay chưa
        self.lost = False
        self.lines_cleared = 0
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)

        # the Tetris grid begins at the top-left corner: lưới Tetris bắt đầu góc trên- trái 
        # and can be indexed by grid[x][y]: được chỉ số bằng lưới [x][y]
        self.grid = []
        for x in range(self.grid_width):
            col = [0] * self.grid_height
            self.grid.append(col)

        # generate random sequence of tetrominos tạo ra chuỗi ngẫu nhiên của tetrominos
        # the sequence will contain all types of tetrominos (excluding rotation): chuỗi chứa tất cả dạng của tetrominous
        # when all the tetrominos in the sequence have been used, another
        # sequence will be generated. this this is to ensure that the distribution is fair
        # khi tất cả tetrominos trong chuỗi được sử dụng, một chuỗi khác được tạo ra  nhằm đảm bảo sự công bằng trong tro chơi
        self.tmino_seq = self.generate_tetromino_seq()
        self.current_tmino = self.tmino_seq[-1]
        self.tmino_seq.pop()
        self.next_tmino = self.tmino_seq[-1]
        self.tmino_seq.pop()

        # keep track of the next move, used by the AI: sử dụng AI trong lần di chuyển tiếp theo
        self.next_move = None

    # move current tetromino down one block: di chuyển tetromino hiện tại xuống dưới
    # sau đó lần lượt lấy từng phần tử ra làm khối tetromino tiếp theo.  
    def update(self):
        if self.lost:
            return

        if self.next_move != None:
            self.current_tmino = self.next_move

        self.current_tmino.y_pos += 1
        # if tetromino is now colliding, then move it back and place it down
        if is_colliding(self.grid, self.current_tmino):
            self.current_tmino.y_pos -= 1
            self.place_tetromino()

    def render(self, surface, next_move_outline):
        # draw grid: vẽ lưới 
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                # draw the cell if it is non empty
                if self.grid[x][y] != 0:
                    pygame.draw.rect(
                        surface,
                        tetromino.get_tetromino_color(self.grid[x][y]),
                        (x * self.cell_width, y * self.cell_width, self.cell_width - 1, self.cell_width - 1))
        # draw a divider line: vẽ đường phân chia
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (self.grid_width * self.cell_width, 0, 1, self.grid_height * self.cell_width))

        # draw current tetromino
        if not self.lost:
            block_data = self.current_tmino.block_data
            pos_x = self.current_tmino.x_pos
            pos_y = self.current_tmino.y_pos
            for x in range(len(block_data)):
                for y in range(len(block_data[0])):
                    if self.current_tmino.block_data[x][y]:
                        pygame.draw.rect(
                            surface,
                            self.current_tmino.color,
                            ((x + pos_x) * self.cell_width, (y + pos_y) * self.cell_width,
                            self.cell_width - 1, self.cell_width - 1))
            # if specified, draw the next move outline
            if next_move_outline:
                if self.next_move != None:
                    pos_x = self.next_move.x_pos
                    pos_y = self.next_move.y_pos
                    for x in range(len(block_data)):
                        for y in range(len(block_data[0])):
                            if self.next_move.block_data[x][y]:
                                pygame.draw.rect(
                                    surface,
                                    self.next_move.color,
                                    ((x + pos_x) * self.cell_width, (y + pos_y) * self.cell_width,
                                    self.cell_width - 1, self.cell_width - 1), 2)

        # draw next piece text
        text_next, rect_next = self.render_text('Next piece:',
            (self.grid_width + 1) * self.cell_width, self.cell_width * 1.5)
        surface.blit(text_next, rect_next)

        # render next tetromino under next piece next: 
        # hoàn trả tetromino tiếp theo dưới 
        block_data = self.next_tmino.block_data
        pos_x = self.grid_width + 1
        pos_y = 3.5
        for x in range(len(block_data)):
            for y in range(len(block_data[0])):
                if block_data[x][y]:
                    pygame.draw.rect(
                        surface,
                        self.next_tmino.color,
                        ((x + pos_x) * self.cell_width, (y + pos_y) * self.cell_width,
                        self.cell_width - 1, self.cell_width - 1))

        # draw lines cleared text: vẽ dòng chữ: dòng đã xoá
        text_cleared, rect_cleared = self.render_text('Lines cleared:',
            (self.grid_width + 1) * self.cell_width, (tetromino.get_largest_tetromino_size() + 3) * self.cell_width)
        surface.blit(text_cleared, rect_cleared)

        # draw lines cleared number
        # vẽ những dòng số đã xoá 
        text_lines, rect_lines = self.render_text(str(self.lines_cleared),
            (self.grid_width + 1) * self.cell_width, (tetromino.get_largest_tetromino_size() + 4) * self.cell_width)
        surface.blit(text_lines, rect_lines)


    # places the current tetromino down and generates a new one
    # đặt tetromino xuống và tạo cái mới 
    def place_tetromino(self):
        # transfer the tetromino data to the grid data
        #chuyển dữ liệu tetromino sang dữ liệu lưới
        for x in range(self.current_tmino.size):
            for y in range(self.current_tmino.size):
                if self.current_tmino.block_data[x][y]:
                    # skip if the cell is out of bounds
                    #bỏ qua nếu ô nằm ngoài giới hạn
                    grid_x = x + self.current_tmino.x_pos
                    grid_y = y + self.current_tmino.y_pos
                    if grid_x < 0 or grid_x >= self.grid_width or grid_y < 0 or grid_y >= self.grid_height:
                        continue
                    self.grid[grid_x][grid_y] = self.current_tmino.id
        # check for cleared lines
        # kiểm tra những dòng đã xoá
        # start from lowest possible line and go up
        # bắt đầu từ dòng có khả năng thấp nhất và đi lên
        current_y = self.current_tmino.y_pos + self.current_tmino.size - 1
        for i in range(self.current_tmino.size):
            # check if this line is out of bounds
            #kiểm tra xem dòng này có nằm ngoài giới hạn không

            if current_y >= self.grid_height:
                current_y -= 1
                continue
            # check for line clear: kiểm tra dòng đã xoá 
            line_cleared = True
            for x in range(self.grid_width):
                if self.grid[x][current_y] == 0:
                    line_cleared = False
                    break
            # move everything above line down one block if cleared: di chuyển dòng từ trên xuống phía dưới dòng đã xoá 
            if line_cleared:
                self.lines_cleared += 1
                for y in range(current_y, 0, -1):
                    for x in range(self.grid_width):
                        self.grid[x][y] = self.grid[x][y - 1]
                # clear upper most line
                for x in range(self.grid_width):
                    self.grid[x][0] = 0
            else:
                # otherwise go to next line
                current_y -= 1

        # generate a new tetromino: tạo ra tetro mơi s
        self.current_tmino = self.next_tmino
        if len(self.tmino_seq) == 0:
            self.tmino_seq = self.generate_tetromino_seq()
        self.next_tmino = self.tmino_seq[-1]
        self.tmino_seq.pop()

        # determine if it is colliding with anything: xác định có đang va chạm không
        if is_colliding(self.grid, self.current_tmino):
            self.current_tmino = None
            self.lost = True

    def move_left(self):
        self.current_tmino.x_pos -= 1
        if is_colliding(self.grid, self.current_tmino):
            self.current_tmino.x_pos += 1

    def move_right(self):
        self.current_tmino.x_pos += 1
        if is_colliding(self.grid, self.current_tmino):
            self.current_tmino.x_pos -= 1

    def move_down(self):
        self.current_tmino.y_pos += 1
        if is_colliding(self.grid, self.current_tmino):
            self.current_tmino.y_pos -= 1
            self.place_tetromino()

    def drop_down(self):
        self.current_tmino.y_pos += 1
        while not is_colliding(self.grid, self.current_tmino):
            self.current_tmino.y_pos += 1
        self.current_tmino.y_pos -= 1
        self.place_tetromino()

    def rotate(self):
        self.current_tmino.rotate()
        if is_colliding(self.grid, self.current_tmino):
            self.current_tmino.rotate(clockwise=False)

    def generate_tetromino_seq(self):
        seq = []
        id_list = [i for i in range(1, tetromino.unique_types + 1)]
        # randomly pull ids from the list and put it into the sequence: random tetro rơi xuống trong mảng
        while len(id_list) != 0:
            rand_idx = randint(0, len(id_list) - 1)
            id = id_list[rand_idx]
            id_list.pop(rand_idx)
            tmino = tetromino.Tetromino(id)
            tmino.x_pos = (tmino.max_x - tmino.min_x) // 2
            tmino.y_pos = tmino.min_y
            seq.append(tmino)
        return seq

    def render_text(self, text, top, left):
        text_render = self.font.render(text, True, (255, 255, 255))
        text_rect = text_render.get_rect()
        text_rect.topleft = (top, left)
        return (text_render, text_rect)

# determines if a given boolean grid and a tetromino are colliding
#xác định xem một lưới boolean đã cho và một tetromino có chạm vào nhau hay không
def is_colliding(grid, tetromino):
    # iterate through each cell in the tetromino itself
    #lặp qua từng ô trong chính tetromino
    for x in range(tetromino.size):
        for y in range(tetromino.size):
            if tetromino.block_data[x][y]:
                grid_x = x + tetromino.x_pos
                # convert local tetromino coordinates to grid coordinates
                # chuyển đổi tetromino cục bộ thành tọa độ lưới
                grid_y = y + tetromino.y_pos
                # check if out of bounds
                if (grid_x < 0 or grid_y < 0
                    or grid_x >= len(grid)
                    or grid_y >= len(grid[0])
                    or grid[grid_x][grid_y] != 0):
                    return True
    return False
