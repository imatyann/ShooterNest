import pygame
import math

import game.settings as settings
import game.board as board
import game.piece as piece
import game.enemy as enemy

def start():
    """起動時に実行される関数"""

    # pygame初期設定
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption("シューティネスト")
    clock = pygame.time.Clock()

    # 盤面初期化
    main_board = board.Board(
        settings.BOARD_COLS, 
        settings.BOARD_ROWS,
        settings.BOARD_COLOR,
        settings.BOARD_ORIGIN,
        settings.CELL_SIZE,
        settings.HIGHLIGHT_COLOR,
        settings.ATTACKED_COLOR        
    )
    selected_piece = None
    highlight_cells = set()
    # attacked_cells = set()
    attacked_cells_time = {}
    time = 1
    

    
    # 赤駒初期化
    red_piece = piece.Piece(
        settings.RED_COLOR,
        settings.RED_START_POSITION,
        settings.PIECE_RADIUS, 
        settings.WIDTH_COLOR,
        settings.RED_SELECTED_COLOR,
        settings.RED_CAN_MOVE,
        settings.RED_CAN_ATTACK,
        settings.RED_DURATION,
        settings.RED_COOLDOWN,
        0
    )

    # 青駒初期化
    blue_piece = piece.Piece(
        settings.BLUE_COLOR,
        settings.BLUE_START_POSITION,
        settings.PIECE_RADIUS, 
        settings.WIDTH_COLOR,
        settings.BLUE_SELECTED_COLOR,
        settings.BLUE_CAN_MOVE,
        settings.BLUE_CAN_ATTACK,
        settings.BLUE_DURATION,
        settings.BLUE_COOLDOWN,
        0
    )

    # 緑駒初期化
    green_piece = piece.Piece(
        settings.GREEN_COLOR,
        settings.GREEN_START_POSITION,
        settings.PIECE_RADIUS, 
        settings.WIDTH_COLOR,
        settings.GREEN_SELECTED_COLOR,
        settings.GREEN_CAN_MOVE,
        settings.GREEN_CAN_ATTACK,
        settings.GREEN_DURATION,
        settings.GREEN_COOLDOWN,
        0
    )

    friends = [red_piece,blue_piece,green_piece]

    # 黒敵駒の初期化
    black_piece = enemy.Enemy(
        settings.BLACK_COLOR,
        settings.BLACK_START_POSITION,
        settings.PIECE_RADIUS, 
        settings.BLACK_COLOR,
        settings.BLACK_CAN_MOVE,
        settings.BLACK_INTERVAL,
        True,
        0
    )

    enemies = [black_piece]

    # 盤面の占有情報
    occupied = {}
    occupied[red_piece.current] = red_piece
    occupied[blue_piece.current] = blue_piece
    occupied[green_piece.current] = green_piece
    for e in enemies:
        occupied[e.current] = e


    
    # 毎秒実行する関数
    running = True
    while running:
        now = pygame.time.get_ticks()

        # 盤面の描画
        screen.fill(settings.BG_COLOR)

        # 操作の受け付け
        for event in pygame.event.get():
            # ウィンドウの終了
            if event.type == pygame.QUIT:
                running = False
            # 左クリックで移動
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos_mouse = event.pos
                clicked_cell = main_board.pos_to_cell(pos_mouse)
                # # ３駒に対するクリック判定
                if red_piece.is_touched(pos_mouse,main_board.origin, main_board.size):
                    highlight_cells.clear()
                    selected_piece = red_piece
                    can_go_cells = red_piece.can_go_cells(occupied,main_board)
                    highlight_cells.update(can_go_cells)
                elif blue_piece.is_touched(pos_mouse,main_board.origin, main_board.size):
                    highlight_cells.clear()
                    selected_piece = blue_piece
                    can_go_cells = blue_piece.can_go_cells(occupied,main_board)
                    highlight_cells.update(can_go_cells)
                elif green_piece.is_touched(pos_mouse,main_board.origin, main_board.size):
                    highlight_cells.clear()
                    selected_piece = green_piece
                    can_go_cells = green_piece.can_go_cells(occupied,main_board)
                    highlight_cells.update(can_go_cells)
            
                # ハイライトクリック判定
                elif clicked_cell in highlight_cells:
                    if (clicked_cell is not None) and (selected_piece is not None):
                        occupied.pop(selected_piece.current, None)
                        selected_piece.move(clicked_cell)
                        occupied[selected_piece.current] = selected_piece
                        highlight_cells.clear()
                        selected_piece = None
                # それ以外クリック判定
                else:
                    selected_piece = None
                    highlight_cells.clear()



            # 右クリックで攻撃
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pos_mouse = event.pos
                clicked_cell = main_board.pos_to_cell(pos_mouse)
                # # ３駒に対する右クリック判定
                if red_piece.is_touched(pos_mouse,main_board.origin, main_board.size):
                    if now >= red_piece.next_attack:
                       red_piece.next_attack = now + red_piece.cooldown
                       for cell in red_piece.can_attack_cells(main_board):
                            attacked_cells_time[cell] = now + red_piece.duration
                            if cell in occupied and occupied[cell] in enemies:
                                occupied[cell].hit()
                                enemies.remove(occupied.get(cell))
                                occupied.pop(cell)
                elif blue_piece.is_touched(pos_mouse,main_board.origin, main_board.size):
                    if now >= blue_piece.next_attack:
                       blue_piece.next_attack = now + blue_piece.cooldown
                       for cell in blue_piece.can_attack_cells(main_board):
                            attacked_cells_time[cell] = now + blue_piece.duration
                            if cell in occupied and occupied[cell] in enemies:
                                occupied[cell].hit()
                                enemies.remove(occupied.get(cell))
                                occupied.pop(cell)
                elif green_piece.is_touched(pos_mouse,main_board.origin, main_board.size):
                    if now >= green_piece.next_attack:
                       green_piece.next_attack = now + green_piece.cooldown
                       for cell in green_piece.can_attack_cells(main_board):
                            attacked_cells_time[cell] = now + green_piece.duration
                            if cell in occupied and occupied[cell] in enemies:
                                occupied[cell].hit()
                                enemies.remove(occupied.get(cell))
                                occupied.pop(cell)

        # 勝利判定
        if not enemies:
            pygame.draw.circle(screen,(255,0,0),(250,250),200,5)

        # 黒敵駒たちのAI
        friends_positions = {p.current for p in friends}
        for e in enemies:
            if e.alive and now >= e.next_move_ms:
                old_cell = e.current
                can_go_cells = e.can_go_cells(main_board)
                go_cells = {cell for cell in can_go_cells if cell not in occupied}
                
                attack_cells = {cell for cell in can_go_cells if cell in friends_positions}
                new_cell = e.choose_random_cell(go_cells | attack_cells)
                if new_cell is not None:
                    if new_cell in go_cells:
                        e.move(new_cell)
                        occupied.pop(old_cell, None)
                        occupied[new_cell] = e
                    elif new_cell in attack_cells:
                        print("gameover")
                        running = False
                e.next_move_ms = now + e.move_interval
            


        # スクリプトの描画
        main_board.draw(screen,highlight_cells,set(attacked_cells_time.keys()))
        
        red_piece.draw(screen, main_board.size,main_board.origin,selected_piece)
        blue_piece.draw(screen, main_board.size,main_board.origin,selected_piece)
        green_piece.draw(screen, main_board.size,main_board.origin,selected_piece)
        for e in enemies:
            black_piece.draw(screen, main_board.size,main_board.origin)

        # 画面更新
        pygame.display.flip()
        clock.tick(settings.FPS)
        time += 1

        over_time_attacked_cells = [cell for cell, expire in attacked_cells_time.items() if expire < now]

        for cell in over_time_attacked_cells:
            attacked_cells_time.pop(cell)


    # pygameを終了
    pygame.quit()

# start関数の実行
if __name__ == "__main__":
    start()
