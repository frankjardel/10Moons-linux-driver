from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from kivy.graphics import Color, Ellipse

import multiprocessing
import driver


class ContentNavigationDrawer(MDCard):

    def __init__(self, **kwargs):
        super(ContentNavigationDrawer, self).__init__(**kwargs)

        with self.canvas:
            Color(1,1,0,.5, mode='rgba')
            self.rect = Ellipse(pos=(0, 0), size=(10, 10))


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.rect.pos = touch.pos

            with self.canvas:
                Color(1, 1, 0, .5, mode='rgba')
                Ellipse(pos=(touch.pos), size=(10, 10))
        else:
            self.canvas.clear()


    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.rect.pos = touch.pos

            with self.canvas:
                Color(1, 1, 0, .5, mode='rgba')
                Ellipse(pos=(touch.pos), size=(10, 10))


class MainApp(MDApp):

    def build(self):

        self.process = multiprocessing.Process(
            target=driver.start,
            args=()
        )
        self.process.start()

        kv = '''
Screen:
    MDBoxLayout:
        id: main
        orientation: 'vertical'

        MDTopAppBar:
            id: toolbar
            orientation: 'vertical'
            type: "top"
            md_bg_color: (0, 0, 0, .1)

            MDBoxLayout:
                orientation: 'horizontal'

                MDRaisedButton:
                    id: button1
                    text: "Ctrl+Shift+L"
                    pos_hint: {"center_x": .1, "center_y": 1}
                    on_release: app.settings()
                    md_bg_color: (.1, .1, .1, 1)

                MDRaisedButton:
                    id: button2
                    text: "Ctrl+Shift+P"
                    pos_hint: {"center_x": .3, "center_y": 1}
                    on_release: app.settings()
                    md_bg_color: (.1, .1, .1, 1)

                MDLabel:
                    text: "          10Moons          "
                    color: (0,0,0, 1)
                    pos_hint: {"center_x": 1, "center_y": 1}

                MDRaisedButton:
                    id: button1
                    text: "Ctrl+Z"
                    pos_hint: {"center_x": 1, "center_y": 1}
                    on_release: app.settings()
                    md_bg_color: (.1, .1, .1, 1)

                MDRaisedButton:
                    id: button2
                    text: "Ctrl+Shift+Z"
                    pos_hint: {"center_x": 1, "center_y": 1}
                    on_release: app.settings()
                    md_bg_color: (.1, .1, .1, 1)


        MDBoxLayout:
            MDStackLayout:
                size_hint: None, None
                pos_hint: {"center_y": 0.475}
                size: root.width, root.height - 65

                ContentNavigationDrawer:
                    size_hint: None, None
                    size: root.width, root.height
                    md_bg_color: (.1, .1, .1, 1)
        '''

        return Builder.load_string(kv)


    def settings(self):
        print("settings.. in working..")


MainApp().run()