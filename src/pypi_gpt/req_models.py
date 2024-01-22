"""
No Constraint: Requirement declared without any version information.
`package`

Exact Match: Requirement declares specific version requirement.
`package==1.0.0`

At Least Version: Requirement specifies a minimum version.
`package>=1.0.0`

Less Than Version: Requirement specifies a maximum version.
`package<1.0.0`

Not Equal: Requirement specifies a version that should not be used.
`package!=1.0.0`

Version Range: Requirement specifies a range of versions.
`package>1.0.0,<2.0.0`

Compatible Version: Requirement specifies a compatible version.
`package~=1.0.0`

Extra Dependencies: Requirement includes extra dependencies and their versions.
`package[extra1,extra2]>=version`

Python Version Constraint: Requirement includes a Python version constraint.
`package; python_version<'3.0'`

Git Repository Dependency: Requirement for a package from a Git repository.
`git+https://git.repo/some_pkg.git@revision#egg=SomePackage`

Local Package Path: Requirement for a package from a local path.
`./lib/some-package`

Editable Requirement: Editable requirement specified with `-e` flag.
`-e .`

Comment: A comment explaining the reason for the version in the requirement.
`package==version # reason for the version`
"""

import re
from enum import StrEnum
from typing import List, Optional

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    field_validator,
)


class SemanticVersion(BaseModel):
    major: int = Field(0, description="Major version number.")
    minor: int = Field(0, description="Minor version number.")
    patch: int | None = Field(None, description="Patch version number.")

    def __str__(self):
        if self.patch is None:
            return f"{self.major}.{self.minor}"
        else:
            return f"{self.major}.{self.minor}.{self.patch}"

    @field_validator("major", "minor", "patch", mode="before")
    def validate_version_component(cls, v):
        if isinstance(v, int) and v >= 0:
            return v
        raise ValueError("Version components must be non-negative integers.")

    @classmethod
    def parse_version_string(cls, version_string: str) -> "SemanticVersion":
        pattern = r"^(\d+)\.(\d+)(?:\.(\d+))?$"
        match = re.match(pattern, version_string)
        if not match:
            raise ValueError(f"Invalid version string: {version_string}")

        major, minor, patch = match.groups()
        if patch is None:
            patch = 0

        return cls(major=int(major), minor=int(minor), patch=int(patch))


class VersionConstraintType(StrEnum):
    EXACT = "=="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    NOT_EQUAL = "!="
    WILDCARD = "~="
    NONE = "None"


class VersionConstraint(BaseModel):
    """
    Single version constraint.
    Requires both a type and version.
    If no constraints provided, use an empty list at the Requirements level.
    Split constraints into multiple objects.
    """

    type: VersionConstraintType | None = Field(
        ...,
        description="Type of version constraint.",
    )
    version: SemanticVersion | None = Field(
        None,
        example="1.0.0",
        description="The version specified in the constraint.",
    )

    @field_validator("version", mode="before")
    def convert_version_to_object(
        cls, value: str | SemanticVersion
    ) -> "SemanticVersion":
        if isinstance(value, str):
            return SemanticVersion.parse_version_string(version_string=value)
        else:
            return value


class Requirement(BaseModel):
    package: str = Field(
        ...,
        example="requests",
        description="The name of the package.",
    )
    constraints: List[VersionConstraint] = Field(
        ...,
        description="If no constraints provided, leave as an empty list. "
        "One entry per constraint. "
        "Split multiple constraints into multiple list items.",
        default_factory=list,
    )
    extras: List[str] = Field(
        None,
        example=["security", "socks"],
        description="List of extras for the package.",
    )
    env_marker: Optional[str] = Field(
        None,
        example="python_version<'3.4'",
        description="Environment marker for the package.",
    )
    git_url: Optional[HttpUrl] = Field(
        None,
        example="https://github.com/psf/requests.git",
        description="Git URL for the package.",
    )
    revision: Optional[str] = Field(
        None,
        example="master",
        description="Git revision for the package.",
    )
    egg: Optional[str] = Field(
        None,
        example="requests",
        description="Egg name for the package.",
    )
    file_path: Optional[str] = Field(
        None,
        example="./libs/MyLocalPackage",
        description="Local file path for the package.",
    )
    directory_path: Optional[str] = Field(
        None,
        example=".",
        description="Directory path for the package.",
    )
    comment: Optional[str] = Field(
        None,
        example="Stable version",
        description="Comment or note regarding the requirement.",
    )

    def generate_requirement_string(self) -> str:
        """
        Generates the requirement string in its standard format.
        """
        parts = [self.package]

        if self.constraints:
            constraint_strings = [
                f"{constraint.type.value}{constraint.version}"
                for constraint in self.constraints
            ]
            parts.append(", ".join(constraint_strings))

        if self.extras:
            extras_string = ",".join(self.extras)
            parts[0] += f"[{extras_string}]"

        if self.env_marker:
            parts.append(f"; {self.env_marker}")

        if self.git_url:
            parts.append(f"@ {self.git_url}")
            if self.revision:
                parts[-1] += f"@{self.revision}"
            if self.egg:
                parts[-1] += f"#egg={self.egg}"

        if self.file_path:
            parts.append(f"@ {self.file_path}")

        if self.directory_path:
            parts.append(f"-e {self.directory_path}")

        return " ".join(parts)


class RequirementList(BaseModel):
    requirements: List[Requirement]

    def __len__(self):
        return len(self.root)
