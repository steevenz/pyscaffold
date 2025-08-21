#!/usr/bin/env python3
"""Test script untuk menguji fungsi scaffold secara langsung."""

import sys
sys.path.insert(0, '.')

from src.core.scaffold import scaffold
from src.core.generators import ProjectType
from pathlib import Path

def test_scaffold():
    """Test scaffold function dengan berbagai project types."""
    test_cases = [
        {
            'name': 'test-standard',
            'type': ProjectType.STANDARD,
            'description': 'Standard Python Project'
        },
        {
            'name': 'test-data-science',
            'type': ProjectType.DATA_SCIENCE,
            'description': 'Data Science Project'
        },
        {
            'name': 'test-web-api',
            'type': ProjectType.WEB_API,
            'description': 'Web API Project'
        }
    ]
    
    print("🚀 Testing PyScaffold functionality...\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}/3: Creating {test_case['description']}...")
        
        try:
            success = scaffold(
                project_path=test_case['name'],
                author='Test Author',
                email='test@example.com',
                project_type=test_case['type'],
                license_name='MIT',
                include_ai=False,
                include_trainer=False,
                progress_callback=lambda msg: print(f"  → {msg}")
            )
            
            if success:
                print(f"  ✅ {test_case['name']} created successfully!")
                
                # Check if key files exist
                project_path = Path(test_case['name'])
                key_files = ['README.md', 'requirements.txt', 'pyproject.toml', '.gitignore']
                
                for file in key_files:
                    if (project_path / file).exists():
                        print(f"    ✓ {file} exists")
                    else:
                        print(f"    ✗ {file} missing")
                        
            else:
                print(f"  ❌ Failed to create {test_case['name']}")
                
        except Exception as e:
            print(f"  ❌ Error creating {test_case['name']}: {e}")
        
        print()
    
    print("🎉 Testing completed!")

if __name__ == '__main__':
    test_scaffold()