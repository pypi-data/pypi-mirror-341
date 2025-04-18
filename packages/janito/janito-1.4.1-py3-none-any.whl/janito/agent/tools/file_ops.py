import os
import shutil
from janito.agent.tool_handler import ToolHandler
from janito.agent.tools.rich_utils import print_info, print_success, print_error
from janito.agent.tools.utils import expand_path, display_path
from janito.agent.tools.tool_base import ToolBase

class CreateFileTool(ToolBase):
    """
    Create a new file or update an existing file with the given content.
    """
    def call(self, path: str, content: str, overwrite: bool = False) -> str:
        original_path = path
        path = expand_path(path)
        updating = os.path.exists(path) and not os.path.isdir(path)
        disp_path = display_path(original_path, path)
        if os.path.exists(path):
            if os.path.isdir(path):
                print_error(f"❌ Error: is a directory")
                return f"❌ Cannot create file: '{disp_path}' is an existing directory."
            if not overwrite:
                print_error(f"❗ Error: file '{disp_path}' exists and overwrite is False")
                return f"❗ Cannot create file: '{disp_path}' already exists and overwrite is False."
        if updating and overwrite:
            print_info(f"📝 Updating file: '{disp_path}' ... ")
        else:
            print_info(f"📝 Creating file: '{disp_path}' ... ")
        old_lines = None
        if updating and overwrite:
            with open(path, "r", encoding="utf-8") as f:
                old_lines = sum(1 for _ in f)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        new_lines = content.count('\n') + 1 if content else 0
        if old_lines is not None:
            print_success(f"✅ Successfully updated the file at '{disp_path}' ({old_lines} > {new_lines} lines).")
            return f"✅ Successfully updated the file at '{disp_path}' ({old_lines} > {new_lines} lines)."
        print_success(f"✅ Successfully created the file at '{disp_path}' ({new_lines} lines).")
        return f"✅ Successfully created the file at '{disp_path}' ({new_lines} lines)."

class CreateDirectoryTool(ToolBase):
    """
    Create a new directory at the specified path.
    """
    def call(self, path: str, overwrite: bool = False) -> str:
        """
        Create a new directory at the specified path.
        Args:
            path (str): Path to the directory to create.
            overwrite (bool): Whether to remove the directory if it exists.
        Returns:
            str: Result message.
        """
        original_path = path
        path = expand_path(path)
        disp_path = display_path(original_path, path)
        if os.path.exists(path):
            if not os.path.isdir(path):
                print_error(f"❌ Path '{disp_path}' exists and is not a directory.")
                return f"❌ Path '{disp_path}' exists and is not a directory."
