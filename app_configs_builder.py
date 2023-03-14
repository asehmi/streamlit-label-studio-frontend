import io
import requests
import json

# Loading the task configs from the `task_configs.json` file.
# When uroll=True, configs with a list of tasks will be expanded into multiple
# configs with one task each. (I have not been able to make LSF accept a
# list of tasks, so I send each task individually.)
# The config name will have the task id appended to it, <config name>@<task id>.
# The function will provide task lists when unroll=False.
def get_app_config(unroll=True):
    print('get_app_config() - Cache Hit!')

    label_studio_app_config = json.loads(io.open('app_configs.json', 'r', encoding='utf8').read())
    
    user = label_studio_app_config['user']
    interfaces = label_studio_app_config['interfaces']
    task_configs_source = label_studio_app_config['task_configs']

    task_configs = []
    for i, tc in enumerate(task_configs_source):
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

        if unroll:
            if isinstance(task, dict):
                task = [task]
            for j, task_item in enumerate(task):
                id = task_item.get('id', j)
                name = f"{tc['name']}@{id}"
                tc_unrolled = {
                    'id': j,
                    'name': name,
                    'description': tc['description'],
                    'annotation_type': tc['annotation_type'],
                    'config': config,
                    'task': task_item,
                }
                task_configs.append(tc_unrolled)
        else:
            tc_untouched = {
                'id': tc.get('id', i),
                'name': tc['name'],
                'description': tc['description'],
                'annotation_type': tc['annotation_type'],
                'config': config,
                'task': task,
            }
            task_configs.append(tc_untouched)

    print('Task Configs Head:\n', task_configs[:5])

    return user, interfaces, task_configs
