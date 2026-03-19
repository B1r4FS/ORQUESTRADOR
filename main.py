import argparse
import os
from datetime import datetime, timezone
from pathlib import Path

import yaml
from dotenv import load_dotenv

from connectors.dehashed import DeHashedConnector
from connectors.harvester import TheHarvesterConnector
from connectors.holehe import HoleheConnector
from connectors.spiderfoot import SpiderFootConnector
from connectors.misp_exporter import MISPExporter
from connectors.opencti_exporter import OpenCTIExporter

from models import Indicator
from report import build_summary, write_outputs
from scoring import apply_scoring
from utils import dedupe, load_targets, logger


def parse_args():
    parser = argparse.ArgumentParser(description="Threat Intelligence Orchestrator")

    parser.add_argument("--targets", required=True)
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--output-dir", default="outputs/latest")

    parser.add_argument(
        "--enable",
        default="harvester,holehe",
        help="harvester, spiderfoot, holehe, dehashed",
    )

    parser.add_argument("--export-misp", action="store_true")
    parser.add_argument("--export-opencti", action="store_true")

    return parser.parse_args()


def build_connectors(enabled: set[str]):
    connectors = []

    if "harvester" in enabled:
        connectors.append(TheHarvesterConnector(binary_path="theHarvester"))

    if "spiderfoot" in enabled:
        connectors.append(SpiderFootConnector(binary_path="spiderfoot"))

    if "holehe" in enabled:
        connectors.append(HoleheConnector(binary_path="holehe"))

    if "dehashed" in enabled and os.getenv("DEHASHED_API_KEY"):
        connectors.append(
            DeHashedConnector(
                email=os.getenv("DEHASHED_EMAIL"),
                api_key=os.getenv("DEHASHED_API_KEY"),
            )
        )

    return connectors


def main():
    load_dotenv()
    args = parse_args()

    config = yaml.safe_load(Path(args.config).read_text())
    organization = config.get("organization", "Unknown")

    targets = load_targets(args.targets)
    enabled = {x.strip() for x in args.enable.split(",")}

    connectors = build_connectors(enabled)

    logger.info("Targets: %s", targets)
    logger.info("Connectors: %s", [c.name for c in connectors])

    findings: list[Indicator] = []

    for connector in connectors:
        try:
            results = connector.collect(targets, organization)
            findings.extend(results)
        except Exception as e:
            logger.warning("Connector failed: %s", e)

    findings = [apply_scoring(f) for f in findings]
    findings = dedupe(findings)

    summary = build_summary(datetime.now(timezone.utc), organization, findings)

    write_outputs(args.output_dir, organization, findings, summary)

    logger.info("Finished successfully")


if __name__ == "__main__":
    main()
