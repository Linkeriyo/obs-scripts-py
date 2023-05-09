from windows_toasts import WindowsToaster, ToastText1
import obspython

def show_notification(body):
    toaster = WindowsToaster('OBS Replay Buffer')

    newToast = ToastText1()
    newToast.SetBody(body)
    
    toaster.show_toast(newToast)


def on_event(event):
    if event == obspython.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STARTING:
        message = "Replay buffer starting"
        print(message)

    elif event == obspython.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STARTED:
        message = "Replay buffer started"
        print(message)
        show_notification(message)

    elif event == obspython.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STOPPING:
        message = "Replay buffer stopping"
        print(message)
        show_notification(message)

    elif event == obspython.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STOPPED:
        message = "Replay buffer stopped"
        print(message)
    
    elif event == obspython.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED:
        message = "Replay buffer saved"
        print(message)
        show_notification(message)


def script_load(settings):
    obspython.obs_frontend_add_event_callback(on_event)


def script_description():
    "Triggered when the current scene has changed."
