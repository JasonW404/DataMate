import json
import os
import yaml


def process_metadata_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = yaml.safe_load(f)
    if content['inputs'] != 'text':
        return
    value = (content['raw_id'], content['name'], content['description'], content['version'],
             content['inputs'].lower(), content['outputs'].lower(),
             json.dumps(content['runtime'], ensure_ascii=False) if 'runtime' in content else 'null',
             json.dumps(content['settings'], ensure_ascii=False) if 'settings' in content else 'null', '', 'false')
    values.append(value)


def traverse_and_generate_sql(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'metadata.yml':
                fullpath = os.path.join(dirpath, filename)
                process_metadata_file(fullpath)


if __name__ == "__main__":
    root_directory = '../ops'
    values = []
    traverse_and_generate_sql(root_directory)
    str_values = ''
    for v in values:
        str_values += str(v).replace("'null'", "null") + ',\n'

    sql = (f"INSERT IGNORE INTO t_operator (id, name, description, version, inputs, outputs, runtime, settings, "
           f"file_name, is_star) VALUES \n{str_values[:-2]};")
    print(f"{len(values)}\n" + sql)

