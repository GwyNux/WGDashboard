import sys
import pathlib

def patch_utilities():
    utilities_path = pathlib.Path(__file__).parent / "Utilities.py"
    with open(utilities_path, encoding="utf-8") as f:
        lines = f.readlines()

    # Собираем новый файл
    new_lines = []
    in_target_func = False
    for line in lines:
        if line.strip().startswith("def GetRemoteEndpoint"):
            new_lines.append(line)
            new_lines.append("    # [PATCH] Always return 127.0.0.1 for offline mode\n")
            new_lines.append("    return '127.0.0.1'\n")
            in_target_func = True
        elif in_target_func:
            # Пропускаем старое тело функции до конца (следующий def/class или пустая строка)
            if line.startswith("def ") or line.startswith("class "):
                in_target_func = False
                new_lines.append(line)
            # Иначе — просто пропускаем
        else:
            new_lines.append(line)

    with open(utilities_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("[patch_utilities] Utilities.py успешно пропатчен!")

if __name__ == "__main__":
    patch_utilities()
