import { render, screen, fireEvent } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import AppNotFoundPage from "@/app/not-found";
import * as BrowserNavigation from "@/lib/utils/browser-navigation";

vi.mock("@/lib/utils/browser-navigation", () => ({
  requestInternalAppNavigation: vi.fn(),
}));

describe("AppNotFoundPage", () => {
  it("renders the visual not found state replacing the silent redirect", () => {
    render(<AppNotFoundPage />);

    // Verify visual recovery card is shown
    expect(screen.getByText("Page not found")).toBeTruthy();
    expect(
      screen.getByText("The page you're looking for doesn't exist or may have been moved.")
    ).toBeTruthy();
    expect(screen.getByRole("button", { name: /Go back/i })).toBeTruthy();
    expect(screen.getByRole("button", { name: /Go home/i })).toBeTruthy();
  });

  it("reconciles navigation with canonical requestInternalAppNavigation", () => {
    render(<AppNotFoundPage />);

    const homeButton = screen.getByRole("button", { name: /Go home/i });
    fireEvent.click(homeButton);

    expect(BrowserNavigation.requestInternalAppNavigation).toHaveBeenCalledWith({
      href: "/",
      replace: true,
      scroll: false,
    });
  });

  it("handles browser back navigation natively", () => {
    const backSpy = vi.spyOn(window.history, "back");
    render(<AppNotFoundPage />);

    const backButton = screen.getByRole("button", { name: /Go back/i });
    fireEvent.click(backButton);

    expect(backSpy).toHaveBeenCalled();
    backSpy.mockRestore();
  });
});
