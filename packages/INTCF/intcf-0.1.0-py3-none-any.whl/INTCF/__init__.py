import os

def main(path):
    try:
        if os.path.exists(path):
            if "." in path:
                return f"[INTCF] Done. File \"{path}\" exists."
            else:
                return f"[INTCF] Error. \"{path}\" is an invalid path, or this is a folder path."
        else:
            if "." in path:
                with open(path, "w"):
                    pass
                return f"[INTCF] Done. \"{path}\" did not exist. Created file."
            else:
                return f"[INTCF] Error. \"{path}\" is an invalid path, or this is a folder path."
    except Exception as e:
        return f"[INTCF] Error! {e}"