"""Temporary pygame view of a Map, for debugging only."""
import math
import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame  # noqa: E402

from config import Connection, Hub, Map, ZoneType  # noqa: E402


WIDTH = 1100
HEIGHT = 750
MARGIN = 90
RADIUS = 26
BACKGROUND = (24, 26, 33)
GRID = (38, 41, 52)
EDGE = (120, 125, 140)
TEXT = (230, 232, 240)
MUTED = (140, 145, 160)
DEFAULT_HUB = (110, 115, 130)


class DebugView:
    """Draw a Map in a pygame window.

    Controls: SPACE / ENTER to continue, ESC or close the window to quit.
    Hover a hub to see its details.
    """

    def __init__(self, game_map: Map) -> None:
        """Open the window and compute the hub screen positions.

        Args:
            game_map: the parsed map.
        """
        pygame.init()
        self.map = game_map
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fly-in debug view")
        self.font = pygame.font.SysFont("dejavusans", 14)
        self.small = pygame.font.SysFont("dejavusans", 12)
        self.big = pygame.font.SysFont("dejavusans", 18, bold=True)
        self.by_name: dict[str, Hub] = {h.name: h for h in game_map.hubs}
        self.pos: dict[str, tuple[int, int]] = self.layout()

    def layout(self) -> dict[str, tuple[int, int]]:
        """Map hub coordinates to pixels, keeping the aspect ratio.

        Returns:
            Screen position of each hub, by name.
        """
        xs = [h.pos_x for h in self.map.hubs]
        ys = [h.pos_y for h in self.map.hubs]
        span_x = max(max(xs) - min(xs), 1)
        span_y = max(max(ys) - min(ys), 1)
        scale = min((WIDTH - 2 * MARGIN) / span_x,
                    (HEIGHT - 2 * MARGIN - 60) / span_y)
        off_x = (WIDTH - span_x * scale) / 2
        off_y = (HEIGHT - 60 - span_y * scale) / 2
        positions: dict[str, tuple[int, int]] = {}
        for hub in self.map.hubs:
            px = off_x + (hub.pos_x - min(xs)) * scale
            # y axis goes up like in a math graph
            py = HEIGHT - 60 - (off_y + (hub.pos_y - min(ys)) * scale)
            positions[hub.name] = (int(px), int(py))
        return positions

    @staticmethod
    def hub_color(hub: Hub) -> pygame.Color:
        """Return the hub color, or a default one if the name is unknown."""
        try:
            return pygame.Color(hub.color or "")
        except ValueError:
            return pygame.Color(DEFAULT_HUB)

    def radius(self, hub: Hub) -> int:
        """Return the drawing radius (start and end are bigger)."""
        if hub is self.map.start or hub is self.map.end:
            return RADIUS + 10
        return RADIUS

    def draw_text(self, text: str, center: tuple[int, int],
                  font: pygame.font.Font,
                  color: tuple[int, int, int] = TEXT) -> None:
        """Draw text centered on a point."""
        surface = font.render(text, True, color)
        self.screen.blit(surface, surface.get_rect(center=center))

    def draw_edge(self, link: Connection) -> None:
        """Draw a connection, thicker and labelled if capacity > 1."""
        a = self.pos[link.first_hub]
        b = self.pos[link.second_hub]
        width = 2 + 2 * (link.max_link_capacity - 1)
        blocked = any(self.by_name[n].zone is ZoneType.BLOCKED
                      for n in (link.first_hub, link.second_hub))
        pygame.draw.line(self.screen, GRID if blocked else EDGE, a, b,
                         min(width, 10))
        if link.max_link_capacity > 1:
            mid = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2 - 12)
            self.draw_text(f"x{link.max_link_capacity}", mid, self.small,
                           (255, 200, 90))

    def draw_hub(self, hub: Hub) -> None:
        """Draw a hub: colored disc, zone marker, name and occupancy."""
        x, y = self.pos[hub.name]
        r = self.radius(hub)
        color = self.hub_color(hub)
        pygame.draw.circle(self.screen, color, (x, y), r)
        if hub is self.map.start or hub is self.map.end:
            pygame.draw.circle(self.screen, TEXT, (x, y), r + 4, 2)
        if hub.zone is ZoneType.BLOCKED:
            d = int(r * 0.7)
            pygame.draw.line(self.screen, (0, 0, 0), (x - d, y - d),
                             (x + d, y + d), 4)
            pygame.draw.line(self.screen, (0, 0, 0), (x - d, y + d),
                             (x + d, y - d), 4)
        elif hub.zone is ZoneType.RESTRICTED:
            self.draw_dashed_ring((x, y), r + 6, (255, 80, 80))
        elif hub.zone is ZoneType.PRIORITY:
            pygame.draw.circle(self.screen, (90, 220, 255), (x, y), r + 6, 3)
        if hub.zone is not ZoneType.BLOCKED:
            dark = color.r * 0.3 + color.g * 0.59 + color.b * 0.11 > 150
            self.draw_text(f"{hub.actual_nb_drones}/{hub.max_drones}",
                           (x, y), self.font,
                           (0, 0, 0) if dark else TEXT)
        self.draw_text(hub.name, (x, y + r + 16), self.font)

    def draw_dashed_ring(self, center: tuple[int, int], r: int,
                         color: tuple[int, int, int]) -> None:
        """Draw a dashed circle (used for restricted zones)."""
        for i in range(0, 360, 30):
            start = math.radians(i)
            end = math.radians(i + 18)
            rect = pygame.Rect(0, 0, 2 * r, 2 * r)
            rect.center = center
            pygame.draw.arc(self.screen, color, rect, start, end, 3)

    def draw_legend(self, title: str) -> None:
        """Draw the title bar and the zone legend."""
        self.draw_text(f"{title}  -  {self.map.nb_drones} drones",
                       (WIDTH // 2, 24), self.big)
        y = HEIGHT - 30
        x = 30
        items: list[tuple[str, str]] = [
            ("dashed red ring = restricted (cost 2)", "restricted"),
            ("blue ring = priority", "priority"),
            ("X = blocked", "blocked"),
            ("xN = link capacity", "link"),
            ("n/m = drones/capacity", "cap"),
            ("SPACE: next  ESC: quit", "keys"),
        ]
        for label, _ in items:
            surface = self.small.render(label, True, MUTED)
            self.screen.blit(surface, (x, y))
            x += surface.get_width() + 28

    def draw_tooltip(self) -> None:
        """Show details of the hub under the mouse."""
        mx, my = pygame.mouse.get_pos()
        for hub in self.map.hubs:
            x, y = self.pos[hub.name]
            if math.hypot(mx - x, my - y) > self.radius(hub):
                continue
            lines = [
                hub.name,
                f"coords: ({hub.pos_x}, {hub.pos_y})",
                f"zone: {hub.zone.value}",
                f"color: {hub.color}",
                f"drones: {hub.actual_nb_drones}/{hub.max_drones}",
            ]
            box = pygame.Rect(mx + 14, my + 14, 190, 18 * len(lines) + 10)
            box.clamp_ip(self.screen.get_rect())
            pygame.draw.rect(self.screen, (10, 10, 14), box)
            pygame.draw.rect(self.screen, EDGE, box, 1)
            for i, line in enumerate(lines):
                surface = self.small.render(line, True, TEXT)
                self.screen.blit(surface, (box.x + 8, box.y + 6 + 18 * i))
            return

    def render(self, title: str = "MAP") -> None:
        """Draw one full frame."""
        self.screen.fill(BACKGROUND)
        for link in self.map.connections:
            self.draw_edge(link)
        for hub in self.map.hubs:
            self.draw_hub(hub)
        self.draw_legend(title)
        self.draw_tooltip()
        pygame.display.flip()

    def show(self, title: str = "MAP") -> bool:
        """Display the map until the user continues or quits.

        Args:
            title: text shown at the top (e.g. "TURN 3").

        Returns:
            True if the user pressed SPACE/ENTER (continue),
            False if they closed the window or pressed ESC.
        """
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        return True
            self.render(title)
            clock.tick(30)

    def close(self) -> None:
        """Close the window."""
        pygame.quit()
