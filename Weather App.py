from tkinter import *
import tkinter as tk
import requests
from datetime import datetime

city = None


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Weathering With You")
        self.geometry("600x500")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.pages = {}

        for PageClass in (Page1, Page2, Page3):
            page_name = PageClass.__name__
            page = PageClass(parent=self.container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("Page1")

    def show_page(self, page_name):
        page = self.pages.get(page_name)
        if page:
            page.tkraise()


page_title_font = ("Calibri", 20)
content_font = ("Calibri", 15)


# Setting Page
class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.city_var = tk.StringVar()

        page1_title_label = tk.Label(self, text="Settings", font=page_title_font)
        page1_title_label.pack()

        divider_label1 = tk.Label(self, text="", font=content_font)
        divider_label1.pack()

        before_city_label = tk.Label(self, text="City:", font=content_font)
        before_city_label.pack()

        self.city_entry = tk.Entry(self, textvariable=self.city_var, font=content_font)
        self.city_entry.pack()

        set_city_button = tk.Button(self, text="Set City", command=self.set_city, font=content_font)
        set_city_button.pack()

        divider_label1 = tk.Label(self, text="\n\n\n\n\n", font=content_font)
        divider_label1.pack()

        app_name_header = tk.Label(self, text="Weathering With You", relief=RIDGE, width=21, height=2)
        app_name_header.pack()
        page1_button = tk.Button(self, text="Settings", command=lambda: controller.show_page("Page1"),
                                 width=20, height=2)
        page1_button.pack()
        page2_button = tk.Button(self, text="Today's Forecast", command=lambda: controller.show_page("Page2"),
                                 width=20, height=2)
        page2_button.pack()
        page3_button = tk.Button(self, text="5-Day Forecast", command=lambda: controller.show_page("Page3"),
                                 width=20, height=2)
        page3_button.pack()

    def set_city(self):
        global city
        city = self.city_entry.get()
        self.controller.pages["Page2"].update_todays_temperature_label()
        self.controller.pages["Page3"].update_temperature_5_day_label()


# Today's Forecast Page
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        page2_title_label = tk.Label(self, text="Today's Forecast", font=page_title_font)
        page2_title_label.pack()

        divider_label3 = tk.Label(self, text="", font=content_font)
        divider_label3.pack()

        global city
        self.todays_temperature_label = tk.Label(self,
                                                 text="It is RAINY, because you did not choose a city!!",
                                                 font=content_font)
        self.todays_temperature_label.pack()

        divider_label4 = tk.Label(self, text="\n\n\n\n\n\n\n\n", font=content_font)
        divider_label4.pack()

        app_name_header = tk.Label(self, text="Weathering With You", relief=RIDGE, width=21, height=2)
        app_name_header.pack()
        page1_button = tk.Button(self, text="Settings", command=lambda: controller.show_page("Page1"),
                                 width=20, height=2)
        page1_button.pack()
        page2_button = tk.Button(self, text="Today's Forecast", command=lambda: controller.show_page("Page2"),
                                 width=20, height=2)
        page2_button.pack()
        page3_button = tk.Button(self, text="5-Day Forecast", command=lambda: controller.show_page("Page3"),
                                 width=20, height=2)
        page3_button.pack()

    def update_todays_temperature_label(self):
        global city
        self.todays_temperature_label.config(text=str(get_weather("d442d64a7a51c161b5b585a28f3956c4", city)))


# 5-Day Forecast Page
class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        page2_title_label = tk.Label(self, text="5-Day Forecast", font=page_title_font)
        page2_title_label.pack()

        divider_label1 = tk.Label(self, text="", font=content_font)
        divider_label1.pack()

        global city
        self.temperature_5_day_label = tk.Label(self, text="It is RAINY on ALL 5 DAYS, "
                                                           "because you did not choose a city!!\n\n\n\n",
                                                font=content_font)
        self.temperature_5_day_label.pack()

        self.divider_label4 = tk.Label(self, text="\n\n\n\n", font=content_font)
        self.divider_label4.pack()

        app_name_header = tk.Label(self, text="Weathering With You", relief=RIDGE, width=21, height=2)
        app_name_header.pack()
        page1_button = tk.Button(self, text="Settings", command=lambda: controller.show_page("Page1"),
                                 width=20, height=2)
        page1_button.pack()
        page2_button = tk.Button(self, text="Today's Forecast", command=lambda: controller.show_page("Page2"),
                                 width=20, height=2)
        page2_button.pack()
        page3_button = tk.Button(self, text="5-Day Forecast", command=lambda: controller.show_page("Page3"),
                                 width=20, height=2)
        page3_button.pack()

    def update_temperature_5_day_label(self):
        global city
        self.temperature_5_day_label.config(text=str(get_5_day_weather("d442d64a7a51c161b5b585a28f3956c4", city)))
        self.divider_label4.config(text="\n\n\n")


def get_weather(api_key, city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}"

    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] == 200:
        main_data = data["main"]
        weather_data = data["weather"][0]

        temperature = main_data["temp"]
        weather_description = weather_data["description"]

        return f"The temperature in {city_name} is {temperature - 273.15:.2f}°C with {weather_description}."
    else:
        return "City not found or an error occurred."


def get_5_day_weather(api_key, city_name):
    geocoding_url = "https://api.openweathermap.org/data/2.5/weather"
    geocoding_params = {
        "q": city_name,
        "appid": api_key,
    }
    response = requests.get(geocoding_url, params=geocoding_params)
    geocoding_data = response.json()
    if geocoding_data["cod"] == 200:
        lat = geocoding_data["coord"]["lat"]
        lon = geocoding_data["coord"]["lon"]

        weekly_forecast_url = (f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}"
                               f"&cnt=5&appid={api_key}")

        weekly_response = requests.get(weekly_forecast_url)
        weekly_data = weekly_response.json()

        string_5_day_weather = ""
        for i in range(5):
            temperature = weekly_data["list"][i]["main"]["temp"]

            weather_description = weekly_data["list"][i]["weather"][0]["description"]

            input_datetime_str = weekly_data["list"][i]["dt_txt"]
            input_datetime = datetime.strptime(input_datetime_str, "%Y-%m-%d %H:%M:%S")
            date = input_datetime.strftime("%Y-%m-%d")

            string_5_day_weather += (f"Date: {date}: "
                                     f"Temperature: {temperature - 273.15:.2f}°C, "
                                     f"Weather: {weather_description}\n")
        return string_5_day_weather
    else:
        return "City not found or an error occurred."


if __name__ == "__main__":
    root = Window()
    root.mainloop()
