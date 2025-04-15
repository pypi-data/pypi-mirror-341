# Copyright (C) 2025 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

import argparse
import sys
import textwrap
from collections import ChainMap

from lib4sbom.generator import SBOMGenerator
from lib4sbom.sbom import SBOM

from sbom4php.scanner import PHPScanner
from sbom4php.version import VERSION

# CLI processing


def main(argv=None):

    argv = argv or sys.argv
    app_name = "sbom4php"
    parser = argparse.ArgumentParser(
        prog=app_name,
        description=textwrap.dedent(
            """
            SBOM4PHP generates a Software Bill of Materials for
            a PHP application identifying all of the dependent components.
            """
        ),
    )
    input_group = parser.add_argument_group("Input")
    input_group.add_argument(
        "-d",
        "--dependency",
        action="store",
        default="",
        help="PHP dependency file",
    )
    input_group.add_argument(
        "--application",
        action="store",
        default="",
        help="application name",
    )
    input_group.add_argument(
        "--release",
        action="store",
        default="",
        help="application release",
    )

    output_group = parser.add_argument_group("Output")
    output_group.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="add debug information",
    )
    output_group.add_argument(
        "--sbom",
        action="store",
        default="spdx",
        choices=["spdx", "cyclonedx"],
        help="specify type of sbom to generate (default: spdx)",
    )
    output_group.add_argument(
        "--format",
        action="store",
        default="tag",
        choices=["tag", "json", "yaml"],
        help="format for SPDX software bill of materials (sbom) (default: tag)",
    )

    output_group.add_argument(
        "-o",
        "--output-file",
        action="store",
        default="",
        help="output filename (default: output to stdout)",
    )

    parser.add_argument("-V", "--version", action="version", version=VERSION)

    defaults = {
        "dependency": "",
        "application": "",
        "release": "",
        "output_file": "",
        "sbom": "spdx",
        "debug": False,
        "format": "tag",
    }

    raw_args = parser.parse_args(argv[1:])
    args = {key: value for key, value in vars(raw_args).items() if value}
    args = ChainMap(args, defaults)

    # Validate CLI parameters

    dependency_file = args["dependency"]

    if dependency_file == "":
        print("[ERROR] Missing dependency file")
        return -1

    if args["application"] == "" or args["release"] == "":
        print("[ERROR} Must specify application name and release")
        return -1

    if args["sbom"] == "spdx":
        bom_format = args["format"]
    else:
        bom_format = "json"

    if args["debug"]:
        print("SBOM type", args["sbom"])
        if args["sbom"] == "spdx":
            print("Format", bom_format)
        print("Output file", args["output_file"])
        print("Dependency File", dependency_file)
        print("Application", args["application"])
        print("Release", args["release"])

    sbom_scan = PHPScanner(
        args["debug"], application=args["application"], release=args["release"]
    )
    sbom_scan.set_dependency_file(dependency_file)
    sbom_scan.process_dependency()

    if args["debug"]:
        print("Valid module", sbom_scan.valid_module())
        sbom_scan.show_record()
        print(sbom_scan.get_relationships())

    # If file not found, abort processing
    if not sbom_scan.valid_module():
        return -1

    # Generate SBOM file

    php_sbom = SBOM()
    php_sbom.add_document(sbom_scan.get_document())
    php_sbom.add_packages(sbom_scan.get_packages())
    php_sbom.add_relationships(sbom_scan.get_relationships())
    php_sbom.set_property("language", "PHP")

    sbom_gen = SBOMGenerator(
        sbom_type=args["sbom"], format=bom_format, application=app_name, version=VERSION
    )
    sbom_gen.generate(
        project_name=f"PHP-{sbom_scan.get_application_name()}",
        sbom_data=php_sbom.get_sbom(),
        filename=args["output_file"],
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
