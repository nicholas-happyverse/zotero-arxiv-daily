import os
import sys
from construct_email import render_email, send_email
from paper import ArxivPaper
from loguru import logger


def test_email_sending():
    """Test email sending functionality with a sample paper."""

    # Test with empty papers list (no papers scenario)
    logger.info("Testing email rendering with no papers...")
    empty_html = render_email([])
    assert "No Papers Today" in empty_html, (
        "Empty email should contain 'No Papers Today' message"
    )
    logger.success("Empty email rendering test passed!")

    # Test email sending if environment variables are configured
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    sender = os.getenv("SENDER")
    receivers = str(os.getenv("RECEIVER")).split(",")
    sender_password = os.getenv("SENDER_PASSWORD")
    assert smtp_server is not None, "SMTP_SERVER is not set"
    assert smtp_port is not None, "SMTP_PORT is not set"
    assert sender is not None, "SENDER is not set"
    assert receivers is not None, "RECEIVER is not set"
    assert sender_password is not None, "SENDER_PASSWORD is not set"

    if all([smtp_server, smtp_port, sender, receivers, sender_password]):
        logger.info("Testing email sending...")
        try:
            for receivee in receivers:
                send_email(
                    sender=sender,
                    receiver=receivee,
                    password=sender_password,
                    smtp_server=smtp_server,
                    smtp_port=int(smtp_port),
                    html=empty_html,
                )
            logger.success("Email sent successfully!")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            sys.exit(1)
    else:
        logger.warning("Email sending skipped - missing environment variables")
        logger.info(
            "Required variables: SMTP_SERVER, SMTP_PORT, SENDER, RECEIVER, SENDER_PASSWORD"
        )

    logger.info("All tests completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(test_email_sending())
