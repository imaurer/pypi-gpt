from pypi_gpt.req_models import (
    SemanticVersion,
    Requirement,
    VersionConstraint,
    VersionConstraintType,
)


def test_exact_version():
    req = Requirement(
        package="requests",
        constraints=[
            VersionConstraint(
                type=VersionConstraintType.EXACT,
                version="2.25.1",
            )
        ],
    )
    assert req.generate_requirement_string() == "requests ==2.25.1"


def test_version_range():
    req = Requirement(
        package="Django",
        constraints=[
            VersionConstraint(
                type=VersionConstraintType.GREATER_THAN,
                version="3.0.0",
            ),
            VersionConstraint(
                type=VersionConstraintType.LESS_THAN,
                version="3.1.0",
            ),
        ],
    )
    assert req.generate_requirement_string() == "Django >3.0.0, <3.1.0"


def test_wildcard_version():
    req = Requirement(
        package="matplotlib",
        constraints=[
            VersionConstraint(
                type=VersionConstraintType.WILDCARD,
                version="3.3.0",
            )
        ],
    )
    assert req.generate_requirement_string() == "matplotlib ~=3.3.0"


def test_extras():
    req = Requirement(package="requests", extras=["security", "socks"])
    assert req.generate_requirement_string() == "requests[security,socks]"


def test_environment_marker():
    req = Requirement(package="pathlib2", env_marker="python_version<'3.4'")
    assert (
        req.generate_requirement_string() == "pathlib2 ; python_version<'3.4'"
    )


def test_git_repository():
    req = Requirement(
        package="requests",
        git_url="https://github.com/psf/requests.git",
        revision="master",
        egg="requests",
    )
    assert (
        req.generate_requirement_string()
        == "requests @ https://github.com/psf/requests.git@master#egg=requests"
    )


def test_local_file_path():
    req = Requirement(
        package="MyLocalPackage", file_path="./libs/MyLocalPackage"
    )
    assert (
        req.generate_requirement_string()
        == "MyLocalPackage @ ./libs/MyLocalPackage"
    )


def test_editable_local_directory():
    req = Requirement(package="MyLocalPackage", directory_path=".")
    assert req.generate_requirement_string() == "MyLocalPackage -e ."


# Additional tests for other scenarios and combinations can be added similarly.


# Example Usage
def test_roundtrip_version_string():
    version = SemanticVersion.parse_version_string("1.2.3")
    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 3
    assert str(version) == "1.2.3"
