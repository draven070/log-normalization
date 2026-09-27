import json
import os
import sys

from pipelines.normalizer import LogNormalizer


def process_linux(
    input_file,
    output_file
):

    normalizer = LogNormalizer()

    results = []

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            result = normalizer.normalize_linux(
                line
            )

            if result:

                results.append(
                    result.model_dump()
                )

    save_results(
        results,
        output_file
    )


def process_windows(
    input_file,
    output_file
):

    normalizer = LogNormalizer()

    results = []

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        events = json.load(file)

    for event in events:

        result = normalizer.normalize_windows(
            event
        )

        if result:

            results.append(
                result.model_dump()
            )

    save_results(
        results,
        output_file
    )


def save_results(
    results,
    output_file
):

    directory = os.path.dirname(
        output_file
    )

    if directory:

        os.makedirs(
            directory,
            exist_ok=True
        )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )

    print(
        f"[+] Normalized events: "
        f"{len(results)}"
    )

    print(
        f"[+] Output: {output_file}"
    )


def main():

    if len(sys.argv) != 4:

        print(
            "Usage:"
        )

        print(
            "python app.py linux "
            "<input> <output>"
        )

        print(
            "python app.py windows "
            "<input> <output>"
        )

        sys.exit(1)

    log_type = sys.argv[1]

    input_file = sys.argv[2]

    output_file = sys.argv[3]

    if log_type == "linux":

        process_linux(
            input_file,
            output_file
        )

    elif log_type == "windows":

        process_windows(
            input_file,
            output_file
        )

    else:

        print(
            "[-] Unknown log type"
        )

        print(
            "Use: linux or windows"
        )


if __name__ == "__main__":
    main()