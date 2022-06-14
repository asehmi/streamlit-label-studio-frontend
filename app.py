import streamlit as st
from frontend import st_label_studio
from app_configs_builder import get_app_config

# --------------------------------------------------------------------------------
# Set Streamlit page style

st.set_page_config(layout='wide')

from style import set_page_container_style
set_page_container_style(
    max_width = 1500, max_width_100_percent = False,
    padding_top = 30, padding_right = 0, padding_left = 0, padding_bottom = 0,
    color = 'black', background_color = 'white',
)

# --------------------------------------------------------------------------------

import streamlit_debug
streamlit_debug.set(flag=False, wait_for_client=True, host='localhost', port=6789)

# -----------------------------------------------------------------------------

empty_results_data = {
    'value': {},
    'rectanglelabels': [],
    'ellipselabels': [],
    'keypointlabels': [],
    'audioregions': [],
    'audioclasses': [],
    'textentities': [],
    'videoclasses': [],
    'relations': [],
}

state = st.session_state
if 'user' not in state:
    state.user = None
if 'interfaces' not in state:
    state.interfaces = None
if 'task_configs' not in state:
    state.task_configs = None
if 'config' not in state:
    state.config = None
if 'task' not in state:
    state.task = None
if 'task_config_names' not in state:
    state.task_config_names = []
if 'results_data' not in state:
    state.results_data = empty_results_data

# -----------------------------------------------------------------------------

# !! Must be the FINAL thing you run in the app's control flow !!
# Causes all updated values to that point to be sent back to the component.
# (Note, this is a HACK to component state to sync given Streamlit's execution semantics)
def sync_component_state_with_rerun():
    if '_sync_' not in state:
        state._sync_ = True

    if state._sync_:
        state._sync_ = False
        st.experimental_rerun()
    else:
        state._sync_ = True

# -----------------------------------------------------------------------------

def refresh_state(task_config_name=None):
    # uroll=True expands config task lists into multiple configs with one task each
    user, interfaces, task_configs = get_app_config(unroll=True)

    # Default to the name of first config
    if task_config_name == None:
        task_config_name = [tc['name'] for tc in task_configs][0]

    # Now choose the matching task config
    # Works for full and partial names
    # Partial names (names withouit ids) are used in the top level selection menu
    task_config = [tc for tc in task_configs if task_config_name in tc['name']][0]

    config = task_config['config']
    task = task_config['task']

    state.user = user
    state.interfaces = interfaces
    state.task_configs = task_configs
    state.config = config
    state.task = task

    # Strip the ids in names that will be used in the selection menu
    # Set() would remove possible dups, but messes order, so using dict keys
    task_config_names_with_dups = [tc['name'].split('@')[0].strip() for tc in task_configs]
    state.task_config_names = list(dict.fromkeys(task_config_names_with_dups).keys())
    
    state.results_data = empty_results_data

# -----------------------------------------------------------------------------

def run_component(name, props):
    print('--------- Props Config --------')
    print(props['config'])
    print('--------- Props Task --------')
    print(props['task'])

    name = name.lower().replace(' ', '_')
    value = st_label_studio(key=f'my_labelstudio_{name}', **props)
    if isinstance(value, list) or isinstance(value, dict):

        print('--------- Component Value --------')
        print(value)

        return value
    else:
        return None

def handle_event(value):
    if value == None or (not 'Annotation' in value['event']):
        return

    # TODO: generate tables for other types
    results_data = empty_results_data
    results_data['value'] = value
    for v in value['data']:
        id = v['id']
        val = v['value']
        to_name = v['to_name']
        v_type = v['type']
        if to_name == 'img' and v_type == 'rectanglelabels':
            results_data['rectanglelabels'].append({
                'id': id,
                'x': val['x'], 'y': val['y'], 
                'width': val['width'], 'height': val['height'],
                'rotation': val['rotation'],
                'label': val['rectanglelabels'],
            })
        if to_name == 'img' and v_type == 'ellipselabels':
            results_data['ellipselabels'].append({
                'id': id,
                'x': val['x'], 'y': val['y'], 
                'radiusX': val['radiusX'], 'radiusY': val['radiusY'],
                'rotation': val['rotation'],
                'label': val['ellipselabels'],
            })
        if to_name == 'img' and v_type == 'keypointlabels':
            results_data['keypointlabels'].append({
                'id': id,
                'x': val['x'], 'y': val['y'], 
                'width': val['width'],
                'label': val['keypointlabels'],
            })
        if to_name == 'audio' and (v_type == 'labels' or v_type == 'number'):
            results_data['audioregions'].append({
                'id': id,
                'start': val.get('start', None), 'end': val.get('end', None),
                'labels': val.get('labels', None),
                'number': val.get('number', None),
            })
        if to_name == 'audio' and v_type == 'choices':
            results_data['audioclasses'].append({
                'id': id, 'choices': val['choices'],
            })
        if to_name == 'video' and v_type == 'choices':
            results_data['videoclasses'].append({
                'id': id, 'choices': val['choices'],
            })
        if to_name == 'text' and v_type == 'labels':
            results_data['textentities'].append({
                'id': id,
                'start': val['start'], 'end': val['end'],
                'text': val['text'], 'labels': val['labels'],
            })
        if v_type == 'relation':
            results_data['relations'].append({
                'id': id,
                'start': val['start'], 'end': val['end'],
            })

    # Store results data to be displayed later
    state.results_data = results_data

    # print('Annotations', [v['value'] for v in value['data']])

    annotations = [{
        'id': value['id'],
        'createdBy': value['createdBy'],
        'createdDate': value['createdDate'],
        'result': value['data']
    }]

    state.task['annotations'] = annotations

