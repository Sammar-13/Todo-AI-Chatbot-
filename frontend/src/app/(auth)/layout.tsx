"use client";

import { ReactNode, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { PageLoading } from "@/components/Common/Loading";

export default function AuthLayout({ children }: { children: ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Don't redirect while loading
    if (isLoading) return;

    // If already authenticated, redirect to tasks
    if (isAuthenticated) {
      router.push("/tasks");
    }
  }, [isAuthenticated, isLoading, router]);

  // Show loading while checking auth
  if (isLoading) {
    return <PageLoading />;
  }

  // If already authenticated, don't render (will redirect)
  if (isAuthenticated) {
    return null;
  }

  // User is not authenticated, show auth page
  return (
    <div className="min-h-screen bg-[#0f172a] relative overflow-hidden flex items-center justify-center px-4">
      {/* Background Decor */}
      <div className="absolute -top-24 -left-24 w-96 h-96 bg-indigo-500/10 rounded-full blur-[120px]"></div>
      <div className="absolute -bottom-24 -right-24 w-96 h-96 bg-purple-500/10 rounded-full blur-[120px]"></div>
      
      <div className="w-full max-w-md relative z-10">{children}</div>
    </div>
  );
}
