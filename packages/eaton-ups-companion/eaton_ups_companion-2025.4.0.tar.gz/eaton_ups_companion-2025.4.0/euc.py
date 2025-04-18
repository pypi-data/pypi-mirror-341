import asyncio
import sys
import datetime
from eaton_ups_companion import EUCClient

async def listen_for_exit(stop_event: asyncio.Event):
    loop = asyncio.get_event_loop()
    while True:
        await loop.run_in_executor(None, sys.stdin.readline)
        stop_event.set()
        print("Exit signal received. Quitting gracefully...")
        break

async def main():
    sys.stdout.write("\033[H\033[J")
    stop_event = asyncio.Event()
    
    # Start the exit listener task.
    exit_listener = asyncio.create_task(listen_for_exit(stop_event))

    client = EUCClient("http://localhost:4679/euc-data.js")
    
    print("Fetching full data...")
    try:
        response = await client.fetch_data()
        dt_local = datetime.datetime.fromtimestamp(response.lastUpdate / 1000)
        print("Initial load:")
        print(f"  Last Update: {dt_local.strftime("%Y-%m-%d %H:%M:%S")}")
        print("  Full Status:")
        print(f"    outputPower:     {response.status.outputPower} W")
        print(f"    outputLoadLevel: {response.status.outputLoadLevel} %")
        print(f"    energy:          {response.status.energy/3600000:.2f} kWh")
        print(f"    batteryRunTime:  {response.status.batteryRunTime/60:.2f} min")
        print("Press 'Enter' to quit.", flush=True)
        sys.stdout.flush()
        await asyncio.sleep(1)
        while not stop_event.is_set():
            await client.update_data(response)
            dt_local = datetime.datetime.fromtimestamp(response.lastUpdate / 1000)
            sys.stdout.write("\033[H\033[J")
            # Now simulate a second call with a patch update.
            print("Fetching patch update...")            
            print("After patch update:")
            print(f"  Last Update: {dt_local.strftime("%Y-%m-%d %H:%M:%S")}")
            print("  Updated Status:")
            print(f"    outputPower:     {response.status.outputPower} W")
            print(f"    outputLoadLevel: {response.status.outputLoadLevel} %")
            print(f"    energy:          {response.status.energy/3600000:.2f} kWh")
            print(f"    batteryRunTime:  {response.status.batteryRunTime/60:.2f} min")
            print("Press 'Enter' to quit.", flush=True)
            sys.stdout.flush()
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
    await exit_listener


if __name__ == "__main__":
    asyncio.run(main())