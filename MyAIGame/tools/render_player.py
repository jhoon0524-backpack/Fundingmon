#!/usr/bin/env python3
"""임시 플레이어 필드 스프라이트 렌더링 (ART_SPEC.md 규격, 32x32, 4방향 x 2프레임).

    python tools/render_player.py            # assets/sprites/player/ 에 8장 생성
    python tools/render_player.py --sheet out.png   # 검수용 확대 시트도 저장

CLAUDE.md 3-1 의 6단계 순서를 따른다:
  1 투명 배경 → 2 그림자 → 3 기본 덩어리 → 4 명암 → 5 하이라이트(좌상단 광원) → 6 외곽선(검정 금지)
SpriteCook 이 연결되기 전까지 쓰는 자리표시자다. 팔레트 밖 색은 쓰지 않는다.
"""
import sys
from pathlib import Path
from PIL import Image

OUT_DIR = Path("assets/sprites/player")
SIZE = 32

# (밝음, 기본, 그림자, 외곽선) — ART_SPEC.md 2번 팔레트만 사용
RAMPS = {
    "skin":  ("#FFFFFF", "#F5F0E8", "#DCD3C6", "#8A7D6E"),
    "hair":  ("#8A7D6E", "#5C5247", "#332E28", "#332E28"),
    "shirt": ("#A7F4C8", "#6BD9A0", "#4CA678", "#337555"),
    "pants": ("#6BAEF4", "#4C7FC4", "#33578E", "#33578E"),
    "shoe":  ("#8A7D6E", "#5C5247", "#332E28", "#332E28"),
}
EYE = "#332E28"
GROUND_SHADOW = "#DCD3C6"


