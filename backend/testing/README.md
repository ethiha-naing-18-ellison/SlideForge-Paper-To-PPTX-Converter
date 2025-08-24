# Testing Folder

This folder contains all test files for the SlideForge application, including test PDFs, generated PPTX files, test scripts, and test results.

## Test PDF Files

### Original Test PDFs
- `A Low-cost Hand Recognition Based Smart Board Model (HRbSBM) for the Education System.pdf` - Original research paper used for testing
- Multiple timestamped versions of the same file for different test runs

### New Test PDF Files (Created 2025-08-24)
These files were created to test different document types and structures:

1. **test_report_type.pdf** - Quarterly Performance Report Q3 2024
   - Document Type: Report
   - Contains: Executive Summary, Methodology, Key Findings, Recommendations, Conclusion

2. **test_user_manual.pdf** - Advanced Data Analytics Platform - User Manual
   - Document Type: User Manual
   - Contains: Introduction, Installation Guide, Getting Started, Core Features, Troubleshooting

3. **test_research_paper.pdf** - Impact of Artificial Intelligence on Healthcare Systems: A Multi-Center Study
   - Document Type: Research Paper
   - Contains: Abstract, Introduction, Literature Review, Methodology, Results, Discussion, Conclusion

4. **test_school_project.pdf** - Effects of Light Wavelength on Plant Growth - Science Project Report
   - Document Type: School Project Report
   - Contains: Project Overview, Materials and Methods, Experimental Setup, Results, Analysis, Conclusion

5. **test_school_assignment.pdf** - Macbeth Character Analysis - English Literature Assignment
   - Document Type: School Assignment
   - Contains: Assignment Title, Introduction, Character Analysis, Thematic Analysis, Literary Devices, Conclusion

6. **test_assignment_report.pdf** - Cybersecurity Threats and Defense Strategies - Assignment Report
   - Document Type: Assignment Report
   - Contains: Executive Summary, Problem Statement, Research Objectives, Methodology, Key Findings, Recommendations, Implementation Plan, Conclusion

7. **test_documentation.pdf** - Enterprise Resource Planning System - Technical Documentation
   - Document Type: Documentation
   - Contains: System Overview, Architecture, Installation and Setup, User Management, Module Configuration, Database Schema, API Documentation, Troubleshooting, Maintenance

## Test Scripts

### Python Test Files
- `test_*.py` - Various test scripts for different components
- `debug_*.py` - Debug scripts for troubleshooting
- `verify_*.py` - Verification scripts
- `create_test_pdfs.py` - Script to generate the 7 new test PDF files
- `create_sample_pdf.py` - Original sample PDF creation script

### Test Results
- `*.pptx` - Generated PowerPoint presentations from test runs
- `.coverage` - Code coverage data
- `htmlcov/` - HTML coverage reports
- `.pytest_cache/` - Pytest cache files

## Samples Directory
- `samples/` - Contains sample files for testing
  - `sample_paper.pdf` - Sample research paper
  - `sample_paper.txt` - Text version of sample paper

## Usage

### Running Tests
```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest test_title_and_conclusion.py -v

# Run with coverage
poetry run pytest --cov=app
```

### Creating New Test PDFs
```bash
# Generate the 7 test PDF files
python create_test_pdfs.py
```

### Testing Different Document Types
Use the various test PDF files to test how SlideForge handles different document types:
- Reports
- User Manuals
- Research Papers
- School Projects
- Assignments
- Documentation

Each PDF has different content structures and formatting to test the application's ability to handle various document types and extract appropriate content for slide generation.

## File Organization

All test files are now organized in this single folder for easy access and management. This includes:
- Input test PDFs
- Generated output PPTX files
- Test scripts and utilities
- Test results and coverage data
- Sample files

This organization makes it easier to:
- Run comprehensive tests
- Compare different document types
- Track test results over time
- Maintain test data
