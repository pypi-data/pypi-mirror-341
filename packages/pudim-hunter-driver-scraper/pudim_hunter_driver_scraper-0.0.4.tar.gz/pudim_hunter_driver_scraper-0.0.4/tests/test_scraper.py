"""
Tests for the PlaywrightScraper class.
"""
import pytest
from pudim_hunter_driver_scraper import PlaywrightScraper

TEST_URL = "https://github.com/luismr"
SELECTORS = {
    "name": ".vcard-fullname",
    "bio": ".user-profile-bio",
    "repositories": "nav.UnderlineNav-body a[href$='repositories'] span.Counter"
}

def test_scraper_context_manager():
    """Test that the scraper can be used as a synchronous context manager."""
    with PlaywrightScraper() as scraper:
        assert scraper._browser is not None
        assert scraper._context is not None
        assert scraper._page is not None
    
    assert scraper._browser is None
    assert scraper._context is None
    assert scraper._page is None

def test_scraper_navigation():
    """Test that the scraper can navigate to a URL synchronously."""
    with PlaywrightScraper() as scraper:
        scraper.navigate(TEST_URL)
        assert "github.com/luismr" in scraper._page.url

def test_scraper_extract_data():
    """Test that the scraper can extract data using selectors synchronously."""
    with PlaywrightScraper() as scraper:
        scraper.navigate(TEST_URL)
        data = scraper.extract_data(SELECTORS)
        assert "name" in data
        assert "bio" in data
        assert "repositories" in data

@pytest.mark.asyncio
async def test_scraper_async_context_manager():
    """Test that the scraper can be used as an asynchronous context manager."""
    async with PlaywrightScraper() as scraper:
        assert scraper._browser is not None
        assert scraper._context is not None
        assert scraper._page is not None
    
    assert scraper._browser is None
    assert scraper._context is None
    assert scraper._page is None

@pytest.mark.asyncio
async def test_scraper_async_navigation():
    """Test that the scraper can navigate to a URL asynchronously."""
    async with PlaywrightScraper() as scraper:
        await scraper.navigate_async(TEST_URL)
        assert "github.com/luismr" in scraper._page.url

@pytest.mark.asyncio
async def test_scraper_async_extract_data():
    """Test that the scraper can extract data using selectors asynchronously."""
    async with PlaywrightScraper() as scraper:
        await scraper.navigate_async(TEST_URL)
        data = await scraper.extract_data_async(SELECTORS)
        assert "name" in data
        assert "bio" in data
        assert "repositories" in data 