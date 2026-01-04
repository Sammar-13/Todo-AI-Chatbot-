"use client";

import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import ConfirmationModal from "@/components/Common/ConfirmationModal";

export default function SettingsPage() {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState("profile");
  const [showLogoutModal, setShowLogoutModal] = useState(false);

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h1 className="text-3xl font-bold text-white mb-8 tracking-tight">Settings</h1>

      <div className="bg-slate-900/50 backdrop-blur-sm border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
        <div className="border-b border-slate-800 bg-slate-900/50">
          <div className="flex gap-2 px-6">
            {["profile", "preferences", "danger"].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-4 px-4 font-semibold text-sm capitalize transition-all relative ${
                  activeTab === tab
                    ? "text-indigo-400"
                    : "text-slate-500 hover:text-slate-300"
                }`}
              >
                {tab === "danger" ? "Danger Zone" : tab}
                {activeTab === tab && (
                  <div className="absolute bottom-0 left-0 w-full h-0.5 bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.5)]" />
                )}
              </button>
            ))}
          </div>
        </div>

        <div className="p-8">
          {activeTab === "profile" && (
            <div className="max-w-2xl space-y-8 animate-in fade-in duration-300">
              <div>
                <h2 className="text-xl font-bold text-white mb-1">Profile Information</h2>
                <p className="text-sm text-slate-500 mb-6">Manage your account details and how others see you.</p>
                
                <div className="space-y-6">
                  <div className="grid gap-2">
                    <label className="text-sm font-semibold text-slate-300">Full Name</label>
                    <input
                      type="text"
                      value={user?.full_name || ""}
                      disabled
                      className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-slate-300 cursor-not-allowed"
                    />
                  </div>
                  <div className="grid gap-2">
                    <label className="text-sm font-semibold text-slate-300">Email Address</label>
                    <input
                      type="email"
                      value={user?.email || ""}
                      disabled
                      className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-slate-300 cursor-not-allowed"
                    />
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "preferences" && (
            <div className="max-w-2xl animate-in fade-in duration-300">
              <h2 className="text-xl font-bold text-white mb-1">Preferences</h2>
              <p className="text-sm text-slate-500 mb-6">Customize your experience and notifications.</p>
              
              <div className="space-y-4">
                {[
                  { id: "notif", label: "Email notifications", desc: "Receive updates about your tasks" },
                  { id: "remind", label: "Due date reminders", desc: "Get alerted when tasks are nearly due" }
                ].map((pref) => (
                  <label key={pref.id} className="flex items-center justify-between p-4 rounded-xl border border-slate-800 bg-slate-800/20 hover:bg-slate-800/40 transition-colors cursor-pointer group">
                    <div>
                      <p className="font-semibold text-slate-200">{pref.label}</p>
                      <p className="text-xs text-slate-500">{pref.desc}</p>
                    </div>
                    <input
                      type="checkbox"
                      defaultChecked
                      className="w-5 h-5 rounded border-slate-700 bg-slate-900 text-indigo-500 focus:ring-indigo-500/50 transition-all cursor-pointer"
                    />
                  </label>
                ))}
              </div>
            </div>
          )}

          {activeTab === "danger" && (
            <div className="max-w-2xl animate-in fade-in duration-300">
              <div className="p-6 border border-red-500/20 bg-red-500/5 rounded-2xl">
                <h2 className="text-xl font-bold text-red-400 mb-1">Danger Zone</h2>
                <p className="text-sm text-red-400/70 mb-6">Irreversible actions for your account.</p>
                
                <button
                  onClick={() => setShowLogoutModal(true)}
                  className="px-6 py-3 bg-red-600 hover:bg-red-500 text-white font-bold rounded-xl transition-all shadow-lg shadow-red-600/20 active:scale-95 flex items-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 11-6 0v-1m6 0H9" />
                  </svg>
                  Log Out of Account
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
      
      <ConfirmationModal
        isOpen={showLogoutModal}
        onClose={() => setShowLogoutModal(false)}
        onConfirm={logout}
        title="Logout Confirmation"
        message="Are you sure you want to log out? You will need to sign in again to access your tasks."
        confirmText="Yes, Logout"
      />
    </div>
  );
}