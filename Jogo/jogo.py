"""
Corrida de Fórmula 1 - Versão Estável (Com Sistema de Pausa)
------------------------------------------------------------
- Botão de Pausa no topo da tela de jogo
- Atalho no teclado: Tecla 'P' ou 'ESC' para pausar/retomar
- Overlay de pausa para congelar a tela com clareza visual

OTIMIZAÇÃO DE PERFORMANCE (mobile):
- game_tick() rodava a ~30x por segundo e chamava page.update() a cada frame.
  page.update() percorre e serializa a ÁRVORE INTEIRA da página (cabeçalho, HUD,
  pista, botões) a cada chamada. Em celular isso satura a ponte Flutter/JS e
  causa o travamento. Trocado por atualizações "cirúrgicas" (track_elements.update()
  e hud_card.update()), que enviam só o que realmente mudou (pista + HUD),
  sem tocar no resto da árvore. Mesmo ajuste em move_player().
  Nenhuma regra de jogo, visual, velocidade ou comportamento foi alterada.
"""

import asyncio
import json
import math
import os
import random
import flet as ft

# ----------------------- Configurações da Pista -----------------------

TRACK_WIDTH = 340
TRACK_HEIGHT = 460
KERB_WIDTH = 12
PLAYABLE_WIDTH = TRACK_WIDTH - (KERB_WIDTH * 2)

LANE_COUNT = 3
LANE_WIDTH = PLAYABLE_WIDTH // LANE_COUNT

CAR_WIDTH = 38
CAR_HEIGHT = 68
PLAYER_Y = TRACK_HEIGHT - CAR_HEIGHT - 15

FRAME_MS = 35  # ~30 FPS

F1_TEAMS = [
    {"name": "Ferrari", "body": "#e8002d", "helmet": "#fcd700"},
    {"name": "Red Bull Racing", "body": "#3671c6", "helmet": "#ff1e1e"},
    {"name": "Mercedes", "body": "#cccccc", "helmet": "#00a19c"},
    {"name": "McLaren", "body": "#ff8000", "helmet": "#1e41ff"},
    {"name": "Aston Martin", "body": "#229971", "helmet": "#cfff00"},
    {"name": "Alpine", "body": "#0093cc", "helmet": "#ff87b4"},
]

LEADERBOARD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.json")
MEDALS = ["🥇", "🥈", "🥉"]


def make_border(width: int, color: str):
    try:
        return ft.border.all(width, color)
    except AttributeError:
        return ft.Border.all(width, color)


# ----------------------- Persistência do Pódio -----------------------

def load_leaderboard() -> list:
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_score(name: str, team_name: str, score: float) -> list:
    data = load_leaderboard()
    data.append({"name": name or "Piloto", "team": team_name, "score": int(score)})
    data.sort(key=lambda item: item["score"], reverse=True)
    data = data[:20]
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data


def get_top(n: int = 3) -> list:
    return load_leaderboard()[:n]


# ----------------------- Componentes Visuais -----------------------

def lane_x(lane: int, track_offset_x: float = 0) -> float:
    base_x = KERB_WIDTH + (lane * LANE_WIDTH) + (LANE_WIDTH - CAR_WIDTH) / 2
    return base_x + track_offset_x


def create_f1_car(
    body_color: str,
    helmet_color: str = "#ffff00",
    is_player: bool = False,
    left: float = 0,
    top: float = 0,
) -> ft.Container:
    accent_wing = "#ffff00" if is_player else body_color

    return ft.Container(
        left=left,
        top=top,
        width=CAR_WIDTH,
        height=CAR_HEIGHT,
        animate_position=ft.Animation(120, ft.AnimationCurve.EASE_OUT) if is_player else None,
        content=ft.Stack(
            controls=[
                ft.Container(left=2, top=2, width=34, height=5, bgcolor=accent_wing, border_radius=2),
                ft.Container(left=15, top=0, width=8, height=20, bgcolor=body_color, border_radius=3),
                ft.Container(left=0, top=8, width=5, height=13, bgcolor="#121214", border_radius=2),
                ft.Container(left=33, top=8, width=5, height=13, bgcolor="#121214", border_radius=2),
                ft.Container(left=5, top=18, width=28, height=28, bgcolor=body_color, border_radius=5),
                ft.Container(left=13, top=22, width=12, height=14, bgcolor="#08080a", border_radius=4),
                ft.Container(left=16, top=26, width=6, height=6, bgcolor="#ffff00" if is_player else helmet_color, border_radius=3),
                ft.Container(left=0, top=42, width=6, height=15, bgcolor="#121214", border_radius=2),
                ft.Container(left=32, top=42, width=6, height=15, bgcolor="#121214", border_radius=2),
                ft.Container(left=2, top=58, width=34, height=6, bgcolor="#0d0d10", border_radius=2),
                ft.Container(left=13, top=62, width=12, height=4, bgcolor="#00ffcc" if is_player else "#ff0044", border_radius=2),
            ]
        ),
    )


