from dataclasses import dataclass
from typing import Dict, Any
from . import Logs, SysInfo, SystemCfg, ShutdownCfg, DeviceInfo, Status, PowerSourceCfg

@dataclass
class EUCResponse:
    logs: Logs
    lastUpdate: int
    lastPurge: int
    sysInfo: SysInfo
    labels: Dict[str, str]
    systemCfg: SystemCfg
    shutdownCfg: ShutdownCfg
    deviceInfo: DeviceInfo
    status: Status
    powerSourceCfg: PowerSourceCfg

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EUCResponse":
        return cls(
            logs=Logs.from_dict(data["logs"]),
            lastUpdate=data["lastUpdate"],
            lastPurge=data["lastPurge"],
            sysInfo=SysInfo.from_dict(data["sysInfo"]),
            labels=data["labels"],
            systemCfg=SystemCfg.from_dict(data["systemCfg"]),
            shutdownCfg=ShutdownCfg.from_dict(data["shutdownCfg"]),
            deviceInfo=DeviceInfo.from_dict(data["deviceInfo"]),
            status=Status.from_dict(data["status"]),
            powerSourceCfg=PowerSourceCfg.from_dict(data["powerSourceCfg"])
        )

    def patch(self, patch_data: Dict[str, Any]) -> None:
        """
        Update the current object with only the fields provided in patch_data.
        For example, if patch_data contains a new 'lastUpdate' and updates for 'status',
        those fields will be updated on this instance.
        """
        if "lastUpdate" in patch_data:
            self.lastUpdate = patch_data["lastUpdate"]
        if "logs" in patch_data:
            # Extend this if patch updates for logs are expected.
            pass
        if "sysInfo" in patch_data:
            # Extend if needed.
            pass
        if "status" in patch_data:
            status_patch = patch_data["status"]
            for key, value in status_patch.items():
                if hasattr(self.status, key):
                    setattr(self.status, key, value)
        # Add patches for other fields if future updates include them.