import os
import sys
from construct_email import render_email, send_email
from paper import ArxivPaper
from loguru import logger
from config import settings
from tqdm import tqdm


def test_email_sending():
    """Test email sending functionality with a sample paper."""

    # Test with empty papers list (no papers scenario)
    logger.info("Testing email rendering with no papers...")
    empty_html = render_email([])
    assert "No Papers Today" in empty_html, (
        "Empty email should contain 'No Papers Today' message"
    )
    logger.success("Empty email rendering test passed!")

    for receiver in tqdm(settings.RECEIVERS):
        send_email(
            sender=settings.SENDER,
            receiver=receiver,
            html=empty_html,
        )
        logger.info(
            "{} should be receiving an email from {} shortly!",
            receiver,
            settings.SENDER,
        )
    return 0


if __name__ == "__main__":
    sys.exit(test_email_sending())
