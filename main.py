import pygame
import sys
import random
import time
import threading
import queue
import json
import uuid
import os
from datetime import datetime

pygame.init()

# VARIABILI

WIDTH, HEIGHT = 1280, 720
SAVE_FILE = "DATA\\save.json"
HEADER_HEIGHT = 50
RESET_BUTTON_RECT = pygame.Rect(WIDTH - 200, 10, 180, 30)
POPUP_RECT = pygame.Rect(320, 180, 640, 360)
TARGET_RECT = pygame.Rect(0, 0, 40, 40)


# COLORI
DARK_GREEN = (34, 49, 34)
RED_ALERT = (200, 0, 0)
GREEN_BUTTON = (0, 120, 0)
GRAY = (70, 70, 70)
WHITE = (255, 255, 255)

# FONT

font = pygame.font.Font(None, 30)
titolo = pygame.font.Font(None, 45)

# STATO DI GIOCO

notifications = []
notification_queue = queue.Queue()

popup_open = False
active_notification = None
target_hits = 0
repair_start_time = 0

# Simon mini-gioco
simon_sequence = []
simon_input = ""
simon_show_time = 3 
simon_timer_start = 0
simon_active = False
simon_error = False

time_remaining = 120
score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("\"Notification Control Hub\" by \"Gli Inimitabili\"")

# FUNZIONI JSON

