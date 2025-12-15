import os

from dotenv import load_dotenv

load_dotenv()

import vertexai
from parent_and_subagents.agent import root_agent
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
STAGING_BUCKET = "gs://datasets-ccibt-hack25ww7-711"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

remote_app = agent_engines.create(
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]"
    ],
    env_vars=[],
    extra_packages=["adk_multiagent/parent_and_subagents"],
)

print(f"Remote app created: {remote_app.resource_name}")
