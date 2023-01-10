import PySimpleGUI as sg
import logging


def get_scaling():
    # called before window created
    root = sg.tk.Tk()
    scaling = root.winfo_fpixels('1i')/72
    root.destroy()
    return scaling


def display_gui(list_of_projects):
    # Find the number in original screen when GUI designed.
    my_scaling = 1.334646962233169      # call get_scaling()
    my_width, my_height = 1536, 864     # call sg.Window.get_screen_size()

    # Get the number for new screen
    scaling_old = get_scaling()
    width, height = sg.Window.get_screen_size()

    scaling = scaling_old * min(width / my_width, height / my_height)

    sg.set_options(scaling=scaling)

    layout = [[sg.Text('Please select the name of the Classify project you would like to work on:')],
              [sg.Combo(list_of_projects)],
              [sg.Submit(), sg.Cancel()],
              [sg.Text('Please ensure your device is connected to the internet and the same time zone as your AWS server.')]]

    window = sg.Window('Classify', layout)

    event, values = window.read()
    window.close()
    if event == "Cancel":
        return None
    else:
        return values[0]
