"use client";

import { ReactNode, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import Navigation from "@/components/Layout/Navigation";
import Sidebar from "@/components/Layout/Sidebar";
import { PageLoading } from "@/components/Common/Loading";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Don't redirect while loading
    if (isLoading) return;

    // If not authenticated, redirect to login
    if (!isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  // Show loading while checking auth
  if (isLoading) {
    return <PageLoading />;
  }

  // If not authenticated, don't render (will redirect)
  if (!isAuthenticated) {
    return null;
  }

  // User is authenticated, render dashboard
  return (
    <div className="flex h-screen bg-[#020617] overflow-hidden">
      {/* Sidebar - Fixed height to screen */}
      <div className="flex-shrink-0">
        <Sidebar />
      </div>

      {/* Main Content Area */}
      <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
        <Navigation />
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}