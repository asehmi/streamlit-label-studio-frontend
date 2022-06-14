import streamlit.components.v1 as components
_component_func = components.declare_component(
    name='streamlit_label_studio_frontend',
    path='./frontend'
)

# Public function for the package wrapping the caller to the frontend code
def st_label_studio(description, config, interfaces, user, task, key='label_studio_frontend', height=1000):
    component_value = _component_func(
        description=description, config=config, 
        interfaces=interfaces, user=user,
        task=task, height=height,
        key=key
    )
    return component_value
