# retry-shield-lab

Backoff/retry utility demo — jittered exponential backoff policies for pacing retries against flaky services.

## Project Status

**prototype** — early-stage demo code, not production-ready. APIs and behavior may change without notice.

## Contact

- **Hezi Liu** — project owner / maintainer

## Overview

This repo demos a small, self-contained backoff policy module that computes retry delays with full-jitter exponential backoff, so retries against flaky dependencies don't stampede them.
