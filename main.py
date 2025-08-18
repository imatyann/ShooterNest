import pygame
import game.settings as settings
import game.board as board
import game.piece as piece

def start():
    """起動時に実行される関数"""

    # pygame初期設定
    pygame.init()
    screen = pygame.display.set_mode((settings.display_width, settings.display_height))
    pygame.display.set_caption("シューティネスト")
    clock = pygame.time.Clock()

    # 盤面初期化
    main_board = board.Board(
        settings.board_width, 
        settings.board_height,
        settings.board_color,
        settings.board_origin,
        settings.board_square_size 
    )
    
    # 赤駒初期化
    red_piece = piece.Piece(
        settings.red_color,
        settings.red_start_position,
        settings.piece_radious, 
        settings.width_color
    )

    # 毎秒実行する関数
    running = True
    while running:
        # 操作の受け付け
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        # オブジェクトの描画
        screen.fill(settings.display_color)
        main_board.draw(screen)
        red_piece.draw(screen, main_board.size,main_board.origin)

        # 画面更新
        pygame.display.flip()
        clock.tick(settings.fps)
    


    # pygameを終了
    pygame.quit()

# start関数の実行
if __name__ == "__main__":
    start()