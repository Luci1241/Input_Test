import pygame
import sys

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Live Peripheral Input")

# Set up font for displaying text
font = pygame.font.SysFont("Arial", 30)

# Initialize all joysticks (covers HOTAS, wheels, pedals, etc.)
pygame.joystick.init()
joysticks = []
joystick_names = {}

def simplify_device_name(name):
    lowered = name.lower()
    if "flight" in lowered:
        return "Flight Stick"
    elif "wheel" in lowered:
        return "Wheel"
    elif "pedal" in lowered:
        return "Pedals"
    elif "gamepad" in lowered:
        return "Gamepad"
    else:
        return name

for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)
    simple_name = simplify_device_name(joystick.get_name())
    joystick_names[i] = simple_name
    print("Initialized:", simple_name)

# Dictionary to keep track of currently active inputs
active_inputs = {}

def draw_active_inputs():
    """Clear the screen and draw the currently active inputs."""
    screen.fill((0, 0, 0))  # clear screen with black
    y_offset = 50
    for key, message in active_inputs.items():
        text_surface = font.render(message, True, (255, 255, 255))
        screen.blit(text_surface, (50, y_offset))
        y_offset += 40
    pygame.display.flip()

while True:
    event_occurred = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ----- Keyboard Events -----
        if event.type == pygame.KEYDOWN:
            active_inputs[f"key_{event.key}"] = f"Key Down: {pygame.key.name(event.key)}"
            event_occurred = True
        elif event.type == pygame.KEYUP:
            active_inputs.pop(f"key_{event.key}", None)
            event_occurred = True

        # ----- Mouse Events -----
        if event.type == pygame.MOUSEBUTTONDOWN:
            active_inputs[f"mouse_{event.button}"] = f"Mouse Button Down: {event.button}"
            event_occurred = True
        elif event.type == pygame.MOUSEBUTTONUP:
            active_inputs.pop(f"mouse_{event.button}", None)
            event_occurred = True

        # ----- Joystick Button Events -----
        if event.type == pygame.JOYBUTTONDOWN:
            device_name = joystick_names.get(event.joy, f"Joystick {event.joy}")
            active_inputs[f"joy_button_{event.joy}_{event.button}"] = f"{device_name} Button Down: {event.button}"
            event_occurred = True
        elif event.type == pygame.JOYBUTTONUP:
            active_inputs.pop(f"joy_button_{event.joy}_{event.button}", None)
            event_occurred = True

        # ----- Joystick Axis Motion -----
        if event.type == pygame.JOYAXISMOTION:
            device_name = joystick_names.get(event.joy, f"Joystick {event.joy}")
            if abs(event.value) > 0.1:
                active_inputs[f"joy_axis_{event.joy}_{event.axis}"] = f"{device_name} Axis {event.axis}: {event.value:.2f}"
            else:
                active_inputs.pop(f"joy_axis_{event.joy}_{event.axis}", None)
            event_occurred = True

        # ----- Joystick Hat Motion -----
        if event.type == pygame.JOYHATMOTION:
            device_name = joystick_names.get(event.joy, f"Joystick {event.joy}")
            if event.value != (0, 0):
                active_inputs[f"joy_hat_{event.joy}_{event.hat}"] = f"{device_name} Hat {event.hat}: {event.value}"
            else:
                active_inputs.pop(f"joy_hat_{event.joy}_{event.hat}", None)
            event_occurred = True

    # Redraw only if any input event occurred
    if event_occurred:
        draw_active_inputs()

    # Limit loop speed to reduce CPU usage
    pygame.time.delay(50)
