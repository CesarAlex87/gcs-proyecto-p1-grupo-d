# Jenkins UI Screenshot Automation

Playwright-based automation scripts for capturing Jenkins UI screenshots for documentation and testing purposes.

## Prerequisites

- Node.js 14+ and npm
- Jenkins running on `localhost:8080` (or custom `JENKINS_URL`)
- Valid Jenkins credentials (default: admin/admin)

## Installation

```bash
npm install
```

This will install Playwright and its browser dependencies.

## Configuration

Set credentials via environment variables:

```bash
export JENKINS_USER=admin
export JENKINS_PASS=your_password
export JENKINS_URL=http://localhost:8080  # Optional, defaults to localhost:8080
```

Or on Windows (PowerShell):

```powershell
$env:JENKINS_USER="admin"
$env:JENKINS_PASS="your_password"
$env:JENKINS_URL="http://localhost:8080"
```

## Usage

### Capture Jenkins UI Screenshots

Captures the main Jenkins interface including login, dashboard, plugins, and job configuration:

```bash
npm run capture
```

**Generates:**
- `01_jenkins_login.png` - Login page
- `02_jenkins_dashboard.png` - Main dashboard
- `03_jenkins_manage.png` - Manage Jenkins page
- `04_jenkins_plugins.png` - Installed plugins list
- `05_pipeline_job.png` - Pipeline job page
- `06_pipeline_config.png` - Job configuration page

### Capture Pipeline Execution

Triggers a build and captures the pipeline execution flow with stages, logs, and results:

```bash
npm run capture-pipeline
```

**Generates:**
- `07_pipeline_building.png` - Build execution page
- `08_pipeline_stages.png` - Pipeline stages visualization
- `09_console_output.png` - Console output (top)
- `10_console_output_2.png` - Console output (scrolled)
- `11_test_results.png` - Test results (if available)
- `12_coverage_report.png` - Code coverage report (if available)
- `13_blue_ocean.png` - Blue Ocean pipeline view (if available)

### Capture Webhook Configuration

Captures Jenkins webhook configuration for build triggers:

```bash
npm run capture-webhook
```

**Generates:**
- `14_build_triggers.png` - Build triggers configuration

**Note:** GitHub webhook configuration must be captured from GitHub repository settings (Settings > Webhooks) or via the GitHub API.

## Complete Workflow

To capture all screenshots in sequence:

```bash
export JENKINS_USER=admin
export JENKINS_PASS=admin_password

# Step 1: Capture Jenkins UI
npm run capture

# Step 2: Capture pipeline execution
npm run capture-pipeline

# Step 3: Capture webhook configuration
npm run capture-webhook
```

## Expected Output

All screenshots are saved as PNG files in the `screenshots/` directory with sequential numbering (01-14).

## Features

- **Headless Chromium**: All scripts run in headless mode (no visible browser window)
- **Error Handling**: Graceful degradation - if a page is unavailable, a warning is logged and execution continues
- **Auto-waits**: Intelligent waiting for network activity and page loads
- **High Resolution**: 1920x1080 viewport for clear, readable screenshots
- **Detailed Logging**: Console messages track progress and capture confirmation

## Troubleshooting

### Connection Refused
```
Error: connect ECONNREFUSED 127.0.0.1:8080
```
Ensure Jenkins is running: `docker run -p 8080:8080 jenkins/jenkins:latest` or start your local Jenkins instance.

### Login Fails
- Verify credentials: `export JENKINS_USER=admin JENKINS_PASS=your_password`
- Check if Jenkins requires different login selectors for your version
- Update selectors in script if Jenkins version differs

### Pages Not Found
- Some pages (test results, coverage, Blue Ocean) are optional and require plugins
- Scripts log warnings but continue if pages are unavailable
- Check Jenkins logs for plugin installation requirements

### Screenshot Quality
- Viewport is set to 1920x1080 for optimal readability
- Full-page screenshots capture all scrollable content
- If screenshots are truncated, Jenkins may require scrolling enabled

## Dependencies

- **playwright** ^1.60.0 - Browser automation framework

## Notes

- Credentials can also be read from environment variables for CI/CD integration
- Each script can be run independently
- Screenshots overwrite previous ones with the same filename
- Network idle wait ensures all resources are fully loaded before capture
