import os
import sys

def create_placeholders(root_dir):
    """
    Recursively checks all subdirectories under the given root_dir.
    If a directory is found to be empty (no files or subdirectories),
    it creates a file named 'placeholder' inside it.

    This function uses os.walk with topdown=False (bottom-up traversal)
    to ensure that if a folder contains only empty subfolders, the
    subfolders are processed first, preventing the parent from being
    incorrectly marked as empty later.

    Args:
        root_dir (str): The starting path for the traversal.
    """
    # Check if the root directory exists
    if not os.path.isdir(root_dir):
        print(f"Error: The directory '{root_dir}' does not exist or is not a directory.")
        return

    print(f"Starting scan from: {os.path.abspath(root_dir)}")

    # Walk directories from bottom up (topdown=False)
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        try:
            # Check if the directory is genuinely empty
            # If filenames is empty AND dirnames is empty, the folder is empty
            if not dirnames and not filenames:
                placeholder_file = os.path.join(dirpath, "placeholder")

                if not os.path.exists(placeholder_file):
                    # Create the placeholder file
                    with open(placeholder_file, 'w') as f:
                        f.write("This file was automatically generated because the folder was empty.\n")
                    print(f"Created: {placeholder_file}")
                else:
                    # File already exists
                    print(f"Skipped: {dirpath} - 'placeholder' already exists.")

        except OSError as e:
            print(f"Error processing directory {dirpath}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred in {dirpath}: {e}")

if __name__ == "__main__":
    # Determine the root directory to start from
    if len(sys.argv) > 1:
        # Use the path provided as a command-line argument
        start_path = sys.argv[1]
    else:
        # Use the current working directory if no argument is provided
        start_path = os.getcwd()

    create_placeholders(start_path)
    print("\nPlaceholder creation complete.")

# Example usage from command line:
# python placeholder_creator.py /path/to/your/project
# OR
# python placeholder_creator.py
