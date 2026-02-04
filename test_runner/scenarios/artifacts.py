"""
Artifact persistence test scenarios.

This module contains scenarios for testing artifact persistence functionality.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tools.persist_artifact import persist_artifacts
from test_runner.scenarios.base import BaseScenario


class PersistArtifactsSuccessScenario(BaseScenario):
    """Scenario 12: Persist artifacts from ad_hoc to artifacts directory."""
    
    def run(self):
        self.print_header(
            12,
            "Persist Artifacts - Success",
            "Moving files from ad_hoc directory to artifacts directory with serial numbering."
        )
        
        # Use the pre-created test_project with ad_hoc files
        print(f"\nProject directory: {self.env.test_project_dir}")
        
        # List ad_hoc files
        ad_hoc_dir = os.path.join(self.env.test_project_dir, ".assistant", "ad_hoc")
        print("\nFiles in ad_hoc directory:")
        for file in os.listdir(ad_hoc_dir):
            print(f"  - {file}")
        
        print("\nCalling: persist_artifacts(")
        print("    abs_path=project_path,")
        print("    files=['test_artifact1.txt', 'test_artifact2.py']")
        print(")")
        
        response = persist_artifacts(
            self.env.test_project_dir,
            ['test_artifact1.txt', 'test_artifact2.py']
        )
        
        self.print_result("Response Object", str(response.model_dump()))
        
        artifacts_dir = os.path.join(self.env.test_project_dir, ".assistant", "artifacts")
        if os.path.exists(artifacts_dir):
            print("\nFiles in artifacts directory:")
            for file in os.listdir(artifacts_dir):
                if not os.path.isdir(os.path.join(artifacts_dir, file)):
                    print(f"  - {file}")


class PersistArtifactsFileNotFoundScenario(BaseScenario):
    """Scenario 13: Persist artifacts - file not found."""
    
    def run(self):
        self.print_header(
            13,
            "Persist Artifacts - File Not Found",
            "Attempting to persist a file that doesn't exist in ad_hoc directory."
        )
        
        print(f"\nProject directory: {self.env.test_project_dir}")
        print("Calling: persist_artifacts(abs_path=project_path, files=['nonexistent.txt'])")
        
        response = persist_artifacts(self.env.test_project_dir, ['nonexistent.txt'])
        
        self.print_result("Response Object", str(response.model_dump()))


class PersistArtifactsWithDeleteScenario(BaseScenario):
    """Scenario 21: Persist artifacts with deletion from ad_hoc."""
    
    def run(self):
        self.print_header(
            21,
            "Persist Artifacts - With Deletion",
            "Moving files from ad_hoc to artifacts and deleting originals."
        )
        
        # Create a fresh project directory for this test
        import tempfile
        project_dir = tempfile.mkdtemp(prefix="glyph_delete_test_")
        print(f"\nProject directory: {project_dir}")
        
        # Initialize assistant directory
        from tools.init_assistant_dir import init_assistant_dir
        init_response = init_assistant_dir(project_dir, overwrite=False)
        print(f"Assistant directory initialized: {init_response.success}")
        
        # Create a test file in ad_hoc
        ad_hoc_dir = os.path.join(project_dir, ".assistant", "ad_hoc")
        test_file = os.path.join(ad_hoc_dir, "temp_test.txt")
        
        with open(test_file, 'w') as f:
            f.write("This is a temporary test file.")
        
        print("\nCreated test file: temp_test.txt")
        print(f"File exists before: {os.path.exists(test_file)}")
        
        print("\nCalling: persist_artifacts(")
        print("    abs_path=project_path,")
        print("    files=['temp_test.txt'],")
        print("    delete_from_ad_hoc=True")
        print(")")
        
        response = persist_artifacts(
            project_dir,
            ['temp_test.txt'],
            delete_from_ad_hoc=True
        )
        
        print(f"\nFile exists after: {os.path.exists(test_file)}")
        
        self.print_result("Response Object", str(response.model_dump()))
        
        # Cleanup
        import shutil
        shutil.rmtree(project_dir)


class PersistArtifactsWithReferenceFixingScenario(BaseScenario):
    """Scenario 22: Persist artifacts with automatic reference fixing."""
    
    def run(self):
        self.print_header(
            22,
            "Persist Artifacts - With Reference Fixing",
            "Persisting artifacts and automatically updating references in design logs and operations."
        )
        
        # Create a fresh project directory for this test
        import tempfile
        project_dir = tempfile.mkdtemp(prefix="glyph_ref_test_")
        print(f"\nProject directory: {project_dir}")
        
        # Initialize assistant directory
        from tools.init_assistant_dir import init_assistant_dir
        init_response = init_assistant_dir(project_dir, overwrite=False)
        print(f"Assistant directory initialized: {init_response.success}")
        
        # Create a test file in ad_hoc
        ad_hoc_dir = os.path.join(project_dir, ".assistant", "ad_hoc")
        test_file = os.path.join(ad_hoc_dir, "referenced_file.txt")
        
        with open(test_file, 'w') as f:
            f.write("This file will be referenced.")
        
        # Create a design log that references the ad_hoc file
        dl_dir = os.path.join(project_dir, ".assistant", "design_logs")
        dl_file = os.path.join(dl_dir, "dl_1_test_references.md")
        
        with open(dl_file, 'w') as f:
            f.write("# Test Design Log\n\n")
            f.write("This design log references referenced_file.txt multiple times.\n\n")
            f.write("See referenced_file.txt for details.\n")
        
        print("\nCreated test file: referenced_file.txt")
        print("Created design log that references it")
        
        # Read the design log before
        with open(dl_file, 'r') as f:
            content_before = f.read()
        print("\nDesign log content BEFORE:")
        print(content_before)
        
        print("\nCalling: persist_artifacts(")
        print("    abs_path=project_path,")
        print("    files=['referenced_file.txt'],")
        print("    fix_references=True")
        print(")")
        
        response = persist_artifacts(
            project_dir,
            ['referenced_file.txt'],
            fix_references=True
        )
        
        # Read the design log after
        with open(dl_file, 'r') as f:
            content_after = f.read()
        print("\nDesign log content AFTER:")
        print(content_after)
        
        self.print_result("Response Object", str(response.model_dump()))
        
        # Cleanup
        import shutil
        shutil.rmtree(project_dir)


class PersistArtifactsWithBothOptionsScenario(BaseScenario):
    """Scenario 23: Persist artifacts with both deletion and reference fixing."""
    
    def run(self):
        self.print_header(
            23,
            "Persist Artifacts - With Both Options",
            "Persisting artifacts with both deletion and reference fixing enabled."
        )
        
        # Create a fresh project directory for this test
        import tempfile
        project_dir = tempfile.mkdtemp(prefix="glyph_both_test_")
        print(f"\nProject directory: {project_dir}")
        
        # Initialize assistant directory
        from tools.init_assistant_dir import init_assistant_dir
        init_response = init_assistant_dir(project_dir, overwrite=False)
        print(f"Assistant directory initialized: {init_response.success}")
        
        # Create a test file in ad_hoc
        ad_hoc_dir = os.path.join(project_dir, ".assistant", "ad_hoc")
        test_file = os.path.join(ad_hoc_dir, "complete_test.txt")
        
        with open(test_file, 'w') as f:
            f.write("This file will be persisted, deleted, and references updated.")
        
        # Create an operation that references the ad_hoc file
        op_dir = os.path.join(project_dir, ".assistant", "operations")
        op_file = os.path.join(op_dir, "op_1_test_operation.md")
        
        with open(op_file, 'w') as f:
            f.write("# Test Operation\n\n")
            f.write("This operation uses complete_test.txt.\n")
        
        print("\nCreated test file: complete_test.txt")
        print("Created operation that references it")
        print(f"File exists before: {os.path.exists(test_file)}")
        
        print("\nCalling: persist_artifacts(")
        print("    abs_path=project_path,")
        print("    files=['complete_test.txt'],")
        print("    delete_from_ad_hoc=True,")
        print("    fix_references=True")
        print(")")
        
        response = persist_artifacts(
            project_dir,
            ['complete_test.txt'],
            delete_from_ad_hoc=True,
            fix_references=True
        )
        
        print(f"\nFile exists after: {os.path.exists(test_file)}")
        
        # Read the operation after
        with open(op_file, 'r') as f:
            content_after = f.read()
        print("\nOperation content AFTER:")
        print(content_after)
        
        self.print_result("Response Object", str(response.model_dump()))
        
        # Cleanup
        import shutil
        shutil.rmtree(project_dir)
