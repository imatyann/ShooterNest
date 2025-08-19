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
        settings.CELL_SIZE 
    )
    selected_piece = None
    
    # 赤駒初期化
    red_piece = piece.Piece(
        settings.RED_COLOR,
        settings.RED_START_POSITION,
        settings.PIECE_RADIUS, 
        settings.WIDTH_COLOR,
        settings.RED_SELECTED_COLOR
    )

    # 青駒初期化
    blue_piece = piece.Piece(
        settings.BLUE_COLOR,
        settings.BLUE_START_POSITION,
        settings.PIECE_RADIUS, 
        settings.WIDTH_COLOR,
        settings.BLUE_SELECTED_COLOR
    )

    # 緑駒初期化
    green_piece = piece.Piece(
        settings.GREEN_COLOR,
        settings.GREEN_START_POSITION,
        settings.PIECE_RADIUS, 
        settings.WIDTH_COLOR,
        settings.GREEN_SELECTED_COLOR
    )

    # 盤面の占有情報
    occupied = {}
    occupied[red_piece.current] = red_piece
    occupied[blue_piece.current] = blue_piece
    occupied[green_piece.current] = green_piece
    
    # 毎秒実行する関数
    running = True
    while running:
        # 操作の受け付け
        for event in pygame.event.get():
            # ウィンドウの終了
            if event.type == pygame.QUIT:
                running = False
            # 駒のクリック判定
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos_mouse = event.pos
                if red_piece.tatch(pos_mouse,main_board.origin, main_board.size):
                    selected_piece = red_piece
                elif blue_piece.tatch(pos_mouse,main_board.origin, main_board.size):
                    selected_piece = blue_piece
                elif green_piece.tatch(pos_mouse,main_board.origin, main_board.size):
                    selected_piece = green_piece
                else:
                    selected_piece = None

        # オブジェクトの描画
        screen.fill(settings.BG_COLOR)
        
        main_board.draw(screen)
        
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