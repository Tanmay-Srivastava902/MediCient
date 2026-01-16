"""Test suite for apt_service.py"""
import services.apt_service as apt_service

def test_package_version():
    print("[TEST 1] _package_version for valid package")
    result = apt_service._package_version("python3")
    if result and getattr(result, 'ok', False):
        print(f"✔️ Version found: {result.data}")
    else:
        print(f"❌ Failed: {result}")

    print("[TEST 2] _package_version for invalid package")
    result = apt_service._package_version("notarealpackage")
    if not result or not getattr(result, 'ok', False):
        print(f"✔️ Correctly failed: {result}")
    else:
        print(f"❌ Unexpected success: {result}")

def test_is_package_installed():
    print("[TEST 3] is_package_installed for valid package")
    installed = apt_service.is_package_installed("ls")
    if installed:
        print("✔️ Package is installed")
    else:
        print("❌ Package should be installed")

    print("[TEST 4] is_package_installed for invalid package")
    installed = apt_service.is_package_installed("notarealpackage")
    if not installed:
        print("✔️ Package is not installed")
    else:
        print("❌ Unexpectedly found package")

def test_update_system_packages():
    print("[TEST 5] update_system_packages (dry run)")
    # WARNING: This will actually run 'apt update' if sudo_password is correct
    # For safety, use a dummy password and expect failure
    result = apt_service.update_system_packages(sudo_password="wrongpassword")
    if not result or not getattr(result, 'ok', False):
        print(f"✔️ Correctly failed to update: {result}")
    else:
        print(f"❌ Unexpected success: {result}")

def test_install_uninstall_system_package():
    print("[TEST 6] install_system_package (dry run)")
    # WARNING: This will actually try to install a package if sudo_password is correct
    # For safety, use a dummy password and expect failure
    result = apt_service.install_system_package(sudo_password="wrongpassword", package="sl")
    if not result or not getattr(result, 'ok', False):
        print(f"✔️ Correctly failed to install: {result}")
    else:
        print(f"❌ Unexpected success: {result}")

    print("[TEST 7] uninstall_system_package (dry run)")
    result = apt_service.uninstall_system_package(sudo_password="wrongpassword", package="sl")
    if not result or not getattr(result, 'ok', False):
        print(f"✔️ Correctly failed to uninstall: {result}")
    else:
        print(f"❌ Unexpected success: {result}")

def run_all():
    test_package_version()
    test_is_package_installed()
    test_update_system_packages()
    test_install_uninstall_system_package()
    print("All apt_service tests complete.")

if __name__ == "__main__":
    run_all()
