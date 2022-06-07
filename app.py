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
streamlit_debug.set(flag=True, wait_for_client=True, host='localhost', port=6789)

# -----------------------------------------------------------------------------

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
    state.results_data = {
        'value': {},
        'rectanglelabels': [],
        'ellipselabels': [],
        'keypointlabels': [],
        'relations': [],
    }

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
    user, interfaces, task_configs = get_app_config()

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
    
    state.results_data = {
        'value': {},
        'rectanglelabels': [],
        'ellipselabels': [],
        'keypointlabels': [],
        'relations': [],
    }

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
    if value == None:
        return

    # TODO: generate tables for other types
    rectanglelabels = []
    ellipselabels = []
    keypointlabels = []
    relations = []
    for v in value['data']:
        if v['type'] == 'rectanglelabels':
            rectanglelabels.append({
                'id': v['id'],
                'x': v['value']['x'], 'y': v['value']['y'], 
                'width': v['value']['width'], 'height': v['value']['height'],
                'rotation': v['value']['rotation'],
                'label': v['value']['rectanglelabels'][0]
            })
        if v['type'] == 'ellipselabels':
            ellipselabels.append({
                'id': v['id'],
                'x': v['value']['x'], 'y': v['value']['y'], 
                'radiusX': v['value']['radiusX'], 'radiusY': v['value']['radiusY'],
                'rotation': v['value']['rotation'],
                'label': v['value']['ellipselabels'][0]
            })
        if v['type'] == 'keypointlabels':
            keypointlabels.append({
                'id': v['id'],
                'x': v['value']['x'], 'y': v['value']['y'], 
                'width': v['value']['width'],
                'label': v['value']['keypointlabels'][0]
            })
        if v['type'] == 'relation':
            relations.append({
                'from_id': v['from_id'], 'to_id': v['to_id'], 
                'direction': v['direction']
            })

    # Store results data to be displayed later
    state.results_data['value'] = value
    state.results_data['rectanglelabels'] = rectanglelabels
    state.results_data['ellipselabels'] = ellipselabels
    state.results_data['keypointlabels'] = keypointlabels
    state.results_data['relations'] = relations

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
    if state.results_data['rectanglelabels']:
        st.caption('Rectangle Labels')
        st.dataframe(state.results_data['rectanglelabels'])
    if state.results_data['ellipselabels']:
        st.caption('Ellipse Labels')
        st.dataframe(state.results_data['ellipselabels'])
    if state.results_data['keypointlabels']:
        st.caption('Keypoint Labels')
        st.dataframe(state.results_data['keypointlabels'])
    if state.results_data['relations']:
        st.caption('Relations')
        st.dataframe(state.results_data['relations'])

    # TODO: display tables for other types

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
        st.sidebar.info('Peer tasks available...')
        task_config_name = st.sidebar.selectbox(
            'Choose a peer task',
            options=peer_task_config_names,
            index=0, key='peer_task_config_name_selector',
            on_change=_reconfigure_peer_task_state_cb,
        )

    with st.sidebar.expander('⚙️ Settings', expanded=False):
        height = st.slider('Adjust viewport height', min_value=500, max_value=2000, value=1200)

    props = {
        'config': state.config,
        'interfaces': state.interfaces,
        'user': state.user,
        'task': state.task,
        'height': height,
    }

    handle_event(run_component(task_config_name, props))

    st.markdown('---')

    if st.sidebar.checkbox('Show annotation data', True):
        display_results_data()
    if st.sidebar.checkbox('Show config and task info', False):
        display_config_and_task_info()

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()
    st.sidebar.markdown('---')
    _, c2, _ = st.sidebar.columns([1,5,1])
    c2.image('./images/a12i_logo.png', output_format='png')
    st.sidebar.info('(c) 2022. CloudOpti Ltd. All rights reserved.')
    sync_component_state_with_rerun()