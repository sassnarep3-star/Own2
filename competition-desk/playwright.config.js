const { defineConfig, devices } = require('@playwright/test');
module.exports = defineConfig({
  testDir: './tests',
  fullyParallel: true,
  workers: 2,
  reporter: 'list',
  timeout: 30000,
  use: {
    baseURL: 'http://127.0.0.1:8000',
    headless: true,
    launchOptions: process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH, args: ['--no-sandbox','--disable-dev-shm-usage','--no-zygote'] } : {},
    trace: 'retain-on-failure'
  },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'], defaultBrowserType: 'chromium' } }
  ],
  webServer: { command: 'python3 -m http.server 8000 --bind 0.0.0.0 --directory _site', url: 'http://127.0.0.1:8000', reuseExistingServer: !process.env.CI }
});
