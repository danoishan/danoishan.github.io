"""Generate the tagged, two-page résumé from resume.html and its print styles."""

from argparse import ArgumentParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import mimetypes

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://danoishan.github.io"
DEFAULT_OUTPUT = ROOT / "Danoishan_Sinnathamby_Resume_2026.pdf"


def serve_local_files(route):
    url = urlsplit(route.request.url)
    path = (ROOT / unquote(url.path).lstrip("/")).resolve()
    if url.netloc != "danoishan.github.io" or not path.is_relative_to(ROOT) or not path.is_file():
        route.abort()
        return
    content_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
    route.fulfill(path=str(path), content_type=content_type)


def build_resume(output, executable):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=executable)
        page = browser.new_page(java_script_enabled=False, color_scheme="light")
        page.route("**/*", serve_local_files)
        page.goto(f"{ORIGIN}/resume.html", wait_until="load")
        page.pdf(path=output, prefer_css_page_size=True, tagged=True, outline=True)
        browser.close()


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--browser-executable", help="Use an installed Chromium executable")
    args = parser.parse_args()
    build_resume(args.output, args.browser_executable)
    print(args.output)


if __name__ == "__main__":
    main()
