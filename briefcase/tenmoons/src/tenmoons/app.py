"""
Driver for Table 10Moons for Linux
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

import os
import multiprocessing
import driver


class TeenMoons(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

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

        html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
	<meta charset="utf-8">
	<title>
		Canvas & EcmaScript
	</title>
	<style type="text/css">
		* {
			margin: 0;
			padding: 0;
		}
		html,
		body,
		#screen {
			width: 100%;
			height: 100%;
			border-radius:10px;
			background-color: #373737;
		}
		canvas {
			background: lightgray;
			overflow-y: hidden;
			position: fixed;
		}
		#erase {
			position:absolute;
			color:red;
			right:10px;
			font-size:50pt;
			z-index: 999;
		}
	</style>
</head>
<body>
<div id="screen">
	<div id="erase">&#10008;</div>
	<canvas id="canvas"></canvas>
</div>
<script type="text/javascript">
	let isDrawing = false
	let x = 0
	let y = 0

	const canvas = document.getElementById("canvas")
	const context = canvas.getContext("2d")

	let screen = document.getElementById("screen")
	canvas.setAttribute("width", screen.offsetWidth)
	canvas.setAttribute("height", screen.offsetHeight)

	canvas.addEventListener("mousedown", event => {
		x = event.offsetX
		y = event.offsetY
		isDrawing = true
	})

	canvas.addEventListener("mousemove", event => {
		if (isDrawing === true) {
			drawLine(context, x, y, event.offsetX, event.offsetY)
			x = event.offsetX
			y = event.offsetY
		}
	})

	window.addEventListener("mouseup", event => {
		if (isDrawing === true) {
			drawLine(context, x, y, event.offsetX, event.offsetY)
			x = 0
			y = 0
			isDrawing = false
		}
	})

	function drawLine(context, x1, y1, x2, y2) {
		context.beginPath()
		context.strokeStyle = "black"
		context.lineWidth = 1
		context.moveTo(x1, y1)
		context.lineTo(x2, y2)
		context.stroke()
		context.closePath()
	}

	const erase = document.getElementById("erase")
	erase.addEventListener("mousedown", event => {
		context.clearRect(0, 0, canvas.width, canvas.height);
	})

	console.log("Easter egg!")
</script>
</body>
</html>
        """

        self.canvas = toga.WebView()
        self.canvas.set_content("", html)

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
    return TeenMoons()
