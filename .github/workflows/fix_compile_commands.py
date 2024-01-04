#!/usr/bin/env python3

import argparse
import json


def main():
    parser = argparse.ArgumentParser(
        description="Fix compile_commands.json generated by Gradle"
    )
    parser.add_argument("filename", help="compile_commands.json location")
    cmd_args = parser.parse_args()

    # Read JSON
    with open(cmd_args.filename) as f:
        data = json.load(f)

    for obj in data:
        out_args = []

        # Filter out -isystem flags that cause false positives
        iter_args = iter(obj["arguments"])
        for arg in iter_args:
            if arg == "-isystem":
                next_arg = next(iter_args)

                # /usr/lib/gcc/x86_64-pc-linux-gnu/13.2.1/include/xmmintrin.h:54:1:
                # error: conflicting types for '_mm_prefetch' [clang-diagnostic-error]
                if not next_arg.startswith("/usr/lib/gcc/"):
                    out_args += ["-isystem", next_arg]
            else:
                out_args.append(arg)

        obj["arguments"] = out_args

    # Write JSON
    with open(cmd_args.filename, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()