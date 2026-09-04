"""Low-overhead process diagnostics loaded automatically by Python."""

import faulthandler
import signal


# Operators can capture all Python thread stacks with `docker kill --signal=USR1
# mem0-dev-mem0-1`. The handler is dormant until explicitly triggered and does
# not include request bodies or local variables.
faulthandler.register(signal.SIGUSR1, all_threads=True)
