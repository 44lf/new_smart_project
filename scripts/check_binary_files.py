from __future__ import annotations

from pathlib import Path

TEXT_CHARS = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x7F)) | set(range(0x80, 0x100)))


def is_binary(path: Path) -> bool:
    data = path.read_bytes()
    if b"\0" in data:
        return True
    nontext = data.translate(None, TEXT_CHARS)
    return len(nontext) > 0 and len(nontext) / max(len(data), 1) > 0.3


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    binary_files: list[Path] = []
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            if is_binary(path):
                binary_files.append(path)

    if binary_files:
        print("Binary files detected:")
        for bf in binary_files:
            print(bf.relative_to(root))
        return 1

    print("No binary files detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
