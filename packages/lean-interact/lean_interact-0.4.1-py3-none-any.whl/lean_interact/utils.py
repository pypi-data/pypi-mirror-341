import logging
import os
import platform
import re
import resource
import shutil
import subprocess

import psutil
from rich.logging import RichHandler

logger = logging.getLogger("document_autoformalization")
logger.setLevel("INFO")
handler = RichHandler(rich_tracebacks=True)
handler.setLevel("NOTSET")
handler.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
logger.handlers = []
logger.addHandler(handler)


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CACHE_DIR = os.path.join(ROOT_DIR, "cache")
DEFAULT_REPL_GIT_URL = "https://github.com/augustepoiroux/repl"
DEFAULT_REPL_VERSION = "v1.0.6"

os.makedirs(DEFAULT_CACHE_DIR, exist_ok=True)


def get_total_memory_usage(proc: psutil.Process):
    """Get total resident memory usage of a process and its children (in bytes)."""
    try:
        total = proc.memory_info().rss
        for child in proc.children(recursive=True):
            total += child.memory_info().rss
        return total
    except psutil.NoSuchProcess:
        return 0


def _limit_memory(max_mb: int | None):
    """Limit the memory usage of the current process."""
    if max_mb is None:
        return
    try:
        resource.setrlimit(resource.RLIMIT_AS, (max_mb * 1024 * 1024, max_mb * 1024 * 1024))
    except ValueError:
        logger.warning(f"Failed to set memory limit to {max_mb} MB.")


def clear_cache():
    shutil.rmtree(DEFAULT_CACHE_DIR, ignore_errors=True)


def get_project_lean_version(project_dir: str) -> str | None:
    """
    Get the Lean version used in a project.
    """
    toolchain_file = os.path.join(project_dir, "lean-toolchain")
    if os.path.isfile(toolchain_file):
        with open(toolchain_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                try:
                    return content.split(":")[-1]
                except Exception:
                    pass
    return None


def install_lean():
    try:
        os_name = platform.system()
        print(f"Detected operating system: {os_name}")
        if os_name == "Linux":
            command = "curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain stable && . ~/.profile"
        elif os_name == "Darwin":
            command = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/leanprover-community/mathlib4/master/scripts/install_macos.sh)" && source ~/.profile'
        elif os_name == "Windows":
            command = (
                "curl -O --location https://raw.githubusercontent.com/leanprover/elan/master/elan-init.ps1"
                " && powershell -ExecutionPolicy Bypass -f elan-init.ps1"
                " && del elan-init.ps1"
            )
        else:
            raise RuntimeError(
                "Unsupported operating system. Please install elan manually: https://leanprover-community.github.io/get_started.html"
            )
        subprocess.run(command, shell=True, check=True)
        if os_name in ["Linux", "Darwin"]:
            # add `export PATH="$HOME/.elan/bin:$PATH"` to ~/.bashrc and ~/.zshrc if they exist
            paths = ["~/.bashrc", "~/.zshrc"]
            for path in paths:
                path = os.path.expanduser(path)
                try:
                    with open(path, "a") as file:
                        file.write('\nexport PATH="$HOME/.elan/bin:$PATH"\n')
                    print(f"Added `elan` to {path}")
                except FileNotFoundError:
                    print(f"{path} not found, skipping.")
            print(
                "Please restart your terminal or run 'source ~/.profile' to update your shell with the new environment variables."
            )
        print("Lean installation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(
            f"An error occurred during Lean installation: {e}. Please check https://leanprover-community.github.io/get_started.html for more information."
        )


def indent_code(code: str, nb_spaces: int = 2) -> str:
    return "\n".join(" " * nb_spaces + line for line in code.split("\n"))


def compress_newlines(lean_code: str):
    # compress lines containing only whitespaces
    lean_code = re.sub(r"^\s+$", "", lean_code, flags=re.MULTILINE)
    # Compress multiple consecutive newlines
    lean_code = re.sub(r"\n\n+", "\n\n", lean_code)
    lean_code = lean_code.lstrip()
    if lean_code.endswith("\n"):
        lean_code = lean_code.rstrip() + "\n"
    return lean_code


def lean_comments_ranges(
    lean_code: str, multiline_comment_suffix: str = "", remove_single_line_comments: bool = True
) -> list[tuple[int, int]]:
    """Extract the ranges of Lean comments from a Lean code snippet."""
    # multiline comments
    open_comment_indices = [m.start() for m in re.finditer(r"/-" + multiline_comment_suffix, lean_code)]
    close_comment_indices = [
        m.start() + len(multiline_comment_suffix) + 2 for m in re.finditer(multiline_comment_suffix + r"-/", lean_code)
    ]

    if len(open_comment_indices) == len(close_comment_indices) + 1:
        # the last comment has probably not been closed due to partial code
        close_comment_indices.append(len(lean_code))

    elif len(open_comment_indices) + 1 == len(close_comment_indices):
        # the first comment has probably been opened before the code snippet
        open_comment_indices.insert(0, 0)

    elif len(open_comment_indices) != len(close_comment_indices):
        raise ValueError("Mismatched open and close comment indices.")

    # trick to handle nested comments in a simple way
    multiline_comment_ranges = list(zip(open_comment_indices, close_comment_indices))

    if remove_single_line_comments:
        # single line comments
        single_line_comment_ranges = [
            (m.start(), lean_code.find("\n", m.start())) for m in re.finditer(r"--", lean_code)
        ]
        multiline_comment_ranges += single_line_comment_ranges

    # merge potential overlapping ranges
    comment_ranges = sorted(multiline_comment_ranges, key=lambda x: x[0])
    merged_comment_ranges: list[tuple[int, int]] = []
    for start, end in comment_ranges:
        if merged_comment_ranges and start <= merged_comment_ranges[-1][1]:
            merged_comment_ranges[-1] = (merged_comment_ranges[-1][0], max(merged_comment_ranges[-1][1], end))
        else:
            merged_comment_ranges.append((start, end))

    return merged_comment_ranges


