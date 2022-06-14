function runLabelStudioComponent() {
    // ----------------------------------------------------
    // Use these functions as is to perform required Streamlit 
    // component lifecycle actions:
    //
    // 1. Signal Streamlit client that component is ready
    // 2. Signal Streamlit client to set visible height of the component
    //    (this is optional, in case Streamlit doesn't correctly auto-set it)
    // 3. Pass values from component to Streamlit client
    //

    // Helper function to send type and data messages to Streamlit client

    const SET_COMPONENT_VALUE = "streamlit:setComponentValue"
    const RENDER = "streamlit:render"
    const COMPONENT_READY = "streamlit:componentReady"
    const SET_FRAME_HEIGHT = "streamlit:setFrameHeight"

    function _sendMessage(type, data) {
        // copy data into object
        var outData = Object.assign({
            isStreamlitMessage: true,
            type: type,
        }, data)

        if (type == SET_COMPONENT_VALUE) {
            // console.log("_sendMessage data: ", JSON.stringify(data))
            console.log("_sendMessage outData: ", JSON.stringify(outData))
        }

        window.parent.postMessage(outData, "*")
    }

    function initialize(pipeline) {
        // Hook Streamlit's message events into a simple dispatcher of pipeline handlers
        window.addEventListener("message", (event) => {
            if (event.data.type == RENDER) {
                // The event.data.args dict holds any JSON-serializable value
                // sent from the Streamlit client. It is already deserialized.
                pipeline.forEach(handler => {
                    handler(event.data.args)
                })
            }
        })

        _sendMessage(COMPONENT_READY, {apiVersion: 1});

        // Component should be mounted by Streamlit in an iframe, so try to autoset the iframe height.
        window.addEventListener("load", () => {
            window.setTimeout(function() {
                setFrameHeight(document.documentElement.clientHeight)
            }, 0)
        })

        // Optionally, if auto-height computation fails, you can manually set it
        // (uncomment below)
        // setFrameHeight(1200)
    }

    function setFrameHeight(height) {
        _sendMessage(SET_FRAME_HEIGHT, {height: height})
    }

    // The `data` argument can be any JSON-serializable value.
    function notifyHost(data) {
        _sendMessage(SET_COMPONENT_VALUE, data)
    }

    // ----------------------------------------------------
    // Here's the custom functionality of the component
    // implemented via a pipeline of inbound property handlers

    function notifyHostWithAnnotation(event, anno) {
        const value = {
            event: event,
            id: anno.id, 
            createdBy: anno.createdBy,
            createdDate: anno.createdDate, 
            data: anno.serialized
        }
        console.log(event, value)
        notifyHost({
            value: value,
            dataType: "json",
        })
    }

    const annotationHistory = []

    let LABELSTUDIO = null

    function _addLabelStudioEventHandlers() {
        LABELSTUDIO.on("labelStudioLoad", (LS) => {
            var c = LS.annotationStore.addAnnotation({
                userGenerate: true
            })
            LS.annotationStore.selectAnnotation(c.id)
        })
  
        LABELSTUDIO.on("storageInitialized", (store) => {
            LABELSTUDIO.on("selectAnnotation", (next) => {
                if (next.type === 'annotation') {
                    store.setHistory(annotationHistory)
                }
            })
            LABELSTUDIO.on("regionFinishedDrawing", (region, list) => {
                console.log("finish drawing", {region, list})
            })
        })
  
        LABELSTUDIO.on("entityCreate", (entity) => {
            data = entity.serialize()
            data.id = entity.id
            data.type = entity.type
            console.log("entityCreate", data)
        })

        LABELSTUDIO.on("entityDelete", (entity) => {
            data = entity.serialize()
            data.id = entity.id
            data.type = entity.type
            console.log("entityDelete", data)
        })

        LABELSTUDIO.on("submitAnnotation", (LS, anno) => {
            notifyHostWithAnnotation("submitAnnotation", anno)
            console.log("submitAnnotation", LS, anno)
        })
  
        LABELSTUDIO.on("updateAnnotation", (LS, anno) => {
            notifyHostWithAnnotation("updateAnnotation", anno)
            console.log("updateAnnotation", LS, anno)
        })
    }

    function renderLabelStudio_Handler(props) {
        // Render LabelStudio with values sent from Streamlit!
        options = {
            description: props?.description,
            user: props?.user,
            users: [],
            config: props?.config,
            interfaces: props?.interfaces,
            task: props?.task,
            history: annotationHistory,
        }
        if (LABELSTUDIO == null) {
            LABELSTUDIO = new LabelStudio('label-studio', options)
            _addLabelStudioEventHandlers()
        } else {
            LABELSTUDIO.options = options
        }
    }

    // Simply log received data dictionary
    function log_Handler(props) {
        console.log("Received from Streamlit: ", JSON.stringify(props))
    }

    function setFrameHeight_Handler(props) {
        setFrameHeight(props.height)
    }

    function forcePageReload_Handler() {
        if(!window.location.hash) {
            window.location = window.location + '#reloaded';
            window.location.reload();
        }
    }
  
    let pipeline = [log_Handler, setFrameHeight_Handler, renderLabelStudio_Handler, forcePageReload_Handler]

    // ----------------------------------------------------
    // Finally, initialize component passing in pipeline

    initialize(pipeline)
  }
