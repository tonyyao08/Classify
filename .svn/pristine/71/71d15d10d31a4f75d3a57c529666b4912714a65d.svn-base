import PySimpleGUI as sg

def get_scaling():
    # called before window created
    root = sg.tk.Tk()
    scaling = root.winfo_fpixels('1i')/72
    root.destroy()
    return scaling

# Find the number in original screen when GUI designed.
my_scaling = 1.334646962233169      # call get_scaling()
my_width, my_height = 1536, 864     # call sg.Window.get_screen_size()

# Get the number for new screen
scaling_old = get_scaling()
width, height = sg.Window.get_screen_size()

scaling = scaling_old * min(width / my_width, height / my_height)

sg.set_options(scaling=scaling)

layout = [[sg.Text('Please enter the name of the Classify project you would like to work on:')],
              [sg.InputText()],
              [sg.Submit(), sg.Cancel()],
              [sg.Combo(['choice 1', 'choice 2'])],
              [sg.Text('Please ensure your device is connected to the internet and the same time zone as your AWS server.')]]

window = sg.Window('Classify', layout)

event, values = window.read()

if event == "Cancel":
    window.close()
else:
    text_input = values[0]
    sg.popup('You entered', text_input)

#if text_input is not None and text_input != "" or cancelled != True:
    # REST OF DRIVER SCRIPT HERE
