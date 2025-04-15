from iprm.util.env import Env
from iprm.backend.backend import Backend


def load_backends(plugin_dir):
    import importlib
    import inspect
    import sys
    from pathlib import Path
    loaded_backend_plugins = {}
    plugin_path = Path(plugin_dir)

    if not plugin_path.is_dir():
        raise ValueError(f"Directory not found: {plugin_path}")

    str_plugin_dir = str(plugin_path.absolute())
    if str_plugin_dir not in sys.path:
        sys.path.insert(0, str_plugin_dir)

    for file_path in plugin_path.iterdir():
        if file_path.is_dir():
            continue

        if file_path.suffix == '.py' and file_path.is_file():
            module_name = file_path.stem

            try:
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and
                            issubclass(obj, Backend) and
                            obj is not Backend and
                            obj.__module__ == module_name and Env.platform in obj.platforms()):
                        loaded_backend_plugins[obj.name()] = obj

            except (ImportError, AttributeError) as e:
                print(f"Error importing plugin module {module_name}: {e}")

    if str_plugin_dir in sys.path:
        sys.path.remove(str_plugin_dir)
    return loaded_backend_plugins
