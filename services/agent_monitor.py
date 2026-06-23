import json
import os
from datetime import datetime


LOG_FILE = "logs/agent_logs.json"


def log_agent(
    agent_name,
    execution_time,
    status
):

    os.makedirs(
        "logs",
        exist_ok=True
    )

    log = {
        "timestamp": str(datetime.now()),
        "agent": agent_name,
        "execution_time": round(
            execution_time,
            3
        ),
        "status": status
    }

    logs = []

    if os.path.exists(LOG_FILE):

        try:

            with open(
                LOG_FILE,
                "r"
            ) as f:

                logs = json.load(f)

        except:
            logs = []

    logs.append(log)

    with open(
        LOG_FILE,
        "w"
    ) as f:

        json.dump(
            logs,
            f,
            indent=4
        )