"""
Driver for 10moons on Linux
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

import os
import multiprocessing
import driver


class teenmoons(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.process = multiprocessing.Process(
            target=driver.start,
            args=()
        )
        self.process.start()

        # hide menu default
        factory_app = self.factory.App
        factory_app.create_menus = lambda _: None

        main_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=10,
                background_color="WHITE"
            )
        )

        header_box = toga.Box()

        main_box.add(header_box)

        # buttons left
        header_box.add(
            toga.Button(
                'Ctrl+Shift+L',
                on_press=self.first_button,
                style=Pack(
                    background_color="BLACK"
                )
            ),
            toga.Button(
                'Ctrl+Shift+P',
                on_press=self.second_button,
                style=Pack(
                    background_color="BLACK"
                )
            )
        )

        # label
        label = toga.Label(
            '10Moons',
            style=Pack(
                direction=COLUMN,
                padding_top=10,
                padding_left=50,
                padding_right=50
            )
        )
        header_box.add(label)

        # button right
        header_box.add(
            toga.Button(
                'Ctrl+Z',
                on_press=self.third_button,
                style=Pack(
                    background_color="BLACK"
                )
            ),
            toga.Button(
                'Ctrl+Shift+Z',
                on_press=self.fourth_button,
                style=Pack(
                    background_color="BLACK"
                )
            )
        )

        self.canvas = toga.Button(
            '',
            style=Pack(
                width=625,
                height=415,
                padding=5,
                padding_left=0,
                background_color="BLACK"
            )
        )
        main_box.add(self.canvas)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


    def first_button(self, button):
        print(button)


    def second_button(self, button):
        print(button)


    def third_button(self, button):
        print(button)


    def fourth_button(self, button):
        print(button)


def main():
    return teenmoons()
