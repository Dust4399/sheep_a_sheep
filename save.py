import pygame
import random
import time
import sys

# 初始化 pygame
pygame.init()
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("消除小游戏")
# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# 字体设置
font_name = pygame.font.match_font('fangsong')
chinese_font = pygame.font.Font(font_name, 36) if font_name else pygame.font.SysFont('Arial', 36)

# 排行榜文件
leaderboard_file = "leaderboard.txt"
# 全局变量
player_name = ""
difficulty = ""
game_over = False
victory = False
start_time = 0
elapsed_time = 0
pairs_left = 0
selected_images = []
# 游戏难度设置
difficulty_settings = {
    "简单": (2, 1),
    "普通": (60, 6),
    "困难": (45, 8)
}
#导入背景图片
def load_back_image(name,x,y):
    try:
        image=pygame.image.load(f"images/{name}.png")
        image=pygame.transform.scale(image,(x,y))
        return image
    except pygame.error as e:
        print(f"无法加载 : {e}")
        return None
# 加载图片集
def load_images(n):
    images = []
    for i in range(1, n+1):
        try:
            img = pygame.image.load(f"images/image{i}.png")
            img = pygame.transform.scale(img, (100, 100))
            images.append(img)
        except pygame.error as e:
            print(f"无法加载: {e}")
    return images
# 读取排行榜
def load_leaderboard():
    try:
        with open(leaderboard_file, "r", encoding='utf-8') as file:
            entries = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []
    # 解析时间并排序
    leaderboard = []
    for entry in entries:
        try:
            name, time_str = entry.split(": ")
            time_taken = float(time_str)
            leaderboard.append((name, time_taken))
        except ValueError:
            print(f"无法解析排行榜条目: {entry}")
    
    # 按时间排序 (时间越短越好，升序)
    leaderboard.sort(key=lambda x: x[1])
    return leaderboard
