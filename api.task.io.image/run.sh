#!/bin/bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload --timeout-keep-alive 180