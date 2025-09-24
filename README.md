# FastAPI S3 Bridge

A minimal FastAPI service that generates presigned Amazon S3 upload URLs and
corresponding public object URLs. It is intended as a small bridge between a
frontend and S3 so client applications can upload files directly to S3 without
exposing long-lived credentials.

This repository contains the FastAPI application and a few helper scripts for
local development and deployment.