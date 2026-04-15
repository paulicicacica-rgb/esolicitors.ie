import os
import glob

root = "."  # Change this to your folder path if needed
count = 0

for filepath in glob.glob(f"{root}/**/*.html", recursive=True):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "2025" in content:
        new_content = content.replace("2025", "2026")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated: {filepath}")
        count += 1

print(f"\nDone. {count} file(s) updated.")
