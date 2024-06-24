import pygame
import style
import random
import os.path

pygame.init()
pygame.font.init()
SCREEN_SIZE = (1920, 1080)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 30)
FONT_SIDE_BAR_HEAD_TEXT = pygame.font.SysFont("Arial", 20)
FONT_SIDE_BAR = pygame.font.SysFont("Arial", 50)
FONT_STOCK_TAB = pygame.font.SysFont("Arial", 36)
FONT_EXIT_BTN = pygame.font.SysFont("Arial", 34)
FONT_HOME_BTN = pygame.font.SysFont("Arial", 42)
FONT_STOCK_PAGE = pygame.font.SysFont("Arial", 40)
FONT_STOCK_NUMBERS = pygame.font.SysFont("Arial", 60)
FONT_GRAPH_NUMBERS = pygame.font.SysFont("Arial", 20)
FONT_MENU_BTN = pygame.font.SysFont("Arial", 40)
FONT_SCROLL = pygame.font.SysFont("Arial", 32)
FONT_QUIT = pygame.font.SysFont("Arial", 44)
FONT_QUIT_BTN = pygame.font.SysFont("Arial", 56)
BACKGROUND = pygame.image.load(os.path.join("data", "bg.png"))
MENU_BACKGROUND = pygame.image.load(os.path.join("data", "menu_bg.png"))
AD_BACKGROUND = pygame.image.load(os.path.join("data", "ad_bg.png"))
TAB_BACKGROUND = pygame.image.load(os.path.join("data", "tab_bg.png"))
TABO_BACKGROUND = pygame.image.load(os.path.join("data", "tabo_bg.png"))
EMA20 = pygame.image.load(os.path.join("data", "ema20.png"))
EMA20C = pygame.image.load(os.path.join("data", "ema20c.png"))
EMA50 = pygame.image.load(os.path.join("data", "ema50.png"))
EMA50C = pygame.image.load(os.path.join("data", "ema50c.png"))
EMA100 = pygame.image.load(os.path.join("data", "ema100.png"))
EMA100C = pygame.image.load(os.path.join("data", "ema100c.png"))
AD1 = pygame.image.load(os.path.join("data", "ad1.png"))
AD2 = pygame.image.load(os.path.join("data", "ad2.png"))
AD3 = pygame.image.load(os.path.join("data", "ad3.png"))
AD4 = pygame.image.load(os.path.join("data", "ad4.png"))
AD5 = pygame.image.load(os.path.join("data", "ad5.png"))

RUNNING = True
FPS = 30
QUIT_MENU = False

PAGE = 1
VIEWING_STOCK = 0
QUANTITY = 0
MONEY = 10000
CURRENT_AD = None
CURRENT_FIRST_SCROLL_STOCK = random.randint(0, 11)
CURRENT_START_PIXEL = 0

EMA20_ACT = False
EMA50_ACT = False
EMA100_ACT = False

RANGE_TOP_TOP = 2.0
RANGE_TOP = 1.5
RANGE_BOTTOM = 0.66
RANGE_BOTTOM_BOTTOM = 0.5


