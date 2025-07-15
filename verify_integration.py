#!/usr/bin/env python3
"""Final verification script for the CodeCoverageAnalyzer integration."""

import os
import sys


def verify_backend_files():
    """Verify all backend files are correctly implemented."""
    print("🔍 Verifying Backend Implementation")
    print("=" * 50)

    # Check CodeCoverageAnalyzer module
    module_path = "backend/modules/code_coverage_analyzer.py"
    if not os.path.exists(module_path):
        print(f"❌ Missing: {module_path}")
        return False

    # Check module registration
    init_path = "backend/modules/__init__.py"
    if os.path.exists(init_path):
        with open(init_path, "r") as f:
            content = f.read()
            if "CodeCoverageAnalyzer" in content:
                print(
                    "✅ CodeCoverageAnalyzer registered in modules/__init__.py"
                )
            else:
                print(
                    "❌ CodeCoverageAnalyzer not found in modules/__init__.py"
                )
                return False
    else:
        print(f"❌ Missing: {init_path}")
        return False

    # Check schemas update
    schemas_path = "backend/schemas.py"
    if os.path.exists(schemas_path):
        with open(schemas_path, "r") as f:
            content = f.read()
            if "coverage_data" in content:
                print("✅ coverage_data field added to schemas.py")
            else:
                print("❌ coverage_data field not found in schemas.py")
                return False
    else:
        print(f"❌ Missing: {schemas_path}")
        return False

    # Check API update
    api_path = "backend/api.py"
    if os.path.exists(api_path):
        with open(api_path, "r") as f:
            content = f.read()
            if "coverage_data" in content:
                print("✅ coverage_data field added to api.py")
            else:
                print("❌ coverage_data field not found in api.py")
                return False
    else:
        print(f"❌ Missing: {api_path}")
        return False

    print("✅ All backend files verified")
    return True


def verify_frontend_files():
    """Verify all frontend files are correctly updated."""
    print("\n🔍 Verifying Frontend Implementation")
    print("=" * 50)

    # Check API types
    api_types_path = "frontend/src/api.ts"
    if os.path.exists(api_types_path):
        with open(api_types_path, "r") as f:
            content = f.read()
            if "coverage_data" in content:
                print("✅ coverage_data field added to frontend/src/api.ts")
            else:
                print(
                    "❌ coverage_data field not found in frontend/src/api.ts"
                )
                return False
    else:
        print(f"❌ Missing: {api_types_path}")
        return False

    # Check ChatHistory component
    chat_history_path = "frontend/src/components/ChatHistory.tsx"
    if os.path.exists(chat_history_path):
        with open(chat_history_path, "r") as f:
            content = f.read()
            if (
                "coverage_data" in content
                and "Code Coverage Analysis" in content
            ):
                print("✅ Coverage display added to ChatHistory.tsx")
            else:
                print("❌ Coverage display not found in ChatHistory.tsx")
                return False
    else:
        print(f"❌ Missing: {chat_history_path}")
        return False

    # Check App.tsx
    app_path = "frontend/src/App.tsx"
    if os.path.exists(app_path):
        with open(app_path, "r") as f:
            content = f.read()
            if "coverage_data: res.coverage_data" in content:
                print("✅ coverage_data passed to ChatMessage in App.tsx")
            else:
                print("❌ coverage_data not passed to ChatMessage in App.tsx")
                return False
    else:
        print(f"❌ Missing: {app_path}")
        return False

    print("✅ All frontend files verified")
    return True


def verify_integration():
    """Verify the integration points."""
    print("\n🔍 Verifying Integration Points")
    print("=" * 50)

    # Check if Docker containers are running
    import subprocess

    try:
        result = subprocess.run(
            ["docker", "compose", "ps"], capture_output=True, text=True
        )
        if "backend" in result.stdout and "frontend" in result.stdout:
            print("✅ Docker containers are running")
        else:
            print("❌ Docker containers not running properly")
            return False
    except Exception:
        print("❌ Could not check Docker containers")
        return False

    # Check if backend endpoints are accessible
    try:
        import requests

        response = requests.get("http://localhost:8000/modules", timeout=5)
        if response.status_code == 200:
            modules = response.json()
            coverage_module = None
            for module in modules:
                if module.get("name") == "CodeCoverageAnalyzer":
                    coverage_module = module
                    break

            if coverage_module:
                print("✅ CodeCoverageAnalyzer available via API")
            else:
                print("❌ CodeCoverageAnalyzer not found in API response")
                return False
        else:
            print("❌ Backend API not accessible")
            return False
    except Exception:
        print("❌ Could not connect to backend API")
        return False

    # Check if frontend is accessible
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend accessible")
        else:
            print("❌ Frontend not accessible")
            return False
    except Exception:
        print("❌ Could not connect to frontend")
        return False

    print("✅ All integration points verified")
    return True


def main():
    """Run all verification checks."""
    print("🚀 CodeCoverageAnalyzer Integration Verification")
    print("=" * 60)

    # Change to the project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Run all verification checks
    backend_ok = verify_backend_files()
    frontend_ok = verify_frontend_files()
    integration_ok = verify_integration()

    # Summary
    print("\n📊 Verification Summary")
    print("=" * 30)
    print(f"Backend Implementation: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(
        f"Frontend Implementation: {'✅ PASS' if frontend_ok else '❌ FAIL'}"
    )
    print(f"Integration Points: {'✅ PASS' if integration_ok else '❌ FAIL'}")

    if backend_ok and frontend_ok and integration_ok:
        print("\n🎉 All verification checks PASSED!")
        print("\nTo test the complete integration:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Click the modules button (☰) in the top bar")
        print("3. Select the 'CodeCoverageAnalyzer' module")
        print("4. Enter some Python code in the chat")
        print("5. Send a message like 'Please analyze the code coverage'")
        print(
            "6. Look for the 'Code Coverage Analysis' section in the response"
        )
        print("\nThe coverage analysis should show:")
        print("- Overall coverage percentage")
        print("- Line coverage percentage")
        print("- Number of covered/total lines")
        print("- List of uncovered lines")
        print("- Detailed analysis")
        return True
    else:
        print("\n❌ Some verification checks FAILED!")
        print("Please review the errors above and fix them.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
