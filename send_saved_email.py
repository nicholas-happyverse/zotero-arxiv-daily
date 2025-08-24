import argparse
import os
import sys
from dotenv import load_dotenv
from construct_email import send_email
from loguru import logger
from tqdm import tqdm
from config import settings

load_dotenv(override=True)

parser = argparse.ArgumentParser(description="Send previously generated email HTML")


def add_argument(*args, **kwargs):
    def get_env(key: str, default=None):
        # handle environment variables generated at Workflow runtime
        # Unset environment variables are passed as '', we should treat them as None
        v = os.environ.get(key)
        if v == "" or v is None:
            return default
        return v

    parser.add_argument(*args, **kwargs)
    arg_full_name = kwargs.get("dest", args[-1][2:])
    env_name = arg_full_name.upper()
    env_value = get_env(env_name)
    if env_value is not None:
        # convert env_value to the specified type
        if kwargs.get("type") == bool:
            env_value = env_value.lower() in ["true", "1"]
        else:
            env_value = kwargs.get("type")(env_value)
        parser.set_defaults(**{arg_full_name: env_value})


if __name__ == "__main__":
    add_argument("--smtp_server", type=str, help="SMTP server")
    add_argument("--smtp_port", type=int, help="SMTP port")
    add_argument("--sender", type=str, help="Sender email address")
    add_argument("--receiver", type=str, help="Receiver email address")
    add_argument("--sender_password", type=str, help="Sender email password")
    add_argument(
        "--input_file",
        type=str,
        help="Input HTML file path",
        default="email.html",
    )
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    args = parser.parse_args()

    if settings.DEBUG:
        logger.remove()
        logger.add(sys.stdout, level="DEBUG")
        logger.debug("Debug mode is on.")
    else:
        logger.remove()
        logger.add(sys.stdout, level="INFO")

    # Check if no_email.flag exists
    if os.path.exists("no_email.flag"):
        logger.info("no_email.flag found - skipping email send.")
        exit(0)

    # Check if HTML file exists
    if not os.path.exists(args.input_file):
        logger.error(f"HTML file {args.input_file} not found!")
        exit(1)

    # Read HTML from file
    logger.info(f"Reading HTML from {args.input_file}...")
    with open(args.input_file, "r", encoding="utf-8") as f:
        html = f.read()

    logger.info(f"Sending email to {len(settings.RECEIVERS)} recipient(s)...")
    for receivee in tqdm(settings.RECEIVERS):
        send_email(
            settings.SENDER,
            receivee,
            html,
        )
    logger.success(
        "Email sent successfully! If you don't receive the email, please check the configuration and the junk box."
    )
