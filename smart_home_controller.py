import flet as ft
import datetime
import asyncio

def main(page: ft.Page):
    page.title = ""
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'start'
    # page.window.width = 800
    # page.window.height = 600
    # page.window.resizable = False
    main_page_instance = main_page(page)
    energy_instance = energy(page, main_page_instance)
    page.main_page_instance = main_page_instance

    def toggle_theme(self):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.page.bgcolor = ft.Colors.BLACK
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.page.bgcolor = ft.Colors.WHITE
        self.page.update()

    def to_energy(e):
        energy.is_updating = True
        e.page.clean()
        e.page.add(energy_instance.build())
        e.page.update()

    def to_main(e):
        energy.is_updating = False
        e.page.clean()
        e.page.add(main_page_instance.build())
        e.page.update()
    
    page.appbar = ft.AppBar(
        title=ft.Text("Smart Home Controller"),
        actions=[
            ft.CupertinoButton(
            content=ft.Text("Theme", color=ft.Colors.BLUE),
            bgcolor=ft.Colors.TRANSPARENT,
            alignment=ft.alignment.top_left,
            border_radius=ft.border_radius.all(10),
            opacity_on_click=0.5,
            on_click=lambda e: toggle_theme(e),
            ),
            ft.CupertinoButton(
            content=ft.Text("Overview", color=ft.Colors.BLUE),
            bgcolor=ft.Colors.TRANSPARENT,
            alignment=ft.alignment.top_left,
            border_radius=ft.border_radius.all(10),
            opacity_on_click=0.5,
            on_click=lambda e: to_main(e),
            ),
            ft.CupertinoButton(
            content=ft.Text("Statistics", color=ft.Colors.BLUE),
            bgcolor=ft.Colors.TRANSPARENT,
            alignment=ft.alignment.top_left,
            border_radius=ft.border_radius.all(10),
            opacity_on_click=0.5,
            on_click=lambda e: to_energy(e),
            ),
        ]
    )
    page.add(main_page_instance.build())

class device:
    def __init__(self, name, id, type, state):
        self.name = name
        self.id = id
        self.type = type
        self.state = state
        self.actions = []
        self.state_text = ft.Text(str(self.state))
    
    def view_details(self, e):
        if hasattr(e.page, 'main_page_instance'):
            main_instance = e.page.main_page_instance
        else:      
            main_instance = main_page(e.page)

    def view_details(self, e):
        detail_page = details(e.page, self.name, self.id, self.type, self.state_text, self.actions, e.page.main_page_instance)
        e.page.clean()
        e.page.add(detail_page.build())
        e.page.update()


class switch_device(device):
    def __init__(self, name, id, type, state, on_type, off_type):
        super().__init__(name, id, type, state)
        self.on_type = on_type
        self.off_type = off_type
        self.state_text.value = self.on_type if state else self.off_type

    def change_state(self, e):
        self.state = not self.state
        self.state_text.value = self.on_type if self.state else self.off_type
        main_page.total_actions.append(f"{str.capitalize(self.name)} changed to {self.state_text.value} at {datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")}")
        self.actions.append(f"{str.capitalize(self.state_text.value)} at {datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")}")
        

        e.page.update()

    
    def build(self, description, action):
        return ft.Container(
            ft.Column([
                ft.Text(f"{self.name}", size=24, weight=ft.FontWeight.BOLD),
                self.state_text,
                ft.Text(description),
                ft.Row([
                    ft.ElevatedButton("View Details", on_click=self.view_details),
                    ft.ElevatedButton(action, on_click = self.change_state)
                ])
            ]),
            padding=20,
        )

class sliding_device(device):
    def __init__(self, name, id, type, state, min, max):
        super().__init__(name, id, type, state)
        self.min = min
        self.max = max

    def change_state(self, e):
        self.state = int(e.control.value)
        self.state_text.value = str(self.state)
        main_page.total_actions.append(f"{str.capitalize(self.name)} changed to {self.state_text.value} at {datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")}")
        self.actions.append(f"{str.capitalize(self.state_text.value)} at {datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")}") 
        e.page.update()

    def build(self, description):
        # self.state_text = ft.Text(str(self.state))

        return ft.Container(
            ft.Column([
                ft.Text(f"{self.name}", size=20, weight=ft.FontWeight.BOLD),
                self.state_text,
                ft.Text(description),
                ft.Row([
                    ft.ElevatedButton("View Details", on_click=self.view_details),
                    ft.Slider(min=self.min, max=self.max, value=self.state, on_change=self.change_state)
                ])
            ]),
            padding=20,
        )
    
