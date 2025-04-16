import base64
import curses
import logging
import os
import re
import sys

from contact.utilities.save_to_radio import save_changes
from contact.utilities.config_io import config_export, config_import
from contact.utilities.input_handlers import get_repeated_input, get_text_input, get_fixed32_input, get_list_input, get_admin_key_input
from contact.ui.menus import generate_menu_from_protobuf
from contact.ui.colors import get_color
from contact.ui.dialog import dialog
from contact.utilities.control_utils import parse_ini_file, transform_menu_path
from contact.ui.user_config import json_editor
from contact.ui.ui_state import MenuState

menu_state = MenuState()

# Constants
width = 80
save_option = "Save Changes"
max_help_lines = 0
help_win = None
sensitive_settings = ["Reboot", "Reset Node DB", "Shutdown", "Factory Reset"]

# Get the parent directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

# Paths
locals_dir = os.path.dirname(os.path.abspath(sys.argv[0]))  # Current script directory
translation_file = os.path.join(parent_dir, "localisations", "en.ini")

config_folder = os.path.join(locals_dir, "node-configs")

# Load translations
field_mapping, help_text = parse_ini_file(translation_file)

# Aliases
Segment = tuple[str, str, bool, bool]
WrappedLine = list[Segment]

def display_menu(menu_state: MenuState) -> tuple[object, object]:  # curses.window or pad types

    min_help_window_height = 6
    num_items = len(menu_state.current_menu) + (1 if menu_state.show_save_option else 0)

    # Determine the available height for the menu
    max_menu_height = curses.LINES 
    menu_height = min(max_menu_height - min_help_window_height, num_items + 5)  
    start_y = (curses.LINES - menu_height) // 2 - (min_help_window_height // 2)
    start_x = (curses.COLS - width) // 2

    # Calculate remaining space for help window
    global max_help_lines
    remaining_space = curses.LINES - (start_y + menu_height + 2)  # +2 for padding
    max_help_lines = max(remaining_space, 1)  # Ensure at least 1 lines for help

    menu_win = curses.newwin(menu_height, width, start_y, start_x)
    menu_win.erase()
    menu_win.bkgd(get_color("background"))
    menu_win.attrset(get_color("window_frame"))
    menu_win.border()
    menu_win.keypad(True)

    menu_pad = curses.newpad(len(menu_state.current_menu) + 1, width - 8)
    menu_pad.bkgd(get_color("background"))

    header = " > ".join(word.title() for word in menu_state.menu_path)
    if len(header) > width - 4:
        header = header[:width - 7] + "..."
    menu_win.addstr(1, 2, header, get_color("settings_breadcrumbs", bold=True))

    transformed_path = transform_menu_path(menu_state.menu_path)

    for idx, option in enumerate(menu_state.current_menu):
        field_info = menu_state.current_menu[option]
        current_value = field_info[1] if isinstance(field_info, tuple) else ""
        full_key = '.'.join(transformed_path + [option])
        display_name = field_mapping.get(full_key, option)

        display_option = f"{display_name}"[:width // 2 - 2]
        display_value = f"{current_value}"[:width // 2 - 4]

        try:
            color = get_color("settings_sensitive" if option in sensitive_settings else "settings_default", reverse=(idx == menu_state.selected_index))
            menu_pad.addstr(idx, 0, f"{display_option:<{width // 2 - 2}} {display_value}".ljust(width - 8), color)
        except curses.error:
            pass

    if menu_state.show_save_option:
        save_position = menu_height - 2
        menu_win.addstr(save_position, (width - len(save_option)) // 2, save_option, get_color("settings_save", reverse=(menu_state.selected_index == len(menu_state.current_menu))))

    # Draw help window with dynamically updated max_help_lines
    draw_help_window(start_y, start_x, menu_height, max_help_lines, transformed_path, menu_state)

    menu_win.refresh()
    menu_pad.refresh(
        menu_state.start_index[-1], 0,
        menu_win.getbegyx()[0] + 3, menu_win.getbegyx()[1] + 4,
        menu_win.getbegyx()[0] + 3 + menu_win.getmaxyx()[0] - 5 - (2 if menu_state.show_save_option else 0),
        menu_win.getbegyx()[1] + menu_win.getmaxyx()[1] - 4
    )

    max_index = num_items + (1 if menu_state.show_save_option else 0) - 1
    visible_height = menu_win.getmaxyx()[0] - 5 - (2 if menu_state.show_save_option else 0)

    draw_arrows(menu_win, visible_height, max_index, menu_state)

    return menu_win, menu_pad


def draw_help_window(
    menu_start_y: int,
    menu_start_x: int,
    menu_height: int,
    max_help_lines: int,
    transformed_path: list[str],
    menu_state: MenuState
) -> None:

    global help_win

    if 'help_win' not in globals():
        help_win = None  # Initialize if it does not exist

    selected_option = list(menu_state.current_menu.keys())[menu_state.selected_index] if menu_state.current_menu else None
    help_y = menu_start_y + menu_height

    help_win = update_help_window(help_win, help_text, transformed_path, selected_option, max_help_lines, width, help_y, menu_start_x)

def update_help_window(
    help_win: object,  # curses window or None
    help_text: dict[str, str],
    transformed_path: list[str],
    selected_option: str | None,
    max_help_lines: int,
    width: int,
    help_y: int,
    help_x: int
) -> object:  # returns a curses window

    """Handles rendering the help window consistently."""
    wrapped_help = get_wrapped_help_text(help_text, transformed_path, selected_option, width, max_help_lines)

    help_height = min(len(wrapped_help) + 2, max_help_lines + 2)  # +2 for border
    help_height = max(help_height, 3)  # Ensure at least 3 rows (1 text + border)

    # Ensure help window does not exceed screen size
    if help_y + help_height > curses.LINES:
        help_y = curses.LINES - help_height

    # Create or update the help window
    if help_win is None:
        help_win = curses.newwin(help_height, width, help_y, help_x)
    else:
        help_win.erase()
        help_win.refresh()
        help_win.resize(help_height, width)
        help_win.mvwin(help_y, help_x)

    help_win.bkgd(get_color("background"))
    help_win.attrset(get_color("window_frame"))
    help_win.border()

    for idx, line_segments in enumerate(wrapped_help):
        x_pos = 2  # Start after border
        for text, color, bold, underline in line_segments:
            try:
                attr = get_color(color, bold=bold, underline=underline)
                help_win.addstr(1 + idx, x_pos, text, attr)
                x_pos += len(text)
            except curses.error:
                pass  # Prevent crashes

    help_win.refresh()
    return help_win


def get_wrapped_help_text(
    help_text: dict[str, str],
    transformed_path: list[str],
    selected_option: str | None,
    width: int,
    max_lines: int
) -> list[WrappedLine]:
    """Fetches and formats help text for display, ensuring it fits within the allowed lines."""
    
    full_help_key = '.'.join(transformed_path + [selected_option]) if selected_option else None
    help_content = help_text.get(full_help_key, "No help available.")

    wrap_width = max(width - 6, 10)  # Ensure a valid wrapping width

    # Color replacements
    color_mappings = {
        r'\[warning\](.*?)\[/warning\]': ('settings_warning', True, False),  # Red for warnings
        r'\[note\](.*?)\[/note\]': ('settings_note', True, False),  # Green for notes
        r'\[underline\](.*?)\[/underline\]': ('settings_default', False, True),  # Underline

        r'\\033\[31m(.*?)\\033\[0m': ('settings_warning', True, False),  # Red text
        r'\\033\[32m(.*?)\\033\[0m': ('settings_note', True, False),  # Green text
        r'\\033\[4m(.*?)\\033\[0m': ('settings_default', False, True)  # Underline
    }

    def extract_ansi_segments(text: str) -> list[Segment]:
        """Extracts and replaces ANSI color codes, ensuring spaces are preserved."""
        matches = []
        last_pos = 0
        pattern_matches = []

        # Find all matches and store their positions
        for pattern, (color, bold, underline) in color_mappings.items():
            for match in re.finditer(pattern, text):
                pattern_matches.append((match.start(), match.end(), match.group(1), color, bold, underline))

        # Sort matches by start position to process sequentially
        pattern_matches.sort(key=lambda x: x[0])

        for start, end, content, color, bold, underline in pattern_matches:
            # Preserve non-matching text including spaces
            if last_pos < start:
                segment = text[last_pos:start]
                matches.append((segment, "settings_default", False, False))
            
            # Append the colored segment
            matches.append((content, color, bold, underline))
            last_pos = end

        # Preserve any trailing text
        if last_pos < len(text):
            matches.append((text[last_pos:], "settings_default", False, False))

        return matches

    def wrap_ansi_text(segments: list[Segment], wrap_width: int) -> list[WrappedLine]:
        """Wraps text while preserving ANSI formatting and spaces."""
        wrapped_lines = []
        line_buffer = []
        line_length = 0

        for text, color, bold, underline in segments:
            words = re.findall(r'\S+|\s+', text)  # Capture words and spaces separately

            for word in words:
                word_length = len(word)

                if line_length + word_length > wrap_width and word.strip():
                    # If the word (ignoring spaces) exceeds width, wrap the line
                    wrapped_lines.append(line_buffer)
                    line_buffer = []
                    line_length = 0

                line_buffer.append((word, color, bold, underline))
                line_length += word_length

        if line_buffer:
            wrapped_lines.append(line_buffer)

        return wrapped_lines

    raw_lines = help_content.split("\\n")  # Preserve new lines
    wrapped_help = []

    for raw_line in raw_lines:
        color_segments = extract_ansi_segments(raw_line)
        wrapped_segments = wrap_ansi_text(color_segments, wrap_width)
        wrapped_help.extend(wrapped_segments)
        pass

    # Trim and add ellipsis if needed
    if len(wrapped_help) > max_lines:
        wrapped_help = wrapped_help[:max_lines]  
        wrapped_help[-1].append(("...", "settings_default", False, False))  

    return wrapped_help


def move_highlight(
    old_idx: int,
    options: list[str],
    menu_win: object,
    menu_pad: object,
    help_win: object,
    help_text: dict[str, str],
    max_help_lines: int,
    menu_state: MenuState
) -> None:
    
    if old_idx == menu_state.selected_index:  # No-op
        return

    max_index = len(options) + (1 if menu_state.show_save_option else 0) - 1
    visible_height = menu_win.getmaxyx()[0] - 5 - (2 if menu_state.show_save_option else 0)

    # Adjust menu_state.start_index only when moving out of visible range
    if menu_state.selected_index == max_index and menu_state.show_save_option:
        pass
    elif menu_state.selected_index < menu_state.start_index[-1]:  # Moving above the visible area
        menu_state.start_index[-1] = menu_state.selected_index
    elif menu_state.selected_index >= menu_state.start_index[-1] + visible_height:  # Moving below the visible area
        menu_state.start_index[-1] = menu_state.selected_index - visible_height
    pass

    # Ensure menu_state.start_index is within bounds
    menu_state.start_index[-1] = max(0, min(menu_state.start_index[-1], max_index - visible_height + 1))

    # Clear old selection
    if menu_state.show_save_option and old_idx == max_index:
        menu_win.chgat(menu_win.getmaxyx()[0] - 2, (width - len(save_option)) // 2, len(save_option), get_color("settings_save"))
    else:
        menu_pad.chgat(old_idx, 0, menu_pad.getmaxyx()[1], get_color("settings_sensitive") if options[old_idx] in sensitive_settings else get_color("settings_default"))

    # Highlight new selection
    if menu_state.show_save_option and menu_state.selected_index == max_index:
        menu_win.chgat(menu_win.getmaxyx()[0] - 2, (width - len(save_option)) // 2, len(save_option), get_color("settings_save", reverse=True))
    else:
        menu_pad.chgat(menu_state.selected_index, 0, menu_pad.getmaxyx()[1], get_color("settings_sensitive", reverse=True) if options[menu_state.selected_index] in sensitive_settings else get_color("settings_default", reverse=True))

    menu_win.refresh()
    
    # Refresh pad only if scrolling is needed
    menu_pad.refresh(menu_state.start_index[-1], 0,
                     menu_win.getbegyx()[0] + 3, menu_win.getbegyx()[1] + 4,
                     menu_win.getbegyx()[0] + 3 + visible_height, 
                     menu_win.getbegyx()[1] + menu_win.getmaxyx()[1] - 4)

    # Update help window
    transformed_path = transform_menu_path(menu_state.menu_path)
    selected_option = options[menu_state.selected_index] if menu_state.selected_index < len(options) else None
    help_y = menu_win.getbegyx()[0] + menu_win.getmaxyx()[0]
    help_win = update_help_window(help_win, help_text, transformed_path, selected_option, max_help_lines, width, help_y, menu_win.getbegyx()[1])

    draw_arrows(menu_win, visible_height, max_index, menu_state)


def draw_arrows(
    win: object,
    visible_height: int,
    max_index: int,
    menu_state: MenuState
) -> None:

    # vh = visible_height + (1 if show_save_option else 0)
    mi = max_index - (2 if menu_state.show_save_option else 0) 

    if visible_height < mi:
        if menu_state.start_index[-1] > 0:
            win.addstr(3, 2, "▲", get_color("settings_default"))
        else:
            win.addstr(3, 2, " ", get_color("settings_default"))

        if mi - menu_state.start_index[-1] >= visible_height + (0 if menu_state.show_save_option else 1) :
            win.addstr(visible_height + 3, 2, "▼", get_color("settings_default"))
        else:
            win.addstr(visible_height + 3, 2, " ", get_color("settings_default"))
        

def settings_menu(stdscr: object, interface: object) -> None:
    curses.update_lines_cols()

    menu = generate_menu_from_protobuf(interface)
    menu_state.current_menu = menu["Main Menu"]
    menu_state.menu_path = ["Main Menu"]


    modified_settings = {}
    
    need_redraw = True
    menu_state.show_save_option = False

    while True:
        if(need_redraw):
            options = list(menu_state.current_menu.keys())

            menu_state.show_save_option = (
                len(menu_state.menu_path) > 2 and ("Radio Settings" in menu_state.menu_path or "Module Settings" in menu_state.menu_path)
            ) or (
                len(menu_state.menu_path) == 2 and "User Settings" in menu_state.menu_path 
            ) or (
                len(menu_state.menu_path) == 3 and "Channels" in menu_state.menu_path
            )

            # Display the menu
            menu_win, menu_pad = display_menu(menu_state)

            need_redraw = False

        # Capture user input
        key = menu_win.getch()

        max_index = len(options) + (1 if menu_state.show_save_option else 0) - 1
        # max_help_lines = 4

        if key == curses.KEY_UP:
            old_selected_index = menu_state.selected_index
            menu_state.selected_index = max_index if menu_state.selected_index == 0 else menu_state.selected_index - 1
            move_highlight(old_selected_index, options, menu_win, menu_pad, help_win, help_text, max_help_lines, menu_state)
            
        elif key == curses.KEY_DOWN:
            old_selected_index = menu_state.selected_index
            menu_state.selected_index = 0 if menu_state.selected_index == max_index else menu_state.selected_index + 1
            move_highlight(old_selected_index, options, menu_win, menu_pad, help_win, help_text, max_help_lines, menu_state)

        elif key == curses.KEY_RESIZE:
            need_redraw = True
            curses.update_lines_cols()

            menu_win.erase()
            help_win.erase()

            menu_win.refresh()
            help_win.refresh()

        elif key == ord("\t") and menu_state.show_save_option:
            old_selected_index = menu_state.selected_index
            menu_state.selected_index = max_index
            move_highlight(old_selected_index, options, menu_win, menu_pad, help_win, help_text, max_help_lines, menu_state)

        elif key == curses.KEY_RIGHT or key == ord('\n'):
            need_redraw = True
            menu_state.start_index.append(0)
            menu_win.erase()
            help_win.erase()

            # draw_help_window(menu_win.getbegyx()[0], menu_win.getbegyx()[1], menu_win.getmaxyx()[0], max_help_lines, menu_state.current_menu, selected_index, transform_menu_path(menu_state.menu_path))

            menu_win.refresh()
            help_win.refresh()

            if menu_state.show_save_option and menu_state.selected_index == len(options):
                save_changes(interface, modified_settings, menu_state)
                modified_settings.clear()
                logging.info("Changes Saved")

                if len(menu_state.menu_path) > 1:
                    menu_state.menu_path.pop()
                    menu_state.current_menu = menu["Main Menu"]
                    for step in menu_state.menu_path[1:]:
                        menu_state.current_menu = menu_state.current_menu.get(step, {})
                    menu_state.selected_index = 0
                continue

            selected_option = options[menu_state.selected_index]

            if selected_option == "Exit":
                break

            elif selected_option == "Export Config File":
                filename = get_text_input("Enter a filename for the config file")
                if not filename:
                    logging.info("Export aborted: No filename provided.")
                    menu_state.start_index.pop()
                    continue  # Go back to the menu
                if not filename.lower().endswith(".yaml"):
                    filename += ".yaml"

                try:
                    config_text = config_export(interface)
                    yaml_file_path = os.path.join(config_folder, filename)

                    if os.path.exists(yaml_file_path):
                        overwrite = get_list_input(f"{filename} already exists. Overwrite?", None, ["Yes", "No"])
                        if overwrite == "No":
                            logging.info("Export cancelled: User chose not to overwrite.")
                            menu_state.start_index.pop()
                            continue  # Return to menu
                    os.makedirs(os.path.dirname(yaml_file_path), exist_ok=True)
                    with open(yaml_file_path, "w", encoding="utf-8") as file:
                        file.write(config_text)
                    logging.info(f"Config file saved to {yaml_file_path}")
                    dialog(stdscr, "Config File Saved:", yaml_file_path)
                    menu_state.start_index.pop()
                    continue
                except PermissionError:
                    logging.error(f"Permission denied: Unable to write to {yaml_file_path}")
                except OSError as e:
                    logging.error(f"OS error while saving config: {e}")
                except Exception as e:
                    logging.error(f"Unexpected error: {e}")
                menu_state.start_index.pop()
                continue
                
            elif selected_option == "Load Config File":

                # Check if folder exists and is not empty
                if not os.path.exists(config_folder) or not any(os.listdir(config_folder)):
                    dialog(stdscr, "", " No config files found. Export a config first.")
                    continue  # Return to menu

                file_list = [f for f in os.listdir(config_folder) if os.path.isfile(os.path.join(config_folder, f))]

                # Ensure file_list is not empty before proceeding
                if not file_list:
                    dialog(stdscr, "", " No config files found. Export a config first.")
                    continue

                filename = get_list_input("Choose a config file", None, file_list)
                if filename:
                    file_path = os.path.join(config_folder, filename)
                    overwrite = get_list_input(f"Are you sure you want to load {filename}?", None, ["Yes", "No"])
                    if overwrite == "Yes":
                        config_import(interface, file_path)
                menu_state.start_index.pop()
                continue

            elif selected_option == "Config URL":
                current_value = interface.localNode.getURL()
                new_value = get_text_input(f"Config URL is currently: {current_value}")
                if new_value is not None:
                    current_value = new_value
                    overwrite = get_list_input(f"Are you sure you want to load this config?", None, ["Yes", "No"])
                    if overwrite == "Yes":
                        interface.localNode.setURL(new_value)
                        logging.info(f"New Config URL sent to node")
                menu_state.start_index.pop()
                continue

            elif selected_option == "Reboot":
                confirmation = get_list_input("Are you sure you want to Reboot?", None,  ["Yes", "No"])
                if confirmation == "Yes":
                    interface.localNode.reboot()
                    logging.info(f"Node Reboot Requested by menu")
                menu_state.start_index.pop()
                continue

            elif selected_option == "Reset Node DB":
                confirmation = get_list_input("Are you sure you want to Reset Node DB?", None,  ["Yes", "No"])
                if confirmation == "Yes":
                    interface.localNode.resetNodeDb()
                    logging.info(f"Node DB Reset Requested by menu")
                menu_state.start_index.pop()
                continue

            elif selected_option == "Shutdown":
                confirmation = get_list_input("Are you sure you want to Shutdown?", None, ["Yes", "No"])
                if confirmation == "Yes":
                    interface.localNode.shutdown()
                    logging.info(f"Node Shutdown Requested by menu")
                menu_state.start_index.pop()
                continue

            elif selected_option == "Factory Reset":
                confirmation = get_list_input("Are you sure you want to Factory Reset?", None,  ["Yes", "No"])
                if confirmation == "Yes":
                    interface.localNode.factoryReset()
                    logging.info(f"Factory Reset Requested by menu")
                menu_state.start_index.pop()
                continue

            elif selected_option == "App Settings":
                menu_win.clear()
                menu_win.refresh()
                menu_state.menu_path.append("App Settings")
                menu_state.menu_index.append(menu_state.selected_index)
                json_editor(stdscr, menu_state)  # Open the App Settings menu
                menu_state.current_menu = menu["Main Menu"]
                menu_state.menu_path = ["Main Menu"]
                menu_state.start_index.pop()
                menu_state.selected_index = 4
                continue
                # need_redraw = True
                
            field_info = menu_state.current_menu.get(selected_option)
            if isinstance(field_info, tuple):
                field, current_value = field_info

                # Transform the menu path to get the full key
                transformed_path = transform_menu_path(menu_state.menu_path)
                full_key = '.'.join(transformed_path + [selected_option])

                # Fetch human-readable name from field_mapping
                human_readable_name = field_mapping.get(full_key, selected_option)

                if selected_option in ['longName', 'shortName', 'isLicensed']:
                    if selected_option in ['longName', 'shortName']:
                        new_value = get_text_input(f"{human_readable_name} is currently: {current_value}")
                        new_value = current_value if new_value is None else new_value
                        menu_state.current_menu[selected_option] = (field, new_value)

                    elif selected_option == 'isLicensed':
                        new_value = get_list_input(f"{human_readable_name} is currently: {current_value}", str(current_value),  ["True", "False"])
                        new_value = new_value == "True"
                        menu_state.current_menu[selected_option] = (field, new_value)

                    for option, (field, value) in menu_state.current_menu.items():
                        modified_settings[option] = value

                    menu_state.start_index.pop()

                elif selected_option in ['latitude', 'longitude', 'altitude']:
                    new_value = get_text_input(f"{human_readable_name} is currently: {current_value}")
                    new_value = current_value if new_value is None else new_value
                    menu_state.current_menu[selected_option] = (field, new_value)

                    for option in ['latitude', 'longitude', 'altitude']:
                        if option in menu_state.current_menu:
                            modified_settings[option] = menu_state.current_menu[option][1]

                    menu_state.start_index.pop()

                elif selected_option == "admin_key":
                    new_values = get_admin_key_input(current_value)
                    new_value = current_value if new_values is None else [base64.b64decode(key) for key in new_values]
                    menu_state.start_index.pop()

                elif field.type == 8:  # Handle boolean type
                    new_value = get_list_input(human_readable_name, str(current_value), ["True", "False"])
                    if new_value == "Not Set":
                        pass  # Leave it as-is
                    else:
                        new_value = new_value == "True" or new_value is True
                    menu_state.start_index.pop()

                elif field.label == field.LABEL_REPEATED:  # Handle repeated field - Not currently used
                    new_value = get_repeated_input(current_value)
                    new_value = current_value if new_value is None else new_value.split(", ")
                    menu_state.start_index.pop()

                elif field.enum_type:  # Enum field
                    enum_options = {v.name: v.number for v in field.enum_type.values}
                    new_value_name = get_list_input(human_readable_name, current_value, list(enum_options.keys()))
                    new_value = enum_options.get(new_value_name, current_value)
                    menu_state.start_index.pop()

                elif field.type == 7: # Field type 7 corresponds to FIXED32
                    new_value = get_fixed32_input(current_value)
                    menu_state.start_index.pop()

                elif field.type == 13: # Field type 13 corresponds to UINT32
                    new_value = get_text_input(f"{human_readable_name} is currently: {current_value}")
                    new_value = current_value if new_value is None else int(new_value)
                    menu_state.start_index.pop()

                elif field.type == 2: # Field type 13 corresponds to INT64
                    new_value = get_text_input(f"{human_readable_name} is currently: {current_value}")
                    new_value = current_value if new_value is None else float(new_value)
                    menu_state.start_index.pop()

                else:  # Handle other field types
                    new_value = get_text_input(f"{human_readable_name} is currently: {current_value}")
                    new_value = current_value if new_value is None else new_value
                    menu_state.start_index.pop()
                
                for key in menu_state.menu_path[3:]:  # Skip "Main Menu"
                    modified_settings = modified_settings.setdefault(key, {})

                # Add the new value to the appropriate level
                modified_settings[selected_option] = new_value

                # Convert enum string to int
                if field and field.enum_type:
                    enum_value_descriptor = field.enum_type.values_by_number.get(new_value)
                    new_value = enum_value_descriptor.name if enum_value_descriptor else new_value

                menu_state.current_menu[selected_option] = (field, new_value)
            else:
                menu_state.current_menu = menu_state.current_menu[selected_option]
                menu_state.menu_path.append(selected_option)
                menu_state.menu_index.append(menu_state.selected_index)
                menu_state.selected_index = 0


        elif key == curses.KEY_LEFT:
            need_redraw = True

            menu_win.erase()
            help_win.erase()

            # max_help_lines = 4
            # draw_help_window(menu_win.getbegyx()[0], menu_win.getbegyx()[1], menu_win.getmaxyx()[0], max_help_lines, menu_state.current_menu, selected_index, transform_menu_path(menu_state.menu_path))

            menu_win.refresh()
            help_win.refresh()

            if len(menu_state.menu_path) < 2:
                modified_settings.clear()

            # Navigate back to the previous menu
            if len(menu_state.menu_path) > 1:
                menu_state.menu_path.pop()
                menu_state.current_menu = menu["Main Menu"]
                for step in menu_state.menu_path[1:]:
                    menu_state.current_menu = menu_state.current_menu.get(step, {})
                menu_state.selected_index = menu_state.menu_index.pop()
                menu_state.start_index.pop()
                
        elif key == 27:  # Escape key
            menu_win.erase()
            menu_win.refresh()
            break

def set_region(interface: object) -> None:
    node = interface.getNode('^local')
    device_config = node.localConfig
    lora_descriptor = device_config.lora.DESCRIPTOR

    # Get the enum mapping of region names to their numerical values
    region_enum = lora_descriptor.fields_by_name["region"].enum_type
    region_name_to_number = {v.name: v.number for v in region_enum.values}

    regions = list(region_name_to_number.keys())

    new_region_name = get_list_input('Select your region:', 'UNSET', regions)

    # Convert region name to corresponding enum number
    new_region_number = region_name_to_number.get(new_region_name, 0)  # Default to 0 if not found

    node.localConfig.lora.region = new_region_number
    node.writeConfig("lora")