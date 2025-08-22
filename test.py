import os
import sys
from construct_email import render_email, send_email
from paper import ArxivPaper
from loguru import logger


def test_email_sending():
    """Test email sending functionality with a sample paper."""

    # Create a test paper
    test_paper = ArxivPaper(
        arxiv_id="2401.00001",
        url="https://arxiv.org/abs/2401.00001",
        pdf_url="https://arxiv.org/pdf/2401.00001.pdf",
        title="Test Paper for Email Functionality",
        abstract="This is a test abstract for testing the email sending functionality.",
        code_url=None,
        tldr="This is a test paper to verify email sending works correctly.",
        score=8.5,
    )

    # Set test authors
    class Author:
        def __init__(self, name):
            self.name = name

    test_paper.authors = [Author("Test Author 1"), Author("Test Author 2")]
    test_paper.affiliations = ["Test University", "Research Institute"]

    # Test with empty papers list (no papers scenario)
    logger.info("Testing email rendering with no papers...")
    empty_html = render_email([])
    assert "No Papers Today" in empty_html, (
        "Empty email should contain 'No Papers Today' message"
    )
    logger.success("Empty email rendering test passed!")

    # Test with one paper
    logger.info("Testing email rendering with one paper...")
    html = render_email([test_paper])
    assert test_paper.title in html, (
        f"Email should contain paper title: {test_paper.title}"
    )
    assert test_paper.arxiv_id in html, (
        f"Email should contain arxiv ID: {test_paper.arxiv_id}"
    )
    logger.success("Email rendering with paper test passed!")

    # Test email sending if environment variables are configured
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    sender = os.getenv("SENDER")
    receiver = os.getenv("RECEIVER")
    sender_password = os.getenv("SENDER_PASSWORD")

    if all([smtp_server, smtp_port, sender, receiver, sender_password]):
        logger.info("Testing email sending...")
        try:
            send_email(
                sender=sender,
                receiver=receiver,
                password=sender_password,
                smtp_server=smtp_server,
                smtp_port=int(smtp_port),
                html=html,
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