class main_page():
    def __init__(self, page):
        self.page = page
    

    thermostat = sliding_device("Living Room Thermostat", "TH12345", "Thermostat", 20, 15, 30)
    light = switch_device("Light", "LT67890", "Light", False, "On", "Off")
    door = switch_device("Front Door Lock", "DL54321", "Door Lock", True, "Locked", "Unlocked")
    fan = sliding_device("Ceiling Fan", "CF98765", "Fan", 3, 0, 5)
    total_actions = []
    
    

    def build(self):
        return ft.Container(
            ft.Column([
                ft.Text("Switch Devices", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([self.light.build("Control the light in your home", "Toggle Light"),
                        self.door.build("Lock or unlock your front door", "Toggle Lock")]),
                ft.Text("Slider-Controlled Devices", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([self.thermostat.build("Thermostat control"), self.fan.build("Fan speed control")])
            ]),
            padding=20,
        )

    def view_details(self, e):
        details_page = details(
            self.page
        )
        self.page.clean()
        self.page.add(details_page.build())
        self.page.update()



class energy():
    def __init__(self, page, main_page_instance=None):
        self.page = page
        self.power_history = []  
        self.time_counter = 0
        self.main_page_instance = main_page_instance if main_page_instance else main_page(page)
    
    is_updating = False

    def compute_power(self):
        total = 0
        if self.main_page_instance.light.state: 
            total += 40
        total += self.main_page_instance.fan.state * 20 
        if self.main_page_instance.thermostat.state > 20: 
            total += 100 * (self.main_page_instance.thermostat.state - 20)
        return total

    def update_power_data(self):
        power = self.compute_power()
        self.power_history.append((self.time_counter, power))
        self.time_counter += 1
        if len(self.power_history) > 20:
            self.power_history.pop(0)
            
    async def auto_update_chart(self):
        while self.is_updating:
            self.update_power_data()
            if hasattr(self, 'chart') and self.chart.data_series:
                self.chart.data_series[0].data_points = [
                    ft.LineChartDataPoint(t, p) for t, p in self.power_history
                ]
                if self.power_history:
                    max_power = max([p for t, p in self.power_history])
                    self.chart.max_y = max_power + 50
                self.chart.update()
            await asyncio.sleep(2)


    def build(self):
        if not self.power_history:
            for _i in range(100):
                self.update_power_data()
    

        data_points = [
            ft.LineChartDataPoint(t, p) for t, p in self.power_history
        ]
    
        chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=data_points,
                    stroke_width=3,
                    color=ft.Colors.BLUE,
                    curved=True,
                )
            ],
            border=ft.border.all(2, ft.Colors.GREY_400),
            expand=True,
            min_y=0,
            max_y=max([p for t, p in self.power_history]) + 50 if self.power_history else 100,
        )
    
        self.chart = chart
    
        self.page.run_task(self.auto_update_chart)
    
        actions = self.main_page_instance.total_actions if self.main_page_instance.total_actions else ["No recent actions"]
        
        return ft.Container(
            ft.Column([
                ft.Text("Energy Consumption Analytics", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(chart, height=200),
                ft.Text("Recent Actions", size=15, weight=ft.FontWeight.BOLD),
                ft.Container(ft.ListView(ft.Text(action) for action in actions), height=400)
            ]),
            padding=20,     
        )
    
class details():
    def __init__(self, page, name, id, type, state_text, actions = ["No recent actions"], main_page_instance=None):
        self.page = page
        self.name = name
        self.id = id
        self.type = type
        self.state_text = state_text
        self.actions = actions
        self.main_page_instance = main_page_instance if main_page_instance else main_page(page)
    
    def return_to_main(self, e):
        e.page.clean()
        e.page.add(self.main_page_instance.build())
        e.page.update()


    def build(self):
        return ft.Container(
            ft.Column([
                ft.Column([
                    ft.Text(f"{self.name} details", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Device ID: {self.id}"),
                    ft.Text(f"Device Type: {self.type}"),
                    ft.Text(f"Device State: {self.state_text.value}"),
                ],horizontal_alignment=ft.CrossAxisAlignment.START),
                ft.Column([
                    ft.Text("Recent actions", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(ft.ListView(ft.Text(action) for action in self.actions), height=200)
                ],horizontal_alignment=ft.CrossAxisAlignment.START),
                ft.ElevatedButton("Back to Main Page", on_click = self.return_to_main)

            ]),
            padding=20,     
        )
    
# if __name__ == "__main__":
#     ft.app(target = main)
ft.app(main)