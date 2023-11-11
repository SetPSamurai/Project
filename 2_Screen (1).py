from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.animation import Animation
from kivy.clock import Clock

class PulseApp(App):
    def build(self):
        self.sm = ScreenManager(transition=NoTransition())

        self.layout = GridLayout(cols=1, spacing=10, padding=10)
        self.layout.background_color = (93/255, 207/255, 195/255, 1)

        self.screen = Screen(name='main_screen')
        self.screen.add_widget(self.layout)
        self.sm.add_widget(self.screen)

        self.result_screen = Screen(name='result_screen')
        self.sm.add_widget(self.result_screen)

        self.time_remaining = 15
        self.timer_event = None
        self.pulse = None
        self.timer_expired = False

        label = Label(text='Замерьте пульс на 15 секунд', font_size=20)
        self.layout.add_widget(label)

        self.result_input = TextInput(hint_text='Пульс', multiline=False, font_size=20, size_hint=(1, 0.3))
        self.layout.add_widget(self.result_input)

        self.timer_label = Label(text='Время: 15 секунд', font_size=20)
        self.layout.add_widget(self.timer_label)

        start_button = Button(text='Начать измерение', font_size=20, size_hint=(1, 0.15))
        start_button.bind(on_press=self.start_measurement)
        self.layout.add_widget(start_button)

        save_button = Button(text='Записать результат', font_size=20, size_hint=(1, 0.15))
        save_button.bind(on_press=self.save_result)
        self.layout.add_widget(save_button)

        next_screen_button = Button(text='Перейти на следующий экран', font_size=20, size_hint=(1, 0.15))
        next_screen_button.bind(on_press=self.switch_screen)
        self.result_screen.add_widget(next_screen_button)

        return self.sm

    def start_measurement(self, instance):
        if not self.timer_event:
            self.time_remaining = 15
            self.timer_expired = False
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.time_remaining -= 1
        self.timer_label.text = f'Время: {self.time_remaining} секунд'
        if self.time_remaining <= 0:
            self.timer_label.text = 'Время вышло!'
            Clock.unschedule(self.timer_event)
            self.timer_event = None
            self.timer_expired = True

    def save_result(self, instance):
        if not self.timer_expired:
            self.timer_label.text = 'Дождитесь окончания таймера!'
        else:
            pulse = self.result_input.text
            if pulse.isdigit() and 40 <= int(pulse) <= 200:
                self.pulse = pulse
                self.timer_label.text = f'Замеренный пульс: {self.pulse} ударов в минуту'
                self.animate_fade_out()
            else:
                self.timer_label.text = 'Неправильный пульс! Введите корректное значение (40-200 уд/мин).'

    def animate_fade_out(self):
        anim = Animation(opacity=0, duration=1.5)
        anim.bind(on_complete=self.switch_screen)
        anim.start(self.layout)

    def animate_fade_in(self):
        anim = Animation(opacity=1, duration=1.5)
        anim.start(self.layout)

    def switch_screen(self, *args):
        self.sm.transition = NoTransition()
        self.sm.switch_to(self.result_screen)
        self.animate_fade_in()

if __name__ == '__main__':
    PulseApp().run()