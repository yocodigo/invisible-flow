import React from 'react';
import ReactDOM from 'react-dom';
import { render, fireEvent } from "@testing-library/react";
import StartScrapeButton from './StartScrapeButton';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<StartScrapeButton />, div);
  ReactDOM.unmountComponentAtNode(div);
});


describe("StartScrapeButton goes to status", function () {
  it('StartScrapeButton should have scrape button', function () {
    const { getByTestId } = render(<StartScrapeButton />);
    const e = getByTestId("startScrape");
    expect(e.tagName).toBe("BUTTON");
  });
  it('scrape button should redirect to scrape page', function () {
    // test to show that the user hit scrape page
    const startScrapeMock = jest.fn();
    const { getByTestId } = render(<StartScrapeButton startScrape = {startScrapeMock} />);
    const e = getByTestId("startScrape");

    fireEvent.click(e);
    expect(startScrapeMock).toHaveBeenCalled();
  });
});