import dearpygui.dearpygui as dpg
import minescript
import os
import threading
import time

# Constants
WIDTH = 500
HEIGHT = 500
SCRIPTS_LOCATION = "scripts"
JOB_UPDATE_INTERVAL = 0.002  # seconds

# Global state
jobs = []
jobs_lock = threading.Lock()
running = True

# Get scripts directory
scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), SCRIPTS_LOCATION)

def get_script_files():
    """Get list of Python script files from the scripts directory."""
    return [f for f in os.listdir(scripts_dir) if os.path.isfile(os.path.join(scripts_dir, f)) and f.endswith('.py')]

files = get_script_files()
checkbox_tags = []  # Store tags for checkboxes so we can delete them


def update_jobs_background():
    """Background thread to continuously update job information."""
    global jobs, running
    while running:
        try:
            current_jobs = minescript.job_info()
            with jobs_lock:
                jobs = current_jobs
        except Exception as e:
            minescript.echo(f"Error updating jobs: {e}")
        time.sleep(JOB_UPDATE_INTERVAL)


def get_jobs():
    """Thread-safe getter for jobs list."""
    with jobs_lock:
        return jobs.copy()


def find_job_by_command(command_path):
    """Find a job ID that matches the given command path."""
    current_jobs = get_jobs()
    # Normalize the command path for comparison
    normalized_path = command_path.replace('/', '\\').lower()
    
    for job in current_jobs:
        if job.command and len(job.command) > 0:
            # Join command parts and normalize for comparison
            job_command = ' '.join(job.command).replace('/', '\\').lower()
            # Check if the command matches (could be exact match or contains the path)
            if normalized_path in job_command or job_command.endswith(normalized_path.lstrip('\\')):
                return job.job_id
    return None


def checkbox_callback(sender, checked, user_data):
    """Callback for checkbox state changes."""
    if checked:  # Checked - start script
        minescript.execute(user_data)
    else:  # Unchecked - stop script
        # Find the job ID that matches this command path
        job_id = find_job_by_command(user_data)
        if job_id is not None:
            minescript.execute(f"\\killjob {job_id}")
        else:
            minescript.echo(f"Could not find running job for: {user_data}")


def refresh_scripts():
    """Refresh the scripts directory and update the UI."""
    global files, checkbox_tags
    
    # Re-scan the scripts directory
    files = get_script_files()
    
    # Delete all existing checkboxes
    for tag in checkbox_tags:
        try:
            dpg.delete_item(tag)
        except:
            pass  # Item might not exist
    
    checkbox_tags.clear()
    
    # Rebuild checkboxes
    for file in files:
        file_nopy = file[:-3]  # Remove .py extension
        # Format: \menu\scripts\filename (with leading backslash)
        file_exe = f"\\menu\\scripts\\{file_nopy}"
        
        checkbox_tag = f"checkbox_{file_nopy}"
        checkbox_tags.append(checkbox_tag)
        
        dpg.add_checkbox(
            label=file_nopy,
            callback=checkbox_callback,
            user_data=file_exe,
            tag=checkbox_tag,
            parent="main_window"
        )
    
    minescript.echo(f"Refreshed scripts directory: {len(files)} script(s) found")


def check_existing_menu_instances():
    """Check for and kill duplicate menu instances."""
    current_jobs = minescript.job_info()
    menu_jobs = []
    
    for job in current_jobs:
        # Check if this is a menu instance
        if job.command and len(job.command) > 0:
            # Normalize path separators for comparison
            command_str = ' '.join(job.command).replace('\\', os.sep).replace('/', os.sep)
            if 'menu' in command_str.lower() and 'menu.py' in command_str.lower():
                menu_jobs.append(job.job_id)
    
    # Kill all but the first menu instance
    if len(menu_jobs) > 1:
        minescript.echo("Only 1 menu instance allowed")
        for job_id in menu_jobs[1:]:  # Keep first, kill the rest
            minescript.execute(f"\\killjob {job_id}")


def main():
    """Initialize and run the GUI."""
    # Check for duplicate menu instances
    check_existing_menu_instances()
    
    # Start background job monitoring thread
    job_thread = threading.Thread(target=update_jobs_background, daemon=True)
    job_thread.start()
    
    # Initialize DearPyGui
    dpg.create_context()
    dpg.create_viewport(
        title='Minescript Menu',
        width=WIDTH,
        height=HEIGHT,
        decorated=True,
        always_on_top=False,
        resizable=False,
    )
    dpg.setup_dearpygui()

    # Create main window
    with dpg.window(
        label="Minescript Menu",
        tag="main_window",
        width=WIDTH,
        height=HEIGHT,
        no_resize=True,
        no_move=True,
        collapsed=False
    ):
        # Header with refresh button
        with dpg.table(header_row=False, borders_innerH=False, borders_outerH=False, 
                       borders_innerV=False, borders_outerV=False, policy=dpg.mvTable_SizingStretchProp):
            dpg.add_table_column(init_width_or_weight=1.0)
            dpg.add_table_column(init_width_or_weight=0.0)
            
            with dpg.table_row():
                dpg.add_text("Scripts:", tag="scripts_label")
                dpg.add_button(
                    label="Refresh",
                    callback=lambda: refresh_scripts(),
                    tag="refresh_button",
                    width=100
                )
        
        dpg.add_separator()
        
        # Script checkboxes
        for file in files:
            file_nopy = file[:-3]  # Remove .py extension
            # Format: \menu\scripts\filename (with leading backslash)
            file_exe = f"\\menu\\scripts\\{file_nopy}"
            
            checkbox_tag = f"checkbox_{file_nopy}"
            checkbox_tags.append(checkbox_tag)
            
            dpg.add_checkbox(
                label=file_nopy,
                callback=checkbox_callback,
                user_data=file_exe,
                tag=checkbox_tag
            )


if __name__ == "__main__":
    try:
        main()
        minescript.echo("Minescript GUI started")
        dpg.show_viewport()
        dpg.start_dearpygui()
    finally:
        running = False
        dpg.destroy_context()

