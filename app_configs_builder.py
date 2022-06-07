import io
import requests
import json
import streamlit as st

# Loading the task configs from the `task_configs.json` file.
st.experimental_memo()
def get_app_config():
    label_studio_app_config = json.loads(io.open('app_configs.json', 'r', encoding='utf8').read())
    
    user = label_studio_app_config['user']
    interfaces = label_studio_app_config['interfaces']
    task_configs = label_studio_app_config['task_configs']

    task_configs_inflated = []
    for tc in task_configs:
        # Inflating the task configs.

        config_spec = tc['config']
        if config_spec.get('url', None):
            config = requests.get(config_spec['url']).text
        elif config_spec.get('file', None):
            config = io.open(config_spec['file'], 'r', encoding='utf8').read()
        else:
            raise ValueError(f'Valid config spec not found in {tc}')

        task_spec = tc['task']
        if task_spec.get('url', None):
            task = json.loads(requests.get(task_spec['url']).text)
        elif task_spec.get('file', None):
            task = json.loads(io.open(task_spec['file'], 'r', encoding='utf8').read())
        elif task_spec.get('object', None):
            task = task_spec['object']
        else:
            raise ValueError(f'Valid task spec not found in {tc}')

        if isinstance(task, dict):
            task = [task]

        for i, task_item in enumerate(task):
            id = task_item.get('id', i)
            name = f"{tc['name']}@{id}"
            tc_inflated = {
                'id': i,
                'name': name,
                'description': tc['description'],
                'annotation_type': tc['annotation_type'],
                'config': config,
                'task': task_item,
            }
            task_configs_inflated.append(tc_inflated)

    # print('Task Configs Head:\n', task_configs[:2])

    return user, interfaces, task_configs_inflated
