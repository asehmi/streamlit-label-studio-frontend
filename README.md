# Streamlit - Label Studio Frontend

_**A Streamlit component integrating Label Studio Frontend in Streamlit applications**_

    date: "2022-06-07"
    author:
        name: "Arvindra Sehmi"
        url: "https://www.linkedin.com/in/asehmi/"
        mail: "vin@thesehmis.com"
        avatar: "https://twitter.com/asehmi/profile_image?size=original"
    related: [Introduction to Streamlit and Streamlit Components](https://auth0.com/blog/introduction-to-streamlit-and-streamlit-components/)

## Overview

[Label Studio](https://labelstud.io/) is an open source data labeling tool providing flexible data annotation. Label Studio comprises Label Studio Backend (LSB) server and ML service and 
Label Studio Frontend (LSF) which is based on React and mobx-state-tree and distributed as an NPM package. LSF can be integrated in third-party applications
without using LSB to provide data annotation support to users. LSF can be customized and extended to build custom UIs or used with pre-built labeling templates. 

This Streamlit application leverages Streamlit Components extensibilty with the simple architecture of _Component Zero_ discussed in my article, 
[Introduction to Streamlit and Streamlit Components](https://auth0.com/blog/introduction-to-streamlit-and-streamlit-components/). Using _Component Zero_
as a template it was straight-forward to take the code snippet in Label Studio's [Frontend integration guide](https://labelstud.io/guide/frontend.html#Frontend-integration-guide)
and build the Streamlit component.

## Demo

![Demo](./images/streamlit-label-studio-frontend.gif)

## Installation

```bash
$ cd streamlit-label-studio-frontend
$ pip install -r requirements.txt
```

## Usage
Run the included app for a quick example. 

```bash
$ streamlit run app.py
```

The Streamlit user interface is used to load annotation task configurations which Label Studio uses to display annotation tools appropriate for the annotation task at hand. Once annotations are done, the annotations data can be submitted via LSF (actually via the custom LSF Streamlit component built to host LSF) to Streamlit, where it is displayed. You can of course extend the Streamlit application and save store this data as you see fit. Outside the scope of this Label Studio demo application, you can also leverage LSB API from Streamlit.

This app is easily customised through externalized configuration.  

# Configuration

Configuration for labeling tasks in made in [`app_config.json`](./app_config.json). There are three sections required for annotation: `"user"`, `"interfaces"` and `"task_configs"`.

In `"task_configs"` you define `task` objects explicitly using the task `"object"` key, or via a local file using the task `"file"` key, or from an external site using the task `"url"` key. Similarly, you can define Label Studio annotation UI elements using `"config"` objects. 

More configurations can be found in the official [Label Studio examples](https://github.com/heartexlabs/label-studio-frontend/tree/master/examples)

Enjoy!
Arvindra