import pygame
import game.settings as settings 

def start():
    """起動時に実行される関数"""

    # pygame初期設定
    pygame.init()
    screen = pygame.display.set_mode((settings.display_width, settings.display_height))
    pygame.display.set_caption("シューティネスト")
    clock = pygame.time.Clock()

    # 毎秒実行する関数
    running = True
    while running:
        # 操作の受け付け
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        # 画面更新
        pygame.display.flip()
        clock.tick(settings.fps)
    
    # pygameを終了
    pygame.quit()




# start関数の実行
if __name__ == "__main__":
    start()