"""Task scorers. Each returns a dict of named metrics in [0, 1] (higher is better),
plus a human-readable metric name mapping for the leaderboard.
"""

from . import reading, describing, linking, translating, faithfulness

SCORERS = {
    "reading": reading.score,
    "describing": describing.score,
    "linking": linking.score,
    "translating": translating.score,
    "faithfulness": faithfulness.score,
}
