00:22:a3:00:00:3a:5f:d2: office lights
a4:c1:38:ba:24:61:f7:46: office shades left
a4:c1:38:89:3d:9f:22:c1: office shades right
a4:c1:38:ac:c5:49:25:31: in-law bedroom shades east
a4:c1:38:56:dc:79:31:c9: in-law living room shades west
a4:c1:38:d4:26:fe:7d:d3: in-law bedroom shades north
a4:c1:38:bb:8f:00:c0:62: in-law bedroom shades west
a4:c1:38:d3:a0:e2:a8:f6: in-law living room shades east

from <https://github.com/zigpy/zigpy-cli/pull/2>
found through this video: <https://www.youtube.com/watch?v=ql58ZfXso1M>
I ran
```
docker exec -it home-assistant_server_1 bash

# Install HA OS packages (only if using HA OS)
apk add gcc musl-dev libffi-dev

# Install modified versions of zigpy, zigpy-znp, zigpy-deconz, bellows, and the new zigpy-cli
pip install \
    'zigpy>=0.47.0' \
    'zigpy-znp>=0.8.0' \
    'zigpy-deconz>=0.17.0' \
    git+https://github.com/puddly/zigpy-cli.git@puddly/zigpy-radio-api \
    git+https://github.com/puddly/bellows.git@puddly/zigpy-radio-api

zigpy -vv radio znp /dev/sonoff backup /config/sonoff.json

```

then later
```
zigpy -vv radio znp /dev/sonoff restore /config/sonoff-changed.json
```

full error
```
2022-06-25 09:02:20 DEBUG (MainThread) [zigpy_znp.zigbee.application] Request failed (Unsuccessful request status code: <Status.NWK_NO_ROUTE: 205>), retry attempt 3 of 5
2022-06-25 09:02:20 DEBUG (MainThread) [zigpy_znp.zigbee.application] Request failed (Unsuccessful request status code: <Status.MAC_NO_ACK: 233>), retry attempt 3 of 5
2022-06-25 09:02:20 DEBUG (MainThread) [zigpy_znp.api] Received command: AF.DataConfirm.Callback(Status=<Status.NWK_NO_ROUTE: 205>, Endpoint=1, TSN=41)
2022-06-25 09:02:20 DEBUG (MainThread) [zigpy_znp.zigbee.application] Request failed (Unsuccessful request status code: <Status.NWK_NO_ROUTE: 205>), retry attempt 5 of 5



2022-06-25 07:10:04 WARNING (MainThread) [homeassistant.components.zha.core.channels.base] [0xAD5A:1:0x0006]: async_initialize: all attempts have failed: [DeliveryError('Request failed after 5 attempts: <Status.APS_NO_ACK: 183>'), DeliveryError('Request failed after 5 attempts: <Status.APS_NO_ACK: 183>'), DeliveryError('Request failed after 5 attempts: <Status.APS_NO_ACK: 183>'), DeliveryError('Request failed after 5 attempts: <Status.APS_NO_ACK: 183>')]

2022-06-25 07:09:45 WARNING (MainThread) [homeassistant.components.zha.core.channels.base] [0x03EE:1:0x0006]: async_initialize: all attempts have failed: [DeliveryError('Request failed after 5 attempts: <Status.NWK_NO_ROUTE: 205>'), DeliveryError('Request failed after 5 attempts: <Status.NWK_NO_ROUTE: 205>'), DeliveryError('Request failed after 5 attempts: <Status.NWK_NO_ROUTE: 205>'), DeliveryError('Request failed after 5 attempts: <Status.NWK_NO_ROUTE: 205>')]
2022-06-25 07:09:45 DEBUG (MainThread) [homeassistant.compon
```

new try from <https://github.com/zigpy/zigpy-znp/blob/dev/TOOLS.md#linux>

```
docker exec home-assistant python -m zigpy_znp.tools.network_scan -a -c 15 /dev/sonoff

docker exec home-assistant python -m zigpy_znp.tools.nvram_reset /dev/sonoff
docker exec home-assistant python -m zigpy_znp.tools.nvram_read /dev/sonoff -o /config/sonoff-backup/sonoff-nvram-$(date +%s).json
docker exec home-assistant python -m zigpy_znp.tools.network_backup /dev/sonoff -o /config/sonoff-backup/sonoff-network-$(date +%s).json

```

it didn't work again in the morning. All I did is disable the zigbee integration, did stuff for like 10 minutes and re-enabled it.

Some shades connected after I dropped others for some reason.

I moved the in-law bedroom shades to in-law living room and tried connecting via multiple routers.
