import streamlit as st
from frontend import st_label_studio

st.set_page_config(layout='wide')

# -----------------------------------------------------------------------------
config = """
      <View>
        <View style="padding: 25px; box-shadow: 2px 2px 8px #AAA;">
          <Image name="img" value="$image" width="100%" brightnessControl="true" contrastControl="true" zoomControl="true" rotateControl="true"></Image>
        </View>
        <RectangleLabels name="tag" toName="img">
          <Label value="Galaxy"></Label>
          <Label value="Star"></Label>
          <Label value="Comet"></Label>
          <Label value="Moon"></Label>
          <Label value="Sky"></Label>
          <Label value="Tree"></Label>
          <Label value="Road"></Label>
          <Label value="Fence"></Label>
        </RectangleLabels>
      </View>
"""
interfaces = [
  "panel",
  "update",
  "controls",
  "side-column",
  "annotations:menu",
  "annotations:add-new",
  "annotations:delete",
  "predictions:menu"
]
user = {
  'pk': 1,
  'firstName': "Arvindra",
  'lastName': "Sehmi"
}
image_url = "https://htx-misc.s3.amazonaws.com/opensource/label-studio/examples/images/nick-owuor-astro-nic-visuals-wDifg5xc9Z4-unsplash.jpg"
task = {
  'annotations': [],
  'predictions': [],
  'id': 1,
  'data': {
    'image': image_url
  }
}

# -----------------------------------------------------------------------------
state = st.session_state
if 'user' not in state:
  state.user = user
if 'config' not in state:
  state.config = config
if 'interfaces' not in state:
  state.interfaces = interfaces
if 'image_url' not in state:
  state.image_url = image_url
if 'task' not in state:
  state.task = task

# -----------------------------------------------------------------------------
def sync_state():
    if '_sync_' not in state:
        state._sync_ = True

    if state._sync_:
        state._sync_ = False
        st.experimental_rerun()
    else:
        state._sync_ = True

# -----------------------------------------------------------------------------
def run_component(props):
    value = st_label_studio(key='my_labelstudio', **props)
    if isinstance(value, list) or isinstance(value, dict):
      print(value)
      return value
    else:
      return None

def handle_event(value):
    if value == None:
      return

    st.subheader('Annotations')
    st.json(value, expanded=False)

    results = []
    for v in value:
        results.append({'id':v['id'], 'x':v['value']['x'], 'y':v['value']['y'], 'width':v['value']['width'], 'height':v['value']['height'], 'label':v['value']['rectanglelabels'][0]})
    st.dataframe(results)

    # print('Annotations', [v['value'] for v in value])

    state.task = {
        'annotations': [{
            'id': 1,
            'result': value 
        }],
        'predictions': [],
        'id': 1,
        'data': {
            'image': image_url
        }
    }

    sync_state()

props = {
    'config': state.config,
    'interfaces': state.interfaces,
    'user': state.user,
    'task': state.task,
    'height': 1200,
}

c1, c2, c3 = st.columns([1,3,1])
with c2:
  st.subheader('Label Studio Demo')
  st.caption('A Streamlit component integrating Label Studio Frontend in Streamlit applications')
  handle_event(run_component(props))