#创建按钮
def create_button(image_name, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    button_image = load_back_image(image_name, width, height)
    screen.blit(button_image, button_rect)
    return button_rect
#名称输入
def handle_input_box(input_box, active, player_name):
    color = BLUE if active else BLACK
    pygame.draw.rect(screen, color, input_box, 2)
    draw_text(player_name, chinese_font, BLACK, input_box.x + 10, input_box.y + 10)
    return player_name

# 保存排行榜
def save_leaderboard(name, time_taken):
    with open(leaderboard_file, "a", encoding='utf-8') as file:
        file.write(f"{name}: {time_taken}\n")

# 绘制文本
def draw_text(text, font, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

# 显示排行榜
def leaderboard_screen():
    screen.fill(WHITE)
    background_img = load_back_image("rank",WIDTH,HEIGHT)
    if background_img:
            screen.blit(background_img, (0, 0))
    leaderboard = load_leaderboard()
    for i, (name, time_taken) in enumerate(leaderboard[:5]):
        draw_text(f"第{i+1}名 {name} {time_taken}秒", chinese_font, BLACK, 250, 185 + i * 65)
    
    # 返回主界面按钮
    return_button=create_button("return",650, 50, 100, 50)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and return_button.collidepoint(event.pos):
                initial_screen()
                return
# 加载和播放背景音乐
def load_and_play_bgm(file_name):
    try:
        pygame.mixer.music.load(f"music/{file_name}.mp3")  # 加载音频文件
        pygame.mixer.music.play(-1)  # 无限循环播放背景音乐
        pygame.mixer.music.set_volume(0.5)  # 设置音量, 0.0 - 1.0 之间
    except pygame.error as e:
        print(f"无法加载背景音乐: {e}")
# 停止背景音乐
def stop_bgm():
    pygame.mixer.music.stop()
# 加载并播放音效
def play_sound_effect(effect_name):
    try:
        sound = pygame.mixer.Sound(f"music/{effect_name}.wav")
        sound.play()
    except pygame.error as e:
        print(f"无法加载音效: {e}")

# 游戏初始界面
def initial_screen():
    global player_name, difficulty

    player_name = ""
    active = False
    input_box = pygame.Rect(200, 170, 400, 50)
    background_img = load_back_image("bk3",WIDTH,HEIGHT)

    while True:
        if background_img:
            screen.blit(background_img, (0, 0))
        draw_text("鱼了个鱼", chinese_font, BLACK, 250, 50)
        draw_text("请输入昵称:", chinese_font, BLACK, 250, 120)
        
        # 绘制排行榜查看按钮
        leaderboard_button = create_button("txt", 250, 300, 200, 50)
        easy_button = create_button("button1", 300, 400, 100, 50)
        normal_button = create_button("button3", 300, 450, 100, 50)
        hard_button = create_button("button2", 300, 500, 100, 50)

        handle_input_box(input_box, active, player_name)
                
        draw_text("排行榜查看", chinese_font, BLACK, leaderboard_button.x+10 , leaderboard_button.y+5 )
        draw_text("简单", chinese_font, BLACK, easy_button.x + 10, easy_button.y + 5)
        draw_text("普通", chinese_font, BLACK, normal_button.x + 10, normal_button.y + 5)
        draw_text("困难", chinese_font, BLACK, hard_button.x + 10, hard_button.y + 5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                if leaderboard_button.collidepoint(event.pos):
                    leaderboard_screen()
                    continue
                if easy_button.collidepoint(event.pos):
                    difficulty = "简单"
                    game_screen()  # 启动游戏
                    return
                if normal_button.collidepoint(event.pos):
                    difficulty = "普通"
                    game_screen()  # 启动游戏
                    return
                if hard_button.collidepoint(event.pos):
                    difficulty = "困难"
                    game_screen()  # 启动游戏
                    return
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 20:
                    player_name += event.unicode
        pygame.display.flip()

# 游戏界面
def game_screen():
    
    global game_over, victory, start_time, elapsed_time, pairs_left, selected_images
    time_limit, total_pairs = difficulty_settings[difficulty]
    start_time = time.time()
    pairs_left = total_pairs
    game_over = False
    victory = False
    selected_images = []

    # 加载图片
    images = load_images(total_pairs)

    # 生成所有图片对
    all_images = images * 2
    random.shuffle(all_images)

    # 生成位置列表
    total_cards = total_pairs * 2
    num_cols = 4
    num_rows = (total_cards + num_cols - 1) // num_cols
    card_width = 100
    card_height = 100
    padding_x = (WIDTH - (num_cols * card_width)) // (num_cols + 1)
    padding_y = (HEIGHT - (num_rows * card_height)) // (num_rows + 1)
    positions = [(padding_x + col * (card_width + padding_x), padding_y + row * (card_height + padding_y))
                 for row in range(num_rows) for col in range(num_cols)]
    # 记录每张卡牌的状态
    cards = [{
        'image': all_images[i],
        'rect': pygame.Rect(positions[i][0], positions[i][1], card_width, card_height),
        'matched': False,
        'revealed': False
    } for i in range(total_cards)]

    background_img = load_back_image("background4",WIDTH,HEIGHT)
    if background_img:
        screen.blit(background_img, (0, 0))
    pygame.display.flip()
    while not game_over:
        if background_img:
            screen.blit(background_img, (0, 0))
        # 绘制卡牌
        for card in cards:
            if card['matched']:
                continue
            if card['revealed']:
                screen.blit(card['image'], card['rect'])
            else:
                pygame.draw.rect(screen, GRAY, card['rect'])
                pygame.draw.rect(screen, BLACK, card['rect'], 2)

        # 计算剩余时间
        elapsed_time = time.time() - start_time
        remaining_time = time_limit - elapsed_time
        if remaining_time <= 0:
            game_over = True
            victory = False

        # 绘制倒计时和剩余配对
        draw_text(f"剩余时间: {int(remaining_time)}秒", chinese_font, BLACK, 50, 20)
        draw_text(f"剩余配对: {pairs_left}对", chinese_font, BLACK, 550, 20)

        if pairs_left == 0:
            game_over = True
            victory = True

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for card in cards:
                    if card['rect'].collidepoint(mouse_pos) and not card['matched'] and not card['revealed']:
                        card['revealed'] = True
                        selected_images.append(card)
                        if len(selected_images) == 2:
                            pygame.display.flip()
                            pygame.time.delay(500)
                            if selected_images[0]['image'] == selected_images[1]['image']:
                                play_sound_effect("match")  # 播放匹配成功音效
                                selected_images[0]['matched'] = True
                                selected_images[1]['matched'] = True            
                                pairs_left -= 1
                            else:
                                play_sound_effect("fail")  # 播放匹配失败音效
                                selected_images[0]['revealed'] = False
                                selected_images[1]['revealed'] = False
                                
                            selected_images = []

        pygame.display.flip()
    game_over_screen()

# 游戏结束画面
def game_over_screen():
    global player_name, victory, elapsed_time

    screen.fill(WHITE)
    
    background_name="gameover"
    if victory:
        background_name="victory"
        if not player_name.strip():
            player_name = "匿名"  # 默认用户名为“匿名”
        save_leaderboard(player_name, int(elapsed_time))      

    background_img = load_back_image(background_name,WIDTH,HEIGHT)
    if background_img:
        screen.blit(background_img, (0, 0))            
    pygame.display.flip()
    
    waiting = True
    while waiting:
        restart_button=create_button("return",300, 450, 200, 60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    initial_screen()
                    return  # 确保退出当前的游戏结束画面循环
        pygame.display.flip()
# 游戏主函数
def main():
    load_and_play_bgm("background_music")
    initial_screen()
    game_screen()
if __name__ == "__main__":
    main()
