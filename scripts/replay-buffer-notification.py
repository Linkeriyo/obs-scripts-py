import os
from windows_toasts import WindowsToaster, ToastText1
import obspython
import simpleobsws
import asyncio
from showinfm import show_in_file_manager

def show_notification(body, path = None):
    toaster = WindowsToaster('OBS Replay Buffer')

    newToast = ToastText1()
    newToast.SetBody(body)

    if path is not None:
        #TODO: this still doesn't work because the script is no longer running when the notification is clicked
        newToast.on_activated = lambda _: show_in_file_manager(path)
    
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
        import debugpy;debugpy.breakpoint()
        replay_path = async_to_sync(get_last_replay_buffer_path()) 
        message = "Replay buffer saved"
        print(message)
        show_notification(message)


async def get_last_replay_buffer_path():
    client = simpleobsws.WebSocketClient("ws://localhost:4455")
    await client.connect()
    await client.wait_until_identified()

    result = await client.call(simpleobsws.Request("GetLastReplayBufferReplay"))
    await client.disconnect()

    if result.ok():
        print("Request succeeded! Response data: {}".format(result.responseData))
        return result.responseData['savedReplayPath']
    else:
        print("Request failed! Error: {}".format(result.error))
        return None
    

def async_to_sync(coro):
    return asyncio.get_event_loop().run_until_complete(coro)
    

def script_load(settings):
    obspython.obs_frontend_add_event_callback(on_event)


def script_description():
    "Triggered when the current scene has changed."
