# script/expand_sql_files.py

import yaml
import glob
import os
import sys

def main():
    baseline_no = os.environ.get("BASELINE_NO")
    if not baseline_no:
        print("Missing baseline_no environment variable")
        sys.exit(1)

    config_path = f"init_repo/script/execute_init/{baseline_no}/execute_init.yml"
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        sys.exit(1)

    with open(config_path) as f:
        config = yaml.safe_load(f)

    ordered_sqls = []
    for category, entries in config.get("scripts", {}).items():
        for entry in entries:
            pattern = entry.get("path")
            if pattern:
                matched = sorted(glob.glob(pattern))
                ordered_sqls.extend(matched)

    with open("sql_file_list.txt", "w") as out:
        for path in ordered_sqls:
            out.write(f"{path}\n")

    with open(os.environ['GITHUB_OUTPUT'], 'a') as ghout:
        ghout.write(f"sql_list_file=sql_file_list.txt\n")

if __name__ == "__main__":
    main()
