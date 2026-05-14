"use client";

import { requestInternalAppNavigation } from "@/lib/utils/browser-navigation";
import { BrandMark, Icon } from "@/lib/morphy-ux/ui";
import { Button } from "@/lib/morphy-ux/button";
import { Card } from "@/lib/morphy-ux/card";
import { ArrowLeft, Home, SearchX } from "lucide-react";
import { ROUTES } from "@/lib/navigation/routes";

/**
 * AppNotFoundPage
 *
 * Catch-all 404 page that provides visual feedback and navigation recovery
 * instead of silently redirecting to home. Uses the Morphy glass-card pattern
 * consistent with RouteErrorBoundary for a unified error-recovery UX.
 */
export default function AppNotFoundPage() {
  const handleGoBack = () => {
    if (typeof window !== "undefined") {
      window.history.back();
    }
  };

  const handleGoHome = () => {
    requestInternalAppNavigation({
      href: ROUTES.HOME,
      replace: true,
      scroll: false,
    });
  };

  return (
    <main className="flex min-h-[100dvh] flex-col items-center justify-center px-6 pb-[var(--app-screen-footer-pad)]">
      <div className="flex flex-col items-center gap-6 w-full max-w-sm text-center">
        <BrandMark size="sm" />

        <Card
          preset="default"
          effect="glass"
          glassAccent="soft"
          className="w-full"
        >
          <div className="flex flex-col items-center gap-4">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-[var(--morphy-primary-start)]/12 to-[var(--morphy-primary-end)]/12 dark:from-[var(--morphy-primary-start)]/16 dark:to-[var(--morphy-primary-end)]/16">
              <SearchX className="h-7 w-7 text-[var(--morphy-primary-start)]" />
            </div>
            <div className="space-y-1.5">
              <h1 className="text-lg font-semibold tracking-tight">
                Page not found
              </h1>
              <p className="text-sm leading-relaxed text-muted-foreground">
                The page you&apos;re looking for doesn&apos;t exist or may have
                been moved.
              </p>
            </div>
            <div className="flex gap-3 pt-1">
              <Button
                variant="muted"
                effect="glass"
                size="sm"
                onClick={handleGoBack}
              >
                <Icon icon={ArrowLeft} size="sm" className="mr-1.5" />
                Go back
              </Button>
              <Button
                variant="blue-gradient"
                effect="fill"
                size="sm"
                onClick={handleGoHome}
              >
                <Icon icon={Home} size="sm" className="mr-1.5" />
                Go home
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </main>
  );
}
