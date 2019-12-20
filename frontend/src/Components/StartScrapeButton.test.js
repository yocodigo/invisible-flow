import React from 'react';
import { unmountComponentAtNode } from "react-dom";
import { fireEvent, render } from "@testing-library/react";
import StartScrapeButton from './StartScrapeButton';

const mockPush = jest.fn();

jest.mock('react-router-dom', () => ({
  useHistory: () => ({
    push: mockPush
  })
}));

window.XMLHttpRequest = jest.fn(() => mockRequest);

const mockRequest = {
  open: jest.fn(),
  send: jest.fn(),
  status: 200
};

let container = null;

beforeEach(() => {
  container = document.createElement("div");
  document.body.appendChild(container);
});

afterEach(() => {
  unmountComponentAtNode(container);
  container.remove();
  container = null;
});

it("renders without crashing", () => {
  render(<StartScrapeButton />, container);
});

describe("When StartScrapeButton is clicked", () => {
  it("redirects to scrape status page and sends HTTP request to backend", () => {
    const { getByText } = render(<StartScrapeButton />, container);

    fireEvent.click(getByText("Initiate COPA Scrape"));

    expect(mockPush).toBeCalledWith("/scrapeStatus");
    expect(mockRequest.send).toHaveBeenCalled();
  });
});