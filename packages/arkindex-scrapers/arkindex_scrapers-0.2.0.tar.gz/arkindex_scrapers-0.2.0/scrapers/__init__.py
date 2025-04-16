import logging

logging.basicConfig(
    format="%(asctime)s [%(levelname)s/%(name)s] %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Silence
logging.getLogger("arkindex.pagination").setLevel(logging.WARNING)
