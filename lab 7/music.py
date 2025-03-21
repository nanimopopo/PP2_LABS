import pygame

pygame.init()
screen=pygame.display.set_mode((400,400))
pygame.mixer.init()

playlist=["Tides.mp3","the pharaoh's curse.mp3","Wicked Mummy.mp3"]

index=0
def load_song(index):
    pygame.mixer_music.load(playlist[index])
    pygame.mixer_music.play()

load_song(index)

running=True
paused=False
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_p:
                if (paused==False):
                    pygame.mixer_music.pause()
                    paused=True
                else:
                    pygame.mixer_music.unpause()
                    paused=False
            elif event.key==pygame.K_s:
                pygame.mixer_music.stop()
            elif event.key==pygame.K_SPACE:
                pygame.mixer_music.play()
            elif event.key==pygame.K_LEFT:
                index=index+1
                load_song(index)
            elif event.key==pygame.K_RIGHT:
                index=index-1
                load_song(index)
pygame.quit()