def hex_rgba(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


class Canvas:
    """램프 이름을 픽셀 단위로 기록해 두고 마지막에 명암·외곽선을 한 번에 계산한다."""

    def __init__(self):
        self.ramp = [[None] * SIZE for _ in range(SIZE)]
        self.overlay = {}  # (x, y) -> hex, 명암 계산 후 그대로 덮는 픽셀 (눈 등)

    def rect(self, ramp, x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if 0 <= x < SIZE and 0 <= y < SIZE:
                    self.ramp[y][x] = ramp

    def px(self, ramp, x, y):
        self.rect(ramp, x, y, x, y)

    def clear(self, x0, y0, x1, y1):
        self.rect(None, x0, y0, x1, y1)

    def render(self, ground_shadow_y):
        img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        p = img.load()

        def r(x, y):
            if 0 <= x < SIZE and 0 <= y < SIZE:
                return self.ramp[y][x]
            return None

        # 2. 그림자 레이어 (발밑 1px, 외곽선보다 먼저 깔린다)
        for x in range(11, 21):
            p[x, ground_shadow_y] = hex_rgba(GROUND_SHADOW)

        # 3~5. 기본 덩어리 + 명암 + 하이라이트. 광원은 좌측 상단 고정.
        for y in range(SIZE):
            for x in range(SIZE):
                name = r(x, y)
                if name is None:
                    continue
                light, base, shadow, _ = RAMPS[name]
                top_edge = r(x, y - 1) != name
                left_edge = r(x - 1, y) != name
                bottom_edge = r(x, y + 1) != name
                right_edge = r(x + 1, y) != name
                if bottom_edge or right_edge:
                    color = shadow
                elif top_edge or left_edge:
                    color = light
                else:
                    color = base
                p[x, y] = hex_rgba(color)

        # 6. 외곽선 — 이웃 덩어리의 외곽선 색. 검정을 쓰지 않는다.
        for y in range(SIZE):
            for x in range(SIZE):
                if r(x, y) is not None:
                    continue
                for nx, ny in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
                    n = r(nx, ny)
                    if n is not None:
                        p[x, y] = hex_rgba(RAMPS[n][3])
                        break

        for (x, y), color in self.overlay.items():
            p[x, y] = hex_rgba(color)
        return img


def draw(direction, frame):
    """발밑(y=29)이 캔버스 아래쪽 타일 격자에 맞도록 그린다. 프레임 1 은 반대 다리가 앞."""
    c = Canvas()
    bob = 1 if frame == 1 else 0  # 걸을 때 몸통이 1px 들썩인다

    # 머리 (12x10, 모서리 깎음)
    hx0, hy0, hx1, hy1 = 10, 5 + bob, 21, 14 + bob
    c.rect("skin", hx0, hy0, hx1, hy1)
    for (x, y) in ((hx0, hy0), (hx1, hy0), (hx0, hy1), (hx1, hy1)):
        c.clear(x, y, x, y)

    # 머리카락
    if direction == "up":
        c.rect("hair", hx0, hy0 + 1, hx1, hy1 - 1)          # 뒤통수 전체
        c.rect("hair", hx0 + 1, hy0, hx1 - 1, hy0)
    else:
        c.rect("hair", hx0 + 1, hy0, hx1 - 1, hy0)          # 윗머리
        c.rect("hair", hx0, hy0 + 1, hx1, hy0 + 3)          # 앞머리
        c.rect("hair", hx0, hy0 + 4, hx0, hy0 + 6)          # 옆머리 좌
        c.rect("hair", hx1, hy0 + 4, hx1, hy0 + 6)          # 옆머리 우
        if direction == "left":
            c.rect("hair", hx1 - 4, hy0 + 1, hx1, hy1 - 1)  # 뒤통수가 오른쪽에 보임
        elif direction == "right":
            c.rect("hair", hx0, hy0 + 1, hx0 + 4, hy1 - 1)

    # 몸통 (셔츠) 10x7
    bx0, by0, bx1, by1 = 11, 15 + bob, 20, 21 + bob
    c.rect("shirt", bx0, by0, bx1, by1)

    # 팔 — 걸을 때 앞뒤로 흔들린다
    swing = 1 if frame == 0 else -1
    if direction in ("down", "up"):
        c.rect("shirt", 9, by0 + 1 + swing, 10, by1 - 1 + swing)
        c.rect("shirt", 21, by0 + 1 - swing, 22, by1 - 1 - swing)
        c.rect("skin", 9, by1 + swing, 10, by1 + swing)
        c.rect("skin", 21, by1 - swing, 22, by1 - swing)
    else:
        ax = 14 if direction == "left" else 15
        c.rect("shirt", ax, by0 + 1 + swing, ax + 2, by1 - 1 + swing)
        c.rect("skin", ax, by1 + swing, ax + 2, by1 + swing)

    # 다리 + 신발. 프레임마다 앞다리가 바뀐다 (앞다리가 1px 길다)
    ly0 = by1 + 1
    left_fwd = frame == 0
    for leg, x0, x1 in (("L", 12, 15), ("R", 16, 19)):
        fwd = (leg == "L") == left_fwd
        end = 27 if fwd else 26
        c.rect("pants", x0, ly0, x1, end)
        c.rect("shoe", x0, end + 1, x1, end + 2 if fwd else end + 1)
    # 옆모습은 다리가 겹쳐 보이도록 안쪽으로 모은다
    if direction in ("left", "right"):
        c.clear(12, ly0, 19, 29)
        for leg, x0, x1 in (("L", 13, 15), ("R", 16, 18)):
            fwd = (leg == "L") == left_fwd
            end = 27 if fwd else 26
            c.rect("pants", x0, ly0, x1, end)
            c.rect("shoe", x0, end + 1, x1, end + 2 if fwd else end + 1)

    # 눈 (명암 뒤에 덮는다)
    ey = hy0 + 6
    if direction == "down":
        c.overlay[(13, ey)] = EYE
        c.overlay[(18, ey)] = EYE
    elif direction == "left":
        c.overlay[(12, ey)] = EYE
    elif direction == "right":
        c.overlay[(19, ey)] = EYE

    return c.render(ground_shadow_y=30)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    frames = []
    for d in ("down", "up", "left", "right"):
        for f in (0, 1):
            img = draw(d, f)
            path = OUT_DIR / f"player_{d}_{f}.png"
            img.save(path)
            frames.append(img)
            print("저장:", path)
    if "--sheet" in sys.argv:
        out = sys.argv[sys.argv.index("--sheet") + 1]
        scale = 8
        sheet = Image.new("RGBA", (SIZE * 8 * scale, SIZE * scale), hex_rgba("#B5A99A"))
        for i, img in enumerate(frames):
            sheet.paste(img.resize((SIZE * scale, SIZE * scale), Image.NEAREST), (i * SIZE * scale, 0), img.resize((SIZE * scale, SIZE * scale), Image.NEAREST))
        sheet.save(out)
        print("시트:", out)


if __name__ == "__main__":
    main()
