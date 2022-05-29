# TETRIS AI USING GENETIC ALGORITHM
Đồ án môn học Trí tuệ nhân tạo (UEH)

# Overview
Trò chơi xếp gạch (Tetris) là trò chơi tiêu biểu cho những nghiên cứu về Trí tuệ nhân tạo và Máy học. Trong báo cáo, chúng tôi sẽ giới thiệu khái quát về trò chơi Tetris. Tiếp theo là những lý thuyết về giải thuật di truyền (GA) và ứng dụng của chúng cho bài toán Tetris. 
Từ đó có được một số kết quả thực nghiệm như sau: Số điểm đạt được sẽ đánh giá độ hiệu quả của thuật toán này, nó tương ứng với những hàng đã xóa. Và nếu thuật toán của chúng tôi đủ tốt, nó có thể tiến tới vô hạn. Trên thực tế, chúng tôi đã triển khai thuật toán này trên game Tetris có bàn cờ kích thước 20x10 với số hàng xóa được trong một lượt chơi lên đến hơn 12.000 dòng

# Giao diện chương trình
![screenshot](https://user-images.githubusercontent.com/95642319/170867166-7bedd402-b7f1-4108-bd12-6e452c6b600c.jpg)


# Cấu trúc file
* `tetro.py`: Main file
* `ai.py`: AI logic
* `tetris.py`: Dựng game Tetris
* `tetromino.py`: Tetromino logic
* `data/properties.txt`: Các thông số kỹ thuật
* `data/weights.txt`: Thông tin về điểm số AI đạt được cao nhất của mỗi thế hệ 