# -----------------------------------------------------------------------------

def display_results_data():
    if not state.results_data['value']:
        st.info('Annotations data is not available to display here. Please submit or update an annotation.')
        return

    st.markdown('#### Annotations tables')
    for k, v in state.results_data.items():
        if k != 'value' and v:
            st.caption(k)
            st.dataframe(v)

    st.markdown('---')

    st.markdown('#### Raw annotations data')
    with st.expander('Show data', expanded=False):
        st.json(state.results_data['value'])

def display_config_and_task_info():
    c1, c2 = st.columns([2,3])
    c1.markdown('#### Config info')
    with c1.expander('Config info', expanded=False):
        config = state.config
        config = config.replace('\n', '\n\n')
        st.markdown(config)
    c2.markdown('#### Task info')
    with c2.expander('Show task', expanded=False):
        st.json(state.task)

# -----------------------------------------------------------------------------

def _reconfigure_state_cb():
    refresh_state(state['task_config_name_selector'])

def _reconfigure_peer_task_state_cb():
    refresh_state(state['peer_task_config_name_selector'])

def main():
    st.image('./images/label_studio_demo.png', output_format='png')
    # st.subheader('Label Studio Demo')
    st.caption('A Streamlit component integrating Label Studio Frontend in Streamlit applications')

    # If any states are not assigned then initialize
    if not (state.user and state.interfaces and state.config and state.task):
        refresh_state()

    st.sidebar.image('./images/label_studio_logo.png', width=50, output_format='png')
    st.sidebar.subheader('Label Studio Tasks')

    task_config_name = st.sidebar.selectbox(
        'Choose a task configuration',
        options=state.task_config_names,
        index=0, key='task_config_name_selector',
        on_change=_reconfigure_state_cb,
    )

    peer_task_config_names = [tc['name'] for tc in state.task_configs if task_config_name in tc['name']]

    if len(peer_task_config_names) > 1:
        c1, c2 = st.sidebar.columns([1,19])
        c1.write('➕')
        with c2:
            task_config_name = st.selectbox(
                'Choose a task',
                options=peer_task_config_names,
                index=0, key='peer_task_config_name_selector',
                on_change=_reconfigure_peer_task_state_cb,
                disabled=(len(peer_task_config_names) == 1),
                help='This configuration has multiple tasks. Please choose one.'
            )

    show_annotation_data = st.sidebar.empty()
    show_config_and_task_info = st.sidebar.empty()

    st.sidebar.markdown('---')
    with st.sidebar.expander('⚙️ Settings', expanded=False):
        st.info('If the viewport area is blank, increase its height 📐 or click the button 🔁 below to force a reload.')
        height = st.number_input(
            '📐 Adjust viewport height',
            min_value=500, max_value=2000, value=1300, step=100,
        )
        st.button('🔁 Label Studio reload')
        if st.button('🔥 Clear config cache', help='Allows refresh of application task configuration.'):
            get_app_config.clear()

    props = {
        'description': task_config_name,
        'config': state.config,
        'interfaces': state.interfaces,
        'user': state.user,
        'task': state.task,
        'height': height,
    }

    handle_event(run_component(task_config_name, props))

    st.markdown('---')
    if show_annotation_data.checkbox('Show annotation data', True):
        display_results_data()
    if show_config_and_task_info.checkbox('Show config and task info', False):
        display_config_and_task_info()

# -----------------------------------------------------------------------------

def about():
    st.sidebar.markdown('---')
    st.sidebar.info('(c) 2022. CloudOpti Ltd. All rights reserved.')
    st.sidebar.image('./images/a12i_logo.png', width=120, output_format='png')

def references():
    st.sidebar.markdown('---')
    st.sidebar.markdown('''
        #### Label Studio resources
        - [Website](https://labelstud.io/)
        - [Frontend docs](https://labelstud.io/guide/frontend.html)
        - [Frontend repo](https://github.com/heartexlabs/label-studio-frontend)
        - [Backend repo](https://github.com/heartexlabs/label-studio)
        - [v1.4.0 on NPM](https://www.npmjs.com/package/@heartexlabs/label-studio)
    ''')

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()
    about()
    references()
    # sync_component_state_with_rerun()
