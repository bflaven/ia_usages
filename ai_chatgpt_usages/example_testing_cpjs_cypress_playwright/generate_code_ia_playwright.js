// generate_code_ia_playwright.js
// source for GPT query
// Generate a login test with Playwright testing Framework



const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Navigate to the login page
  await page.goto('https://www.example.com/login');

  // Fill in the login form
  await page.fill('input[name="username"]', 'testuser');
  await page.fill('input[name="password"]', 'password123');

  // Submit the form
  await page.click('button[type="submit"]');

  // Wait for the next page to load
  await page.waitForSelector('h1');

  // Verify that the user is logged in
  const title = await page.title();
  console.assert(title === 'Welcome, testuser', 'Login failed');

  await browser.close();
})();
