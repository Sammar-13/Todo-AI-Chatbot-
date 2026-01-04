"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import SidebarRobot from "./SidebarRobot";

export default function Sidebar() {
  const pathname = usePathname();
  const { user } = useAuth();

  const links = [
    { href: "/tasks", label: "Tasks", icon: "✅" },
    { href: "/settings", label: "Settings", icon: "⚙️" },
  ];

  const isActive = (href: string) => {
    if (href === "/tasks") {
      return pathname === href || pathname === "/dashboard";
    }
    return pathname.startsWith(href);
  };

  return (
    <aside className="w-64 border-r border-slate-800 bg-[#020617] text-slate-300 flex flex-col h-full">
      {/* Top: Logo */}
      <div className="p-6">
        <div className="flex items-center gap-2 mb-8 px-2">
          <div className="w-8 h-8 bg-indigo-500 rounded-lg flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-indigo-500/20">
            T
          </div>
          <span className="text-xl font-bold text-white tracking-tight">Todo App</span>
        </div>

        <nav className="space-y-1">
          {links.map((link) => {
            const active = isActive(link.href);
            return (
              <Link
                key={link.label}
                href={link.href}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group ${
                  active
                    ? "bg-indigo-500/10 text-indigo-400 font-medium shadow-[0_0_20px_rgba(99,102,241,0.15)] border border-indigo-500/20"
                    : "text-slate-400 hover:bg-slate-800/50 hover:text-slate-100 border border-transparent"
                }`}
              >
                <span className={`text-xl transition-transform duration-200 ${active ? "scale-110" : "group-hover:scale-110"}`}>
                  {link.icon}
                </span>
                <span>{link.label}</span>
                {active && (
                  <div className="ml-auto w-1.5 h-1.5 rounded-full bg-indigo-400 shadow-[0_0_8px_currentColor]" />
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Middle: Robot */}
      <div className="flex-1 flex flex-col items-center justify-center p-4 overflow-hidden">
          <SidebarRobot username={user?.full_name?.split(' ')[0]} />
          <div className="mt-4 px-4 py-1.5 rounded-full bg-slate-800/50 border border-slate-700/50">
            <p className="text-[9px] text-indigo-400 uppercase tracking-[0.2em] font-black">
              AI System Active
            </p>
          </div>
      </div>

      {/* Bottom: Extra space or footer info if needed */}
      <div className="p-6 border-t border-slate-800/50 opacity-0 h-20">
        {/* Keeping layout consistent */}
      </div>
    </aside>
  );
}
