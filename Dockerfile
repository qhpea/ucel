from python:3-slim as daemon
ENV UCEL_FABRIC_BASE = "/mnt/ucel"
VOLUME $UCEL_FABRIC_BASE
RUN pip install ucel ucel-aml ucel-docker