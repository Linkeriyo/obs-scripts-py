from windows_toasts import WindowsToaster, ToastText1
import obspython
import simpleobsws
import asyncio
from showinfm import show_in_file_manager

def show_notification(message, path=None):
    toaster = WindowsToaster('OBS Replay Buffer')
    newToast = ToastText1(body=message)

    if path is not None:
        newToast.on_activated = lambda _: show_in_file_manager(path)
    
    toaster.show_toast(newToast)


def on_event(event):
    messages = {
        obspython.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STARTING: "Replay buffer starting",
        obspython.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STARTED: "Replay buffer started",
        obspython.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STOPPING: "Replay buffer stopping",
        obspython.OBS_FRONTEND_EVENT_REPLAY_BUFFER_STOPPED: "Replay buffer stopped",
        obspython.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED: "Replay buffer saved",
    }

    message = messages.get(event)
    
    if event == obspython.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED:
        replay_path = asyncio.run(get_last_replay_buffer_path())
        show_notification(message, replay_path)
    else:
        show_notification(message)

    if message:
        print(message)  


async def get_last_replay_buffer_path():
    client = simpleobsws.WebSocketClient("ws://localhost:4455")
    await client.connect()
    await client.wait_until_identified()

    result = await client.call(simpleobsws.Request("GetLastReplayBufferReplay"))
    await client.disconnect()

    if result.ok():
        print(f"Request succeeded! Response data: {result.responseData}")
        return result.responseData.get('savedReplayPath')
    else:
        print(f"Request failed! Error: {result.error}")
        return None
    

def script_load(settings):
    obspython.obs_frontend_add_event_callback(on_event)
