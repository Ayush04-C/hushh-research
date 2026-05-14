import { describe, expect, it, vi } from "vitest";

vi.mock("next/font/google", () => ({
  Geist: () => ({ variable: "geist-sans" }),
  Geist_Mono: () => ({ variable: "geist-mono" }),
  Inter: () => ({ variable: "inter" }),
}));

import { metadata } from "@/app/layout";

describe("Root Layout SEO Metadata", () => {
  it("extends existing SEO metadata with global OpenGraph properties", () => {
    // Assert that OpenGraph is present and structured correctly
    expect(metadata.openGraph).toBeDefined();
    expect(metadata.openGraph?.title).toBe("One | Your Personal Agent");
    expect(metadata.openGraph?.siteName).toBe("Hussh");
    expect(metadata.openGraph?.url).toBe("https://hushh.ai");
    expect(metadata.openGraph?.type).toBe("website");
  });

  it("extends existing SEO metadata with Twitter Card properties", () => {
    // Assert that Twitter is present and structured correctly
    expect(metadata.twitter).toBeDefined();
    expect(metadata.twitter?.card).toBe("summary_large_image");
    expect(metadata.twitter?.title).toBe("One: Your Personal Agent");
    expect(metadata.twitter?.images).toEqual(["/quiet-emoji-icon.png"]);
  });

  it("retains core capability base configurations", () => {
    // Check that metadataBase is present to establish canonical paths
    expect(metadata.metadataBase).toBeDefined();
    expect(metadata.metadataBase?.toString()).toBe("https://hushh.ai/");
  });
});
