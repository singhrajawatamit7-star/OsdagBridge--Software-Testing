# Official OsdagBridge source checkout

The official desktop application source is maintained separately by the OsdagBridge
project. It is intentionally not copied into this QA repository as a second,
independently editable source tree.

- Upstream repository: https://github.com/osdagbridge/OsdagBridge-Desktop
- Default upstream branch: `main`
- Reproducible source revision pinned for this QA project:
  `f62ceba7f3324431c76d92184ef61da9cd265731`
- Local checkout destination: `vendor/OsdagBridge-Desktop/`

## Fetch the official source

From the QA repository root, with Git installed and network access available:

```bash
python scripts/checkout_official_osdagbridge.py
```

To use a different verified upstream commit:

```bash
python scripts/checkout_official_osdagbridge.py --commit <full-commit-sha>
```

The script checks out a detached, pinned revision and verifies the resulting
commit SHA. It refuses to overwrite a non-empty destination. The downloaded
source directory is ignored by Git so upstream application files are not
accidentally committed into this QA repository.

## Important testing boundary

Fetching source is not the same as installing or launching the desktop
application. Follow the upstream installation instructions in the checkout
before running application-level tests. Record the exact checked-out SHA,
environment, command, result, and genuine evidence in the test execution log.
Do not mark a manual test as passed merely because the source was downloaded.