def load_game_data():
    default = {"session":{"time_remaining":120,"score":0},"completed_repairs":[]}
    if not os.path.exists(SAVE_FILE):
        return default
    with open(SAVE_FILE,"r",encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("session", default["session"])
    data.setdefault("completed_repairs", [])
    return data

def save_game_data():
    data = load_game_data()
    data["session"]["time_remaining"] = int(time_remaining)
    data["session"]["score"] = score
    with open(SAVE_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4)

def save_repair(notification, gained_score, repair_time):
    data = load_game_data()
    data["completed_repairs"].append({
        "id": notification["id"],
        "message": notification["message"],
        "created_at": notification["created_at"],
        "repaired_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "repair_time_seconds": round(repair_time,2),
        "score_gained": gained_score,
        "minigame_type": notification["minigame_type"]
    })
    with open(SAVE_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4)

def reset_game():
    global time_remaining, score, notifications, popup_open, active_notification
    global simon_active, simon_error
    time_remaining = 120
    score = 0
    notifications.clear()
    popup_open = False
    active_notification = None
    simon_active = False
    simon_error = False
    with open(SAVE_FILE,"w",encoding="utf-8") as f:
        json.dump({"session":{"time_remaining":120,"score":0},"completed_repairs":[]}, f, indent=4)

# NOTIFICHE

def add_notification(message):
    notifications.append({
        "id": str(uuid.uuid4()),
        "message": message,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "spawn_time": time.time(),
        "button_rect": pygame.Rect(0,0,100,40),
        "minigame_type": random.choice(["click_target","simon"])
    })

def draw_notifications():
    y = HEADER_HEIGHT + 20
    for n in notifications:
        rect = pygame.Rect(10, y, WIDTH-20, 60)
        pygame.draw.rect(screen, RED_ALERT, rect)

        # Prima riga: id + messaggio + data
        txt1 = font.render(f"[{n['id'][:8]}] {n['message']} | {n['created_at']}", True, WHITE)
        screen.blit(txt1, (rect.x+10, rect.y+5))

        # Seconda riga: tipo di minigioco
        txt2 = font.render(f"Minigioco: {n['minigame_type']}", True, WHITE)
        screen.blit(txt2, (rect.x+10, rect.y+30))

        # Pulsante "Ripara"
        btn = pygame.Rect(rect.right-110, rect.y+10, 100, 40)
        n["button_rect"] = btn
        pygame.draw.rect(screen, GREEN_BUTTON, btn, border_radius=3)
        btn_txt = font.render("Ripara", True, WHITE)
        screen.blit(btn_txt, btn_txt.get_rect(center=btn.center))

        y += 70


# MINIGIOCO : CLICK TARGET

def move_target():
    TARGET_RECT.x = random.randint(POPUP_RECT.x+20, POPUP_RECT.right-60)
    TARGET_RECT.y = random.randint(POPUP_RECT.y+80, POPUP_RECT.bottom-60)

# THREAD NOTIFICHE

def generate_notifications():
    messages = [
        "Guasto al radar!",
        "Attacco nemico in corso!",
        "Malfunzionamento motori!",
        "Sistema comunicazioni danneggiato!",
        "Perdita di segnale satellitare!",
        "Allarme incendio motore!",
        "Sensori di movimento non funzionanti!",
        "Guasto sistema armi!",
        "Interferenze radar rilevate!",
        "Sonda esplorativa offline!",
        "Sistema di navigazione compromesso!",
        "Allarme pressione carburante!"
    ]
    while True:
        time.sleep(random.uniform(2,5))
        notification_queue.put(random.choice(messages))

# MAIN LOOP

def main():
    global time_remaining, score, target_hits, popup_open, active_notification
    global simon_input, simon_sequence, simon_timer_start, simon_active, simon_error, repair_start_time

    saved = load_game_data()
    time_remaining = saved["session"]["time_remaining"]
    score = saved["session"]["score"]

    clock = pygame.time.Clock()
    threading.Thread(target=generate_notifications, daemon=True).start()
    last_time = time.time()
    last_save = time.time()
    running = True

    while running:
        screen.fill(DARK_GREEN)
        now = time.time()
        time_remaining -= (now-last_time)
        last_time = now
        if time_remaining < 0:
            time_remaining = 0

        # HEADER
        pygame.draw.rect(screen,(66,66,66),(0,0,WIDTH,HEADER_HEIGHT))
        screen.blit(titolo.render("Notification Control Hub", True, WHITE), (10,10))
        screen.blit(font.render(f"Tempo: {int(time_remaining)//60:02d}:{int(time_remaining)%60:02d}", True, WHITE), (500,15))
        screen.blit(font.render(f"Punteggio: {score}", True, WHITE), (WIDTH-450,15))

        # RESET BUTTON
        mouse_pos = pygame.mouse.get_pos()
        color_reset = (180,30,30)
        if RESET_BUTTON_RECT.collidepoint(mouse_pos):
            color_reset = (220,50,50)
        pygame.draw.rect(screen,color_reset,RESET_BUTTON_RECT,border_radius=6)
        reset_surf = font.render("RESET", True, WHITE)
        screen.blit(reset_surf, reset_surf.get_rect(center=RESET_BUTTON_RECT.center))

        # NOTIFICHE
        draw_notifications()

        # POPUP
        if popup_open and active_notification:
            pygame.draw.rect(screen,GRAY,POPUP_RECT)
            pygame.draw.rect(screen,WHITE,POPUP_RECT,2)

            if active_notification["minigame_type"]=="click_target":
                screen.blit(font.render("Colpisci il bersaglio 3 volte", True, WHITE), (POPUP_RECT.x+60, POPUP_RECT.y+20))
                pygame.draw.rect(screen, RED_ALERT, TARGET_RECT)
                screen.blit(font.render(f"Colpi: {target_hits}/3", True, WHITE), (POPUP_RECT.x+20, POPUP_RECT.y+60))
            else:
                # MINIGIOCO : SIMON
                if not simon_active:
                    screen.blit(font.render("Memorizza la sequenza:", True, WHITE), (POPUP_RECT.x+60, POPUP_RECT.y+20))
                    screen.blit(font.render(" ".join(simon_sequence), True, WHITE), (POPUP_RECT.x+60, POPUP_RECT.y+60))
                    if time.time()-simon_timer_start >= simon_show_time:
                        simon_active = True
                else:
                    screen.blit(font.render("Digita la sequenza:", True, WHITE), (POPUP_RECT.x+60, POPUP_RECT.y+20))
                    screen.blit(font.render(simon_input, True, WHITE), (POPUP_RECT.x+60, POPUP_RECT.y+60))
                    if simon_error:
                        screen.blit(font.render("Errore! Ricomincia.", True, RED_ALERT), (POPUP_RECT.x+60, POPUP_RECT.y+100))

        # EVENTI
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                save_game_data()
                running=False

            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                # RESET
                if RESET_BUTTON_RECT.collidepoint(event.pos):
                    reset_game()
                    continue

                # APRI MINIGIOCO
                if not popup_open:
                    for n in notifications:
                        if n["button_rect"].collidepoint(event.pos):
                            popup_open=True
                            active_notification=n
                            repair_start_time=time.time()
                            target_hits=0
                            if n["minigame_type"]=="click_target":
                                move_target()
                            else:
                                # Simon: lunghezza sequenza base 4 + 1 ogni 500 punti
                                length = 4 + score // 500
                                simon_sequence = [str(random.randint(0,9)) for _ in range(length)]
                                simon_input = ""
                                simon_timer_start = time.time()
                                simon_active = False
                                simon_error = False
                            break
                else:
                    # click-target
                    if active_notification and active_notification["minigame_type"]=="click_target":
                        if TARGET_RECT.collidepoint(event.pos):
                            target_hits+=1
                            move_target()
                            if target_hits>=3:
                                repair_time = time.time()-repair_start_time
                                gained_score=max(50,min(200,int(200-repair_time*10)))
                                score+=gained_score
                                time_remaining+=random.randint(2,10)
                                save_repair(active_notification,gained_score,repair_time)
                                save_game_data()
                                notifications.remove(active_notification)
                                popup_open=False
                                active_notification=None

            elif event.type==pygame.KEYDOWN:
                if popup_open and active_notification and active_notification["minigame_type"]=="simon" and simon_active:
                    if event.unicode.isdigit():
                        simon_input += event.unicode
                        if not "".join(simon_sequence).startswith(simon_input):
                            simon_input = ""
                            simon_error = True
                            simon_timer_start = time.time()
                        else:
                            simon_error = False
                    elif event.key==pygame.K_BACKSPACE:
                        simon_input = simon_input[:-1]

                    if simon_input == "".join(simon_sequence):
                        repair_time = time.time()-repair_start_time
                        gained_score=max(50,min(200,int(200-repair_time*10)))
                        score+=gained_score
                        time_remaining+=random.randint(2,10)
                        save_repair(active_notification,gained_score,repair_time)
                        save_game_data()
                        notifications.remove(active_notification)
                        popup_open=False
                        active_notification=None
                        simon_active=False
                        simon_error=False

        # Notifiche dalla coda
        while not notification_queue.empty():
            add_notification(notification_queue.get())

        # Rimuovi vecchie notifiche, MA NON quella attiva
        notifications[:] = [n for n in notifications if (time.time()-n["spawn_time"]<20) or (n == active_notification)]

        # Salvataggio automatico ogni 1 secondo
        if time.time() - last_save >= 1:
            save_game_data()
            last_save = time.time()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# AVVIO

main()
