import pygame
import math
import random

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
        settings.HIGHLIGHT_EDGE_COLOR,
        settings.ATTACKED_COLOR
    )
    selected_piece = None
    highlight_cells = set()
    attacked_cells_time = {}
    spawn_interval = settings.SPAWN_INTERVAL
    spawn_time = pygame.time.get_ticks() + spawn_interval
    max_enemies = settings.MAX_ENEMIES
    enemy_spawn_cell = settings.ENEMY_SPAWN_CELLS
    score = 0
    state = "playing"

    # スコア表示
    score_font = pygame.font.SysFont(None, settings.SCORE_FONT_SIZE_PLAY)
    
    # 赤駒初期化
    red_piece = piece.Piece(
        settings.RED_COLOR,
        settings.RED_START_POSITION,
        settings.PIECE_RADIUS, 
        settings.EDGE_COLOR,
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
        settings.EDGE_COLOR,
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
        settings.EDGE_COLOR,
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
        settings.BLACK_INTERVAL_MS,
        True,
        0
    )

    # 黒敵駒2の初期化
    black_piece2 = enemy.Enemy(settings.BLACK_COLOR,(1,1),settings.PIECE_RADIUS, settings.BLACK_COLOR,settings.BLACK_CAN_MOVE,settings.BLACK_INTERVAL_MS,True,0)
    black_piece3 = enemy.Enemy(settings.BLACK_COLOR,(3,1),settings.PIECE_RADIUS, settings.BLACK_COLOR,settings.BLACK_CAN_MOVE,settings.BLACK_INTERVAL_MS,True,0)
    black_piece4 = enemy.Enemy(settings.BLACK_COLOR,(5,1),settings.PIECE_RADIUS, settings.BLACK_COLOR,settings.BLACK_CAN_MOVE,settings.BLACK_INTERVAL_MS,True,0)
    black_piece5 = enemy.Enemy(settings.BLACK_COLOR,(7,1),settings.PIECE_RADIUS, settings.BLACK_COLOR,settings.BLACK_CAN_MOVE,settings.BLACK_INTERVAL_MS,True,0)    
    
    enemies = [black_piece,black_piece2,black_piece3,black_piece4,black_piece5]

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

            # ゲームの進行中以外は操作を拒否
            if state != "playing":
                continue

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
                                score += 1
                elif blue_piece.is_touched(pos_mouse,main_board.origin, main_board.size):
                    if now >= blue_piece.next_attack:
                       blue_piece.next_attack = now + blue_piece.cooldown
                       for cell in blue_piece.can_attack_cells(main_board):
                            attacked_cells_time[cell] = now + blue_piece.duration
                            if cell in occupied and occupied[cell] in enemies:
                                occupied[cell].hit()
                                enemies.remove(occupied.get(cell))
                                occupied.pop(cell)
                                score += 1
                elif green_piece.is_touched(pos_mouse,main_board.origin, main_board.size):
                    if now >= green_piece.next_attack:
                       green_piece.next_attack = now + green_piece.cooldown
                       for cell in green_piece.can_attack_cells(main_board):
                            attacked_cells_time[cell] = now + green_piece.duration
                            if cell in occupied and occupied[cell] in enemies:
                                occupied[cell].hit()
                                enemies.remove(occupied.get(cell))
                                occupied.pop(cell)
                                score += 1

        # 勝利判定
        if not enemies and state == "playing":
            state = "win"

        # 黒駒召喚
        if state == "playing" and len(enemies) < max_enemies and spawn_time <= now:
            spawn_candidates = [cell for cell in enemy_spawn_cell if cell not in occupied]
            if spawn_candidates:
                cell = random.choice(spawn_candidates)
                e = enemy.Enemy(
                settings.BLACK_COLOR,
                cell,
                settings.PIECE_RADIUS, 
                settings.BLACK_COLOR,
                settings.BLACK_CAN_MOVE,
                settings.BLACK_INTERVAL_MS,
                True,
                0
                )
                enemies.append(e)
                occupied[cell] = e
            spawn_time = pygame.time.get_ticks() + spawn_interval



        # 黒敵駒たちのAI
        friends_positions = {p.current for p in friends}
        for e in enemies:
            if state != "playing":
                continue
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
                        state = "gameover"
                e.next_move_ms = now + e.move_interval
            

        # スクリプトの描画
        main_board.draw(screen,highlight_cells,set(attacked_cells_time.keys()),state)
        
        red_piece.draw(screen, main_board.size,main_board.origin,selected_piece)
        blue_piece.draw(screen, main_board.size,main_board.origin,selected_piece)
        green_piece.draw(screen, main_board.size,main_board.origin,selected_piece)
        for e in enemies:
            e.draw(screen, main_board.size,main_board.origin)

        # スコア表示
        text_score = score_font.render(f"Score: {score}", True, settings.SCORE_FONT_COLOR_PLAY)
        rect_score = text_score.get_rect()
        rect_score.topright = (settings.SCREEN_WIDTH - 12, 12)
        
        bg = pygame.Surface((rect_score.width + 8, rect_score.height + 8), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 120))
        screen.blit(bg, (rect_score.left - 4, rect_score.top - 4))
        
        screen.blit(text_score,rect_score)

        # 終了処理
        if state == "playing":
            over_time_attacked_cells = [cell for cell, expire in attacked_cells_time.items() if expire < now]
        elif state == "gameover":
            over_time_attacked_cells = [cell for cell in attacked_cells_time.items()]
            selected_piece = None
            highlight_cells.clear()
        for cell in list(over_time_attacked_cells):
            attacked_cells_time.pop(cell,None)
        
        if state != "playing":
                msg = "YOU WIN!" if state == "win" else "GAME OVER"
                draw_end_overlay(screen, msg, score, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

        # 画面更新
        pygame.display.flip()
        clock.tick(settings.FPS)


    # pygameを終了
    pygame.quit()

def draw_end_overlay(screen, msg, score, w, h):
    """ゲームオーバーorクリア時のメッセージ表示"""
    # 半透明オーバーレイ
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill(settings.GAMEOVER_COLOR)
    screen.blit(overlay, (0, 0))

    # でか文字
    font_big = pygame.font.SysFont(None, settings.GAMEOVER_FONT_SIZE)
    text_msg = font_big.render(msg, True, settings.GAMEOVER_FONT_COLOR)
    rect_msg = text_msg.get_rect(center=(w // 2, h // 2 - 60))
    screen.blit(text_msg, rect_msg)

    # スコア
    font_score = pygame.font.SysFont(None, settings.SCORE_FONT_SIZE)
    text_score = font_score.render(f"Score: {score}", True, settings.SCORE_FONT_COLOR)
    rect_score = text_score.get_rect(center=(w // 2, h // 2 + 40))
    screen.blit(text_score, rect_score)



# start関数の実行
if __name__ == "__main__":
    start()

