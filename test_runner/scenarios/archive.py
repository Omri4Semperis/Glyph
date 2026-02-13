"""
Archive document test scenarios.

This module contains scenarios for testing document archiving functionality.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tools.archive_doc import archive_document
from tools.add_design_log import add_design_log
from tools.add_operation import add_operation
from tools.persist_artifact import persist_artifacts
from tools.init_assistant_dir import init_assistant_dir
from test_runner.scenarios.base import BaseScenario


class ArchiveDesignLogScenario(BaseScenario):
    """Scenario: Archive a design log and update all references."""
    
    def run(self):
        self.print_header(
            "Archive-1",
            "Archive Design Log",
            "Archive a design log and verify that all references are updated."
        )
        
        # Create a project with cross-referencing files
        archive_project = os.path.join(self.env.temp_dir, "archive_project")
        os.makedirs(archive_project)
        init_assistant_dir(archive_project, False)
        
        # Add design logs
        add_design_log(archive_project, "Authentication", "Auth system design")
        add_design_log(archive_project, "Database Schema", "DB design")
        add_design_log(archive_project, "API Design", "API endpoints")
        
        # Add operations that reference the design logs
        add_operation(archive_project, "Implement Auth", "Implementation steps for auth")
        
        # Add content with cross-references
        dl_dir = os.path.join(archive_project, ".assistant", "design_logs")
        op_dir = os.path.join(archive_project, ".assistant", "operations")
        
        # dl_2 references dl_1
        dl2_path = os.path.join(dl_dir, "dl_2_Database_Schema.md")
        with open(dl2_path, 'a') as f:
            f.write("\n\nThis design should align with dl_1_Authentication.md requirements.")
        
        # dl_3 references dl_1
        dl3_path = os.path.join(dl_dir, "dl_3_API_Design.md")
        with open(dl3_path, 'a') as f:
            f.write("\n\nSee dl_1_Authentication.md for auth requirements.")
        
        # op_1 references dl_1
        op1_path = os.path.join(op_dir, "op_1_Implement_Auth.md")
        with open(op1_path, 'a') as f:
            f.write("\n\nRefer to dl_1_Authentication.md for design details.")
        
        # dl_1 references other docs (to test internal reference updates)
        dl1_path = os.path.join(dl_dir, "dl_1_Authentication.md")
        with open(dl1_path, 'a') as f:
            f.write("\n\nThis design uses database schema from dl_2_Database_Schema.md")
            f.write("\nImplementation details are in op_1_Implement_Auth.md")
        
        print(f"\nProject directory: {archive_project}")
        print("\nBefore archiving - dl_2_Database_Schema.md content:")
        with open(dl2_path, 'r') as f:
            print(f.read())
        
        print("\nCalling: archive_document(abs_path=project_path, doc_type='design_log', number=1)")
        
        response = archive_document(archive_project, "design_log", 1)
        
        self.print_result("Response Object", str(response.model_dump()))
        
        # Verify the file was moved
        archived_path = os.path.join(dl_dir, "archived", "dl_1_Authentication.md")
        original_path = os.path.join(dl_dir, "dl_1_Authentication.md")
        
        print("\n--- Verification ---")
        print(f"Original file exists: {os.path.exists(original_path)}")
        print(f"Archived file exists: {os.path.exists(archived_path)}")
        
        # Check if references were updated
        print("\nAfter archiving - dl_2_Database_Schema.md content:")
        with open(dl2_path, 'r') as f:
            print(f.read())
        
        print("\nAfter archiving - dl_3_API_Design.md content:")
        with open(dl3_path, 'r') as f:
            print(f.read())
        
        print("\nAfter archiving - op_1_Implement_Auth.md content:")
        with open(op1_path, 'r') as f:
            print(f.read())
        
        # Check internal references in archived file
        print("\nArchived file content (should have updated internal references):")
        if os.path.exists(archived_path):
            with open(archived_path, 'r') as f:
                print(f.read())


class ArchiveOperationScenario(BaseScenario):
    """Scenario: Archive an operation document and update all references."""
    
    def run(self):
        self.print_header(
            "Archive-2",
            "Archive Operation",
            "Archive an operation and verify that all references are updated."
        )
        
        # Create a project
        archive_project = os.path.join(self.env.temp_dir, "archive_op_project")
        os.makedirs(archive_project)
        init_assistant_dir(archive_project, False)
        
        # Add operations
        add_operation(archive_project, "Setup Environment", "Initial setup steps")
        add_operation(archive_project, "Deploy Application", "Deployment steps")
        
        # Add content with cross-references
        op_dir = os.path.join(archive_project, ".assistant", "operations")
        
        # op_2 references op_1
        op2_path = os.path.join(op_dir, "op_2_Deploy_Application.md")
        with open(op2_path, 'a') as f:
            f.write("\n\nBefore deployment, complete op_1_Setup_Environment.md steps.")
        
        print(f"\nProject directory: {archive_project}")
        print("\nBefore archiving - op_2_Deploy_Application.md content:")
        with open(op2_path, 'r') as f:
            print(f.read())
        
        print("\nCalling: archive_document(abs_path=project_path, doc_type='operation', number=1)")
        
        response = archive_document(archive_project, "operation", 1)
        
        self.print_result("Response Object", str(response.model_dump()))
        
        # Verify
        print("\nAfter archiving - op_2_Deploy_Application.md content:")
        with open(op2_path, 'r') as f:
            print(f.read())


class ArchiveArtifactScenario(BaseScenario):
    """Scenario: Archive an artifact and update all references."""
    
    def run(self):
        self.print_header(
            "Archive-3",
            "Archive Artifact",
            "Archive an artifact and verify that all references are updated."
        )
        
        # Create a project
        archive_project = os.path.join(self.env.temp_dir, "archive_art_project")
        os.makedirs(archive_project)
        init_assistant_dir(archive_project, False)
        
        # Create a temporary file to persist as artifact
        ad_hoc_dir = os.path.join(archive_project, ".assistant", "ad_hoc")
        temp_file = os.path.join(ad_hoc_dir, "test_diagram.png")
        with open(temp_file, 'w') as f:
            f.write("fake image data")
        
        # Persist as artifact
        persist_artifacts(
            archive_project,
            ["test_diagram.png"],
            {"test_diagram.png": "Architecture diagram"},
            delete_from_ad_hoc=False,
            fix_references=False
        )
        
        # Add a design log that references the artifact
        add_design_log(archive_project, "System Architecture", "Architecture overview")
        
        dl_dir = os.path.join(archive_project, ".assistant", "design_logs")
        dl1_path = os.path.join(dl_dir, "dl_1_System_Architecture.md")
        with open(dl1_path, 'a') as f:
            f.write("\n\nSee art_1_test_diagram.png for visual representation.")
        
        print(f"\nProject directory: {archive_project}")
        print("\nBefore archiving - dl_1_System_Architecture.md content:")
        with open(dl1_path, 'r') as f:
            print(f.read())
        
        print("\nCalling: archive_document(abs_path=project_path, doc_type='artifact', number=1)")
        
        response = archive_document(archive_project, "artifact", 1)
        
        self.print_result("Response Object", str(response.model_dump()))
        
        # Verify
        print("\nAfter archiving - dl_1_System_Architecture.md content:")
        with open(dl1_path, 'r') as f:
            print(f.read())
