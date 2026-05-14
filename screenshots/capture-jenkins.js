const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const JENKINS_URL = process.env.JENKINS_URL || 'http://localhost:8080';
const JENKINS_USER = process.env.JENKINS_USER || 'admin';
const JENKINS_PASS = process.env.JENKINS_PASS || 'admin';
const SCREENSHOTS_DIR = path.dirname(__filename);

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function captureScreenshot(page, filename) {
  const filepath = path.join(SCREENSHOTS_DIR, filename);
  await page.screenshot({ path: filepath, fullPage: true });
  console.log(`✓ Captured: ${filename}`);
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.createContext();
  const page = await context.newPage();

  page.setViewportSize({ width: 1920, height: 1080 });

  try {
    // 1. Capture login page
    console.log('Navigating to Jenkins login page...');
    await page.goto(`${JENKINS_URL}/login`, { waitUntil: 'networkidle', timeout: 30000 });
    await delay(500);
    await captureScreenshot(page, '01_jenkins_login.png');

    // 2. Fill in credentials and login
    console.log('Logging in...');
    await page.fill('input[name="j_username"]', JENKINS_USER);
    await page.fill('input[name="j_password"]', JENKINS_PASS);
    await page.click('button[name="Submit"]');
    await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 30000 });
    await delay(1000);
    await captureScreenshot(page, '02_jenkins_dashboard.png');

    // 3. Navigate to Manage Jenkins
    console.log('Navigating to Manage Jenkins...');
    await page.goto(`${JENKINS_URL}/manage`, { waitUntil: 'networkidle', timeout: 30000 });
    await delay(1000);
    await captureScreenshot(page, '03_jenkins_manage.png');

    // 4. Navigate to Plugins page
    console.log('Navigating to Plugins...');
    await page.goto(`${JENKINS_URL}/manage/pluginManager/`, { waitUntil: 'networkidle', timeout: 30000 });
    await delay(1000);
    await captureScreenshot(page, '04_jenkins_plugins.png');

    // 5. Navigate to pipeline job
    console.log('Navigating to pipeline job...');
    await page.goto(`${JENKINS_URL}/job/gcs-proyecto-p1/`, { waitUntil: 'networkidle', timeout: 30000 });
    await delay(1000);
    await captureScreenshot(page, '05_pipeline_job.png');

    // 6. Navigate to job configuration
    console.log('Navigating to job configuration...');
    await page.goto(`${JENKINS_URL}/job/gcs-proyecto-p1/configure`, { waitUntil: 'networkidle', timeout: 30000 });
    await delay(1000);
    await captureScreenshot(page, '06_pipeline_config.png');

    console.log('\n✅ All Jenkins UI screenshots captured successfully!');
    console.log(`Screenshots saved to: ${SCREENSHOTS_DIR}`);

  } catch (error) {
    console.error('❌ Error during Jenkins UI capture:', error.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

main();
