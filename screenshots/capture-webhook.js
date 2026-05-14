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

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.createContext();
  const page = await context.newPage();

  page.setViewportSize({ width: 1920, height: 1080 });

  try {
    // Login
    await loginToJenkins(page);

    // Navigate to pipeline job configuration
    console.log('Navigating to pipeline job configuration...');
    await page.goto(`${JENKINS_URL}/job/gcs-proyecto-p1/configure`, { waitUntil: 'networkidle', timeout: 30000 });
    await delay(1000);

    // Scroll to build triggers section
    console.log('Scrolling to Build Triggers section...');
    try {
      // Try to find and scroll to the Build Triggers section
      const buildTriggersSection = await page.$('text=Build Triggers');
      if (buildTriggersSection) {
        await buildTriggersSection.scrollIntoViewIfNeeded();
        await delay(800);
      } else {
        console.warn('⚠ Build Triggers section not found, scrolling down...');
        await page.evaluate(() => window.scrollBy(0, window.innerHeight * 3));
        await delay(800);
      }

      await captureScreenshot(page, '14_build_triggers.png');
    } catch (error) {
      console.warn('⚠ Error scrolling to Build Triggers:', error.message);
      await captureScreenshot(page, '14_build_triggers.png');
    }

    // Note about GitHub webhook configuration
    console.log('\n📝 GitHub Webhook Configuration:');
    console.log('   To capture GitHub webhook configuration:');
    console.log('   1. Go to your GitHub repository settings');
    console.log('   2. Navigate to Settings > Webhooks');
    console.log('   3. Find the Jenkins webhook (typically http://your-jenkins:8080/github-webhook/)');
    console.log('   4. Take a screenshot manually or use the GitHub API');
    console.log('\n   Alternatively, from Jenkins configuration above, note the webhook URL');
    console.log('   that Jenkins expects from GitHub (usually /github-webhook/ endpoint).');

    console.log('\n✅ Webhook configuration screenshots captured!');
    console.log(`Screenshots saved to: ${SCREENSHOTS_DIR}`);

  } catch (error) {
    console.error('❌ Error during webhook capture:', error.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

main();
