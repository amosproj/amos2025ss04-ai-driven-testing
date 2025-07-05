"""Demo script to show ExportManager output."""
import os
from export_manager import ExportManager


def demo_export_manager():
    """Demonstrate ExportManager functionality."""
    # Create ExportManager with demo directory
    export_manager = ExportManager("demo_exports")

    # Sample LLM response content
    sample_response = """# Generated Test Case

## Test Function: test_user_authentication

```python
def test_user_authentication():
    # Test valid user credentials
    user = User("testuser", "password123")
    assert user.authenticate("testuser", "password123") == True

    # Test invalid credentials
    assert user.authenticate("testuser", "wrongpassword") == False
    assert user.authenticate("wronguser", "password123") == False

    # Test empty credentials
    assert user.authenticate("", "") == False
    assert user.authenticate(None, None) == False

def test_user_authorization():
    # Test user role permissions
    admin_user = User("admin", "adminpass", role="admin")
    regular_user = User("user", "userpass", role="user")

    assert admin_user.has_permission("delete_user") == True
    assert regular_user.has_permission("delete_user") == False
    assert regular_user.has_permission("view_profile") == True
```

## Test Coverage Analysis
- **Authentication**: Covers valid/invalid credentials, edge cases
- **Authorization**: Tests role-based permissions
- **Edge Cases**: Empty and None inputs handled

## Recommendations
1. Add tests for password strength validation
2. Include tests for account lockout after failed attempts
3. Test session management and timeout scenarios
"""

    print("=== ExportManager Demo ===")
    print(f"Supported formats: {export_manager.get_supported_formats()}")

    # Export in all formats
    print("\nExporting sample LLM response in all formats...")
    exported_files = export_manager.export_all_formats(
        sample_response, "demo_llm_response"
    )

    for format_type, filepath in exported_files.items():
        if not filepath.startswith("Error:"):
            print(f"✓ {format_type.upper()}: {filepath}")

            # Show first few lines of each file
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()[:5]  # First 5 lines
                    print(f"  Preview: {lines[0].strip()}")
                    if len(lines) > 1:
                        print(f"           {lines[1].strip()}")
            except Exception as e:
                print(f"  Could not preview: {e}")
        else:
            print(f"✗ {format_type.upper()}: {filepath}")

    # Show statistics
    print("\n=== Export Statistics ===")
    stats = export_manager.get_export_stats()
    print(f"Total files exported: {stats['total_files']}")
    print(f"Format breakdown: {stats['formats']}")
    print(f"Output directory: {stats['output_directory']}")

    # List all files
    print(f"\n=== Files in {export_manager.output_dir} ===")
    for file in os.listdir(export_manager.output_dir):
        filepath = os.path.join(export_manager.output_dir, file)
        size = os.path.getsize(filepath)
        print(f"  📄 {file} ({size} bytes)")

    print("\n=== Demo Complete ===")
    print(
        f"Check the '{export_manager.output_dir}' directory to see exported files!"
    )


if __name__ == "__main__":
    demo_export_manager()
