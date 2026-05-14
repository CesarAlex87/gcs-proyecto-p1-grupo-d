const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const JENKINS_URL = process.env.JENKINS_URL || 'http://localhost:8080';
const JENKINS_USER = process.env.JENKINS_USER || 'admin';
const JENKINS_PASS = process.env.JENKINS_PASS || 'admin';
const SCREENSHOTS_DIR = path.dirname(__filename);
const MAX_BUILD_WAIT = 5 * 60 * 1000; // 5 minutes in milliseconds

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function captureScreenshot(page, filename) {
  const filepath = path.join(SCREENSHOTS_DIR, filename);
  await page.screenshot({ path: filepath, fullPage: true });
  console.log(`✓ Captured: ${filename}`);
}

async function loginToJenkins(page) {
  console.log('Logging in to Jenkins...');
  await page.goto(`${JENKINS_URL}/login`, { waitUntil: 'networkidle', timeout: 30000 });
  await delay(500);
  await page.fill('input[name="j_username"]', JENKINS_USER);
  await page.fill('input[name="j_password"]', JENKINS_PASS);
  await page.click('button[name="Submit"]');
  await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 30000 });
  await delay(1000);
  console.log('✓ Logged in successfully');
}

async function isBuildComplete(page) {
  try {
    const response = await page.goto(`${JENKINS_URL}/job/gcs-proyecto-p1/lastBuild/api/json`, {
      waitUntil: 'networkidle',
      timeout: 10000
    });
    const data = await response.json();
    return data.result !== null;
  } catch (error) {
    return false;
  }
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.createContext();
  const page = await context.newPage();

  page.setViewportSize({ width: 1920, height: 1080 });

  try {
    // Login
    await loginToJenkins(page);

    // Navigate to pipeline job
    console.log('Navigating to pipeline job...');
    await page.goto(`${JENKINS_URL}/job/gcs-proyecto-p1/`, { waitUntil: 'networkidle', timeout: 30000 });
    await delay(1000);

    // Click Build Now
    console.log('Triggering build...');
    try {
      await page.click('button:has-text("Build Now")');
      await delay(2000);
      console.log('✓ Build triggered');
    } catch (error) {
      console.warn('⚠ Could not find Build Now button, attempting with link...');
      try {
        await page.click('a:has-text("Build Now")');
        await delay(2000);
      } catch (innerError) {
        console.warn('⚠ Build Now button/link not found, continuing anyway...');
      }
    }

    // Navigate to last build
    console.log('Navigating to build page...');
    await page.goto(`${JENKINS_URL}/job/gcs-proyecto-p1/lastBuild/`, { waitUntil: 'networkidle', timeout: 30000 });
    await delay(1000);
    await captureScreenshot(page, '07_pipeline_building.png');

    // Wait for build to complete
    console.log('Waiting for build to complete (max 5 minutes)...');
    const startTime = Date.now();
    let isComplete = await isBuildComplete(page);

    while (!isComplete && (Date.now() - startTime) < MAX_BUILD_WAIT) {
      await delay(3000);
      isComplete = await isBuildComplete(page);
      const elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);
      process.stdout.write(`\rWaiting... ${elapsedSeconds}s`);
    }

    if (isComplete) {
      console.log('\n✓ Build completed');
    } else {
      console.log('\n⚠ Build still running after 5 minutes, continuing with screenshots...');
    }

    // Refresh the page to see updated status
    await delay(1000);
    await page.reload({ waitUntil: 'networkidle', timeout: 30000 });
    await delay(1000);

    // 8. Capture pipeline stages view
    console.log('Navigating to pipeline stages view...');
    try {
      await page.goto(`${JENKINS_URL}/job/gcs-proyecto-p1/lastBuild/wfapi/describe`, { waitUntil: 'networkidle', timeout: 15000 });
      // If pipeline view exists, capture it
      await page.goto(`${JENKINS_URL}/job/gcs-proyecto-p1/lastBuild/`, { waitUntil: 'networkidle', timeout: 30000 });
      await delay(1000);
      await captureScreenshot(page, '08_pipeline_stages.png');
    } catch (error) {
      console.warn('⚠ Pipeline stages view not available, skipping...');
    }

    // 9. Navigate to console output
    console.log('Navigating to console output...');
    try {
      await page.goto(`${JENKINS_URL}/job/gcs-proyecto-p1/lastBuild/console`, { waitUntil: 'networkidle', timeout: 30000 });
      await delay(1000);
      await captureScreenshot(page, '09_console_output.png');

      // Scroll down for more console output
      await page.evaluate(() => window.scrollBy(0, window.innerHeight * 2));
      await delay(800);
      await captureScreenshot(page, '10_console_output_2.png');
    } catch (error) {
      console.warn('⚠ Console output page not available:', error.message);
    }

    // 11. Navigate to test results
    console.log('Navigating to test results...');
    try {
      await page.goto(`${JENKINS_URL}/job/gcs-proyecto-p1/lastBuild/testReport/`, { waitUntil: 'networkidle', timeout: 30000 });
      await delay(1000);
      await captureScreenshot(page, '11_test_results.png');
    } catch (error) {
      console.warn('⚠ Test results page not available, skipping...');
    }

    // 12. Navigate to coverage report
    console.log('Navigating to coverage report...');
    try {
      await page.goto(`${JENKINS_URL}/job/gcs-proyecto-p1/lastBuild/jacoco/`, { waitUntil: 'networkidle', timeout: 30000 });
      await delay(1000);
      await captureScreenshot(page, '12_coverage_report.png');
    } catch (error) {
      console.warn('⚠ Coverage report not available, skipping...');
    }

    // 13. Navigate to Blue Ocean view
    console.log('Navigating to Blue Ocean view...');
    try {
      await page.goto(`${JENKINS_URL}/blue/organizations/jenkins/gcs-proyecto-p1/detail/gcs-proyecto-p1/lastBuild/`, {
        waitUntil: 'networkidle',
        timeout: 30000
      });
      await delay(1500);
      await captureScreenshot(page, '13_blue_ocean.png');
    } catch (error) {
      console.warn('⚠ Blue Ocean view not available, skipping...');
    }

    console.log('\n✅ All pipeline execution screenshots captured successfully!');
    console.log(`Screenshots saved to: ${SCREENSHOTS_DIR}`);

  } catch (error) {
    console.error('❌ Error during pipeline capture:', error.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

main();
