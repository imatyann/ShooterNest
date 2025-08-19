import pygame
import math

import game.settings as settings
import game.board as board
import game.piece as piece

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
        settings.HIGHLIGHT_COLOR        
    )
    selected_piece = None
    highlight_cells = set()

    
    # 赤駒初期化
    red_piece = piece.Piece(
        settings.RED_COLOR,
        settings.RED_START_POSITION,
        settings.PIECE_RADIUS, 
        settings.WIDTH_COLOR,
        settings.RED_SELECTED_COLOR,
        settings.RED_CAN_MOVE
    )

    # 青駒初期化
    blue_piece = piece.Piece(
        settings.BLUE_COLOR,
        settings.BLUE_START_POSITION,
        settings.PIECE_RADIUS, 
        settings.WIDTH_COLOR,
        settings.BLUE_SELECTED_COLOR,
        settings.BLUE_CAN_MOVE
    )

    # 緑駒初期化
    green_piece = piece.Piece(
        settings.GREEN_COLOR,
        settings.GREEN_START_POSITION,
        settings.PIECE_RADIUS, 
        settings.WIDTH_COLOR,
        settings.GREEN_SELECTED_COLOR,
        settings.GREEN_CAN_MOVE
    )

    # 盤面の占有情報
    occupied = {}
    occupied[red_piece.current] = red_piece
    occupied[blue_piece.current] = blue_piece
    occupied[green_piece.current] = green_piece


    
    # 毎秒実行する関数
    running = True
    while running:
        # 盤面の描画
        screen.fill(settings.BG_COLOR)

        # 操作の受け付け
        for event in pygame.event.get():
            # ウィンドウの終了
            if event.type == pygame.QUIT:
                running = False
            # クリック判定
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
                # それ以外クリック判定
                else:
                    selected_piece = None
                    highlight_cells.clear()
            



        # スクリプトの描画
        main_board.draw(screen,highlight_cells)
        
        red_piece.draw(screen, main_board.size,main_board.origin,selected_piece)

        blue_piece.draw(screen, main_board.size,main_board.origin,selected_piece)

        green_piece.draw(screen, main_board.size,main_board.origin,selected_piece)

        # 画面更新
        pygame.display.flip()
        clock.tick(settings.FPS)
    


    # pygameを終了
    pygame.quit()

# start関数の実行
if __name__ == "__main__":
    start()