def create_car_preview(body_color: str, helmet_color: str) -> ft.Container:
    return ft.Container(
        width=44,
        height=44,
        alignment=ft.Alignment(0, 0),
        content=ft.Stack(
            controls=[
                ft.Container(left=6, top=8, width=32, height=28, bgcolor=body_color, border_radius=8),
                ft.Container(left=14, top=14, width=16, height=16, bgcolor="#08080a", border_radius=8),
                ft.Container(left=17.5, top=17.5, width=9, height=9, bgcolor=helmet_color, border_radius=5),
            ]
        ),
    )


class Rival:
    def __init__(self, lane: int, y: float, team: dict, initial_offset: float = 0):
        self.lane = lane
        self.y = y
        self.control = create_f1_car(
            body_color=team["body"],
            helmet_color=team["helmet"],
            is_player=False,
            left=lane_x(lane, initial_offset),
            top=y,
        )


# ----------------------- Aplicação Principal -----------------------

async def main(page: ft.Page):
    page.title = "F1 Ultra Smooth 🏎️"
    page.window.width = 400
    page.window.height = 760
    page.bgcolor = "#0b0c10"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 6

    state = {
        "player_lane": 1,
        "player_x_offset": 0.0,
        "rivals": [],
        "speed": 6.0,
        "score": 0,
        "running": False,
        "paused": False,
        "spawn_timer": 0,
        "track_offset": 0,
        "ticks": 0,
        "curve": 0.0,
        "player_name": "",
        "team": None,
        "team_index": None,
    }

    player_car = None

    left_kerb_items = [ft.Container(width=KERB_WIDTH, height=52, bgcolor="#e63946" if i % 2 == 0 else "#ffffff") for i in range(10)]
    right_kerb_items = [ft.Container(width=KERB_WIDTH, height=52, bgcolor="#e63946" if i % 2 == 0 else "#ffffff") for i in range(10)]

    kerb_left_container = ft.Container(left=0, top=-52, content=ft.Column(controls=left_kerb_items, spacing=0))
    kerb_right_container = ft.Container(left=TRACK_WIDTH - KERB_WIDTH, top=-52, content=ft.Column(controls=right_kerb_items, spacing=0))

    lane_dashes = []
    for lane_edge in range(1, LANE_COUNT):
        x = KERB_WIDTH + (lane_edge * LANE_WIDTH)
        dashes = ft.Column(spacing=28, controls=[ft.Container(width=3, height=35, bgcolor="#ffffff22", border_radius=2) for _ in range(8)])
        lane_dashes.append(ft.Container(left=x - 1, top=-52, content=dashes))

    score_text = ft.Text("0", size=18, weight=ft.FontWeight.BOLD, color="#00f2fe")
    speed_text = ft.Text("180", size=18, weight=ft.FontWeight.BOLD, color="#ff007f")
    curve_text = ft.Text("RETA", size=13, weight=ft.FontWeight.BOLD, color="#00ffcc")

    hud_card = ft.Container(
        width=TRACK_WIDTH,
        padding=8,
        bgcolor="#12141c",
        border_radius=10,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.Column([ft.Text("PONTOS", size=9, color="#8888a0", weight=ft.FontWeight.BOLD), score_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1),
                ft.Column([ft.Text("TRAÇADO", size=9, color="#8888a0", weight=ft.FontWeight.BOLD), curve_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1),
                ft.Column([ft.Text("VELOCIDADE", size=9, color="#8888a0", weight=ft.FontWeight.BOLD), ft.Row([speed_text, ft.Text("KM/H", size=9, color="#ff007f")])], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1),
            ],
        ),
    )

    # ----------------------- Overlays (Game Over e Pausa) -----------------------

    game_over_column = ft.Column(alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)
    overlay = ft.Container(width=TRACK_WIDTH, height=TRACK_HEIGHT, bgcolor="#0b0c10f0", alignment=ft.Alignment(0, 0), visible=False, content=game_over_column)

    def toggle_pause(e=None):
        if not state["running"]:
            return
        state["paused"] = not state["paused"]
        pause_overlay.visible = state["paused"]
        page.update()

    pause_column = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        controls=[
            ft.Text("⏸️ JOGO PAUSADO", size=22, weight=ft.FontWeight.BOLD, color="white"),
            ft.Text("Tome um ar e volte para a pista!", size=12, color="#8888a0"),
            ft.Container(height=6),
            ft.Container(
                content=ft.Text("▶️ CONTINUAR", size=13, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
                alignment=ft.Alignment(0, 0),
                bgcolor="#00a19c",
                border_radius=10,
                width=180,
                height=44,
                ink=True,
                on_click=toggle_pause,
            )
        ]
    )

    pause_overlay = ft.Container(
        width=TRACK_WIDTH,
        height=TRACK_HEIGHT,
        bgcolor="#0b0c10d0",
        alignment=ft.Alignment(0, 0),
        visible=False,
        content=pause_column
    )

    track_asphalt = ft.Container(width=TRACK_WIDTH, height=TRACK_HEIGHT, bgcolor="#181920", border_radius=14)

    track_elements = ft.Stack(
        controls=[track_asphalt, kerb_left_container, kerb_right_container, *lane_dashes, pause_overlay, overlay],
        width=TRACK_WIDTH,
        height=TRACK_HEIGHT,
    )

    # Controles de Direção
    btn_left = ft.Container(
        content=ft.Text("◄ ESQUERDA", size=13, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
        alignment=ft.Alignment(0, 0),
        bgcolor="#1e41ff",
        border_radius=10,
        height=50,
        expand=True,
        ink=True,
        on_click=lambda _: move_player(-1),
    )

    btn_right = ft.Container(
        content=ft.Text("DIREITA ►", size=13, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
        alignment=ft.Alignment(0, 0),
        bgcolor="#1e41ff",
        border_radius=10,
        height=50,
        expand=True,
        ink=True,
        on_click=lambda _: move_player(1),
    )

    # Botão de Pausa Superior
    btn_pause_header = ft.Container(
        content=ft.Text("⏸️ PAUSA", size=11, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
        alignment=ft.Alignment(0, 0),
        bgcolor="#2b2d42",
        border_radius=8,
        width=80,
        height=32,
        ink=True,
        on_click=toggle_pause,
    )

    header_row = ft.Container(
        width=TRACK_WIDTH,
        content=ft.Row(
            [
                ft.Row([ft.Text("FORMULA 1", size=18, weight=ft.FontWeight.BOLD, color="white"), ft.Text("GRAND PRIX", size=18, color="#ff1e1e", weight=ft.FontWeight.BOLD)]),
                btn_pause_header,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    )

    game_view = ft.Column(
        [
            header_row,
            hud_card,
            ft.Container(content=track_elements, width=TRACK_WIDTH, height=TRACK_HEIGHT),
            ft.Container(width=TRACK_WIDTH, content=ft.Row([btn_left, btn_right], spacing=10)),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
    )

    # ----------------------- Tela de Seleção -----------------------

    name_field = ft.TextField(label="Nome do piloto", width=TRACK_WIDTH, max_length=16, bgcolor="#12141c", color="white", border_color="#2a2c3a")

    start_button = ft.Container(
        content=ft.Text("🏁 COMEÇAR CORRIDA", size=14, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
        alignment=ft.Alignment(0, 0),
        width=TRACK_WIDTH,
        height=50,
        bgcolor="#555555",
        border_radius=10,
        ink=False,
    )

    team_cards = []

    def build_team_card(index: int, team: dict) -> ft.Container:
        return ft.Container(
            width=100,
            height=112,
            border=make_border(2, "transparent"),
            border_radius=12,
            bgcolor="#12141c",
            padding=6,
            content=ft.Column(
                [
                    create_car_preview(team["body"], team["helmet"]),
                    ft.Text(team["name"], size=10, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            on_click=lambda e, i=index: select_team(i),
        )

    for i, team in enumerate(F1_TEAMS):
        team_cards.append(build_team_card(i, team))

    teams_grid = ft.Row(controls=team_cards, wrap=True, spacing=10, run_spacing=10, alignment=ft.MainAxisAlignment.CENTER)
    login_status_text = ft.Text("Escolha uma equipe para continuar", size=11, color="#8888a0")

    podium_dialog_content = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, height=280)

    def close_podium_dialog(e=None):
        if hasattr(page, "close"):
            page.close(podium_dialog)
        else:
            podium_dialog.open = False
            page.update()

    podium_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("🏆 Pódio Geral"),
        content=podium_dialog_content,
        actions=[ft.TextButton(content=ft.Text("Fechar"), on_click=close_podium_dialog)],
    )

    def refresh_podium_dialog():
        podium_dialog_content.controls.clear()
        data = load_leaderboard()
        if not data:
            podium_dialog_content.controls.append(ft.Text("Ainda não há corridas registradas.", color="#8888a0"))
        else:
            for idx, entry in enumerate(data):
                prefix = MEDALS[idx] if idx < 3 else f"{idx + 1}º"
                podium_dialog_content.controls.append(
                    ft.Text(f"{prefix}  {entry['name']} — {entry['score']} pts  ({entry['team']})", size=13, color="white")
                )

    def open_podium_dialog(e=None):
        refresh_podium_dialog()
        if hasattr(page, "open"):
            page.open(podium_dialog)
        else:
            page.dialog = podium_dialog
            podium_dialog.open = True
            page.update()

    view_podium_button = ft.TextButton(content=ft.Text("🏆 Ver pódio geral"), on_click=open_podium_dialog)

    login_view = ft.Column(
        [
            ft.Text("FORMULA 1", size=22, weight=ft.FontWeight.BOLD, color="white"),
            ft.Text("GRAND PRIX", size=22, color="#ff1e1e", weight=ft.FontWeight.BOLD),
            ft.Container(height=6),
            name_field,
            ft.Container(height=4),
            ft.Text("ESCOLHA SUA EQUIPE", size=12, weight=ft.FontWeight.BOLD, color="#00f2fe"),
            teams_grid,
            login_status_text,
            ft.Container(height=4),
            start_button,
            view_podium_button,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
        width=TRACK_WIDTH,
    )

    def update_start_button():
        ready = bool(name_field.value and name_field.value.strip()) and state["team_index"] is not None
        if ready:
            start_button.bgcolor = "#ff1e1e"
            start_button.ink = True
            start_button.on_click = start_race
            login_status_text.value = "Tudo pronto! Bom treino, piloto."
            login_status_text.color = "#00ffcc"
        else:
            start_button.bgcolor = "#555555"
            start_button.ink = False
            start_button.on_click = None
            if state["team_index"] is None:
                login_status_text.value = "Escolha uma equipe para continuar"
                login_status_text.color = "#8888a0"
            else:
                login_status_text.value = "Digite seu nome para continuar"
                login_status_text.color = "#8888a0"
        page.update()

    def select_team(index: int):
        state["team_index"] = index
        for i, card in enumerate(team_cards):
            if i == index:
                card.border = make_border(3, F1_TEAMS[i]["body"])
                card.bgcolor = "#1c1e2b"
            else:
                card.border = make_border(2, "transparent")
                card.bgcolor = "#12141c"
        update_start_button()

    name_field.on_change = lambda e: update_start_button()

    # ----------------------- Transição e Lógica -----------------------

    def show_login(e=None):
        state["running"] = False
        state["paused"] = False
        for rival in state["rivals"]:
            if rival.control in track_elements.controls:
                track_elements.controls.remove(rival.control)
        state["rivals"] = []

        nonlocal player_car
        if player_car is not None and player_car in track_elements.controls:
            track_elements.controls.remove(player_car)
        player_car = None

        overlay.visible = False
        pause_overlay.visible = False
        page.controls.clear()
        page.add(login_view)
        page.update()

    def start_race(e=None):
        state["player_name"] = (name_field.value or "Piloto").strip()
        state["team"] = F1_TEAMS[state["team_index"]]

        reset_game(first_start=True)

        page.controls.clear()
        page.add(game_view)
        page.update()

    def reset_game(first_start: bool = False):
        nonlocal player_car

        state["player_lane"] = 1
        state["player_x_offset"] = 0.0
        state["speed"] = 6.0
        state["score"] = 0
        state["running"] = True
        state["paused"] = False
        state["spawn_timer"] = 0
        state["ticks"] = 0
        state["curve"] = 0.0

        for rival in state["rivals"]:
            if rival.control in track_elements.controls:
                track_elements.controls.remove(rival.control)
        state["rivals"] = []

        if player_car is not None and player_car in track_elements.controls:
            track_elements.controls.remove(player_car)

        team = state["team"] or F1_TEAMS[0]
        player_car = create_f1_car(
            body_color=team["body"],
            helmet_color=team["helmet"],
            is_player=True,
            left=lane_x(state["player_lane"]),
            top=PLAYER_Y,
        )

        pause_index = track_elements.controls.index(pause_overlay)
        track_elements.controls.insert(pause_index, player_car)

        overlay.visible = False
        pause_overlay.visible = False
        score_text.value = "0"
        speed_text.value = "180"
        curve_text.value = "RETA"
        if not first_start:
            page.update()

    def spawn_rival():
        lane = random.randint(0, LANE_COUNT - 1)
        pool = [t for t in F1_TEAMS if t["body"] != state["team"]["body"]] or F1_TEAMS
        team = random.choice(pool)
        rival = Rival(lane, -CAR_HEIGHT, team)
        state["rivals"].append(rival)

        if player_car in track_elements.controls:
            player_index = track_elements.controls.index(player_car)
            track_elements.controls.insert(player_index, rival.control)
        else:
            track_elements.controls.append(rival.control)

    def check_collision(rival: Rival) -> bool:
        if rival.lane != state["player_lane"]:
            return False
        return (rival.y + CAR_HEIGHT > PLAYER_Y) and (rival.y < PLAYER_Y + CAR_HEIGHT)

    def build_game_over_overlay():
        game_over_column.controls.clear()
        game_over_column.controls.append(ft.Text("💥 DNF - BATEU!", size=22, weight=ft.FontWeight.BOLD, color="#ff4d4d"))
        game_over_column.controls.append(ft.Text(f"{state['player_name']} • {int(state['score'])} pontos", size=13, color="#bbbbcc", text_align=ft.TextAlign.CENTER))
        game_over_column.controls.append(ft.Container(height=4))
        game_over_column.controls.append(ft.Text("🏆 PÓDIO", size=13, weight=ft.FontWeight.BOLD, color="#00f2fe"))

        top3 = get_top(3)
        if not top3:
            game_over_column.controls.append(ft.Text("Seja o primeiro no pódio!", size=11, color="#8888a0"))
        else:
            for idx, entry in enumerate(top3):
                game_over_column.controls.append(ft.Text(f"{MEDALS[idx]} {entry['name']} — {entry['score']} pts", size=12, color="white"))

        game_over_column.controls.append(ft.Container(height=6))

        btn_reset = ft.Container(
            content=ft.Text("🔄 JOGAR NOVAMENTE", size=12, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
            alignment=ft.Alignment(0, 0),
            bgcolor="#00a19c",
            border_radius=10,
            width=210,
            height=44,
            ink=True,
            on_click=lambda e: reset_game(),
        )

        btn_change_driver = ft.Container(
            content=ft.Text("🔁 TROCAR PILOTO / EQUIPE", size=12, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
            alignment=ft.Alignment(0, 0),
            bgcolor="#2b2d42",
            border_radius=10,
            width=210,
            height=44,
            ink=True,
            on_click=lambda e: show_login(),
        )

        game_over_column.controls.append(btn_reset)
        game_over_column.controls.append(btn_change_driver)

    def end_game():
        state["running"] = False
        state["paused"] = False
        save_score(state["player_name"], state["team"]["name"], state["score"])
        build_game_over_overlay()
        overlay.visible = True
        page.update()

    def game_tick():
        if not state["running"] or state["paused"] or player_car is None:
            return

        state["ticks"] += 1
        state["speed"] = min(18.0, state["speed"] + 0.003)
        state["score"] += state["speed"] * 0.1

        curve_factor = math.sin(state["ticks"] * 0.025)
        state["curve"] = curve_factor * 28.0

        if curve_factor < -0.3:
            curve_text.value = "◄ CURVA ESQ"
            curve_text.color = "#ff8700"
        elif curve_factor > 0.3:
            curve_text.value = "CURVA DIR ►"
            curve_text.color = "#ff8700"
        else:
            curve_text.value = "RETA"
            curve_text.color = "#00ffcc"

        track_curve_x = state["curve"]
        kerb_left_container.left = track_curve_x
        kerb_right_container.left = (TRACK_WIDTH - KERB_WIDTH) + track_curve_x

        for idx, dash in enumerate(lane_dashes):
            base_x = KERB_WIDTH + ((idx + 1) * LANE_WIDTH)
            dash.left = base_x - 1 + track_curve_x

        state["track_offset"] = (state["track_offset"] + state["speed"]) % 104
        kerb_left_container.top = -104 + state["track_offset"]
        kerb_right_container.top = -104 + state["track_offset"]

        for dash in lane_dashes:
            dash.top = -63 + state["track_offset"]

        state["player_x_offset"] = track_curve_x
        player_car.left = lane_x(state["player_lane"], state["player_x_offset"])

        state["spawn_timer"] += 1
        spawn_interval = max(16, int(38 - state["speed"] * 1.2))
        if state["spawn_timer"] >= spawn_interval:
            state["spawn_timer"] = 0
            spawn_rival()

        to_remove = []
        for rival in state["rivals"]:
            rival.y += state["speed"]
            rival.control.top = rival.y
            rival.control.left = lane_x(rival.lane, track_curve_x)

            if rival.y > TRACK_HEIGHT:
                to_remove.append(rival)
            elif check_collision(rival):
                end_game()
                return

        for rival in to_remove:
            state["rivals"].remove(rival)
            if rival.control in track_elements.controls:
                track_elements.controls.remove(rival.control)

        score_text.value = f"{int(state['score'])}"
        speed_text.value = f"{int(state['speed'] * 30)}"

        # OTIMIZAÇÃO: em vez de page.update() (redesenha a página inteira a
        # cada frame), atualizamos só a pista e o HUD, que são os únicos
        # trechos que mudam a cada tick. Isso reduz drasticamente os dados
        # enviados ao celular a cada frame e elimina o travamento.
        track_elements.update()
        hud_card.update()

    def move_player(direction: int):
        if not state["running"] or state["paused"] or player_car is None:
            return
        new_lane = state["player_lane"] + direction
        if 0 <= new_lane < LANE_COUNT:
            state["player_lane"] = new_lane
            player_car.left = lane_x(new_lane, state["player_x_offset"])
            # OTIMIZAÇÃO: atualiza só o carro do jogador, não a página inteira.
            player_car.update()

    def on_keyboard(e: ft.KeyboardEvent):
        if not state["team"]:
            return
        if e.key in ("p", "P", "Escape"):
            toggle_pause()
        elif state["running"] and not state["paused"]:
            if e.key in ("Arrow Left", "A", "a"):
                move_player(-1)
            elif e.key in ("Arrow Right", "D", "d"):
                move_player(1)
        elif e.key == " " and not state["running"]:
            reset_game()

    page.on_keyboard_event = on_keyboard

    # Loop da aplicação
    async def loop():
        while True:
            game_tick()
            await asyncio.sleep(FRAME_MS / 1000)

    asyncio.create_task(loop())
    show_login()


if __name__ == "__main__":
    ft.app(target=main)