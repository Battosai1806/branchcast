// Local end-to-end smoke test. Pass a Playwright module path, a browser
// executable path, and the URL of a running BranchCast server as arguments.
const { chromium } = require(process.argv[2]);
const executablePath = process.argv[3];
const base = process.argv[4];

(async () => {
  const browser = await chromium.launch({ executablePath, headless: true });
  const streamerContext = await browser.newContext();
  const viewerContext = await browser.newContext();
  const obsContext = await browser.newContext();
  try {
    const streamer = await streamerContext.newPage();
    await streamer.goto(base);
    await streamer.getByRole('heading', { name: 'Streamer editor' }).waitFor();
    await streamer.getByRole('button', { name: 'Add shape' }).click();
    streamer.once('dialog', dialog => dialog.accept('Comet garden'));
    await streamer.getByRole('button', { name: 'New idea', exact: true }).click();
    await streamer.getByText('Saved to this server').waitFor();
    const url = new URL(streamer.url());
    const viewer = await viewerContext.newPage();
    url.hash = 'viewer';
    await viewer.goto(url.href);
    await viewer.getByLabel('Your name').fill('Demo viewer');
    await viewer.getByLabel('Idea title').fill('A moonlit garden');
    await viewer.getByLabel('Tell us more').fill('A garden among the stars.');
    await viewer.getByRole('button', { name: 'Submit your branch' }).click();
    await viewer.getByText('Branch sent to the streamer for review.').waitFor();
    const display = await obsContext.newPage();
    url.hash = 'display';
    await display.goto(url.href);
    await display.getByText('Waiting for an approved branch').waitFor();
    await streamer.getByRole('link', { name: /Submission queue/ }).click();
    await streamer.getByText('A moonlit garden').waitFor();
    await streamer.getByRole('button', { name: 'Approve & feature' }).click();
    await display.getByText('A moonlit garden').waitFor();
    await display.getByText('Comet garden').waitFor();
    console.log('Browser flow passed: edit, viewer fork, submission, approval, OBS display.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
