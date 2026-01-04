"use client";

import React from "react";
import { AuthProvider } from "@/context/AuthContext";
import { TaskProvider } from "@/context/TaskContext";
import { UIProvider } from "@/context/UIContext";

interface RootLayoutClientProps {
  children: React.ReactNode;
}

export default function RootLayoutClient({
  children,
}: RootLayoutClientProps) {
  return (
    <AuthProvider>
      <TaskProvider>
        <UIProvider>
          {children}
        </UIProvider>
      </TaskProvider>
    </AuthProvider>
  );
}