def remove_lean_comments(lean_code: str) -> str | None:
    try:
        comment_ranges = lean_comments_ranges(lean_code)

        new_lean_code = ""
        prev_start = 0
        for start, end in comment_ranges:
            new_lean_code += lean_code[prev_start:start]
            prev_start = end

        new_lean_code += lean_code[prev_start:]
        return new_lean_code

    except Exception:
        return None


def split_implementation(declaration: str, start: int = 0):
    # for a theorem, an implementation is the proof
    if ":=" in declaration:
        # we have to be careful here as ":=" can be used inside the declaration itself
        indices = set([m.start() for m in re.finditer(r":=", declaration)])

        # we remove the ones related to "let", "haveI", ... declarations
        for keyword in ["let", "haveI"]:
            regex = rf"{keyword}\s+\S*?\s*(:=)"
            decl_indices = set([m.start(1) for m in re.finditer(regex, declaration)])
            indices = indices - decl_indices

        # implementation using pcre2 blows up the memory, and it turns out it is faster to use a python loop
        counters = {"(": 0, "{": 0, "[": 0}
        closing = {")": "(", "}": "{", "]": "["}
        for i, c in enumerate(declaration[start:]):
            if c in counters:
                counters[c] += 1
            elif c in [")", "}", "]"]:
                counters[closing[c]] -= 1
            if all([v == 0 for v in counters.values()]) and (i + start) in indices:
                return i + start
    return None


def split_conclusion(declaration: str, start: int = 0) -> int | None:
    counters = {"(": 0, "{": 0, "[": 0}
    closing = {")": "(", "}": "{", "]": "["}
    for i, c in enumerate(declaration[start:]):
        if c in counters:
            counters[c] += 1
        elif c in [")", "}", "]"]:
            counters[closing[c]] -= 1
        if all([v == 0 for v in counters.values()]) and c == ":":
            return i + start
    return None


def clean_theorem_string(theorem_string: str, new_theorem_name: str = "dummy", add_sorry: bool = True) -> str | None:
    """Clean a theorem string by removing the proof, comments, and updating the theorem name.
    This method assumes that no other declarations are present in the theorem string."""
    try:
        # clean the theorem string
        clean_formal = remove_lean_comments(theorem_string)
        if clean_formal is None:
            raise ValueError("Comment removal failed.")
        clean_formal = clean_formal.strip()

        # we remove the first part of the string until the first "theorem" or "lemma" keyword
        theorem_decl_keywords = "|".join(["theorem", "lemma", "example"])
        re_match = re.search(rf"\b{theorem_decl_keywords}\s", clean_formal)
        if re_match is None:
            raise ValueError("Theorem declaration keyword not found.")
        idx_theorem = re_match.start()
        clean_formal = clean_formal[idx_theorem:]

        # if a proof is provided we remove it
        idx_implement = split_implementation(clean_formal)
        if idx_implement is not None:
            clean_formal = clean_formal[:idx_implement].strip()

        # remove "theorem" and the theorem name
        if clean_formal.strip().startswith("example"):
            clean_formal = re.sub(r"^[^\s]+", "", clean_formal).strip()
        else:
            clean_formal = re.sub(r"^[^\s]+", "", clean_formal).strip()
            clean_formal = re.sub(r"^[^\s:({\[]+", "", clean_formal).strip()
        clean_formal = f"theorem {new_theorem_name} " + clean_formal
        if add_sorry:
            clean_formal += " := sorry"
        return clean_formal
    except Exception:
        return None


def extract_last_theorem(lean_code: str) -> int:
    """Extract the last theorem from a Lean code snippet. It assumes that the Lean code snippet ends with a theorem."""
    comments_ranges = lean_comments_ranges(lean_code)

    # find last theorem by looking for `theorem` keyword surrounded by whitespaces, or by being at the beginning of the string
    theorem_decl_keywords = ["theorem", "lemma", "example"]
    theorem_indices = []
    for keyword in theorem_decl_keywords:
        theorem_indices += [m.start() for m in re.finditer(rf"\b{keyword}\s", lean_code)]

    # remove matches that are inside comments
    theorem_indices = [idx for idx in theorem_indices if not any(start <= idx <= end for start, end in comments_ranges)]

    if not theorem_indices:
        raise ValueError(f"No theorem found in the provided Lean code:\n{lean_code}")

    return theorem_indices[-1]


def clean_last_theorem_string(lean_code: str, new_theorem_name: str = "dummy", add_sorry: bool = False) -> str:
    """Clean the last theorem string from a Lean code snippet. It assumes that the Lean code snippet ends with a theorem."""
    idx_last_theorem = extract_last_theorem(lean_code)
    clean_thm = clean_theorem_string(lean_code[idx_last_theorem:], new_theorem_name, add_sorry=add_sorry)
    if clean_thm is not None:
        return lean_code[:idx_last_theorem] + clean_thm

    raise ValueError(f"Theorem extraction failed for the following Lean code:\n{lean_code}")
