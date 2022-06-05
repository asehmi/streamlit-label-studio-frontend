# Streamlit - Label Studio Frontend

_**A Streamlit component integrating Label Studio Frontend in Streamlit applications**_

    date: "2022-06-05"
    author:
        name: "Arvindra Sehmi"
        url: "https://www.linkedin.com/in/asehmi/"
        mail: "vin@thesehmis.com"
        avatar: "https://twitter.com/asehmi/profile_image?size=original"
    related: [Introduction to Streamlit and Streamlit Components](https://auth0.com/blog/introduction-to-streamlit-and-streamlit-components/)

## Overview

[Label Studio](https://labelstud.io/) is an open source data labeling tool providing flexible data annotation. Label Studio comprises Label Studio Backend (LSB) server and ML service and 
Label Studio Frontend (LSF) whihc is based on React and mobx-state-tree and distributed as an NPM package. LSF can be integrated in third-party applications
without using LSB to provide data annotation support to users. LSF can be customized and extended to build custom UIs or used with pre-built labeling templates. 

This Streamlit application leverages Streamlit Components extensibilty with the simple architecture of _Component Zero_ discussed in my article, 
[Introduction to Streamlit and Streamlit Components](https://auth0.com/blog/introduction-to-streamlit-and-streamlit-components/). Using _Component Zero_
as a template it was straight-forward to take the code snippet in Label Studio's [Frontend integration guide](https://labelstud.io/guide/frontend.html#Frontend-integration-guide)
and build the Streamlit component.

## Installation
```
$ pip install -r requirements.txt
$ cd streamlit_labelstudio_frontend
```

## Usage
Run the included app for a quick example. 

```
streamlit run app.py
```

More configurations can be found in the official [Label Studio examples](https://github.com/heartexlabs/label-studio-frontend/tree/master/examples)
