# Copyright (C) 2025 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

import json
import os
import re
import unicodedata

from lib4package.metadata import Metadata
from lib4sbom.data.document import SBOMDocument
from lib4sbom.data.package import SBOMPackage
from lib4sbom.data.relationship import SBOMRelationship
from lib4sbom.license import LicenseScanner


class PHPScanner:
    """
    Simple php File Scanner.
    """

    DEFAULT_LICENCE = "NOASSERTION"
    DEFAULT_AUTHOR = "UNKNOWN"
    DEFAULT_PARENT = "-"
    VERSION_UNKNOWN = "NA"
    LOCK_FILE = "composer.lock"

    def __init__(self, debug, application="PHP_dummy", release=""):
        self.record = []
        self.packages = []
        self.php_file = None
        self.module_data = {}
        self.debug = debug
        self.php_package = SBOMPackage()
        self.php_relationship = SBOMRelationship()
        self.sbom_document = SBOMDocument()
        self.php_packages = {}
        self.php_relationships = []
        self.license = LicenseScanner()
        self.package_metadata = Metadata("php", debug=self.debug)
        self.lock_file = None
        self.sbom_document.set_value("lifecycle", "build")
        self.sbom_document.set_metadata_type("application")
        self.application_name = application
        self.application_release = release
        self.dependency_list = []

    def set_dependency_file(self, dependency_file):
        # lock_file = self.LOCK_FILE
        self.dependency_file = dependency_file
        self.module_valid = False
        if self.debug:
            print(f"Process {self.dependency_file}")
        if os.path.exists(self.dependency_file):
            # Load data from file
            with open(os.path.abspath(self.dependency_file), "r") as file_handle:
                self.module_data = json.load(file_handle)
            self.lock_file = self.dependency_file
            if self.debug:
                print(json.dumps(self.module_data, indent=2))
        elif self.debug:
            print(f"No {self.dependency_file} not found")

    def _format_supplier(self, supplier_info, include_email=True):
        # See https://stackoverflow.com/questions/1207457/convert-a-unicode-string-to-a-string-in-python-containing-extra-symbols
        # And convert byte object to a string
        name_str = (
            unicodedata.normalize("NFKD", supplier_info)
            .encode("ascii", "ignore")
            .decode("utf-8")
        )
        if " " in name_str:
            # Get names assumed to be at least two names <first> <surname>
            names = re.findall(r"[a-zA-Z\.\]+ [A-Za-z]+ ", name_str)
        else:
            # Handle case where only single name provided
            names = [name_str]
        # Get email addresses
        if self.debug:
            print(f"{supplier_info} => {name_str} => {names}")
        # Use RFC-5322 compliant regex (https://regex101.com/library/6EL6YF)
        emails = re.findall(
            r"((?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))",
            supplier_info,
            re.IGNORECASE,
        )
        supplier = " ".join(n for n in names)
        if include_email and len(emails) > 0:
            # Only one email can be specified, so choose last one
            supplier = supplier + "(" + emails[-1] + ")"
        return re.sub(" +", " ", supplier.strip())

    def _dependencies(self, module, parent):
        if self.debug:
            print(f"Process dependencies for {parent}: {module}")

        for entry in module:
            # To handle @actions/<product>: lines, extract product name from line
            product = entry.split("/")[1] if "/" in entry else entry
            # product = entry
            # Ignore product if not named
            if len(product) == 0:
                continue
            try:
                version = module[entry]["version"]
            except Exception:
                # Cater for case when version field not present
                version = "UNKNOWN"
            if version != "UNKNOWN":
                self.packages.append([product, version])
                self.add_entry(parent, product, version)
            else:
                if self.debug:
                    print(f"Version not found for {product}")
                # Add relationship once all modules defined
                self.dependency_list.append([parent, product])
        for entry in module:
            product = entry.split("/")[1] if "/" in entry else entry
            # product = entry
            if self.debug:
                print(f"Process {product}")
            # Ignore product if not named
            if len(product) == 0:
                continue
            for x in module[entry]:
                if "dependencies" in x:
                    self._dependencies(module[entry]["dependencies"], product)
                if "requires" in x:
                    for dep in module[entry]["requires"]:
                        dep_version = self.VERSION_UNKNOWN
                        # dep_package = dep.split("/")[1] if "/" in dep else dep
                        dep_package = dep
                        if self.debug:
                            print(f"Search for {dep_package}")
                        package = self.get_package(dep_package)
                        if package is None:
                            if self.debug:
                                print(f"Dependent package {dep_package} not defined")
                            dep_package = None
                        else:
                            dep_version = package[2]
                        if dep_package is not None:
                            self.add_entry(product, dep_package, dep_version)

    def show_module(self):
        print(self.module_data)

    def process_dependency(self):
        # If file not found, no metadata to process
        if len(self.module_data) > 0:
            self.packages.append([self.application_name, self.application_release])
            self.sbom_document.set_name(self.application_name)
            self.add_entry(
                self.DEFAULT_PARENT,
                {"name": self.application_name, "version": self.application_release},
                package_type="APPLICATION",
            )
            self.module_valid = True

            # Note exclude development dependencies
            packages = self.module_data.get("packages", [])

            for package in packages:
                component = {
                    "name": package.get("name"),
                    "version": package.get("version"),
                    "type": package.get("type"),
                    "description": package.get("description"),
                    "homepage": package.get("homepage"),
                    "license": package.get("license"),
                    "authors": package.get("authors"),
                    "dist": package.get("dist"),
                    "source": package.get("source"),
                    "require": package.get("require"),
                    "require-dev": package.get("require-dev"),
                    "replace": package.get("replace"),
                    "provide": package.get("provide"),
                    "suggest": package.get("suggest"),
                    "conflict": package.get("conflict"),
                    "funding": package.get("funding"),
                    "time": package.get("time"),
                }

                # Normalise license to a list of strings
                if isinstance(component["license"], str):
                    component["license"] = [component["license"]]
                elif component["license"] is None:
                    component["license"] = []

                parent = self.application_name

                self.add_entry(parent, component)

            # Add dependencies
            for entry in self.dependency_list:
                parent = entry[0]
                name = entry[1]
                self._add_relationship(parent, name)
        elif self.debug:
            print(f"[ERROR] File {self.dependency_file} not found")

    def add(self, entry):
        if entry not in self.record:
            self.record.append(entry)

    def get_package(self, name, version=None):
        for package in self.record:
            if version is None and name == package[1]:
                return package
            elif name == package[1] and version == package[2]:
                return package
        return None

    def _add_relationship(self, parent, name):
        self.php_relationship.initialise()
        if parent != self.DEFAULT_PARENT:
            if self.debug:
                print(f"Add relationship {parent} DEPENDS ON {name}")

            self.php_relationship.set_relationship(parent, "DEPENDS_ON", name)
        else:
            if self.debug:
                print(f"Add relationship {parent} DESCRIBES {name}")
            self.php_relationship.set_relationship(
                self.application_name, "DESCRIBES", name
            )
        self.php_relationships.append(self.php_relationship.get_relationship())

    def add_entry(self, parent, component, package_type="LIBRARY"):
        name = component["name"]
        version = component["version"]
        p = (name, version)
        if p not in self.php_packages:
            self.php_package.initialise()
            self.php_package.set_name(name)
            self.php_package.set_version(version)
            self.php_package.set_property("language", "php")
            self.php_package.set_type(package_type)
            self.php_package.set_evidence(self.lock_file)
            originator = component.get("authors")
            description = component.get("description")
            package_licence = component.get("license")
            homepage = component.get("homepage")
            download_location = component.get("source")
            self.php_package.set_filesanalysis(False)
            # Assume supplier not known
            self.php_package.set_supplier("UNKNOWN", "NOASSERTION")
            if originator is not None:
                originator = originator[0]["name"]
                if len(originator.split()) > 3:
                    self.php_package.set_supplier(
                        "Organization", self._format_supplier(originator)
                    )
                elif len(originator) > 1:
                    if self.debug:
                        print(f"{originator} => {self._format_supplier(originator)}")
                    self.php_package.set_supplier(
                        "Person", self._format_supplier(originator)
                    )
                component_supplier = self._format_supplier(
                    originator, include_email=False
                )
                if version is not None:
                    cpe_version = version.replace(":", "\\:")
                else:
                    cpe_version = ""
                self.php_package.set_cpe(
                    f"cpe:2.3:a:{component_supplier.replace(' ', '_').lower()}:{name}:{cpe_version}:*:*:*:*:*:*:*"
                )
            if package_licence is not None:
                package_licence = package_licence[0]
                license = self.license.find_license(package_licence)
                if self.debug:
                    print(f"{package_licence} => {license}")
                # If not valid SPDX, report NOASSERTION
                if license != package_licence:
                    self.php_package.set_licensedeclared("NOASSERTION")
                else:
                    self.php_package.set_licensedeclared(license)
                # Report license if valid SPDX identifier
                self.php_package.set_licenseconcluded(license)
                # Add comment if metadata license was modified
                license_comment = ""
                if len(package_licence) > 0 and license != package_licence:
                    license_comment = f"{name} declares {package_licence} which is not currently a valid SPDX License identifier or expression."
                # Report if license is deprecated
                if self.license.deprecated(license):
                    deprecated_comment = f"{license} is now deprecated."
                    if len(license_comment) > 0:
                        license_comment = f"{license_comment} {deprecated_comment}"
                    else:
                        license_comment = deprecated_comment
                if len(license_comment) > 0:
                    self.php_package.set_licensecomments(license_comment)
            else:
                self.php_package.set_licenseconcluded(self.DEFAULT_LICENCE)
                self.php_package.set_licensedeclared(self.DEFAULT_LICENCE)
            # if checksum is not None:
            #     self.php_package.set_checksum(checksum_algorithm, checksum)
            if homepage is not None:
                self.php_package.set_homepage(homepage)
            if download_location is not None:
                self.php_package.set_downloadlocation(download_location.get("url"))
            if description is not None:
                self.php_package.set_summary(description)
            if package_type == "LIBRARY":
                self.php_package.set_externalreference(
                    "PACKAGE-MANAGER", "purl", f"pkg:composer/{name}@{version}"
                )
            # Copyright
            self.php_package.set_copyrighttext("NOASSERTION")
            if component.get("time") is not None:
                self.php_package.set_value("release_date", component.get("time"))

            try:
                self.package_metadata.get_package(name, version)
                checksum, checksum_algorithm = self.package_metadata.get_checksum(
                    version=version
                )
                if checksum is not None:
                    self.php_package.set_checksum(checksum_algorithm, checksum)
            except Exception as ex:
                if self.debug:
                    print(f"[ERROR] Unable to retrieve metadata for {name} - {ex}")

            self.php_packages[(name, version)] = self.php_package.get_package()

            # Add dependencies
            if component.get("require") is not None:
                for p, v in component["require"].items():
                    self.dependency_list.append([name, p])

        # Record relationship
        self._add_relationship(parent, name)

    def get_record(self):
        return self.record

    def get_packages(self):
        return self.php_packages

    def get_relationships(self):
        return self.php_relationships

    def get_document(self):
        return self.sbom_document.get_document()

    def get_application_name(self):
        return self.application_name

    def get_lock_file(self):
        return self.lock_file

    def valid_module(self):
        return self.module_valid

    def show_record(self):
        for r in self.record:
            print(r)
