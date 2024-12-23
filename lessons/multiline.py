import pygame

class MultilineText:
    def __init__(
        self, 
        text, 
        font, 
        max_width, 
        max_height, 
        text_color=(0, 0, 0), 
        bg_color=None,
        typing_effect=False,
        typing_speed=50
    ):
        self.text = text
        self.font = font
        self.max_width = max_width
        self.max_height = max_height
        self.text_color = text_color
        self.bg_color = bg_color

        self.typing_effect = typing_effect
        self.typing_speed = typing_speed
        self._typed_char_count = 0
        self._last_time = 0

        self.surface = None
        self.wrapped_lines = []
        self._wrap_lines()

    def _wrap_lines(self):
        self.wrapped_lines = []
        for line in self.text.split('\n'):
            if not line.strip():
                self.wrapped_lines.append("")

            current_line = ""
            for word in line.split(' '):
                test_line = current_line + ("" if not current_line else " ") + word
                w, _ = self.font.size(test_line)
                if w <= self.max_width:
                    current_line = test_line
                else:
                    self.wrapped_lines.append(current_line)
                    current_line = word

            if current_line:
                self.wrapped_lines.append(current_line)

    def _get_typed_lines(self):
        typed_lines = []
        chars_left = self._typed_char_count

        for line in self.wrapped_lines:
            if chars_left <= 0:
                break
            if chars_left >= len(line):
                typed_lines.append(line)
                chars_left -= len(line)
            else:
                typed_lines.append(line[:chars_left])
                chars_left = 0

        return typed_lines

    def render(self):
        if self.typing_effect:
            now = pygame.time.get_ticks()
            if self._last_time == 0:
                self._last_time = now

            while now - self._last_time >= self.typing_speed:
                self._typed_char_count += 1
                self._last_time += self.typing_speed

        line_height = self.font.get_linesize()
        max_lines = self.max_height // line_height

        if not self.typing_effect:
            visible_lines = self.wrapped_lines
        else:
            visible_lines = self._get_typed_lines()

        if len(visible_lines) > max_lines:
            visible_lines = visible_lines[:max_lines]

        surface_height = min(len(visible_lines) * line_height, self.max_height)
        self.surface = pygame.Surface((self.max_width, surface_height), pygame.SRCALPHA)
        if self.bg_color is not None:
            self.surface.fill(self.bg_color)

        y = 0
        for line in visible_lines:
            r = self.font.render(line, True, self.text_color)
            self.surface.blit(r, (0, y))
            y += line_height

        return self.surface