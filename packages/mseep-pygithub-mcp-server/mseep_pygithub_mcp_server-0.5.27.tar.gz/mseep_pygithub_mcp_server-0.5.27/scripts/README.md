# Scripts for PyGithub MCP Server

This directory contains utility scripts for development, testing, and maintenance of the PyGithub MCP Server project.

## Available Scripts

### Coverage Analysis

The `analyze_coverage.py` script provides detailed analysis of test coverage with prioritized recommendations:

```bash
# Run unit tests and generate reports
python scripts/analyze_coverage.py --run-tests --html

# Run both unit and integration tests for coverage
python scripts/analyze_coverage.py --run-tests --include-integration --html

# Use existing .coverage file and generate reports
python scripts/analyze_coverage.py --html

# Set a minimum coverage threshold
python scripts/analyze_coverage.py --run-tests --threshold 85
```

#### Features:
- Identifies high, medium, and low priority modules based on coverage
- Shows exact line numbers that need testing
- Generates both JSON and HTML reports
- Colorful console output with summary statistics
- Can run tests or use existing .coverage file
- HTML report with interactive details for each module

#### Viewing Generated Reports:

The `analyze_coverage.py` script generates two types of reports:

1. **JSON Report** (default: `coverage_report.json`):
   - Contains structured data about coverage metrics
   - Useful for programmatic analysis or CI/CD pipelines

2. **HTML Report** (when using `--html` flag):
   - Interactive web-based report that can be opened in any browser
   - No web server required - simply open the HTML file directly:
     ```bash
     # On Linux
     xdg-open coverage_report.html
     
     # On macOS
     open coverage_report.html
     
     # Or double-click the file in your file explorer
     ```
   - Features collapsible sections showing exact lines needing tests
   - Color-coded priorities to focus testing efforts
   - Progress bars showing coverage percentages

#### Using Reports Effectively:

The coverage analysis report is designed to help you focus your testing efforts:

1. **Prioritized Modules**: Focus first on "High Priority" modules (under 70% coverage)
2. **Missing Lines**: Each module shows exactly which lines need test coverage
3. **Strategic Improvement**: Implement tests for the highest-priority modules first
4. **Tracking Progress**: Re-run the analyzer to see your coverage improvements

### Test Generator

The `generate_tool_tests.py` script creates standardized test files for new PyGithub MCP Server tools:

```bash
# Create tests for a repository tool
python scripts/generate_tool_tests.py --module repositories --tool-name GetRepository

# Create tests for an issue tool with custom schema
python scripts/generate_tool_tests.py --module issues --tool-name CreateIssue --schema-module issues --schema-name CreateIssueParams

# Create only integration tests
python scripts/generate_tool_tests.py --module repositories --tool-name ListCommits --integration-only
```

#### Features:
- Generates both unit and integration tests
- Uses dataclasses instead of mocks (following ADR-002)
- Follows project's test patterns and conventions
- Includes templates for most common tools
- Customizable test parameters and schemas
- Option to generate only unit or integration tests

## Integration with Development Workflow

These scripts integrate with the project's development workflow to improve quality and maintainability:

1. **Test-Driven Development**:
   - Use the coverage analyzer to identify untested code
   - Focus testing efforts on high-priority modules
   - Track improvement in coverage metrics

2. **Adding New Tools**:
   - Use the test generator to create standardized tests
   - Follow the Pydantic-First Architecture (ADR-007)
   - Ensure proper test coverage from the start

3. **Continuous Integration**:
   - Set coverage thresholds for CI pipelines
   - Generate coverage reports as part of CI
   - Prevent coverage regression

4. **Documentation**:
   - Coverage reports help document the test status
   - Generated tests document expected behavior
   - Clear code examples show how tools should be used
