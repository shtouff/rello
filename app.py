import glob
import os
import tempfile

import uvicorn


def init_prometheus_multiproc(path: str):
    if not os.path.isdir(path):
        os.mkdir(path)
    for filepath in glob.glob(os.path.join(path, "*.db")):
        os.remove(filepath)


if __name__ == "__main__":
    prometheus_multiproc = os.environ.get(
        "PROMETHEUS_MULTIPROC_DIR",
        tempfile.mkdtemp(prefix="prometheus_multiproc_", dir=tempfile.gettempdir()),
    )
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = prometheus_multiproc
    init_prometheus_multiproc(prometheus_multiproc)

    uvicorn.run(
        "rello.main:app",
        host="0.0.0.0",
        port=8000,
        workers=os.cpu_count() * 2 + 1,
    )