def main():
    PRICE_UPDATE = pygame.USEREVENT + 1
    CANDLE_UPDATE = pygame.USEREVENT + 2
    AD_UPDATE = pygame.USEREVENT + 3
    RATING_EVENT = pygame.USEREVENT + 4
    DIST_EVENT = pygame.USEREVENT + 5
    TEST_EVENT = pygame.USEREVENT + 6
    pygame.time.set_timer(PRICE_UPDATE, 500)
    pygame.time.set_timer(CANDLE_UPDATE, 10000)
    pygame.time.set_timer(AD_UPDATE, 20000)
    pygame.time.set_timer(RATING_EVENT, 30000)
    pygame.time.set_timer(DIST_EVENT, 10000)

    global MONEY
    global RUNNING
    global QUIT_MENU
    global QUANTITY
    global CURRENT_AD
    global RANGE_TOP_TOP
    global RANGE_TOP
    global RANGE_BOTTOM
    global RANGE_BOTTOM_BOTTOM
    global EMA20_ACT
    global EMA50_ACT
    global EMA100_ACT

    class ImageButton:
        def __init__(self, x, y, image, width, height, image2=None):
            self.x = x
            self.y = y
            self.image = image
            self.width = width
            self.height = height
            self.clicked = False
            self.image2 = image2
            self.state = 1

        def draw(self):
            action = False
            mouse_position = pygame.mouse.get_pos()
            if self.x <= mouse_position[0] <= self.x + self.width and self.y <= mouse_position[1] <= self.y + \
                    self.height:
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    action = True
                    if self.state == 1:
                        self.state = 2
                    else:
                        self.state = 1
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            if self.state == 1:
                SCREEN.blit(self.image, (self.x, self.y))
            else:
                SCREEN.blit(self.image2, (self.x, self.y))
            return action

    class Button:
        def __init__(self, x, y, width, height, text, bg_color, text_color, font=FONT, frame_color=None):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text
            self.bg_color = bg_color
            self.text_color = text_color
            self.font = font
            self.frame_color = frame_color
            self.clicked = False

        def draw(self):
            action = False
            mouse_position = pygame.mouse.get_pos()
            if self.x - 1 <= mouse_position[0] <= self.x + self.width + 2 and self.y - 1 <= mouse_position[1] <= \
                    self.y + self.height + 2:
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            if self.frame_color is not None:
                pygame.draw.rect(SCREEN, self.frame_color, (self.x - 1, self.y - 1, self.width + 2, self.height + 2))
            pygame.draw.rect(SCREEN, self.bg_color, (self.x, self.y, self.width, self.height))
            btn_text = self.font.render(self.text, True, self.text_color)
            SCREEN.blit(btn_text, (self.x + 1, self.y + 1))

            return action

    class Stock:
        def __init__(self, ID, name):
            self.ID = ID
            self.name = name
            self.owned = 0
            self.price = random.gauss(100, 50)
            if self.price < 0:
                self.price *= -1
            self.price_initialized = self.price
            self.price_range = [0.0, 99999.9]
            self.last_prices = []
            self.average_buy_in = 0
            self.clicked = False

        def buy(self, amount):
            global MONEY
            global QUANTITY
            if amount > 0 and len(STOCKS_OWNED) < 8:
                if (MONEY - (amount * self.price)) > 0:
                    MONEY -= amount * self.price
                    if self not in STOCKS_OWNED:
                        STOCKS_OWNED.append(self)

                    self.average_buy_in = ((self.average_buy_in * self.owned) + (amount * self.price)) / (
                            self.owned + amount)
                    self.owned += amount
                    QUANTITY = 0

        def sell(self, amount):
            global MONEY
            global QUANTITY
            if amount > 0:
                if amount <= self.owned:
                    MONEY += amount * self.price
                    self.owned -= amount
                    QUANTITY = 0
                    if self.owned == 0:
                        STOCKS_OWNED.remove(self)

        def add_price_range(self):
            length = len(self.last_prices)
            sum20 = 0
            sum50 = 0
            sum100 = 0
            if length >= 19:
                for p in range(length - 19, length):
                    sum20 += ((self.last_prices[p][0] - self.last_prices[p][1]) / 2 + self.last_prices[p][1])
                sum20 += (self.price_range[0] - self.price_range[1]) / 2 + self.price_range[1]
                self.price_range.append(sum20 / 20)
                if length >= 49:
                    for q in range(length - 49, length - 19):
                        sum50 += ((self.last_prices[q][0] - self.last_prices[q][1]) / 2 + self.last_prices[q][1])
                    sum50 += sum20
                    self.price_range.append(sum50 / 50)
                    if length >= 99:
                        for r in range(length - 99, length - 49):
                            sum100 += ((self.last_prices[r][0] - self.last_prices[r][1]) / 2 + self.last_prices[r][1])
                        sum100 += sum50
                        self.price_range.append(sum100 / 100)
            if length > 299:
                self.last_prices.pop(0)
                self.last_prices.append(self.price_range)
            else:
                self.last_prices.append(self.price_range)
            self.price_range = [0, 99999]

        def add_price(self, price):
            self.price = price
            if price > self.price_range[0]:
                self.price_range[0] = price
            if price < self.price_range[1]:
                self.price_range[1] = price

        def get_ID(self):
            return self.ID

        def get_name(self):
            return self.name

        def get_price(self):
            return self.price

        def get_amount(self):
            return self.owned

        def get_initialized(self):
            return self.price_initialized

        def get_last_price(self):
            return (self.last_prices[len(self.last_prices) - 1][0] - self.last_prices[len(self.last_prices) - 1][
                1]) / 2 + self.last_prices[len(self.last_prices) - 1][1]

        def draw_menu(self):
            pygame.draw.rect(SCREEN, style.GREY_VERY_DARK, (1620, 190, 290, 200))
            pygame.draw.line(SCREEN, style.GREY_LIGHT, (1640, 250), (1890, 250))
            trade_amount = FONT_MENU_BTN.render(str(QUANTITY), True, style.WHITE)
            SCREEN.blit(trade_amount, (1650, 205))
            if buy_btn.draw():
                self.buy(QUANTITY)
            if sell_btn.draw():
                self.sell(QUANTITY)

        def draw_scroll(self, x, y):
            pygame.draw.rect(SCREEN, style.GREY_VERY_DARK, (x, y, 320, 56))
            scroll_name = FONT_SCROLL.render(self.name, True, style.WHITE)
            change_percent = (self.price - self.price_initialized) / self.price_initialized * 100
            if change_percent > 0:
                change = FONT_SCROLL.render("▲%.2f" % change_percent + "%", True, style.GREEN)
            elif change_percent < 0:
                change = FONT_SCROLL.render("▼%.2f" % (-change_percent) + "%", True, style.RED)
            else:
                change = FONT_SCROLL.render("%.2f" % change_percent + "%", True, style.WHITE)

            SCREEN.blit(scroll_name, (x + 10, y + 10))
            SCREEN.blit(change, (x + 186, y + 10))

        def draw_position_info(self):
            pygame.draw.rect(SCREEN, style.GREY_VERY_DARK, (1620, 390, 290, 480))
            amount_text = FONT_SIDE_BAR_HEAD_TEXT.render("Shares", True, style.GREY_LIGHT)
            amount_value = FONT_SIDE_BAR.render(str(self.owned), True, style.WHITE)
            buyin_text = FONT_SIDE_BAR_HEAD_TEXT.render("Average", True, style.GREY_LIGHT)
            buyin_value = FONT_SIDE_BAR.render("%.2f$" % self.average_buy_in, True, style.WHITE)
            total_text = FONT_SIDE_BAR_HEAD_TEXT.render("Value", True, style.GREY_LIGHT)
            position = self.owned * self.price
            total_value = FONT_SIDE_BAR.render("%.2f$" % position, True, style.WHITE)
            total_change_text = FONT_SIDE_BAR_HEAD_TEXT.render("Change", True, style.GREY_LIGHT)
            change_buyin = ((self.price * self.owned) / (self.average_buy_in * self.owned) - 1) * 100

            if change_buyin > 0:
                total_change_value = FONT_SIDE_BAR.render("▲%.2f$" % (position - (self.owned * self.average_buy_in)),
                                                          True, style.GREEN)
                total_change_percent = FONT_SIDE_BAR.render("▲%.2f" % change_buyin + "%", True, style.GREEN)
            elif change_buyin < 0:
                total_change_value = FONT_SIDE_BAR.render("▼%.2f$" % (-(position - (self.owned * self.average_buy_in))),
                                                          True, style.RED)
                total_change_percent = FONT_SIDE_BAR.render("▼%.2f" % (-change_buyin) + "%", True, style.RED)
            else:
                total_change_value = FONT_SIDE_BAR.render("%.2f$" % (position - (self.owned * self.average_buy_in)),
                                                          True, style.WHITE)
                total_change_percent = FONT_SIDE_BAR.render("%.2f" % change_buyin + "%", True, style.WHITE)

            SCREEN.blit(amount_text, (1640, 400))
            SCREEN.blit(amount_value, (1640, 420))
            SCREEN.blit(buyin_text, (1640, 510))
            SCREEN.blit(buyin_value, (1640, 530))
            SCREEN.blit(total_text, (1640, 620))
            SCREEN.blit(total_value, (1640, 640))
            SCREEN.blit(total_change_text, (1640, 730))
            SCREEN.blit(total_change_value, (1640, 750))
            SCREEN.blit(total_change_percent, (1640, 800))

        def draw_tab(self, x, y):
            mouse_position = pygame.mouse.get_pos()
            action = False
            if x <= mouse_position[0] <= x + 580 and y <= mouse_position[1] <= y + 60:
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            name = FONT_STOCK_TAB.render(self.name, True, style.WHITE)
            price = FONT_STOCK_TAB.render("%.2f$" % self.price, True, style.WHITE)
            change_percent = (self.price - self.price_initialized) / self.price_initialized * 100
            if change_percent > 0:
                change = FONT_STOCK_TAB.render("▲%.2f" % change_percent + "%", True, style.GREEN)
            elif change_percent < 0:
                change = FONT_STOCK_TAB.render("▼%.2f" % (-change_percent) + "%", True, style.RED)
            else:
                change = FONT_STOCK_TAB.render("%.2f" % change_percent + "%", True, style.WHITE)

            SCREEN.blit(TAB_BACKGROUND, (x, y))
            SCREEN.blit(name, (x + 12, y + 9))
            SCREEN.blit(price, (x + 280, y + 9))
            SCREEN.blit(change, (x + 425, y + 9))

            return action

        def draw_tab_owned(self, x, y):
            mouse_position = pygame.mouse.get_pos()
            action = False
            if x <= mouse_position[0] <= x + 580 and y <= mouse_position[1] <= y + 100:
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            name = FONT_STOCK_TAB.render(self.name, False, style.WHITE)
            price = FONT_STOCK_TAB.render("%.2f$" % self.price, False, style.WHITE)
            change_percent = (self.price - self.price_initialized) / self.price_initialized * 100
            change_buy_in = ((self.price * self.owned) / (self.average_buy_in * self.owned) - 1) * 100

            if change_percent > 0:
                change = FONT_STOCK_TAB.render("▲%.2f" % change_percent + "%", True, style.GREEN)
            elif change_percent < 0:
                change = FONT_STOCK_TAB.render("▼%.2f" % (-change_percent) + "%", True, style.RED)
            else:
                change = FONT_STOCK_TAB.render("%.2f" % change_percent + "%", True, style.WHITE)

            if change_buy_in > 0:
                value_change = FONT_STOCK_TAB.render("▲%.2f" % change_buy_in + "%", True, style.GREEN)
                value = FONT_STOCK_TAB.render("%.2f$" % (self.owned * self.price), True, style.GREEN)
            elif change_buy_in < 0:
                value_change = FONT_STOCK_TAB.render("▼%.2f" % (-change_buy_in) + "%", True, style.RED)
                value = FONT_STOCK_TAB.render("%.2f$" % (self.owned * self.price), True, style.RED)
            else:
                value_change = FONT_STOCK_TAB.render("%.2f" % change_buy_in + "%", True, style.WHITE)
                value = FONT_STOCK_TAB.render("%.2f$" % (self.owned * self.price), True, style.WHITE)

            owned = FONT_STOCK_TAB.render(str(self.owned) + " @ %.2f$" % self.average_buy_in, False, style.WHITE)

            SCREEN.blit(TABO_BACKGROUND, (x, y))
            SCREEN.blit(name, (x + 8, y + 7))
            SCREEN.blit(price, (x + 280, y + 7))
            SCREEN.blit(change, (x + 425, y + 7))
            SCREEN.blit(owned, (x + 8, y + 50))
            SCREEN.blit(value, (x + 280, y + 50))
            SCREEN.blit(value_change, (x + 425, y + 50))

            return action

        def draw_graph(self, x, y):

            # HEAD
            change_percent = (self.price - self.price_initialized) / self.price_initialized * 100
            pygame.draw.rect(SCREEN, style.GREY_VERY_DARK, (x, y, 1200, 800))
            pygame.draw.rect(SCREEN, style.GREY_DARK, (x + 10, y + 130, 1180, 660))

            name_text = FONT_STOCK_PAGE.render(self.name, True, style.WHITE)
            price_value = FONT_STOCK_NUMBERS.render("%.2f$" % self.price, True, style.WHITE)

            if change_percent > 0:
                change_value = FONT_STOCK_NUMBERS.render("▲%.2f" % change_percent + "%", True, style.GREEN)
            elif change_percent < 0:
                change_value = FONT_STOCK_NUMBERS.render("▼%.2f" % (-change_percent) + "%", True, style.RED)
            else:
                change_value = FONT_STOCK_NUMBERS.render("%.2f" % change_percent + "%", True, style.WHITE)

            SCREEN.blit(name_text, (x + 10, y + 5))
            SCREEN.blit(price_value, (x + 10, y + 50))
            SCREEN.blit(change_value, (x + 960, y + 50))

            # GRAPH
            length = len(self.last_prices)
            up = self.price * 1.001
            down = self.price * 0.999
            if length < 200:
                for m in self.last_prices:
                    if m[0] > up:
                        up = m[0]
                    if m[1] < down:
                        down = m[1]
            else:
                for n in range(length - 200, length):
                    if self.last_prices[n][0] > up:
                        up = self.last_prices[n][0]
                    if self.last_prices[n][1] < down:
                        down = self.last_prices[n][1]
            if self.price_range[0] > up:
                up = self.price_range[0]
            if self.price_range[1] < down:
                down = self.price_range[1]

            full_range = 640 / (up - down)

            pygame.draw.line(SCREEN, style.GREY_LIGHT, (x + 1120, y + 140), (x + 1120, y + 780))
            pygame.draw.line(SCREEN, style.GREY_LIGHT, (x + 20, y + 152), (x + 1110, y + 152))
            pygame.draw.line(SCREEN, style.GREY_LIGHT, (x + 20, y + 306), (x + 1110, y + 306))
            pygame.draw.line(SCREEN, style.GREY_LIGHT, (x + 20, y + 460), (x + 1110, y + 460))
            pygame.draw.line(SCREEN, style.GREY_LIGHT, (x + 20, y + 614), (x + 1110, y + 614))
            pygame.draw.line(SCREEN, style.GREY_LIGHT, (x + 20, y + 768), (x + 1110, y + 768))

            upper_price = FONT_GRAPH_NUMBERS.render("%.2f" % up, True, style.GREEN)
            mid_price = FONT_GRAPH_NUMBERS.render("%.2f" % ((up + down) / 2), True, style.WHITE)
            lower_price = FONT_GRAPH_NUMBERS.render("%.2f" % down, True, style.RED)
            SCREEN.blit(upper_price, (x + 1130, y + 140))
            SCREEN.blit(mid_price, (x + 1130, y + 449))
            SCREEN.blit(lower_price, (x + 1130, y + 758))

            y_height = full_range * (up - self.price) + y + 140
            pygame.draw.line(SCREEN, style.WHITE, (x + 20, y_height), (x + 1110, y_height))
            pygame.draw.rect(SCREEN, style.GREY_LIGHT, (x + 1130, y_height - 10, 52, 20))
            price_indicator = FONT_GRAPH_NUMBERS.render("%.2f" % self.price, True, style.BLACK)
            SCREEN.blit(price_indicator, (x + 1130, y_height - 11))

            if EMA20_ACT and length >= 20:
                if length < 200:
                    last = self.last_prices[19][2]
                    for e in range(20, length):
                        if up > last > down:
                            pygame.draw.line(SCREEN, style.GREEN,
                                             (e * 5 + x + 18, full_range * (up - last) + y + 140),
                                             (e * 5 + x + 22, full_range * (up - self.last_prices[e][2]) + y + 140), 1)
                        last = self.last_prices[e][2]
                elif length < 220:
                    last = self.last_prices[19][2]
                    for e in range(220 - length, 200):
                        if up > last > down:
                            pygame.draw.line(SCREEN, style.GREEN,
                                             (e * 5 + x + 18, full_range * (up - last) + y + 140),
                                             (e * 5 + x + 22,
                                              full_range * (up - self.last_prices[e + length - 200][2]) + y + 140), 1)
                        last = self.last_prices[e + length - 200][2]
                else:
                    last = self.last_prices[length - 201][2]
                    for e in range(0, 200):
                        if up > last > down:
                            pygame.draw.line(SCREEN, style.GREEN,
                                             (e * 5 + x + 18, full_range * (up - last) + y + 140),
                                             (e * 5 + x + 22,
                                              full_range * (up - self.last_prices[e + length - 200][2]) + y + 140), 1)
                        last = self.last_prices[e + length - 200][2]

            if EMA50_ACT and length >= 50:
                if length < 200:
                    last = self.last_prices[49][3]
                    for e in range(50, length):
                        if up > last > down:
                            pygame.draw.line(SCREEN, style.ORANGE,
                                             (e * 5 + x + 18, full_range * (up - last) + y + 140),
                                             (e * 5 + x + 22, full_range * (up - self.last_prices[e][3]) + y + 140), 1)
                        last = self.last_prices[e][3]
                elif length < 250:
                    last = self.last_prices[49][3]
                    for e in range(250 - length, 200):
                        if up > last > down:
                            pygame.draw.line(SCREEN, style.ORANGE,
                                             (e * 5 + x + 18, full_range * (up - last) + y + 140),
                                             (e * 5 + x + 22,
                                              full_range * (up - self.last_prices[e + length - 200][3]) + y + 140), 1)
                        last = self.last_prices[e + length - 200][3]
                else:
                    last = self.last_prices[length - 201][3]
                    for e in range(0, 200):
                        if up > last > down:
                            pygame.draw.line(SCREEN, style.ORANGE,
                                             (e * 5 + x + 18, full_range * (up - last) + y + 140),
                                             (e * 5 + x + 22,
                                              full_range * (up - self.last_prices[e + length - 200][3]) + y + 140), 1)
                        last = self.last_prices[e + length - 200][3]

            if EMA100_ACT and length >= 100:
                if length < 200:
                    last = self.last_prices[99][4]
                    for e in range(100, length):
                        if up > last > down:
                            pygame.draw.line(SCREEN, style.RED,
                                             (e * 5 + x + 18, full_range * (up - last) + y + 140),
                                             (e * 5 + x + 22, full_range * (up - self.last_prices[e][4]) + y + 140), 1)
                        last = self.last_prices[e][4]
                elif length < 300:
                    last = self.last_prices[99][4]
                    for e in range(300 - length, 200):
                        if up > last > down:
                            pygame.draw.line(SCREEN, style.RED,
                                             (e * 5 + x + 18, full_range * (up - last) + y + 140),
                                             (e * 5 + x + 22,
                                              full_range * (up - self.last_prices[e + length - 200][4]) + y + 140), 1)
                        last = self.last_prices[e + length - 200][4]
                else:
                    last = self.last_prices[length - 201][4]
                    for e in range(0, 200):
                        if up > last > down:
                            pygame.draw.line(SCREEN, style.RED,
                                             (e * 5 + x + 18, full_range * (up - last) + y + 140),
                                             (e * 5 + x + 22,
                                              full_range * (up - self.last_prices[e + length - 200][4]) + y + 140), 1)
                        last = self.last_prices[e + length - 200][4]

            if length < 200:
                for candle in range(0, length):
                    pygame.draw.rect(SCREEN, style.WHITE, (
                        candle * 5 + x + 21, full_range * (up - self.last_prices[candle][0]) + y + 140, 4,
                        full_range * (self.last_prices[candle][0] - self.last_prices[candle][1])))
                pygame.draw.rect(SCREEN, style.WHITE, (
                    length * 5 + x + 21, full_range * (up - self.price_range[0]) + y + 140, 4,
                    full_range * (self.price_range[0] - self.price_range[1])))
            else:
                for candle in range(length - 200, length):
                    pygame.draw.rect(SCREEN, style.WHITE, (
                        (candle - length) * 5 + x + 1021,
                        full_range * (up - self.last_prices[candle][0]) + y + 140, 4,
                        full_range * (self.last_prices[candle][0] - self.last_prices[candle][1])))
                pygame.draw.rect(SCREEN, style.WHITE, (
                    1021 + x, full_range * (up - self.price_range[0]) + y + 140, 4,
                    full_range * (self.price_range[0] - self.price_range[1])))

    stock1 = Stock(1, "BookStop")
    stock2 = Stock(2, "Musket Oils")
    stock3 = Stock(3, "Chibado Grill")
    stock4 = Stock(4, "Chadpumps")
    stock5 = Stock(5, "Billiard Power")
    stock6 = Stock(6, "WSB")
    stock7 = Stock(7, "Bepsi")
    stock8 = Stock(8, "Macrohard")
    stock9 = Stock(9, "C4 AI")
    stock10 = Stock(10, "NoVideo")
    stock11 = Stock(11, "Fivecent")
    stock12 = Stock(12, "Pear")

    STOCKS_LIST = [
        stock1,
        stock2,
        stock3,
        stock4,
        stock5,
        stock6,
        stock7,
        stock8,
        stock9,
        stock10,
        stock11,
        stock12,
    ]

    for stock in STOCKS_LIST:
        for i in range(0, 50):
            for j in range(0, 10):
                stock.add_price(stock.get_price() * ((100 + random.gauss(0, 0.05)) / 100))
            stock.add_price_range()
            stock.add_price(stock.get_price())

    STOCKS_OWNED = []

    ADS = [
        AD1,
        AD2,
        AD3,
        AD4,
        AD5,
    ]

    CURRENT_AD = random.choice(ADS)

    # exit_btn = Button(1852, 0, 78, 40, "   ×", style.RED, style.WHITE, FONT_EXIT_BTN)
    back_btn = Button(1, 1, 145, 54, "   Start", style.HOME, style.WHITE, FONT_HOME_BTN, style.HOME)
    buy_btn = Button(1640, 260, 250, 50, "          BUY", style.GREY_VERY_DARK, style.GREEN, FONT_MENU_BTN, style.GREEN)
    sell_btn = Button(1640, 320, 250, 50, "          SELL", style.GREY_VERY_DARK, style.RED, FONT_MENU_BTN, style.RED)
    quit_yes_btn = Button(641, 101, 308, 69, "        YES", style.GREY_VERY_DARK, style.RED, FONT_QUIT_BTN, style.RED)
    quit_no_btn = Button(971, 101, 308, 69, "         NO", style.GREY_VERY_DARK, style.GREEN, FONT_QUIT_BTN,
                         style.GREEN)
    ema_20_btn = ImageButton(360, 1000, EMA20, 150, 50, EMA20C)
    ema_50_btn = ImageButton(520, 1000, EMA50, 150, 50, EMA50C)
    ema_100_btn = ImageButton(680, 1000, EMA100, 150, 50, EMA100C)

    # MAIN DRAW

    def draw():
        global PAGE
        global VIEWING_STOCK
        global RUNNING
        global QUIT_MENU
        global QUANTITY
        global CURRENT_AD
        global CURRENT_START_PIXEL
        global CURRENT_FIRST_SCROLL_STOCK
        global RANGE_TOP_TOP
        global RANGE_TOP
        global RANGE_BOTTOM
        global RANGE_BOTTOM_BOTTOM
        global EMA20_ACT
        global EMA50_ACT
        global EMA100_ACT

        # BACKGROUND ELEMENTS
        SCREEN.blit(BACKGROUND, (0, 0))
        for k in range(0, 8):
            STOCKS_LIST[(CURRENT_FIRST_SCROLL_STOCK + k) % 12].draw_scroll(CURRENT_START_PIXEL + (k * 320), 0)

        CURRENT_START_PIXEL -= 1
        if CURRENT_START_PIXEL < -319:
            CURRENT_FIRST_SCROLL_STOCK += 1
            CURRENT_START_PIXEL += 320

        # PAGE 1 ELEMENTS
        if PAGE == 1:
            view_list = list(set(STOCKS_LIST) - set(STOCKS_OWNED))
            pygame.draw.rect(SCREEN, style.GREY_VERY_DARK, (355, 190, 600, len(view_list) * 70 + 10))
            SCREEN.blit(AD_BACKGROUND, (1620, 190))
            SCREEN.blit(CURRENT_AD, (1630, 200))
            for o in range(0, len(view_list)):
                if view_list[o].draw_tab(365, o * 70 + 200):
                    QUANTITY = 0
                    PAGE = 2
                    VIEWING_STOCK = view_list[o].get_ID()
            if len(STOCKS_OWNED) > 0:
                pygame.draw.rect(SCREEN, style.GREY_VERY_DARK, (965, 190, 600, len(STOCKS_OWNED) * 106 + 10))
                for m in range(0, len(STOCKS_OWNED)):
                    if STOCKS_OWNED[m].draw_tab_owned(975, m * 106 + 200):
                        QUANTITY = 0
                        PAGE = 2
                        VIEWING_STOCK = STOCKS_OWNED[m].get_ID()
            else:
                pygame.draw.rect(SCREEN, style.GREY_DARK, (1090, 490, 280, 60))
                error = FONT.render("Try buying some stocks", True, style.WHITE)
                SCREEN.blit(error, (1100, 500))

        # PAGE 2 ELEMENTS
        else:
            stock_site = None
            for cur in STOCKS_LIST:
                if cur.get_ID() == VIEWING_STOCK:
                    stock_site = cur

            stock_site.draw_graph(360, 190)
            stock_site.draw_menu()
            if stock_site.get_amount() > 0:
                stock_site.draw_position_info()

            if back_btn.draw():
                PAGE = 1
                VIEWING_STOCK = None

            if ema_20_btn.draw():
                if EMA20_ACT:
                    EMA20_ACT = False
                else:
                    EMA20_ACT = True
            if ema_50_btn.draw():
                if EMA50_ACT:
                    EMA50_ACT = False
                else:
                    EMA50_ACT = True
            if ema_100_btn.draw():
                if EMA100_ACT:
                    EMA100_ACT = False
                else:
                    EMA100_ACT = True

        # BASE PAGE ELEMENTS
        stocks_worth = 0.0
        for cur in STOCKS_OWNED:
            stocks_worth += cur.get_price() * cur.get_amount()
        total_worth = stocks_worth + MONEY
        total_percent = (total_worth / 10000 - 1) * 100
        pygame.draw.rect(SCREEN, style.GREY_DARK, (10, 190, 290, 372))
        SCREEN.blit(MENU_BACKGROUND, (10, 190))
        portfolio_text = FONT_SIDE_BAR_HEAD_TEXT.render("Portfolio", True, style.GREY_LIGHT)
        portfolio_value = FONT_SIDE_BAR.render("%.2f$" % stocks_worth, True, style.WHITE)
        cash_text = FONT_SIDE_BAR_HEAD_TEXT.render("Cash", True, style.GREY_LIGHT)
        cash_value = FONT_SIDE_BAR.render("%.2f$" % MONEY, True, style.WHITE)
        total_text = FONT_SIDE_BAR_HEAD_TEXT.render("Total", True, style.GREY_LIGHT)

        if total_worth > 10000:
            total_value = FONT_SIDE_BAR.render("%.2f$" % total_worth, True, style.GREEN)
        elif total_worth < 10000:
            total_value = FONT_SIDE_BAR.render("%.2f$" % total_worth, True, style.RED)
        else:
            total_value = FONT_SIDE_BAR.render("%.2f$" % total_worth, True, style.WHITE)

        if total_percent > 0:
            total_change = FONT_SIDE_BAR.render("▲%.2f" % total_percent + "%", True, style.GREEN)
        elif total_percent < 0:
            total_change = FONT_SIDE_BAR.render("▼%.2f" % (-total_percent) + "%", True, style.RED)
        else:
            total_change = FONT_SIDE_BAR.render("%.2f" % total_percent + "%", True, style.WHITE)

        SCREEN.blit(portfolio_text, (20, 200))
        SCREEN.blit(portfolio_value, (20, 220))
        SCREEN.blit(cash_text, (20, 310))
        SCREEN.blit(cash_value, (20, 330))
        SCREEN.blit(total_text, (20, 420))
        SCREEN.blit(total_value, (20, 440))
        SCREEN.blit(total_change, (20, 500))

        # QUIT MENU
        if QUIT_MENU:
            pygame.draw.rect(SCREEN, style.GREY_VERY_DARK, (630, 20, 660, 160))
            quit_text = FONT_QUIT.render("DO YOU WANT TO QUIT THE GAME?", True, style.WHITE)
            SCREEN.blit(quit_text, (648, 30))
            if quit_yes_btn.draw():
                RUNNING = False
            if quit_no_btn.draw():
                QUIT_MENU = False

        pygame.display.update()

    while RUNNING:
        CLOCK.tick(FPS)

        for event in pygame.event.get():

            # 500 ms EVENT

            if event.type == PRICE_UPDATE:
                for stock in STOCKS_LIST:
                    if random.randint(1, 10) < 7:
                        if (stock.get_price() / stock.get_initialized()) > RANGE_TOP_TOP:
                            stock.add_price(stock.get_price() * ((100 + random.gauss(-0.1, 3)) / 100))
                        elif (stock.get_price() / stock.get_initialized()) > RANGE_TOP:
                            stock.add_price(stock.get_price() * ((100 + random.gauss(-0.1, 1.5)) / 100))
                        elif (stock.get_price() / stock.get_initialized()) < RANGE_BOTTOM:
                            stock.add_price(stock.get_price() * ((100 + random.gauss(0.1, 1.5)) / 100))
                        elif (stock.get_price() / stock.get_initialized()) < RANGE_BOTTOM_BOTTOM:
                            stock.add_price(stock.get_price() * ((100 + random.gauss(0.1, 3)) / 100))
                        else:
                            stock.add_price(stock.get_price() * ((100 + random.gauss(0, 0.15)) / 100))

            # 10.000 ms EVENT

            elif event.type == DIST_EVENT:

                # RANDOM EVENT SELECTOR MISSING HERE
                pygame.time.set_timer(TEST_EVENT, 1000)
                print("LUL")

            # 10.000 ms EVENT

            elif event.type == CANDLE_UPDATE:
                for stock in STOCKS_LIST:
                    stock.add_price_range()
                    stock.add_price(stock.get_price())

            # 20.000 ms EVENT

            elif event.type == AD_UPDATE:
                CURRENT_AD = random.choice(ADS)

            # 30.000 ms EVENT

            elif event.type == RATING_EVENT:
                RANGE_TOP_TOP = random.uniform(1.75, 2.10)
                RANGE_TOP = random.uniform(1.35, 1.60)
                RANGE_BOTTOM = random.uniform(0.63, 0.74)
                RANGE_BOTTOM_BOTTOM = random.uniform(0.48, 0.57)

            # DISTED EVENTS

            elif event.type == TEST_EVENT:
                print("LUL 1s after")
                pygame.time.set_timer(TEST_EVENT, 0)

            # KEYEVENTS

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if QUIT_MENU:
                        QUIT_MENU = False
                    else:
                        QUIT_MENU = True
                elif event.key == pygame.K_RETURN:
                    if QUIT_MENU:
                        RUNNING = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_0:
                    if QUANTITY != 0 and QUANTITY < 999999:
                        QUANTITY *= 10
                elif event.key == pygame.K_1:
                    if QUANTITY != 0 and QUANTITY < 999999:
                        QUANTITY *= 10
                        QUANTITY += 1
                    else:
                        QUANTITY = 1
                elif event.key == pygame.K_2:
                    if QUANTITY != 0 and QUANTITY < 999999:
                        QUANTITY *= 10
                        QUANTITY += 2
                    else:
                        QUANTITY = 2
                elif event.key == pygame.K_3:
                    if QUANTITY != 0 and QUANTITY < 999999:
                        QUANTITY *= 10
                        QUANTITY += 3
                    else:
                        QUANTITY = 3
                elif event.key == pygame.K_4:
                    if QUANTITY != 0 and QUANTITY < 999999:
                        QUANTITY *= 10
                        QUANTITY += 4
                    else:
                        QUANTITY = 4
                elif event.key == pygame.K_5:
                    if QUANTITY != 0 and QUANTITY < 999999:
                        QUANTITY *= 10
                        QUANTITY += 5
                    else:
                        QUANTITY = 5
                elif event.key == pygame.K_6:
                    if QUANTITY != 0 and QUANTITY < 999999:
                        QUANTITY *= 10
                        QUANTITY += 6
                    else:
                        QUANTITY = 6
                elif event.key == pygame.K_7:
                    if QUANTITY != 0 and QUANTITY < 999999:
                        QUANTITY *= 10
                        QUANTITY += 7
                    else:
                        QUANTITY = 7
                elif event.key == pygame.K_8:
                    if QUANTITY != 0 and QUANTITY < 999999:
                        QUANTITY *= 10
                        QUANTITY += 8
                    else:
                        QUANTITY = 8
                elif event.key == pygame.K_9:
                    if QUANTITY != 0 and QUANTITY < 999999:
                        QUANTITY *= 10
                        QUANTITY += 9
                    else:
                        QUANTITY = 9
                elif event.key == pygame.K_BACKSPACE:
                    if QUANTITY != 0 and QUANTITY < 999999:
                        QUANTITY //= 10

            elif event.type == pygame.QUIT:
                RUNNING = False

        draw()

    pygame.quit()


if __name__ == "__main__":
    main()
